# Final Submission Checklist: Josh Talks Growth Assessment

## 1. Candidate Submission Deliverables Audit

| Deliverable Name | File Location | Format | Status | Notes |
|---|---|---|---|---|
| **Question 2 Forensic Report** | `FirstName_LastName_Report.pdf`<br/>`JoshTalks_Growth_Assessment/question_2/final_report/FirstName_LastName_Report.pdf` | PDF (7 Pages) | **READY** | Official Title: *"Deepgram Nova-3 Performance on Voice Arena Diarization-Bench"*. Contains Parts A & B, executive summary, 5 diagnostic charts, full case studies, 10-hypothesis matrix, recommendations, and final reflection. |
| **Social Media Posts** | `FirstName_LastName_Posts.md`<br/>`JoshTalks_Growth_Assessment/social_media/social_posts.md` | Markdown | **READY** | Part A: 5-post X thread.<br/>Part B: LinkedIn post strictly **1,262 characters** (<1,300 char limit). Uses `[link]` placeholder. |
| **Playground Experiment Runbook & Proof** | `JoshTalks_Growth_Assessment/question_2/experiments/EXPERIMENT_RUNBOOK.md`<br/>`JoshTalks_Growth_Assessment/question_2/experiments/experiment_tracker.csv`<br/>`JoshTalks_Growth_Assessment/proof/` | Runbook + CSV + Folder | **READY FOR USER EXECUTION** | 7 experiment configurations specified (3 poor, 2 good, 2 alternative settings) with direct GCS links, tracker, and automated ingestion script. |
| **Working Code, Scripts & Notebooks** | `JoshTalks_Growth_Assessment/question_2/scripts/`<br/>`JoshTalks_Growth_Assessment/question_2/notebooks/` | Python / CSV | **READY** | 8 modular Python scripts covering data audit, master dataset creation, transcript inspection, RTTM scoring engine, statistical correlations, and chart generation. |
| **Question 2 Video Script** | `JoshTalks_Growth_Assessment/video_scripts/Q2_Video_Investigation_Script.md` | Markdown | **READY** | Structured 2 min 50 sec presentation script with timestamps, visual directives, and spoken lines. |
| **Question 1 Methodology Report** | `JoshTalks_Growth_Assessment/question_1/final_report/Q1_Methodology_Report.md`<br/>`JoshTalks_Growth_Assessment/question_1/final_report/Q1_Methodology_Report.pdf` | Markdown & PDF | **READY** | Complete specification covering 7 corpora, 3 toolkits, 10 models, Bharat-Diarize 1000 corpus design, metrics, bootstrap CI, Wilcoxon tests, and 4 final reflections. |
| **Question 1 Executive Summary** | `JoshTalks_Growth_Assessment/question_1/executive_summary/Q1_Executive_Summary.md`<br/>`JoshTalks_Growth_Assessment/question_1/executive_summary/Q1_Executive_Summary.pdf` | Markdown & PDF | **READY** | Condensed 1-page executive brief (2-minute read) for leadership. |
| **Question 1 Leaderboard Product** | `JoshTalks_Growth_Assessment/question_1/leaderboard/index.html`<br/>`JoshTalks_Growth_Assessment/question_1/leaderboard/leaderboard_mockup.png`<br/>`JoshTalks_Growth_Assessment/question_1/leaderboard/leaderboard_compare_mockup.png` | Web App + 300 DPI Images | **READY** | Functional interactive web app with multi-dimensional filtering, strict/standard collar toggles, model inspection drawer, and high-res mockups. |
| **Question 1 Video Script** | `JoshTalks_Growth_Assessment/video_scripts/Q1_Video_Walkthrough_Script.md` | Markdown | **READY** | Structured 2 min 45 sec video script with timestamps, visual cues, and narrative arc. |
| **QA Verification Report** | `JoshTalks_Growth_Assessment/documentation/QA_VERIFICATION_REPORT.md` | Markdown | **READY** | Complete quality assurance report verifying calculations, RTTM scoring deltas, and constraints. |
| **Requirements Specification** | `JoshTalks_Growth_Assessment/REQUIREMENTS.md` | Markdown | **READY** | Comprehensive extraction of all requirements, evaluation criteria, and constraints. |
| **Project Status Log** | `JoshTalks_Growth_Assessment/PROJECT_STATUS.md` | Markdown | **READY** | Tracking log recording status and validation evidence for each milestone. |

---

## 2. Step-by-Step Instructions for Reviewer Verification

1. **Viewing the Question 2 Final Report**:
   - Open `FirstName_LastName_Report.pdf` in any PDF reader.
   - Verify all 16 required sections, the 5 embedded diagnostic charts, the 15-session overview table, and case studies.
2. **Testing the Interactive Leaderboard Prototype (Question 1)**:
   - Double-click `JoshTalks_Growth_Assessment/question_1/leaderboard/index.html` to open in any web browser.
   - Test the filters (Language, Environment, Speaker Density, Overlap) and the **Strict (0.0s Collar) vs Standard (0.25s Collar)** toggle.
   - Click **"Compare Models"** to test the head-to-head inspection drawer.
3. **Reproducing the Data Analysis & RTTM Scoring**:
   - Run: `python JoshTalks_Growth_Assessment/question_2/scripts/05_independent_rttm_scoring.py`
   - Observe the terminal output: the independently computed DER matches published benchmark scores across all sessions within 0.00% to 0.09%.
4. **Executing Playground Runs (For Candidate / User)**:
   - Follow the step-by-step instructions in `JoshTalks_Growth_Assessment/question_2/experiments/EXPERIMENT_RUNBOOK.md`.
   - Paste the provided GCS audio links into [Deepgram Playground](https://playground.deepgram.com).
   - Save screenshots to `JoshTalks_Growth_Assessment/proof/screenshots/`.
   - Run `python JoshTalks_Growth_Assessment/question_2/scripts/import_playground_results.py` to auto-validate!

