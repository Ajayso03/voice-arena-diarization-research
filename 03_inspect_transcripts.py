import pandas as pd

excel_path = "JoshTalks_Growth_Assessment/input/analysis_data.xlsx"
xl = pd.ExcelFile(excel_path)

transcripts = xl.parse('Transcripts', skiprows=2)
transcripts = transcripts.dropna(subset=['Session ID'])
transcripts.columns = [str(c).strip() for c in transcripts.columns]

print("Columns:", transcripts.columns.tolist())
failing = ['D20260825_S003_015_5SPK_IN_EN', 'D20260825_S003_014_5SPK_IN_EN', 'D20260826_S001_03_4SPK_IN_EN', 'D20260825_S004_26_2SPK_IN_EN', 'D20260825_S004_31_2SPK_IN_EN']

for sid in failing:
    print(f"\n=======================================================")
    print(f"SESSION: {sid}")
    sub = transcripts[transcripts['Session ID'] == sid]
    for _, r in sub.iterrows():
        spk = r.get('Reference speaker')
        rw = r.get('Reference words')
        nw = r.get('Nova-3 words')
        ew = r.get('ElevenLabs Scribe v2 words')
        rt = str(r.get('Human reference transcript'))[:160]
        nt = str(r.get('Nova-3 transcript'))[:160]
        et = str(r.get('ElevenLabs Scribe v2 transcript'))[:160]
        print(f"\nSpk: {spk} | Ref Words: {rw} | Nova Words: {nw} | Scribe Words: {ew}")
        print(f"  Ref:    {rt}")
        print(f"  Nova-3: {nt}")
        print(f"  Scribe: {et}")
