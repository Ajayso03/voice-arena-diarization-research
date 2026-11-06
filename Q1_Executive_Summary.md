# Executive Summary: Voice of India Diarization Benchmark
### National Evaluation Standard & Public Leaderboard Architecture for Indian Conversational Speech
**Prepared for**: Leadership & Enterprise AI Decision Makers | **Reading Time**: 2 Minutes

---

### The Problem & Industry Need
Enterprise voice assistants, meeting intelligence tools, and customer support analytics platforms rely critically on speaker diarization ("who spoke when"). However, commercial models that boast single-digit Diarization Error Rates (DER) on Western benchmarks frequently collapse in India. Under Indian accents, regional vernaculars, rapid turn-taking, and room reverberation, published benchmark scores overstate real-world accuracy by 3x to 5x. Decision-makers currently lack a neutral, statistically rigorous, and representative leaderboard to guide technology selection.

---

### The Evaluation Architecture at a Glance

```
+----------------------------------------------------------------------------------------------------+
|                                    VOICE OF INDIA BENCHMARK CORE                                   |
+-----------------------------+------------------------------------+---------------------------------+
|     The 100-Hour Test Set   |         Hardware Channel           |      The Gold Standard Ref      |
|  - 35% Indian English       |  - Distant Room Mic (Test Feed):   |  - Synchronous Close-Talking    |
|  - 45% Regional Vernaculars |    Omnidirectional Tabletop WAV    |    Lavalier Mics (Ground Truth) |
|  - 20% Hinglish/Code-Switch |  - 16 kHz, 16-bit Mono Linear PCM  |  - Dual-Annotator Redundancy    |
|  - 2 to 8 Speakers / file   |  - Telephony 8kHz Narrowband Track |  - Inter-Annotator Alpha >= 0.92|
+-----------------------------+------------------------------------+---------------------------------+
```

---

### Three Foundational Design Choices That Matter Most

1. **Dual-Collar Evaluation (Strict 0.0s vs Standard 0.25s)**:
   - *Design*: We report both strict zero-collar DER (penalizing every turn-boundary error and short vocable) and standard 250ms forgiving collar DER.
   - *Impact*: Eliminates benchmark gaming. Systems that artificially blur boundary transitions are immediately exposed.
2. **Architecture Decoupling (ASR-Dependent vs Acoustic-Only)**:
   - *Design*: We explicitly distinguish pure acoustic diarizers (e.g., `pyannote`) from joint ASR systems (e.g., `Deepgram`, `ElevenLabs`), reporting speech coverage and `tcpWER` alongside DER.
   - *Impact*: Prevents catastrophic misdiagnoses. When an ASR system drops accented speech tokens, our breakdown shows whether the failure is an ASR deletion or a clustering error.
3. **Statistically Defensible Tiering (Bootstrap CI & Wilcoxon Tests)**:
   - *Design*: Every score publishes a 95% Bootstrap Confidence Interval ($B = 10,000$ iterations). Pairwise comparisons enforce Wilcoxon signed-rank tests with Benjamini-Hochberg FDR control.
   - *Impact*: Stops buyers from selecting vendors based on statistical noise (e.g., a 0.8% score difference that has $p > 0.10$).

---

### Evaluated Model Landscape
We evaluate 10 canonical production systems spanning:
- **Pure Acoustic Diarizers**: `pyannote 3.1` (OSS), `pyannoteAI Precision-3` (Commercial).
- **Commercial ASR + Diarization APIs**: `Deepgram Nova-3`, `ElevenLabs Scribe v2`, `Speechmatics Enhanced`, `Soniox async v5`, `Smallest AI Pulse`, `AssemblyAI Universal-2`.
- **Modular & LLM Foundation Systems**: `Whisper-Large-v3 + pyannote` (WhisperX), `Meta Muse Voice Transcribe`.

---

### Core Takeaway
**Real diarization quality in India requires phonetic resilience, not just acoustic clustering.** 
Commercial systems integrated with speech-to-text decoders are vulnerable to catastrophic dropout when encountering Indian English phonology or vernacular code-switching, producing 90%+ Missed Speech despite pristine audio. The Voice of India Leaderboard provides the first transparent, multi-dimensional truth source for enterprise procurement and research acceleration.

