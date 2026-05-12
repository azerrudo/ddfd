import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY    = '#0D2B55'
SLATE   = '#44546E'
GOLD    = '#C89A2A'
TEAL    = '#1B7F8E'
CORAL   = '#C0392B'
LIGHT   = '#F0F4F8'
MID_BLU = '#2E6DA4'
WHITE   = '#FFFFFF'

plt.rcParams.update({
    'font.family':      'DejaVu Sans',
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'axes.grid':        True,
    'grid.color':       '#E2E8F0',
    'grid.linewidth':   0.6,
    'axes.axisbelow':   True,
})

fig = plt.figure(figsize=(16, 10), facecolor=WHITE)
fig.subplots_adjust(hspace=0.42, wspace=0.32,
                    left=0.06, right=0.97, top=0.88, bottom=0.08)

gs = GridSpec(2, 3, figure=fig)

# ── Title block ───────────────────────────────────────────────────────────────
fig.text(0.5, 0.955, 'Meridian Technologies — Board Financial Dashboard',
         ha='center', va='center', fontsize=17, fontweight='bold', color=NAVY)
fig.text(0.5, 0.925, 'Annual Strategic Review  ·  May 2026',
         ha='center', va='center', fontsize=10, color=SLATE)

# gold rule under title
line = matplotlib.lines.Line2D([0.06, 0.97], [0.912, 0.912],
                                transform=fig.transFigure,
                                color=GOLD, linewidth=1.5)
fig.add_artist(line)

# ── Helper: label on bar ──────────────────────────────────────────────────────
def bar_label(ax, bars, fmt='{:.0f}', color='white', fontsize=8, offset=0):
    for bar in bars:
        h = bar.get_height()
        x = bar.get_x() + bar.get_width() / 2
        ax.text(x, h + offset, fmt.format(h),
                ha='center', va='bottom', fontsize=fontsize, color=color)

def axis_style(ax, title, ylabel=''):
    ax.set_title(title, fontsize=10.5, fontweight='bold', color=NAVY,
                 pad=10, loc='left')
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=8.5, color=SLATE)
    ax.tick_params(colors=SLATE, labelsize=8)
    ax.spines['left'].set_color('#CBD5E0')
    ax.spines['bottom'].set_color('#CBD5E0')


# ══════════════════════════════════════════════════════════════════════════════
# Chart 1 — Revenue & YoY Growth  (top-left, wide)
# ══════════════════════════════════════════════════════════════════════════════
ax1 = fig.add_subplot(gs[0, :2])

years  = ['FY 2022', 'FY 2023', 'FY 2024', 'FY 2025', 'FY 2026\n(Guide)']
rev    = [260.4, 310.6, 360.2, 400.0, 447.5]   # midpoint of guide for 2026
growth = [None, 19, 16, 11, 12]                 # midpoint ~12%

x = np.arange(len(years))
bars = ax1.bar(x, rev, color=[NAVY, NAVY, NAVY, NAVY, MID_BLU],
               width=0.5, zorder=3, alpha=0.92)

# revenue labels
for bar, r in zip(bars, rev):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 4,
             f'${r:.0f}M', ha='center', va='bottom', fontsize=8.5,
             fontweight='bold', color=NAVY)

# growth rate line on secondary axis
ax1b = ax1.twinx()
g_vals = [np.nan if g is None else g for g in growth]
ax1b.plot(x[1:], g_vals[1:], color=GOLD, marker='o',
          linewidth=2.2, markersize=7, zorder=4, label='YoY Growth %')
for i, g in enumerate(g_vals[1:], 1):
    ax1b.text(i, g + 1.2, f'{g:.0f}%', ha='center', va='bottom',
              fontsize=8.5, color=GOLD, fontweight='bold')

ax1b.set_ylim(0, 35)
ax1b.set_ylabel('YoY Growth (%)', fontsize=8.5, color=GOLD)
ax1b.tick_params(colors=GOLD, labelsize=8)
ax1b.spines['right'].set_color(GOLD)
ax1b.spines['top'].set_visible(False)
ax1b.spines['left'].set_visible(False)

ax1.set_xticks(x)
ax1.set_xticklabels(years, fontsize=9)
ax1.set_ylim(0, 520)
ax1.set_ylabel('Revenue ($M)', fontsize=8.5, color=SLATE)
axis_style(ax1, 'Revenue & YoY Growth Rate')

# guide annotation
ax1.axvline(x=3.5, color='#CBD5E0', linewidth=1, linestyle='--', zorder=2)
ax1.text(3.52, 490, 'Guidance →', fontsize=7.5, color=SLATE, va='top')


# ══════════════════════════════════════════════════════════════════════════════
# Chart 2 — Operating Margin & FCF Margin  (top-right)
# ══════════════════════════════════════════════════════════════════════════════
ax2 = fig.add_subplot(gs[0, 2])

quarters = ['Q1\n2024','Q2','Q3','Q4','Q1\n2025','Q2','Q3','Q4']
op_margin  = [9.4, 9.8, 10.1, 10.5, 11.1, 11.6, 12.0, 12.4]
fcf_margin = [14.8,15.7,16.2,16.8,15.9,16.5,17.2,17.8]

xq = np.arange(len(quarters))
ax2.fill_between(xq, fcf_margin, alpha=0.15, color=TEAL, zorder=2)
ax2.plot(xq, fcf_margin, color=TEAL, linewidth=2, marker='o',
         markersize=5, label='FCF Margin', zorder=3)
ax2.plot(xq, op_margin, color=GOLD, linewidth=2.2, marker='s',
         markersize=5, label='Operating Margin', zorder=3)

ax2.set_xticks(xq)
ax2.set_xticklabels(quarters, fontsize=7.5)
ax2.set_ylim(6, 22)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}%'))
ax2.legend(fontsize=7.5, loc='upper left', frameon=False)
axis_style(ax2, 'Margin Expansion', ylabel='Margin (%)')

# end labels
ax2.text(len(quarters)-1+0.08, fcf_margin[-1], f'{fcf_margin[-1]:.1f}%',
         va='center', fontsize=8, color=TEAL, fontweight='bold')
ax2.text(len(quarters)-1+0.08, op_margin[-1], f'{op_margin[-1]:.1f}%',
         va='center', fontsize=8, color=GOLD, fontweight='bold')


# ══════════════════════════════════════════════════════════════════════════════
# Chart 3 — Segment ARR Mix  (bottom-left)
# ══════════════════════════════════════════════════════════════════════════════
ax3 = fig.add_subplot(gs[1, 0])

seg_years = ['Q4 2022', 'Q4 2023', 'Q4 2024', 'Q4 2025']
enterprise = [74,  108, 138, 167]
midmarket  = [96,  130, 160, 194]
smb        = [105, 90,  68,  52]

x3 = np.arange(len(seg_years))
w  = 0.52
p1 = ax3.bar(x3, enterprise, w, label='Enterprise', color=NAVY,   zorder=3)
p2 = ax3.bar(x3, midmarket,  w, bottom=enterprise, label='Mid-market', color=MID_BLU, zorder=3)
p3 = ax3.bar(x3, smb, w, bottom=[e+m for e,m in zip(enterprise,midmarket)],
             label='SMB', color='#A0B4C8', zorder=3)

# % mix labels inside bars
totals = [e+m+s for e,m,s in zip(enterprise,midmarket,smb)]
for i, (e,m,s,t) in enumerate(zip(enterprise,midmarket,smb,totals)):
    ax3.text(i, e/2,    f'{e/t*100:.0f}%', ha='center', va='center',
             fontsize=7.5, color=WHITE, fontweight='bold')
    ax3.text(i, e+m/2,  f'{m/t*100:.0f}%', ha='center', va='center',
             fontsize=7.5, color=WHITE, fontweight='bold')
    ax3.text(i, e+m+s/2,f'{s/t*100:.0f}%', ha='center', va='center',
             fontsize=7.5, color=NAVY,  fontweight='bold')
    ax3.text(i, t+4, f'${t}M', ha='center', va='bottom',
             fontsize=8, color=SLATE, fontweight='bold')

ax3.set_xticks(x3)
ax3.set_xticklabels(seg_years, fontsize=8.5)
ax3.set_ylim(0, 450)
ax3.set_ylabel('ARR ($M)', fontsize=8.5, color=SLATE)
ax3.legend(fontsize=7.5, loc='upper left', frameon=False)
axis_style(ax3, 'Segment ARR Mix Shift')


# ══════════════════════════════════════════════════════════════════════════════
# Chart 4 — NRR by Segment  (bottom-middle)
# ══════════════════════════════════════════════════════════════════════════════
ax4 = fig.add_subplot(gs[1, 1])

nrr_q = ['Q1\n2024','Q2','Q3','Q4','Q1\n2025','Q2','Q3','Q4']
nrr_ent = [127,127,126,126,125,125,125,125]
nrr_mid = [108,107,106,105,104,103,103,102]
nrr_smb = [98, 96, 93, 91, 89, 88, 86, 84]

xn = np.arange(len(nrr_q))
ax4.plot(xn, nrr_ent, color=NAVY,    linewidth=2.2, marker='o', markersize=5, label='Enterprise')
ax4.plot(xn, nrr_mid, color=MID_BLU, linewidth=2.2, marker='s', markersize=5, label='Mid-market')
ax4.plot(xn, nrr_smb, color=CORAL,   linewidth=2.2, marker='^', markersize=5, label='SMB')

ax4.axhline(100, color='#CBD5E0', linewidth=1.2, linestyle='--', zorder=1)
ax4.text(len(nrr_q)-0.1, 100.8, '100%', fontsize=7.5, color=SLATE, va='bottom', ha='right')

# end labels
for vals, col in [(nrr_ent, NAVY), (nrr_mid, MID_BLU), (nrr_smb, CORAL)]:
    ax4.text(len(nrr_q)-1+0.1, vals[-1], f'{vals[-1]}%',
             va='center', fontsize=8, color=col, fontweight='bold')

ax4.set_xticks(xn)
ax4.set_xticklabels(nrr_q, fontsize=7.5)
ax4.set_ylim(78, 135)
ax4.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}%'))
ax4.legend(fontsize=7.5, loc='upper right', frameon=False)
axis_style(ax4, 'Net Revenue Retention by Segment', ylabel='NRR (%)')


# ══════════════════════════════════════════════════════════════════════════════
# Chart 5 — AI Copilot Ramp & Sales Efficiency  (bottom-right)
# ══════════════════════════════════════════════════════════════════════════════
ax5 = fig.add_subplot(gs[1, 2])

cop_q      = ['Q2\n2025', 'Q3\n2025', 'Q4\n2025']
cop_seats  = [140, 420, 710]
magic_q    = ['Q1\n2024','Q2','Q3','Q4','Q1\n2025','Q2','Q3','Q4']
magic_num  = [1.20,1.16,1.10,1.05,1.02,0.98,0.95,0.92]

# Copilot seats as bars
xc = np.arange(len(cop_q))
# offset so bars sit at Q2/Q3/Q4 2025 positions (indices 5,6,7 of 8-quarter span)
bars5 = ax5.bar([5,6,7], cop_seats, width=0.45, color=TEAL, alpha=0.85,
                label='Copilot Seats', zorder=3)
for bar, s in zip(bars5, cop_seats):
    ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+12,
             f'{s}', ha='center', va='bottom', fontsize=8,
             color=TEAL, fontweight='bold')

# magic number on secondary axis
ax5b = ax5.twinx()
xm = np.arange(len(magic_q))
ax5b.plot(xm, magic_num, color=GOLD, linewidth=2.2, marker='o',
          markersize=5, label='Magic Number', zorder=4)
ax5b.axhline(1.0, color=CORAL, linewidth=1, linestyle='--', zorder=2)
ax5b.text(7.1, 1.01, '1.0', fontsize=7.5, color=CORAL, va='bottom')
ax5b.set_ylim(0.5, 1.6)
ax5b.set_ylabel('Magic Number', fontsize=8.5, color=GOLD)
ax5b.tick_params(colors=GOLD, labelsize=8)
ax5b.spines['right'].set_color(GOLD)
ax5b.spines['top'].set_visible(False)
ax5b.spines['left'].set_visible(False)

ax5.set_xticks(xm)
ax5.set_xticklabels(magic_q, fontsize=7.5)
ax5.set_ylim(0, 900)
ax5.set_ylabel('AI Copilot Paying Seats', fontsize=8.5, color=TEAL)
ax5.tick_params(colors=SLATE, labelsize=8)

# combined legend
h1 = mpatches.Patch(color=TEAL, label='Copilot Seats')
from matplotlib.lines import Line2D
h2 = Line2D([0],[0], color=GOLD, linewidth=2, marker='o', label='Magic Number')
ax5.legend(handles=[h1,h2], fontsize=7.5, loc='upper left', frameon=False)
axis_style(ax5, 'AI Ramp vs. Sales Efficiency')

ax5.spines['left'].set_color('#CBD5E0')
ax5.spines['bottom'].set_color('#CBD5E0')
ax5.spines['top'].set_visible(False)

# ── Footer ────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.015,
         'Sources: meridian_financials_2022_2025.csv · meridian_kpis_2024.csv · '
         'meridian_segments_overview.md · earnings call transcripts Q1–Q4 2025  |  '
         'Meridian Technologies — Confidential',
         ha='center', fontsize=7.5, color='#94A3B8')

plt.savefig('/home/user/ddfd/meridian_board_chart.png',
            dpi=180, bbox_inches='tight', facecolor=WHITE)
print('Saved: meridian_board_chart.png')
