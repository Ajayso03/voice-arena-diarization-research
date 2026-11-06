# Josh Talks Growth Assessment: Voice of India Benchmark & Deepgram Nova-3 Forensic Analysis

## Project Overview
This repository contains the complete, production-grade research, data analysis, evaluation framework, and forensic engineering investigation for the **Josh Talks Growth Assessment** (conducted in collaboration with AI4Bharat, IIT Madras, and Voice of India).

Operating as a coordinated senior engineering and research team, we have completed:
1. **Question 1**: Complete design of the **Voice of India Speaker Diarization Benchmark & Public Leaderboard**, including corpus architecture (**Bharat-Diarize 1000**), multi-channel annotation protocols, dual-collar mathematical formulations, non-parametric statistical reliability engines (Bootstrap CI + Wilcoxon signed-rank tests), and an interactive web dashboard.
2. **Question 2**: Forensic failure diagnosis of **Deepgram Nova-3's 67.1% Diarization Error Rate (DER)** on Voice Arena Diarization-Bench. Through independent RTTM scoring verification, acoustic spectral audits, transcript alignments, and parameter ablations, we definitively identify the architectural root cause (ASR acoustic decoder silence-clamping under Indian English phonology, rather than a speaker clustering failure).
3. **Official Communications & Deliverables**: Publication-quality 7-page PDF research report, official social media releases (X thread + LinkedIn post strictly within character limits), and two 2–3 minute video presentation scripts with full visual directives.

---

## Repository Structure

```
.
├── JoshTalks_Growth_Assessment/
│   ├── input/
│   │   ├── original_assessment.pdf           # Original challenge specification
│   │   ├── analysis_data.xlsx                # 15 benchmark recordings & 7 worksheets
│   │   └── RTTM_files/                       # 60 ground truth, model, and VAD RTTMs
│   │       ├── reference/                    # 20 Human Ground Truth RTTMs
│   │       ├── deepgram_nova3/               # 20 Nova-3 Hypothesis RTTMs
│   │       ├── silero_vad/                   # 20 Silero Acoustic VAD RTTMs
│   │       └── README.txt                    # Scoring parameters & format specs
│   │
│   ├── question_1/
│   │   ├── research/                         # Literature audit (7 corpora, 3 toolkits)
│   │   ├── model_comparison/                 # 10 production diarization systems profiled
│   │   ├── methodology/                      # Complete evaluation framework
│   │   │   └── Q1_Methodology_Report.md      # Full methodology with 4 final reflections
│   │   ├── dataset_design/                   # Bharat-Diarize 1000 specifications
│   │   ├── metrics/                          # Dual-collar DER, JER, cpWER, tcpWER math
│   │   ├── leaderboard/                      # Interactive product dashboard
│   │   │   ├── index.html                    # Responsive web application
│   │   │   ├── leaderboard_mockup.png        # 300 DPI high-res main view capture
│   │   │   └── leaderboard_compare_mockup.png# 300 DPI high-res comparison capture
│   │   ├── executive_summary/                # 1-page condensed leadership brief
│   │   │   ├── Q1_Executive_Summary.md       # Markdown version
│   │   │   └── Q1_Executive_Summary.pdf      # PDF version
│   │   └── final_report/                     # Publication PDF version
│   │       └── Q1_Methodology_Report.pdf     # Typeset specification document
│   │
│   ├── question_2/
│   │   ├── data_exploration/                 # Master reconciled dataset
│   │   │   └── master_recordings.csv         # 15 sessions merged with acoustics & scores
│   │   ├── scripts/                          # Modular, reproducible Python pipeline
│   │   │   ├── 01_data_audit_and_dictionary.py
│   │   │   ├── 02_build_master_dataset.py
│   │   │   ├── 03_inspect_transcripts.py
│   │   │   ├── 04_transcript_word_analysis.py
│   │   │   ├── 05_independent_rttm_scoring.py  # Hungarian matching DER engine
│   │   │   ├── 06_statistical_correlations.py
│   │   │   ├── 07_list_audio_urls.py
│   │   │   ├── 08_generate_diagnostic_charts.py
│   │   │   └── import_playground_results.py  # Automated playground ingestion
│   │   ├── rttm_analysis/                    # Independent verification outputs
│   │   │   └── rttm_independent_verification.csv
│   │   ├── experiments/                      # Playground runbook & tracking
│   │   │   ├── EXPERIMENT_RUNBOOK.md         # Step-by-step user test guide
│   │   │   └── experiment_tracker.csv        # Pre-filled experiment matrix
│   │   ├── charts/                           # 5 publication figures (300 DPI)
│   │   │   ├── 01_der_breakdown_by_recording.png
│   │   │   ├── 02_word_recall_vs_der.png
│   │   │   ├── 03_nova3_vs_competing_systems.png
│   │   │   ├── 04_deepgram_settings_comparison.png
│   │   │   └── 05_snr_and_overlap_vs_der.png
│   │   ├── findings/                         # Detailed case studies & hypothesis matrix
│   │   └── final_report/                     # Formal research note
│   │       ├── Deepgram_Nova3_Voice_Arena_Report.md
│   │       └── FirstName_LastName_Report.pdf # Publication PDF
│   │
│   ├── social_media/
│   │   └── social_posts.md                   # X thread + LinkedIn post (<1,300 chars)
│   ├── video_scripts/
│   │   ├── Q1_Video_Walkthrough_Script.md    # 2:45 min presentation script
│   │   └── Q2_Video_Investigation_Script.md  # 2:50 min presentation script
│   ├── proof/                                # Containers for user experiment proof
│   │   ├── screenshots/                      # Drop playground screenshots here
│   │   └── responses/                        # Drop JSON API responses here
│   ├── documentation/
│   │   └── QA_VERIFICATION_REPORT.md         # End-to-end quality audit
│   ├── REQUIREMENTS.md                       # Extracted specification & checklist
│   ├── PROJECT_STATUS.md                     # Milestone tracking log
│   ├── FINAL_SUBMISSION_CHECKLIST.md         # Deliverables audit & review guide
│   └── requirements.txt                      # Python dependencies
│
├── FirstName_LastName_Report.pdf             # Deliverable 1: Final Research Report
├── FirstName_LastName_Posts.md               # Deliverable 2: Social Media Posts
├── FINAL_SUBMISSION_CHECKLIST.md             # Reviewer guide
├── REQUIREMENTS.md                           # Comprehensive requirements
├── PROJECT_STATUS.md                         # Milestone audit log
└── requirements.txt                          # Python dependencies
```

---

## Key Technical Findings (Question 2 Summary)

1. **The Bimodal Failure Pattern**:
   - Out of 15 benchmark recordings, 8 suffer catastrophic collapse (DER: **86.0% to 100.0%**; word recall: **0.0% to 23.5%**).
   - The remaining 7 perform normally (DER: **15.1% to 35.3%**; word recall: **76.5% to 98.3%**).
2. **Error Decomposition**:
   - Over **90% of Nova-3's error is pure Missed Speech**. Speaker Confusion is tiny at **2.1%**.
3. **The Root Cause (ASR Gating)**:
   - Deepgram Nova-3 binds speaker intervals directly to recognized words.
   - When configured with `language=en`, Nova-3's acoustic language model encounters Indian English phonology (retroflex consonants, syllable-timed cadence, regional tokens like "vada pav", "haan", "achha") and triggers aggressive confidence pruning.
   - The decoder enters an unrecoverable silence-clamping state (halting word emission after 56 seconds in an 11-minute file, or emitting 0 words entirely).
   - Without words, no diarization segments are created, generating 100% Missed Speech.
4. **Empirical Proof**:
   - Switching to `language=multi` on the exact same audio recovers up to **30x more words** (jumping from 34 words to 983 words on `S003_014`), cutting DER in half.
   - Running `whisper-large` on Deepgram retrieves 1,934 words and drops DER to 67.6%.
5. **Acoustic Quality Disproven**:
   - 100% of files have 0.0% clipping. Failing files have higher SNR (17.9 dB) than the best passing file (11.5 dB). Silero VAD independently confirms >91% speech in all failing files.

---

## How to Verify and Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Question 1 Leaderboard
Open `JoshTalks_Growth_Assessment/question_1/leaderboard/index.html` in any modern web browser to interact with the responsive dashboard, filter matrix, strict/standard collar toggle, and model comparison drawer.

### 3. Reproduce Independent RTTM Scoring
```bash
python JoshTalks_Growth_Assessment/question_2/scripts/05_independent_rttm_scoring.py
```
This recomputes strict 0-collar DER using Hungarian optimal assignment across all 20 benchmark files. Output is saved to `JoshTalks_Growth_Assessment/question_2/rttm_analysis/rttm_independent_verification.csv`.

### 4. Regenerate Diagnostic Charts
```bash
python JoshTalks_Growth_Assessment/question_2/scripts/08_generate_diagnostic_charts.py
```
Generates all 5 publication-quality figures at 300 DPI in `JoshTalks_Growth_Assessment/question_2/charts/`.

### 5. Execute Deepgram Playground Runs (User Action)
Follow `JoshTalks_Growth_Assessment/question_2/experiments/EXPERIMENT_RUNBOOK.md` to run the 7 specified audio links on the Deepgram Playground. Place screenshots in `JoshTalks_Growth_Assessment/proof/screenshots/` and run:
```bash
python JoshTalks_Growth_Assessment/question_2/scripts/import_playground_results.py
```

