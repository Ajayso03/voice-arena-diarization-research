import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs("JoshTalks_Growth_Assessment/question_1/leaderboard", exist_ok=True)

# -------------------------------------------------------------
# IMAGE 1: Leaderboard Product Main View Mockup
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
ax.set_facecolor('#f8fafc')
fig.patch.set_facecolor('#0f172a')

# Header Bar
header = patches.Rectangle((0, 0.88), 1, 0.12, transform=ax.transAxes, color='#0f172a', zorder=1)
ax.add_patch(header)

ax.text(0.03, 0.95, "Voice of India Diarization-Bench", transform=ax.transAxes, 
        color='white', fontsize=16, fontweight='bold', va='center')
ax.text(0.03, 0.91, "National Diarization Standard v2.4 | 100 Hours Multi-Accented Indian Conversational Speech", 
        transform=ax.transAxes, color='#94a3b8', fontsize=9.5, va='center')

# Header Pill
badge = patches.FancyBboxPatch((0.29, 0.94), 0.10, 0.024, transform=ax.transAxes, 
                              boxstyle="round,pad=0.005", fc="#1e3a8a", ec="#3b82f6", lw=1)
ax.add_patch(badge)
ax.text(0.34, 0.952, "AUDITED", transform=ax.transAxes, color='#93c5fd', fontsize=7.5, fontweight='bold', ha='center', va='center')

# Header Buttons
for x, label in [(0.72, "Methodology & Math"), (0.83, "Dataset Specs"), (0.92, "Compare Models")]:
    btn = patches.FancyBboxPatch((x, 0.93), 0.07, 0.028, transform=ax.transAxes,
                                boxstyle="round,pad=0.004", fc="#1e293b" if "Compare" not in label else "#3b82f6", 
                                ec="#475569" if "Compare" not in label else "#2563eb", lw=1)
    ax.add_patch(btn)
    ax.text(x + 0.035, 0.944, label, transform=ax.transAxes, color='white', fontsize=7.5, fontweight='bold', ha='center', va='center')

# KPI Summary Cards (Row at 0.78 to 0.86)
kpis = [
    ("TEST CORPUS SIZE", "100 Hours", "15 Languages & 4 Accents", "#3b82f6"),
    ("GROUND TRUTH INTEGRITY", "α = 0.94", "Krippendorff Dual-Annotator", "#10b981"),
    ("BEST STRICT DER (0s)", "14.8%", "pyannoteAI Precision-3", "#16a34a"),
    ("COMMERCIAL ASR SPREAD", "18.9% – 67.1%", "ElevenLabs vs Deepgram Nova-3", "#ef4444")
]

for i, (label, val, sub, col) in enumerate(kpis):
    x = 0.03 + i * 0.24
    card = patches.FancyBboxPatch((x, 0.79), 0.22, 0.075, transform=ax.transAxes,
                                 boxstyle="round,pad=0.005", fc="white", ec="#e2e8f0", lw=1)
    ax.add_patch(card)
    ax.text(x + 0.015, 0.845, label, transform=ax.transAxes, color='#64748b', fontsize=7, fontweight='bold')
    ax.text(x + 0.015, 0.818, val, transform=ax.transAxes, color=col, fontsize=13, fontweight='bold')
    ax.text(x + 0.015, 0.802, sub, transform=ax.transAxes, color='#64748b', fontsize=7)

# Filter Bar (Row at 0.71 to 0.76)
filter_bar = patches.FancyBboxPatch((0.03, 0.71), 0.94, 0.06, transform=ax.transAxes,
                                   boxstyle="round,pad=0.005", fc="white", ec="#e2e8f0", lw=1)
ax.add_patch(filter_bar)

filters = [
    ("LANGUAGE", "All Languages (Composite)", 0.05),
    ("ENVIRONMENT", "All Environments", 0.23),
    ("SPEAKERS", "All Speaker Counts", 0.41),
    ("OVERLAP", "All Overlap Levels", 0.59),
    ("SCORING", "Strict (0.0s Collar) [ACTIVE]", 0.77)
]
for lbl, val, x in filters:
    ax.text(x, 0.75, lbl, transform=ax.transAxes, color='#64748b', fontsize=6.5, fontweight='bold')
    pill = patches.FancyBboxPatch((x, 0.72), 0.15, 0.022, transform=ax.transAxes,
                                 boxstyle="round,pad=0.003", fc="#f1f5f9" if "Strict" not in val else "#eff6ff", 
                                 ec="#cbd5e1" if "Strict" not in val else "#3b82f6", lw=0.8)
    ax.add_patch(pill)
    ax.text(x + 0.008, 0.731, val, transform=ax.transAxes, color='#0f172a' if "Strict" not in val else "#1d4ed8", fontsize=7, fontweight='bold' if "Strict" in val else 'normal')

# Table Container (Row 0.05 to 0.69)
tbl_bg = patches.FancyBboxPatch((0.03, 0.05), 0.94, 0.64, transform=ax.transAxes,
                               boxstyle="round,pad=0.005", fc="white", ec="#e2e8f0", lw=1)
ax.add_patch(tbl_bg)

# Table Header
tbl_hdr = patches.Rectangle((0.03, 0.64), 0.94, 0.05, transform=ax.transAxes, color='#f8fafc', ec="#e2e8f0", lw=1)
ax.add_patch(tbl_hdr)

cols = [
    ("RANK", 0.05), ("MODEL & PROVIDER", 0.10), ("TYPE", 0.28), ("LICENSE", 0.38),
    ("DER (%) & 95% CI", 0.48), ("ERROR BREAKDOWN (MS / FA / SC)", 0.60), 
    ("JER (%)", 0.76), ("COV (%)", 0.83), ("COST", 0.90)
]
for col_name, cx in cols:
    ax.text(cx, 0.665, col_name, transform=ax.transAxes, color='#475569', fontsize=7.5, fontweight='bold', va='center')

# Table Rows
rows_data = [
    ("1", "pyannoteAI Precision-3", "pyannoteAI", "Acoustic", "Commercial", "14.8%", "±1.1%", 6.2, 3.8, 4.8, "18.2%", "98.4%", "$0.005/m"),
    ("2", "pyannote.audio 3.1", "HuggingFace (OSS)", "Acoustic", "Open Source", "18.4%", "±1.3%", 8.5, 4.1, 5.8, "22.4%", "97.1%", "Self-Host"),
    ("3", "ElevenLabs Scribe v2", "ElevenLabs", "ASR+Diarize", "Commercial", "18.9%", "±1.4%", 9.2, 4.5, 5.2, "23.1%", "96.8%", "$0.024/m"),
    ("4", "WhisperX (v3 + pyannote)", "Open Source", "Modular ASR", "Open Source", "21.6%", "±1.5%", 10.4, 4.2, 7.0, "25.8%", "95.2%", "Self-Host"),
    ("5", "Smallest AI Pulse", "Smallest AI", "ASR+Diarize", "Commercial", "22.4%", "±1.4%", 11.2, 5.1, 6.1, "26.5%", "95.8%", "$0.012/m"),
    ("6", "Speechmatics Enhanced", "Speechmatics", "ASR+Diarize", "Commercial", "24.6%", "±1.6%", 12.1, 5.9, 6.6, "28.2%", "94.6%", "$0.025/m"),
    ("7", "Meta Muse Voice Transcribe", "Meta AI", "Foundation ASR", "Open Weights", "28.7%", "±1.8%", 14.5, 6.2, 8.0, "31.4%", "93.8%", "Self-Host"),
    ("8", "Soniox async v5", "Soniox", "ASR+Diarize", "Commercial", "31.8%", "±1.7%", 16.8, 6.8, 8.2, "34.0%", "92.4%", "$0.010/m"),
    ("9", "AssemblyAI Universal-2", "AssemblyAI", "ASR+Diarize", "Commercial", "34.2%", "±1.9%", 17.5, 7.4, 9.3, "36.8%", "91.5%", "$0.015/m"),
    ("10", "Deepgram Nova-3 (en)", "Deepgram Inc.", "ASR+Diarize", "Commercial", "67.1%", "±3.8%", 58.2, 4.8, 4.1, "69.4%", "46.2%", "$0.0077/m"),
]

for idx, r in enumerate(rows_data):
    ry = 0.585 - idx * 0.058
    # line
    ax.plot([0.03, 0.97], [ry - 0.01, ry - 0.01], transform=ax.transAxes, color='#f1f5f9', lw=0.8)
    
    # rank circle
    rc = '#fef3c7' if r[0]=='1' else ('#f1f5f9' if r[0]=='2' else ('#ffedd5' if r[0]=='3' else '#ffffff'))
    rt = '#b45309' if r[0]=='1' else ('#475569' if r[0]=='2' else ('#9a3412' if r[0]=='3' else '#64748b'))
    circ = patches.Circle((0.055, ry + 0.015), 0.012, transform=ax.transAxes, fc=rc, ec='#cbd5e1', lw=0.5)
    ax.add_patch(circ)
    ax.text(0.055, ry + 0.015, r[0], transform=ax.transAxes, color=rt, fontsize=7.5, fontweight='bold', ha='center', va='center')
    
    # model name & provider
    ax.text(0.10, ry + 0.022, r[1], transform=ax.transAxes, color='#0f172a', fontsize=8, fontweight='bold')
    ax.text(0.10, ry + 0.006, r[2], transform=ax.transAxes, color='#64748b', fontsize=6.5)
    
    # type & license tags
    tt_c = '#e0e7ff' if 'Acoustic' in r[3] else '#e0f2fe'
    tt_t = '#3730a3' if 'Acoustic' in r[3] else '#0369a1'
    tag1 = patches.FancyBboxPatch((0.28, ry + 0.005), 0.08, 0.02, transform=ax.transAxes, boxstyle="round,pad=0.002", fc=tt_c, ec=tt_c)
    ax.add_patch(tag1)
    ax.text(0.32, ry + 0.015, r[3], transform=ax.transAxes, color=tt_t, fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    tag2 = patches.FancyBboxPatch((0.38, ry + 0.005), 0.08, 0.02, transform=ax.transAxes, boxstyle="round,pad=0.002", fc='#f8fafc', ec='#cbd5e1')
    ax.add_patch(tag2)
    ax.text(0.42, ry + 0.015, r[4], transform=ax.transAxes, color='#475569', fontsize=6.5, ha='center', va='center')
    
    # DER & CI
    der_col = '#16a34a' if float(r[5].replace('%','')) < 20 else ('#d97706' if float(r[5].replace('%','')) < 35 else '#dc2626')
    ax.text(0.48, ry + 0.020, r[5], transform=ax.transAxes, color=der_col, fontsize=9, fontweight='bold')
    ax.text(0.48, ry + 0.006, r[6], transform=ax.transAxes, color='#64748b', fontsize=6.5)
    
    # Error bar
    tot_err = r[7] + r[8] + r[9]
    w_tot = 0.12
    w_m = (r[7] / tot_err) * w_tot
    w_fa = (r[8] / tot_err) * w_tot
    w_sc = (r[9] / tot_err) * w_tot
    
    bar_m = patches.Rectangle((0.60, ry + 0.01), w_m, 0.01, transform=ax.transAxes, color='#ef4444')
    bar_fa = patches.Rectangle((0.60 + w_m, ry + 0.01), w_fa, 0.01, transform=ax.transAxes, color='#f59e0b')
    bar_sc = patches.Rectangle((0.60 + w_m + w_fa, ry + 0.01), w_sc, 0.01, transform=ax.transAxes, color='#3b82f6')
    ax.add_patch(bar_m); ax.add_patch(bar_fa); ax.add_patch(bar_sc)
    ax.text(0.60, ry + 0.025, f"MS:{r[7]:.1f}%  FA:{r[8]:.1f}%  SC:{r[9]:.1f}%", transform=ax.transAxes, color='#64748b', fontsize=6)
    
    # JER, Cov, Cost
    ax.text(0.76, ry + 0.015, r[10], transform=ax.transAxes, color='#0f172a', fontsize=8, va='center')
    cov_col = '#dc2626' if float(r[11].replace('%','')) < 70 else '#16a34a'
    ax.text(0.83, ry + 0.015, r[11], transform=ax.transAxes, color=cov_col, fontsize=8, fontweight='bold', va='center')
    ax.text(0.90, ry + 0.015, r[12], transform=ax.transAxes, color='#64748b', fontsize=7.5, va='center')

ax.axis('off')
plt.tight_layout()
fig.savefig("JoshTalks_Growth_Assessment/question_1/leaderboard/leaderboard_mockup.png", bbox_inches='tight')
plt.close()
print("Saved leaderboard_mockup.png successfully.")

