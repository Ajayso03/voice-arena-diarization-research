import pandas as pd

master = pd.read_csv('JoshTalks_Growth_Assessment/question_2/data_exploration/master_recordings.csv')
for idx, r in master.iterrows():
    print(f"[{idx:02d}] {r['Session ID']}")
    print(f"     DER: {r['Nova-3 DER %']:.2f}% | Words: {r['Nova-3 words returned']} / {r['Words spoken (human reference)']} ({r['Speech covered by Nova-3 (%)']:.1f}% cov)")
    print(f"     URL: {r['Audio link']}\n")

