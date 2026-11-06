import pandas as pd

excel_path = "JoshTalks_Growth_Assessment/input/analysis_data.xlsx"
xl = pd.ExcelFile(excel_path)

transcripts = xl.parse('Transcripts', skiprows=3)
transcripts = transcripts.dropna(subset=['Session ID'])
transcripts.columns = [str(c).strip() for c in transcripts.columns]

# Group by session and compute totals
grouped = transcripts.groupby('Session ID').agg({
    'Reference speaker': 'count',
    'Reference words': 'sum',
    'Nova-3 words': 'sum',
    'ElevenLabs Scribe v2 words': 'sum'
}).reset_index()

grouped.columns = ['Session ID', 'Speakers in Transcripts', 'Total Ref Words', 'Total Nova-3 Words', 'Total Scribe Words']
grouped['Nova-3 Word Recall %'] = (grouped['Total Nova-3 Words'] / grouped['Total Ref Words'] * 100).round(1)
grouped['Scribe Word Recall %'] = (grouped['Total Scribe Words'] / grouped['Total Ref Words'] * 100).round(1)

print("=== TRANSCRIPT WORD RECALL SUMMARY ===")
print(grouped.to_string())

# Also inspect API check sheet
api_check = xl.parse('Deepgram API check', skiprows=3)
api_check.columns = [str(c).strip() for c in api_check.columns]
print("\n=== DEEPGRAM API CHECK ===")
print(api_check[['Session ID', 'File length (s)', 'Words returned', 'First word at (s)', 'Last word at (s)', 'Transcript confidence', 'Average word confidence', 'Warnings']].to_string())

