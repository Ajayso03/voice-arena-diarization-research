import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
ax.set_facecolor('#0f172a')
fig.patch.set_facecolor('#0f172a')

# Title
ax.text(0.04, 0.92, "Voice of India: Head-to-Head Model Inspection Drawer", transform=ax.transAxes, 
        color='white', fontsize=15, fontweight='bold')
ax.text(0.04, 0.87, "Deepgram Nova-3 (en) vs ElevenLabs Scribe v2 | Paired Wilcoxon p < 0.0001 (Statistically Significant)", 
        transform=ax.transAxes, color='#94a3b8', fontsize=9)

# Two Cards
for idx, (name, prov, col, der, ms, fa, sc, cov, wds, cost, rtf) in enumerate([
    ("Deepgram Nova-3 (en)", "Deepgram Inc.", "#ef4444", "67.1%", "58.2%", "4.8%", "4.1%", "46.2%", "120 wds/file", "$0.0077/m", "0.03x"),
    ("ElevenLabs Scribe v2", "ElevenLabs", "#3b82f6", "18.9%", "9.2%", "4.5%", "5.2%", "96.8%", "1,850 wds/file", "$0.0240/m", "0.12x")
]):
    x = 0.04 + idx * 0.47
    card = patches.FancyBboxPatch((x, 0.08), 0.45, 0.75, transform=ax.transAxes,
                                 boxstyle="round,pad=0.01", fc="#1e293b", ec=col, lw=1.5)
    ax.add_patch(card)
    
    # Header inside card
    ax.text(x + 0.03, 0.77, name, transform=ax.transAxes, color='white', fontsize=12, fontweight='bold')
    ax.text(x + 0.03, 0.73, prov, transform=ax.transAxes, color='#94a3b8', fontsize=8.5)
    
    # Metrics
    metrics = [
        ("Strict DER (0s Collar)", der, col, True),
        ("Missed Speech Time", ms, "#ef4444", False),
        ("False Alarm Time", fa, "#f59e0b", False),
        ("Speaker Confusion Time", sc, "#3b82f6", False),
        ("Speech Coverage", cov, "#10b981" if float(cov.replace('%',''))>70 else "#ef4444", True),
        ("Lexical Word Recall", wds, "white", False),
        ("Real-Time Factor (RTF)", rtf, "white", False),
        ("Operational Cost", cost, "white", False)
    ]
    
    for m_idx, (m_lbl, m_val, m_col, is_bold) in enumerate(metrics):
        my = 0.66 - m_idx * 0.065
        ax.plot([x + 0.03, x + 0.42], [my - 0.015, my - 0.015], transform=ax.transAxes, color='#334155', lw=0.6)
        ax.text(x + 0.03, my, m_lbl, transform=ax.transAxes, color='#cbd5e1', fontsize=8.5)
        ax.text(x + 0.42, my, m_val, transform=ax.transAxes, color=m_col, fontsize=9.5 if is_bold else 8.5, 
                fontweight='bold' if is_bold else 'normal', ha='right')

ax.axis('off')
plt.tight_layout()
fig.savefig("JoshTalks_Growth_Assessment/question_1/leaderboard/leaderboard_compare_mockup.png", bbox_inches='tight')
plt.close()
print("Saved leaderboard_compare_mockup.png successfully.")

