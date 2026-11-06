import os
import pandas as pd
import numpy as np

excel_path = "JoshTalks_Growth_Assessment/input/analysis_data.xlsx"
xl = pd.ExcelFile(excel_path)
print(f"Loading workbook: {excel_path}")
print(f"Sheet names: {xl.sheet_names}\n")

# 1. Parse 'Read me'
readme_raw = xl.parse('Read me', header=None)
print("=== READ ME SHEET ===")
for idx, row in readme_raw.iterrows():
    val = str(row[0]).strip() if pd.notna(row[0]) else ""
    if val:
        print(f"[{idx}] {val}")

# 2. Parse 'Sessions'
# Header is at row 3 (0-indexed)
sessions_df = xl.parse('Sessions', skiprows=3)
sessions_df.columns = [c.strip() for c in sessions_df.columns]
print("\n=== SESSIONS SHEET ===")
print(sessions_df.info())
print(sessions_df.head(3))

# 3. Parse 'Results'
# Header is at row 4
results_df = xl.parse('Results', skiprows=4)
results_df.columns = [c.strip() for c in results_df.columns]
print("\n=== RESULTS SHEET ===")
print(results_df.info())
print(results_df.head(3))

# 4. Parse 'Transcripts'
# Header is at row 2 or 3
transcripts_raw = xl.parse('Transcripts', header=None)
# Find row with 'Session ID'
header_idx = None
for r in range(5):
    if 'Session ID' in [str(x) for x in transcripts_raw.iloc[r]]:
        header_idx = r
        break
transcripts_df = xl.parse('Transcripts', skiprows=header_idx)
transcripts_df.columns = [str(c).strip() for c in transcripts_df.columns]
print("\n=== TRANSCRIPTS SHEET ===")
print(transcripts_df.info())
print(transcripts_df.head(3))

# 5. Parse 'Deepgram API check'
api_check_df = xl.parse('Deepgram API check', skiprows=3)
api_check_df.columns = [c.strip() for c in api_check_df.columns]
print("\n=== DEEPGRAM API CHECK SHEET ===")
print(api_check_df.info())
print(api_check_df.head(3))

# 6. Parse 'Audio quality'
audio_quality_df = xl.parse('Audio quality', skiprows=4)
audio_quality_df.columns = [c.strip() for c in audio_quality_df.columns]
print("\n=== AUDIO QUALITY SHEET ===")
print(audio_quality_df.info())
print(audio_quality_df.head(3))

# 7. Parse 'Deepgram settings'
settings_raw = xl.parse('Deepgram settings', header=None)
# Note that Deepgram settings contains two tables: Table 1 (DER %) and Table 2 (words returned)
print("\n=== DEEPGRAM SETTINGS SHEET RAW ===")
for r in range(min(25, len(settings_raw))):
    row_vals = [str(x) if pd.notna(x) else "" for x in settings_raw.iloc[r].tolist()]
    print(f"Row {r:02d}:", " | ".join(row_vals[:10]))

