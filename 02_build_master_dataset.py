import pandas as pd
import numpy as np

excel_path = "JoshTalks_Growth_Assessment/input/analysis_data.xlsx"
xl = pd.ExcelFile(excel_path)

sessions = xl.parse('Sessions', skiprows=3)
sessions.columns = [c.strip() for c in sessions.columns]

results = xl.parse('Results', skiprows=4)
results.columns = [c.strip() for c in results.columns]

audio_q = xl.parse('Audio quality', skiprows=4)
audio_q.columns = [c.strip() for c in audio_q.columns]

print("=== RESULTS SHEET COLUMNS ===")
for i, col in enumerate(results.columns):
    print(f"{i:02d}: {col}")

# Merge sessions, results, audio quality
master = sessions.merge(results, on='Session ID', how='outer')
master = master.merge(audio_q, on='Session ID', how='outer')

print(f"\nMaster shape: {master.shape}")
print("\n=== RECORDINGS SUMMARY ===")
summary_cols = [
    'Session ID', 'Setting', 'Accent', 'Speakers', 'Audio length (min)',
    'Time with 2+ people talking (% of speech)', 'Nova-3 DER %',
    'Nova-3 missed speech %', 'Nova-3 false alarm %', 'Nova-3 speaker confusion %',
    'Nova-3 words returned', 'Words spoken (human reference)',
    'Speech covered by Nova-3 (%)', 'Speech covered by VAD (%)',
    'Speech above background (dB)'
]

for col in results.columns:
    if 'DER %' in col and col != 'Nova-3 DER %':
        summary_cols.append(col)

print(master[summary_cols].to_string())

# Save master dataset to question_2/data_exploration/master_recordings.csv
out_dir = "JoshTalks_Growth_Assessment/question_2/data_exploration"
master.to_csv(f"{out_dir}/master_recordings.csv", index=False)
print(f"\nSaved master dataset to {out_dir}/master_recordings.csv")

