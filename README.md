# Voice Arena Diarization Research
### An Independent Forensic Analysis of Deepgram Nova-3 Speech Recognition and Speaker Diarization Performance

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Research](https://img.shields.io/badge/Project-Speech%20AI-purple)
![Domain](https://img.shields.io/badge/Domain-ASR%20%7C%20Diarization-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

## Overview

This project presents an independent technical investigation into the performance of **Deepgram Nova-3** on the Voice Arena Diarization-Bench.

The research examines speech recognition and speaker diarization failures, focusing on missed speech, transcription coverage, acoustic conditions, speaker overlap, and configuration sensitivity.

The investigation combines dataset analysis, transcript inspection, independent RTTM scoring, statistical analysis, and alternative model/configuration experiments to understand why a speech AI system can experience substantial diarization errors even when speech is clearly present in the recording.

The detailed investigation covers **15 recordings** from the larger benchmark.

## Research Objectives

The primary objectives were:

- Evaluate Deepgram Nova-3's diarization performance.
- Identify the dominant contributors to diarization errors.
- Investigate the relationship between transcription output and diarization accuracy.
- Examine whether background noise, audio quality, and overlapping speech explain performance degradation.
- Compare alternative language and model configurations.
- Independently verify diarization metrics using RTTM annotations.
- Develop recommendations for more robust speech AI evaluation and deployment.

## Key Findings

The analysis revealed a significant performance difference across the 15 recordings.

| Metric | Result |
|---|---:|
| Detailed recordings analysed | 15 |
| Catastrophic failure recordings | 8 |
| Better-performing recordings | 7 |
| DER in catastrophic cases | 86.0–100.0% |
| DER in better-performing cases | 15.1–35.3% |
| Word recall in catastrophic cases | 0.0–23.5% |
| Word recall in better-performing cases | 76.5–98.3% |
| Word recall vs. DER correlation | -0.99 |

**Primary observation:** Missed speech was the dominant contributor to the most severe diarization failures, rather than false alarms or speaker confusion.

The strong inverse correlation between word recall and DER suggests that transcription dropout and diarization degradation are closely associated in the analysed recordings. This correlation does not, by itself, establish causation.

## Experimental Investigation

### 1. Diarization Error Analysis

Diarization Error Rate (DER) was decomposed into three components:

- **Missed Speech:** Speech present in the reference that the system failed to detect.
- **False Alarm:** Speech incorrectly detected during reference silence.
- **Speaker Confusion:** Speech attributed to an incorrect speaker.

The results indicated that missed speech dominated the most severe failures.

### 2. Transcription Coverage Analysis

Reference transcripts were compared against Nova-3 outputs to calculate word recall.

A strong relationship was observed between reduced transcription coverage and increased diarization error.

This investigation examined whether the absence of recognised words could be associated with missing speaker-labelled segments.

### 3. Acoustic Quality and Overlap Analysis

The investigation considered:

- Signal-to-noise ratio (SNR).
- Background noise.
- Audio clipping.
- Speech activity.
- Overlapping speakers.
- Voice activity detection (VAD) coverage.

The observed failures could not be explained by audio quality or overlapping speech alone.

### 4. Alternative Configuration Experiments

Alternative configurations were evaluated on selected recordings.

| Configuration | Mean DER across failing sessions |
|---|---:|
| Nova-3 (`language=en`) | 96.6% |
| Nova-3 (`language=en-IN`) | 96.5% |
| Nova-3 (`language=multi`) | 73.5% |
| Nova-3 (`language=multi`, diarize v1) | 63.3% |
| Nova-2 | 93.1% |
| Whisper-Large | 54.4% |

Multilingual configuration restored substantially more transcription output in selected recordings.

For example:
- One recording increased from 34 to 983 returned words.
- Another increased from 56 to 1,624 returned words.

These findings suggest that language configuration and transcription behaviour may significantly influence downstream diarization performance.

They do not establish the exact internal cause of the model's failures.

## Diagnostic Visualizations

The repository includes five diagnostic figures.

### 1. Diarization Error Breakdown

Shows the contribution of missed speech, false alarms, and speaker confusion across the analysed recordings.

![DER Breakdown](figures/01_der_breakdown_by_recording.png)

### 2. Word Recall vs. Diarization Error

Examines the relationship between transcription coverage and diarization error.

![Word Recall vs DER](figures/02_word_recall_vs_der.png)

### 3. System Performance Comparison

Compares the performance of Nova-3 and competing systems across failing and better-performing cohorts.

![System Comparison](figures/03_nova3_vs_competing_systems.png)

### 4. Configuration Comparison

Shows the impact of alternative language and model configurations on DER and transcription output.

![Configuration Comparison](figures/04_deepgram_settings_comparison.png)

### 5. Acoustic Quality and Speaker Overlap

Examines whether signal-to-noise ratio and overlapping speech distinguish failing recordings from better-performing ones.

![Acoustic Diagnostics](figures/05_snr_and_overlap_vs_der.png)

## Technical Methodology

The project uses a combination of Python-based data processing, statistical analysis, and independent diarization evaluation.

### Technologies and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- SciPy
- Scikit-learn
- RTTM (Rich Transcription Time Marked)
- Voice Activity Detection (VAD)

### Independent RTTM Scoring

A standalone scoring implementation was developed to evaluate diarization outputs.

The implementation includes:

1. Parsing reference
