import pandas as pd
import numpy as np

master = pd.read_csv("JoshTalks_Growth_Assessment/question_2/data_exploration/master_recordings.csv")
rttm_verif = pd.read_csv("JoshTalks_Growth_Assessment/question_2/rttm_analysis/rttm_independent_verification.csv")

# Merge
df = master.copy()
df['Failing'] = df['Nova-3 DER %'] > 50.0

print("=== CORRELATION & GROUP ANALYSIS ===")
print("\nBy Station:")
print(df.groupby('Recording station').agg(
    count=('Session ID', 'count'),
    failing_count=('Failing', 'sum'),
    mean_der=('Nova-3 DER %', 'mean'),
    mean_missed=('Nova-3 missed speech %', 'mean'),
    mean_nova_cov=('Speech covered by Nova-3 (%)', 'mean'),
    mean_vad_cov=('Speech covered by VAD (%)', 'mean'),
    mean_snr=('Speech above background (dB)', 'mean')
))

print("\nBy Accent:")
print(df.groupby('Accent').agg(
    count=('Session ID', 'count'),
    failing_count=('Failing', 'sum'),
    mean_der=('Nova-3 DER %', 'mean'),
    mean_missed=('Nova-3 missed speech %', 'mean')
))

print("\nBy Number of Speakers:")
print(df.groupby('Speakers').agg(
    count=('Session ID', 'count'),
    failing_count=('Failing', 'sum'),
    mean_der=('Nova-3 DER %', 'mean'),
    mean_words_returned=('Nova-3 words returned', 'mean'),
    mean_ref_words=('Words spoken (human reference)', 'mean')
))

print("\nCorrelations with Nova-3 DER %:")
num_cols = [
    'Speakers', 'Audio length (min)', 'Time with 2+ people talking (% of speech)',
    'Words spoken (human reference)', 'Overall loudness (dBFS)',
    'Background noise level (dBFS)', 'Speech level (dBFS)',
    'Speech above background (dB)', 'Clipped samples (%)'
]
corr = df[num_cols + ['Nova-3 DER %']].corr()['Nova-3 DER %'].sort_values(ascending=False)
print(corr)

