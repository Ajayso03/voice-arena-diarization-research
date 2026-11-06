import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 14

charts_dir = "JoshTalks_Growth_Assessment/question_2/charts"
os.makedirs(charts_dir, exist_ok=True)

master = pd.read_csv("JoshTalks_Growth_Assessment/question_2/data_exploration/master_recordings.csv")
excel_path = "JoshTalks_Growth_Assessment/input/analysis_data.xlsx"
xl = pd.ExcelFile(excel_path)
settings_der = xl.parse('Deepgram settings', skiprows=4, nrows=8)
settings_der.columns = [str(c).strip() for c in settings_der.columns]

settings_words = xl.parse('Deepgram settings', skiprows=15, nrows=8)
settings_words.columns = [str(c).strip() for c in settings_words.columns]

# Sort master by DER descending
master_sorted = master.sort_values('Nova-3 DER %', ascending=True).reset_index(drop=True)

# -------------------------------------------------------------
# CHART 1: Stacked DER Breakdown by Recording
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7))

y_pos = np.arange(len(master_sorted))
p1 = ax.barh(y_pos, master_sorted['Nova-3 missed speech %'], color='#d9534f', label='Missed Speech (%)', height=0.65)
p2 = ax.barh(y_pos, master_sorted['Nova-3 false alarm %'], left=master_sorted['Nova-3 missed speech %'], color='#f0ad4e', label='False Alarm (%)', height=0.65)
p3 = ax.barh(y_pos, master_sorted['Nova-3 speaker confusion %'], 
             left=master_sorted['Nova-3 missed speech %'] + master_sorted['Nova-3 false alarm %'], 
             color='#5bc0de', label='Speaker Confusion (%)', height=0.65)

ax.set_yticks(y_pos)
labels = [f"{r['Session ID']} ({r['Accent']})" for _, r in master_sorted.iterrows()]
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel('Diarization Error Rate (%)', fontweight='bold')
ax.set_title('Figure 1: Deepgram Nova-3 Diarization Error Breakdown across 15 Benchmark Sessions\n(Massive Missed Speech Drives All Failures >85%)', fontweight='bold', pad=15)
ax.set_xlim(0, 105)
ax.axvline(50, color='gray', linestyle='--', alpha=0.7, label='50% DER Threshold')

# Annotate DER totals on bars
for i, r in master_sorted.iterrows():
    total = r['Nova-3 DER %']
    ax.text(total + 1.0, i, f"{total:.1f}%", va='center', fontsize=8.5, fontweight='bold', color='#333333')

ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
fig.savefig(f"{charts_dir}/01_der_breakdown_by_recording.png", dpi=300)
plt.close()
print("Saved 01_der_breakdown_by_recording.png")

# -------------------------------------------------------------
# CHART 2: Word Recall % vs DER % (The Smoking Gun)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))

master['Word Recall %'] = (master['Nova-3 words returned'] / master['Words spoken (human reference)'] * 100)

scatter = ax.scatter(master['Word Recall %'], master['Nova-3 DER %'], 
                     s=master['Speakers']*50, c=master['Time with 2+ people talking (% of speech)'], 
                     cmap='viridis', alpha=0.85, edgecolors='black', linewidth=1.5)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Overlap Ratio (% of speech time)', rotation=270, labelpad=15, fontweight='bold')

for _, r in master.iterrows():
    offset_x = 2
    offset_y = 1
    if r['Word Recall %'] < 10:
        offset_y = -3 if '014' in r['Session ID'] else 1.5
    ax.annotate(r['Session ID'].split('_')[1] + '_' + r['Session ID'].split('_')[2], 
                (r['Word Recall %'], r['Nova-3 DER %']), 
                xytext=(r['Word Recall %'] + offset_x, r['Nova-3 DER %'] + offset_y),
                fontsize=8, alpha=0.85)

ax.set_xlabel('Nova-3 Word Recall (% of Reference Words Transcribed)', fontweight='bold')
ax.set_ylabel('Nova-3 Diarization Error Rate (%)', fontweight='bold')
ax.set_title('Figure 2: Empirical Coupling of Diarization Error to Transcription Dropout\n(r = -0.99: Diarization Segments Vanish when ASR Decoder Drops Words)', fontweight='bold', pad=15)
ax.set_xlim(-5, 110)
ax.set_ylim(0, 108)

# Add quadrant shade
ax.axvspan(-5, 40, ymin=0.75, ymax=1.05, color='#d9534f', alpha=0.15)
ax.text(15, 92, "Catastrophic ASR Dropout Zone\n(Word Recall < 35%, DER > 85%)", ha='center', color='#d9534f', fontweight='bold', fontsize=9)

ax.axvspan(70, 110, ymin=0, ymax=0.45, color='#5cb85c', alpha=0.15)
ax.text(88, 12, "Normal Operational Zone\n(Word Recall > 75%, DER 15-35%)", ha='center', color='#4cae4c', fontweight='bold', fontsize=9)

plt.tight_layout()
fig.savefig(f"{charts_dir}/02_word_recall_vs_der.png", dpi=300)
plt.close()
print("Saved 02_word_recall_vs_der.png")

# -------------------------------------------------------------
# CHART 3: Nova-3 vs Competing Systems on Failing vs Good Sessions
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6))

systems = [
    ('Nova-3 DER %', 'Deepgram Nova-3', '#d9534f'),
    ('ElevenLabs Scribe v2 DER %', 'ElevenLabs Scribe v2', '#337ab7'),
    ('Smallest AI Pulse DER %', 'Smallest AI Pulse', '#5cb85c'),
    ('Meta Muse Voice Transcribe DER %', 'Meta Muse Voice', '#9b59b6'),
    ('pyannoteAI Precision-3 DER %', 'pyannoteAI Precision-3', '#e67e22')
]

master['Cohort'] = np.where(master['Nova-3 DER %'] > 50, 'Failing Sessions (n=8)', 'Passing Sessions (n=7)')
cohort_means = master.groupby('Cohort')[[col for col, _, _ in systems]].mean()

x = np.arange(len(systems))
width = 0.35

rects1 = ax.bar(x - width/2, cohort_means.loc['Failing Sessions (n=8)'], width, label='Failing Cohort (Nova-3 DER > 85%)', color='#d9534f', alpha=0.9)
rects2 = ax.bar(x + width/2, cohort_means.loc['Passing Sessions (n=7)'], width, label='Passing Cohort (Nova-3 DER < 36%)', color='#337ab7', alpha=0.9)

ax.set_ylabel('Mean Diarization Error Rate (%)', fontweight='bold')
ax.set_title('Figure 3: System Performance Divergence on Failing vs Passing Cohorts\n(While Competing Systems Degrade Mildly, Nova-3 Collapses from 28% to 96%)', fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels([name for _, name, _ in systems], rotation=15, ha='right', fontweight='bold')
ax.legend(frameon=True, facecolor='white')
ax.set_ylim(0, 110)

# Add values above bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
fig.savefig(f"{charts_dir}/03_nova3_vs_competing_systems.png", dpi=300)
plt.close()
print("Saved 03_nova3_vs_competing_systems.png")

# -------------------------------------------------------------
# CHART 4: Deepgram Settings Impact on Failing Sessions
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

configs = [
    ('Benchmark-style setting (nova-3, language en)', 'Nova-3 (en)', '#d9534f'),
    ('nova-3, language en-IN', 'Nova-3 (en-IN)', '#e74c3c'),
    ('nova-3, language multi', 'Nova-3 (multi)', '#f39c12'),
    ('nova-3, language multi, diarize v1', 'Nova-3 (multi+v1)', '#e67e22'),
    ('nova-2', 'Nova-2', '#95a5a6'),
    ('whisper-large (hosted by Deepgram)', 'Whisper-Large', '#2ecc71')
]

mean_ders = [settings_der[col].mean() for col, _, _ in configs]
mean_words = [settings_words[col].mean() for col, _, _ in configs]
labels = [label for _, label, _ in configs]
colors = [c for _, _, c in configs]

ax1.bar(labels, mean_ders, color=colors, width=0.6, edgecolor='black', alpha=0.9)
ax1.set_ylabel('Mean DER (%) across 8 Failing Sessions', fontweight='bold')
ax1.set_title('DER Reduction by Configuration Setting', fontweight='bold')
ax1.set_xticklabels(labels, rotation=25, ha='right')
ax1.set_ylim(0, 110)
for i, v in enumerate(mean_ders):
    ax1.text(i, v + 2, f"{v:.1f}%", ha='center', fontweight='bold', fontsize=9)

ax2.bar(labels, mean_words, color=colors, width=0.6, edgecolor='black', alpha=0.9)
ax2.set_ylabel('Mean Words Returned per Session', fontweight='bold')
ax2.set_title('Word Recovery by Configuration Setting', fontweight='bold')
ax2.set_xticklabels(labels, rotation=25, ha='right')
for i, v in enumerate(mean_words):
    ax2.text(i, v + 30, f"{int(v)}", ha='center', fontweight='bold', fontsize=9)

plt.suptitle('Figure 4: Impact of Language Configuration & Model Architecture on Failing Sessions\n(language=multi and Whisper-Large Restore Word Emission and Reduce DER by 30-65%)', fontweight='bold', y=1.02)
plt.tight_layout()
fig.savefig(f"{charts_dir}/04_deepgram_settings_comparison.png", dpi=300)
plt.close()
print("Saved 04_deepgram_settings_comparison.png")

# -------------------------------------------------------------
# CHART 5: Acoustic Noise & Overlap vs DER (Falsifying Noise Hypothesis)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# Panel A: SNR vs DER
ax1.scatter(master['Speech above background (dB)'], master['Nova-3 DER %'], 
            c=np.where(master['Nova-3 DER %'] > 50, '#d9534f', '#5cb85c'), s=90, edgecolors='black')
ax1.set_xlabel('Speech Above Background Noise (dB SNR)', fontweight='bold')
ax1.set_ylabel('Nova-3 DER (%)', fontweight='bold')
ax1.set_title('A: SNR vs Diarization Error Rate\n(Clean audio files with SNR > 16dB still suffer 98% DER)', fontweight='bold')

# Annotate counterexamples
for _, r in master.iterrows():
    if r['Session ID'] in ['D20260825_S004_31_2SPK_IN_EN', 'D20260825_S003_014_5SPK_IN_EN']:
        ax1.annotate(r['Session ID'].split('_')[1] + '_' + r['Session ID'].split('_')[2] + f" ({r['Nova-3 DER %']:.1f}%)", 
                     (r['Speech above background (dB)'], r['Nova-3 DER %']),
                     xytext=(r['Speech above background (dB)'] + 1, r['Nova-3 DER %'] - 3),
                     fontsize=8.5, fontweight='bold')

# Panel B: Overlap vs DER
ax2.scatter(master['Time with 2+ people talking (% of speech)'], master['Nova-3 DER %'], 
            c=np.where(master['Nova-3 DER %'] > 50, '#d9534f', '#5cb85c'), s=90, edgecolors='black')
ax2.set_xlabel('Time with 2+ People Talking (% of Speech)', fontweight='bold')
ax2.set_ylabel('Nova-3 DER (%)', fontweight='bold')
ax2.set_title('B: Overlap Ratio vs Diarization Error Rate\n(Sessions with < 5% overlap still collapse to 97% DER)', fontweight='bold')

for _, r in master.iterrows():
    if r['Session ID'] in ['D20260906_S003_04_4SPK_IN_EN', 'D20260826_S001_012_3SPK_IN_EN']:
        ax2.annotate(r['Session ID'].split('_')[1] + '_' + r['Session ID'].split('_')[2] + f" ({r['Nova-3 DER %']:.1f}%)", 
                     (r['Time with 2+ people talking (% of speech)'], r['Nova-3 DER %']),
                     xytext=(r['Time with 2+ people talking (% of speech)'] + 1, r['Nova-3 DER %'] - 4),
                     fontsize=8.5, fontweight='bold')

plt.suptitle('Figure 5: Acoustic Environmental Metrics vs Diarization Failure\n(Acoustic Quality and Overlap Do Not Differentiate Failing from Passing Files)', fontweight='bold', y=1.03)
plt.tight_layout()
fig.savefig(f"{charts_dir}/05_snr_and_overlap_vs_der.png", dpi=300)
plt.close()
print("Saved 05_snr_and_overlap_vs_der.png")

