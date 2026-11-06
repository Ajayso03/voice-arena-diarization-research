import os
import glob
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

def parse_rttm(file_path):
    """
    Parses an RTTM file into a list of tuples: (start, end, speaker)
    Format: SPEAKER <session> 1 <start> <duration> <NA> <NA> <speaker> <NA> <NA>
    """
    segments = []
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return segments
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 8 and parts[0] == 'SPEAKER':
                start = float(parts[3])
                duration = float(parts[4])
                end = start + duration
                speaker = parts[7]
                segments.append((start, end, speaker))
    return segments

def score_diarization(ref_segments, hyp_segments, step=0.01):
    """
    Evaluates diarization using fine-grained time-step discretization (10ms steps).
    This handles arbitrary overlaps, strict 0-collar, and Hungarian speaker assignment.
    """
    if not ref_segments:
        if not hyp_segments:
            return 0.0, 0.0, 0.0, 0.0 # 0% DER if both empty
        else:
            return 100.0, 0.0, 100.0, 0.0 # 100% False alarm
            
    # Find overall time bounds
    max_time = max(max(s[1] for s in ref_segments), max([s[1] for s in hyp_segments] if hyp_segments else [0.0]))
    n_steps = int(np.ceil(max_time / step)) + 1
    
    # Get unique speakers
    ref_spks = sorted(list(set(s[2] for s in ref_segments)))
    hyp_spks = sorted(list(set(s[2] for s in hyp_segments))) if hyp_segments else []
    
    ref_spk_to_id = {spk: i for i, spk in enumerate(ref_spks)}
    hyp_spk_to_id = {spk: i for i, spk in enumerate(hyp_spks)}
    
    # Multi-label speech presence per step: [n_steps, n_spks]
    # To be memory efficient, we can build per-step sets of active speakers
    ref_timeline = [set() for _ in range(n_steps)]
    for start, end, spk in ref_segments:
        start_idx = int(round(start / step))
        end_idx = int(round(end / step))
        spk_id = ref_spk_to_id[spk]
        for t in range(start_idx, min(end_idx, n_steps)):
            ref_timeline[t].add(spk_id)
            
    hyp_timeline = [set() for _ in range(n_steps)]
    for start, end, spk in hyp_segments:
        start_idx = int(round(start / step))
        end_idx = int(round(end / step))
        spk_id = hyp_spk_to_id[spk]
        for t in range(start_idx, min(end_idx, n_steps)):
            hyp_timeline[t].add(spk_id)
            
    # Build co-occurrence / confusion matrix between ref and hyp speakers
    # shape: [n_ref_spks, n_hyp_spks]
    if hyp_spks:
        cost_matrix = np.zeros((len(ref_spks), len(hyp_spks)))
        for t in range(n_steps):
            r_set = ref_timeline[t]
            h_set = hyp_timeline[t]
            for r in r_set:
                for h in h_set:
                    cost_matrix[r, h] += 1
                    
        # Hungarian algorithm maximizes overlap (minimizes negative overlap)
        row_ind, col_ind = linear_sum_assignment(-cost_matrix)
        mapping = {hyp_spks[c]: ref_spks[r] for r, c in zip(row_ind, col_ind)}
    else:
        mapping = {}
        
    # Map hyp speakers
    mapped_hyp_timeline = [set() for _ in range(n_steps)]
    for start, end, spk in hyp_segments:
        start_idx = int(round(start / step))
        end_idx = int(round(end / step))
        mapped_spk = mapping.get(spk, f"unmapped_{spk}")
        for t in range(start_idx, min(end_idx, n_steps)):
            mapped_hyp_timeline[t].add(mapped_spk)
            
    # Calculate DER components across all frames
    total_ref_frames = 0
    missed_frames = 0
    false_alarm_frames = 0
    confusion_frames = 0
    
    for t in range(n_steps):
        r_set = {ref_spks[i] for i in ref_timeline[t]}
        h_set = mapped_hyp_timeline[t]
        
        N_ref = len(r_set)
        N_hyp = len(h_set)
        
        total_ref_frames += N_ref
        
        if N_ref == 0 and N_hyp > 0:
            false_alarm_frames += N_hyp
        elif N_ref > 0 and N_hyp == 0:
            missed_frames += N_ref
        elif N_ref > 0 and N_hyp > 0:
            correct = len(r_set.intersection(h_set))
            conf = min(N_ref, N_hyp) - correct
            confusion_frames += conf
            if N_ref > N_hyp:
                missed_frames += (N_ref - N_hyp)
            elif N_hyp > N_ref:
                false_alarm_frames += (N_hyp - N_ref)
                
    if total_ref_frames == 0:
        return 0.0, 0.0, 0.0, 0.0
        
    der = (missed_frames + false_alarm_frames + confusion_frames) / total_ref_frames * 100.0
    missed_rate = missed_frames / total_ref_frames * 100.0
    fa_rate = false_alarm_frames / total_ref_frames * 100.0
    conf_rate = confusion_frames / total_ref_frames * 100.0
    
    return der, missed_rate, fa_rate, conf_rate

def main():
    base_dir = "JoshTalks_Growth_Assessment/input/RTTM_files"
    ref_dir = os.path.join(base_dir, "reference")
    hyp_dir = os.path.join(base_dir, "deepgram_nova3")
    vad_dir = os.path.join(base_dir, "silero_vad")
    
    ref_files = sorted(glob.glob(os.path.join(ref_dir, "*.rttm")))
    print(f"Found {len(ref_files)} reference RTTM files.")
    
    results = []
    
    for r_path in ref_files:
        fname = os.path.basename(r_path)
        session_id = fname.replace(".rttm", "")
        h_path = os.path.join(hyp_dir, fname)
        v_path = os.path.join(vad_dir, fname)
        
        ref_segs = parse_rttm(r_path)
        hyp_segs = parse_rttm(h_path)
        vad_segs = parse_rttm(v_path)
        
        # Calculate ref speech duration
        # Account for overlaps in total time vs total speaker speech time
        ref_spk_time = sum(s[1] - s[0] for s in ref_segs)
        hyp_spk_time = sum(s[1] - s[0] for s in hyp_segs)
        vad_spk_time = sum(s[1] - s[0] for s in vad_segs)
        
        # Score Nova-3
        der, ms, fa, sc = score_diarization(ref_segs, hyp_segs)
        
        # Calculate Speech Coverage % by Nova-3 and VAD relative to Ref speech timeline
        # Union of ref intervals
        step = 0.05 # 50ms step for coverage calculation
        max_t = max(max([s[1] for s in ref_segs] if ref_segs else [0]),
                    max([s[1] for s in hyp_segs] if hyp_segs else [0]),
                    max([s[1] for s in vad_segs] if vad_segs else [0]))
        n_steps = int(np.ceil(max_t / step)) + 1
        
        ref_active = np.zeros(n_steps, dtype=bool)
        for s in ref_segs:
            ref_active[int(round(s[0]/step)):min(int(round(s[1]/step)), n_steps)] = True
            
        hyp_active = np.zeros(n_steps, dtype=bool)
        for s in hyp_segs:
            hyp_active[int(round(s[0]/step)):min(int(round(s[1]/step)), n_steps)] = True
            
        vad_active = np.zeros(n_steps, dtype=bool)
        for s in vad_segs:
            vad_active[int(round(s[0]/step)):min(int(round(s[1]/step)), n_steps)] = True
            
        ref_total_active = np.sum(ref_active)
        hyp_cov = (np.sum(ref_active & hyp_active) / ref_total_active * 100.0) if ref_total_active > 0 else 0.0
        vad_cov = (np.sum(ref_active & vad_active) / ref_total_active * 100.0) if ref_total_active > 0 else 0.0
        
        results.append({
            'Session ID': session_id,
            'Ref Segments': len(ref_segs),
            'Nova Segments': len(hyp_segs),
            'Ref Speech Time (s)': round(ref_spk_time, 2),
            'Nova Speech Time (s)': round(hyp_spk_time, 2),
            'Computed DER %': round(der, 2),
            'Computed Missed %': round(ms, 2),
            'Computed FA %': round(fa, 2),
            'Computed Conf %': round(sc, 2),
            'Computed Nova Cov %': round(hyp_cov, 1),
            'Computed VAD Cov %': round(vad_cov, 1),
        })
        
    df_res = pd.DataFrame(results)
    
    # Load published Results from Excel to compare
    excel_path = "JoshTalks_Growth_Assessment/input/analysis_data.xlsx"
    xl = pd.ExcelFile(excel_path)
    pub_res = xl.parse('Results', skiprows=4)
    pub_res.columns = [c.strip() for c in pub_res.columns]
    
    merged = df_res.merge(pub_res[['Session ID', 'Nova-3 DER %', 'Nova-3 missed speech %', 'Nova-3 false alarm %', 'Nova-3 speaker confusion %', 'Speech covered by Nova-3 (%)', 'Speech covered by VAD (%)']], on='Session ID', how='left')
    
    merged['DER Delta'] = (merged['Computed DER %'] - merged['Nova-3 DER %']).round(2)
    
    print("\n=== INDEPENDENT RTTM SCORING VS PUBLISHED BENCHMARK ===")
    print(merged[['Session ID', 'Computed DER %', 'Nova-3 DER %', 'DER Delta', 'Computed Missed %', 'Nova-3 missed speech %', 'Computed Nova Cov %', 'Speech covered by Nova-3 (%)']].to_string())
    
    out_csv = "JoshTalks_Growth_Assessment/question_2/rttm_analysis/rttm_independent_verification.csv"
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    merged.to_csv(out_csv, index=False)
    print(f"\nSaved independent RTTM verification to: {out_csv}")

if __name__ == "__main__":
    main()

