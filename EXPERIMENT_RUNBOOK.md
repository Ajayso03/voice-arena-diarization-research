# Deepgram Playground Experiment Runbook

## Objective
Verify benchmark claims independently by executing live inference runs on the official [Deepgram Playground](https://playground.deepgram.com) using the exact benchmark audio files. 

Per the assessment requirements:
- **3 Poor-Performing Recordings**: Confirm catastrophic ASR dropout under benchmark configuration.
- **2 Good-Performing Recordings**: Confirm normal transcription and low DER.
- **At least 2 Alternative Settings on a Poor Recording**: Test `language=multi` and an alternative model (e.g., `nova-2`) to demonstrate word recovery and falsify acoustic defect hypotheses.

---

## Required Test Matrix

| Exp ID | Session ID | Classification | Model | Language | Diarize | Utterances | Audio URL | Target Validation Metric |
|---|---|---|---|---|---|---|---|---|
| **EXP-01** | `D20260825_S003_015_5SPK_IN_EN` | Poor (100% Fail) | `nova-3` | `en` | `true` | `true` | [GCS Audio Link](https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260825_S003_015_5SPK_IN_EN/merged.wav) | 0 words returned (or near 0) |
| **EXP-02** | `D20260825_S003_014_5SPK_IN_EN` | Poor (99.1% Fail) | `nova-3` | `en` | `true` | `true` | [GCS Audio Link](https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260825_S003_014_5SPK_IN_EN/merged.wav) | ~34 words returned; halts at ~56s |
| **EXP-03** | `D20260826_S001_03_4SPK_IN_EN` | Poor (98.6% Fail) | `nova-3` | `en` | `true` | `true` | [GCS Audio Link](https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260826_S001_03_4SPK_IN_EN/merged.wav) | ~114 words returned (<5% recall) |
| **EXP-04** | `D20260825_S004_31_2SPK_IN_EN` | Good (15.1% DER) | `nova-3` | `en` | `true` | `true` | [GCS Audio Link](https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_day3_2person_full_pad30_split_none/D20260825_S004_31_2SPK_IN_EN/merged.wav) | ~788 words returned (high recall) |
| **EXP-05** | `D20260825_S004_24_2SPK_IN_EN` | Good (27.7% DER) | `nova-3` | `en` | `true` | `true` | [GCS Audio Link](https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_day3_2person_full_pad30_split_none/D20260825_S004_24_2SPK_IN_EN/merged.wav) | ~964 words returned (high recall) |
| **EXP-06** | `D20260825_S003_014_5SPK_IN_EN` | Alternative Lang | `nova-3` | `multi` | `true` | `true` | [GCS Audio Link](https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260825_S003_014_5SPK_IN_EN/merged.wav) | ~980 words returned (~30x word recovery) |
| **EXP-07** | `D20260825_S003_014_5SPK_IN_EN` | Alternative Model| `nova-2` | `en` | `true` | `true` | [GCS Audio Link](https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260825_S003_014_5SPK_IN_EN/merged.wav) | ~131 words returned (compare degradation) |

---

## Step-by-Step Execution Protocol

1. Navigate to **[https://playground.deepgram.com](https://playground.deepgram.com)** and sign in.
2. Select **Pre-recorded Audio** mode.
3. Paste the **Audio URL** for the corresponding experiment into the URL input box.
4. Configure Model & Parameters:
   - **Model**: `Nova-3` (or `Nova-2` for EXP-07).
   - **Language**: `English` (or `Multilingual / code switching` for EXP-06).
   - **Diarization**: Toggle **ON** (`diarize=true`).
   - **Utterances**: Toggle **ON** (`utterances=true`).
5. Click **Run** / **Transcribe**.
6. When the response renders:
   - Capture a clear screenshot showing:
     - The Audio URL entered.
     - The configuration pane (Model, Language, Diarization, Utterances).
     - The Request ID (if displayed in the console / UI).
     - The transcript and word/speaker count.
   - Save the screenshot to `JoshTalks_Growth_Assessment/proof/screenshots/` named as `EXP-01_D20260825_S003_015.png`, `EXP-02_...`, etc.
   - (Optional but recommended) Click **Download JSON** or copy the JSON response and save to `JoshTalks_Growth_Assessment/proof/responses/` as `EXP-01_response.json`.
7. Record the **Request ID**, **Date/Time**, **Words Returned**, and **Observed Behavior** in `JoshTalks_Growth_Assessment/question_2/experiments/experiment_tracker.csv`.
8. Run `python JoshTalks_Growth_Assessment/question_2/scripts/import_playground_results.py` to automatically validate the runs against benchmark baselines!

