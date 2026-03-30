"""
ZELO EV/EBITDA REGRESSION — STANDALONE REFRESH SCRIPT
REQUIREMENTS: pip install pandas numpy scipy matplotlib openpyxl
OPTIONAL (melhora muito os labels): pip install adjustText
"""

try:
    get_ipython().run_line_magic('matplotlib', 'inline')
except Exception:
    pass

import pandas as pd
import numpy as np
from scipy import stats as sp_stats
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XlImage
import os, warnings
warnings.filterwarnings('ignore')

try:
    from adjustText import adjust_text
    HAS_ADJUST = True
except ImportError:
    HAS_ADJUST = False

# =============================================================================
# LINEAR REGRESSION
# =============================================================================
class LinearRegression:
    def __init__(self, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coef_ = None
        self.intercept_ = 0.0

    def fit(self, X, y):
        X, y = np.array(X), np.array(y)
        Xc = np.column_stack([np.ones(len(X)), X]) if self.fit_intercept else X
        beta, _, _, _ = np.linalg.lstsq(Xc, y, rcond=None)
        if self.fit_intercept:
            self.intercept_ = beta[0]
            self.coef_      = beta[1:]
        else:
            self.intercept_ = 0.0
            self.coef_      = beta
        return self

    def predict(self, X):
        return np.array(X) @ self.coef_ + self.intercept_

    def score(self, X, y):
        X, y  = np.array(X), np.array(y)
        return 1 - np.sum((y - self.predict(X))**2) / np.sum((y - y.mean())**2)

# =============================================================================
# CONFIG
# =============================================================================
EXCEL_OUTPUT = r'C:\Users\marravi\Downloads\zelo_ev_ebitda_final.xlsx'
CHART_DIR    = r'C:\Users\marravi\Downloads'

# =============================================================================
# COMP SET — 29 empresas comparáveis (2027E)
# =============================================================================
COMP_DATA = [
    # Company              Ticker   Exchange  Category          EV/EBITDA  CAGR   Pred
    ('SCI',                'SCI',   'NYSE',   'Deathcare',        11.5,    3.7,   4.1),
    ('Propel Funeral',     'PFP',   'ASX',    'Deathcare',        11.5,    5.2,   4.2),
    ('Waste Connections',  'WCN',   'NYSE',   'Waste/Env',        13.8,    5.4,   4.0),
    ('Waste Management',   'WM',    'NYSE',   'Waste/Env',        13.0,    5.1,   3.7),
    ('Republic Services',  'RSG',   'NYSE',   'Waste/Env',        13.8,    4.3,   3.7),
    ('Rentokil Initial',   'RTO',   'LSE',    'Pest/Essential',   11.0,    4.9,   3.8),
    ('FirstService Corp',  'FSV',   'TSX',    'Property Svc',     12.3,    5.0,   3.6),
    ('ABM Industries',     'ABM',   'NYSE',   'Facility Svc',      6.7,    3.9,   3.3),
    ('ADP',                'ADP',   'NASDAQ', 'Recurring Rev',    12.2,    5.9,   4.3),
    ('Broadridge',         'BR',    'NYSE',   'Recurring Rev',    11.3,    5.6,   4.0),
    ('Copart',             'CPRT',  'NASDAQ', 'Asset-Light',      13.2,    3.5,   3.8),
    ("Moody's",            'MCO',   'NYSE',   'Quality Comp',     16.9,    7.6,   4.2),
    ('S&P Global',         'SPGI',  'NYSE',   'Quality Comp',     15.3,    7.3,   4.2),
    ('Visa',               'V',     'NYSE',   'Quality Comp',     16.4,   10.7,   4.2),
    ('Quest Diagnostics',  'DGX',   'NYSE',   'Health Svc',       11.4,    5.0,   4.0),
    ('Laboratory Corp',    'LH',    'NYSE',   'Health Svc',       10.4,    5.1,   4.0),
    ('Henry Schein',       'HSIC',  'NASDAQ', 'Health Svc',       11.0,    3.7,   3.6),
    ('Chemed Corp',        'CHE',   'NYSE',   'Health Svc',       10.1,    5.9,   4.4),
    ('Encompass Health',   'EHC',   'NYSE',   'Health Svc',        9.1,    7.9,   3.8),
    ('Brown & Brown',      'BRO',   'NYSE',   'Insurance Svc',     9.9,   11.4,   4.1),
    ('Copasa',             'CSMG3', 'B3',     'Sanitation',        6.9,    3.9,   4.4),
    ('Motiva',             'MOTV3', 'B3',     'Toll Roads',        5.1,   7.6,   3.9),
    ("Rede D'or",          'RDOR3', 'B3',     'Health Svc',        7.1,   8.4,   3.5),
    ('Bravida Holding',    'BRAV',  'SE',     'Services',          9.0,    3.0,   3.6),
]

# Grupo Zelo — plotado separadamente, não entra na regressão
ZELO_CAGR = 20.0
ZELO_PRED = 4.3

# =============================================================================
# PALETA BTG
# =============================================================================
BTG_NAVY      = '#002D6E'
BTG_BLUE      = '#0057A8'
BTG_GOLD      = '#C8A84B'
BTG_DARKGOLD  = '#9B7D3A'
BTG_STEEL     = '#4A7FB5'
BTG_LIGHTBLUE = '#7BA7BC'
BTG_DEEPBLUE  = '#1B5EA3'
BTG_MIDBLUE   = '#006BB6'
BTG_GRAY      = '#5C6670'
BTG_DARKNAVY  = '#001A45'

cat_colors = {
    'Deathcare':      BTG_NAVY,
    'Waste/Env':      BTG_BLUE,
    'Pest/Essential': BTG_GOLD,
    'Property Svc':   BTG_STEEL,
    'Facility Svc':   BTG_LIGHTBLUE,
    'Recurring Rev':  BTG_MIDBLUE,
    'Asset-Light':    BTG_DARKGOLD,
    'Quality Comp':   BTG_DEEPBLUE,
    'Health Svc':     BTG_DARKNAVY,
    'Insurance Svc':  '#D4A940',
    'Sanitation':     '#2E86AB',
    'Toll Roads':     '#7B6D8D',
    'Private Equity': '#8E4162',
    'Services':       '#5C6670',
}

# =============================================================================
# STEP 1: BUILD DATAFRAME
# =============================================================================
df = pd.DataFrame(COMP_DATA,
                  columns=['Company','Ticker','Exchange','Category',
                            'EV_EBITDA','Revenue_CAGR','Predictability'])
n = len(df)

print("=" * 70)
print(f"COMP SET — {n} empresas  |  EV/EBITDA 2027E")
print("=" * 70)
print(f"\n{'#':<4} {'Company':<22} {'Ticker':<7} {'Exch':<7} {'Category':<16} {'EV/EBITDA':>9}  {'CAGR':>6}  {'Pred':>5}")
print("-" * 78)
for i, row in df.iterrows():
    print(f"{i+1:<4} {row['Company']:<22} {row['Ticker']:<7} {row['Exchange']:<7} "
          f"{row['Category']:<16} {row['EV_EBITDA']:>8.1f}x  {row['Revenue_CAGR']:>5.1f}%  {row['Predictability']:>5.1f}")

# =============================================================================
# STEP 2: REGRESSION
# =============================================================================
print("\nRUNNING REGRESSION...")

X = df[['Revenue_CAGR', 'Predictability']].values
y = df['EV_EBITDA'].values

reg             = LinearRegression().fit(X, y)
df['Predicted'] = reg.predict(X)
df['Residual']  = y - df['Predicted']
r2     = reg.score(X, y)
adj_r2 = 1 - (1-r2)*(n-1)/(n-3)

reg_g = LinearRegression().fit(X[:,0:1], y)
reg_p = LinearRegression().fit(X[:,1:2], y)
r2_g  = reg_g.score(X[:,0:1], y)
r2_p  = reg_p.score(X[:,1:2], y)

X_std   = (X - X.mean(0)) / X.std(0)
y_std   = (y - y.mean()) / y.std()
reg_std = LinearRegression(fit_intercept=False).fit(X_std, y_std)

Xc     = np.column_stack([np.ones(n), X])
beta   = np.linalg.lstsq(Xc, y, rcond=None)[0]
resids = y - Xc @ beta
mse    = np.sum(resids**2) / (n-3)
var_b  = mse * np.linalg.inv(Xc.T @ Xc)
se     = np.sqrt(np.diag(var_b))
t_st   = beta / se
p_vals = 2 * (1 - sp_stats.t.cdf(np.abs(t_st), n-3))

# Médias do dataset — divisórias da matriz 2x2
avg_growth = float(np.mean(df['Revenue_CAGR']))
avg_pred   = float(np.mean(df['Predictability']))

df['GC']       = np.where(df['Revenue_CAGR'] >= avg_growth, 'High', 'Low')
df['PC']       = np.where(df['Predictability'] >= avg_pred,  'High', 'Low')
df['Quadrant'] = df['GC'] + ' Growth / ' + df['PC'] + ' Pred'

# Zelo implied
zelo_implied = reg.predict([[ZELO_CAGR, ZELO_PRED]])[0]

print(f"\n  EV/EBITDA = {beta[0]:.2f} + {beta[1]:.4f}×CAGR + {beta[2]:.2f}×Pred")
print(f"  R²={r2:.3f}  |  Adj R²={adj_r2:.3f}")
print(f"  Médias:  CAGR={avg_growth:.1f}%  |  Pred={avg_pred:.1f}")
print(f"\n  Grupo Zelo  CAGR={ZELO_CAGR:.0f}%  Pred={ZELO_PRED:.1f}  →  {zelo_implied:.1f}x 2027E")
print(f"  Quadrante: {'✓ HG / HP (superior direito)' if ZELO_CAGR >= avg_growth and ZELO_PRED >= avg_pred else '⚠ fora do superior direito'}")

print()
for quad in ['High Growth / High Pred','High Growth / Low Pred',
             'Low Growth / High Pred','Low Growth / Low Pred']:
    sub = df[df['Quadrant'] == quad]
    if len(sub):
        names = ' | '.join(sub['Company'].tolist())
        print(f"  [{quad}]  avg {sub['EV_EBITDA'].mean():.1f}x  n={len(sub)}")
        print(f"    {names}")

# =============================================================================
# FUNÇÃO DA MATRIZ — usada tanto no painel 2x2 quanto no chart individual
# =============================================================================
def draw_matrix(ax, bscale, font_in, font_name, quad_fs=13, standalone=False):
    """
    Matriz 2x2 completa:
    - Divisores nas MÉDIAS do dataset
    - Grupo Zelo como bolinha dourada
    - Labels com fundo branco para legibilidade
    - Médias dos quadrantes nos centros geométricos reais
    """
    xmax = max(df['Revenue_CAGR'].max(), ZELO_CAGR) * 1.18
    ymin = df['Predictability'].min() - 0.28
    ymax = df['Predictability'].max() + 0.22

    # ── Fundo dos quadrantes ──────────────────────────────────────────────
    ax.fill_between([0, avg_growth],  [avg_pred]*2, [ymax]*2, color='#EBF0F8', alpha=0.55, zorder=0)
    ax.fill_between([avg_growth,xmax],[avg_pred]*2, [ymax]*2, color='#EBF5EB', alpha=0.55, zorder=0)
    ax.fill_between([0, avg_growth],  [ymin]*2, [avg_pred]*2, color='#F8F2EB', alpha=0.55, zorder=0)
    ax.fill_between([avg_growth,xmax],[ymin]*2, [avg_pred]*2, color='#F2EBF8', alpha=0.55, zorder=0)

    # ── Linhas divisórias nas médias ──────────────────────────────────────
    ax.axhline(y=avg_pred,   color=BTG_GRAY, linestyle='--', linewidth=1.4, alpha=0.65, zorder=1)
    ax.axvline(x=avg_growth, color=BTG_GRAY, linestyle='--', linewidth=1.4, alpha=0.65, zorder=1)

    # ── Scatter por categoria ────────────────────────────────────────────
    for cat in df['Category'].unique():
        m = df['Category'] == cat
        ax.scatter(df.loc[m,'Revenue_CAGR'], df.loc[m,'Predictability'],
                   c=cat_colors.get(cat, BTG_GRAY),
                   s=df.loc[m,'EV_EBITDA'] * bscale,
                   alpha=0.88, edgecolors='white', linewidth=1.0, zorder=3)

    # ── Múltiplo DENTRO de cada bolinha ──────────────────────────────────
    for _, row in df.iterrows():
        ax.text(row['Revenue_CAGR'], row['Predictability'],
                f"{row['EV_EBITDA']:.1f}x",
                fontsize=font_in, ha='center', va='center',
                color='white', fontweight='bold', zorder=5)

    # ── Nome da empresa ACIMA com fundo branco ───────────────────────────
    texts = []
    for _, row in df.iterrows():
        br = max((row['EV_EBITDA'] * bscale)**0.5 * 0.62, 12) + 3
        t = ax.annotate(
            row['Company'],
            xy=(row['Revenue_CAGR'], row['Predictability']),
            fontsize=font_name, ha='center', va='bottom',
            xytext=(0, br), textcoords='offset points',
            zorder=6,
            bbox=dict(boxstyle='round,pad=0.18', facecolor='white',
                      alpha=0.80, edgecolor='none', linewidth=0)
        )
        texts.append(t)

    # adjustText se disponível
    if HAS_ADJUST and standalone:
        try:
            adjust_text(
                texts, ax=ax,
                expand_points=(1.8, 1.8),
                expand_text=(1.3, 1.3),
                force_points=(0.4, 0.6),
                force_text=(0.3, 0.5),
                arrowprops=dict(arrowstyle='-', color=BTG_GRAY, lw=0.6, alpha=0.6)
            )
        except Exception:
            pass

    # ── Grupo Zelo ────────────────────────────────────────────────────────
    s_zelo = max(zelo_implied * bscale, 300)
    ax.scatter([ZELO_CAGR], [ZELO_PRED], c=BTG_GOLD, s=s_zelo,
               marker='o', zorder=7, edgecolors=BTG_NAVY, linewidth=2.2)
    ax.text(ZELO_CAGR, ZELO_PRED,
            f"{zelo_implied:.1f}x",
            fontsize=font_in, ha='center', va='center',
            color=BTG_NAVY, fontweight='bold', zorder=8)
    br_z = max((zelo_implied * bscale)**0.5 * 0.62, 12) + 4
    ax.annotate(
        'Grupo Zelo',
        xy=(ZELO_CAGR, ZELO_PRED),
        fontsize=font_name + 1, ha='center', va='bottom',
        fontweight='bold', color=BTG_NAVY, zorder=8,
        xytext=(0, br_z), textcoords='offset points',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFF8E7',
                  alpha=0.95, edgecolor=BTG_GOLD, linewidth=1.2)
    )

    # ── Labels dos quadrantes nos centros geométricos REAIS ──────────────
    xc_L = avg_growth / 2
    xc_R = (avg_growth + xmax) / 2
    yc_T = (avg_pred + ymax) / 2
    yc_B = (ymin + avg_pred) / 2

    for qk, lb, xp, yp in [
        ('High Growth / High Pred', 'HG / HP', xc_R, yc_T),
        ('High Growth / Low Pred',  'HG / LP', xc_R, yc_B),
        ('Low Growth / High Pred',  'LG / HP', xc_L, yc_T),
        ('Low Growth / Low Pred',   'LG / LP', xc_L, yc_B),
    ]:
        sub = df[df['Quadrant'] == qk]
        if not len(sub):
            continue
        ax.text(xp, yp,
                f"{lb}\navg  {sub['EV_EBITDA'].mean():.1f}x",
                fontsize=quad_fs, ha='center', va='center',
                fontweight='bold', color=BTG_NAVY, alpha=0.42, zorder=2,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                          alpha=0.45, edgecolor='none'))

    ax.set_xlim(0, xmax)
    ax.set_ylim(ymin, ymax)

# =============================================================================
# HELPERS GERAIS
# =============================================================================
xr  = np.linspace(0, max(df['Revenue_CAGR'].max(), ZELO_CAGR)*1.15, 100)
xr2 = np.linspace(df['Predictability'].min()-0.1, df['Predictability'].max()+0.1, 100)
lr  = np.linspace(df['Predicted'].min()-1, df['Predicted'].max()+2, 100)

S_SCATTER = 900   # scatter nos outros gráficos
FONT_IN   = 8
FONT_IN_S = 10
FONT_NAME = 8
FONT_NAME_S = 9

def scatter_xy(ax, x_col, y_col, s=S_SCATTER, fi=FONT_IN, fn=FONT_NAME):
    for cat in df['Category'].unique():
        m = df['Category'] == cat
        ax.scatter(df.loc[m,x_col], df.loc[m,y_col],
                   c=cat_colors.get(cat, BTG_GRAY), label=cat,
                   s=s, alpha=0.90, edgecolors='white', linewidth=0.8, zorder=3)
    off = (s**0.5)*0.6 + 3
    for _, row in df.iterrows():
        ax.annotate(row['Company'], (row[x_col], row[y_col]),
                    fontsize=fn, ha='center', va='bottom', alpha=0.85,
                    xytext=(0, off), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                              alpha=0.7, edgecolor='none'))
        ax.annotate(f"{row['EV_EBITDA']:.1f}x", (row[x_col], row[y_col]),
                    fontsize=fi, ha='center', va='center',
                    color='white', fontweight='bold', zorder=4)

def plot_zelo(ax, x, y, label='Grupo Zelo', s=900, fi=FONT_IN, fn=FONT_NAME):
    ax.scatter([x], [y], c=BTG_GOLD, s=s, marker='o', zorder=5,
               edgecolors=BTG_NAVY, linewidth=2)
    ax.annotate(f"{zelo_implied:.1f}x", (x, y),
                fontsize=fi, ha='center', va='center',
                color=BTG_NAVY, fontweight='bold', zorder=6)
    off = (s**0.5)*0.6 + 3
    ax.annotate(label, (x, y), fontsize=fn, ha='center', va='bottom',
                fontweight='bold', color=BTG_NAVY,
                xytext=(0, off), textcoords='offset points', zorder=6,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF8E7',
                          alpha=0.95, edgecolor=BTG_GOLD, linewidth=1.0))

def style_ax(ax, xlabel, ylabel, title):
    ax.set_xlabel(xlabel, fontsize=13, color='#333333', labelpad=8)
    ax.set_ylabel(ylabel, fontsize=13, color='#333333', labelpad=8)
    ax.set_title(title, fontsize=15, fontweight='bold', color=BTG_NAVY, pad=12)
    ax.tick_params(labelsize=11)
    ax.grid(True, alpha=0.20, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# =============================================================================
# PAINEL 2x2
# =============================================================================
print("\nGenerating charts...")

fig, axes = plt.subplots(2, 2, figsize=(28, 22))
fig.patch.set_facecolor('#F8F9FA')
fig.suptitle(f'EV/EBITDA 2027E Multiple Drivers  |  n={n}  |  R²={r2:.2f}',
             fontsize=19, fontweight='bold', color=BTG_NAVY, y=0.98)

# Plot 1 — Growth
ax1 = axes[0,0]
ax1.set_facecolor('#FAFAFA')
scatter_xy(ax1, 'Revenue_CAGR', 'EV_EBITDA')
ax1.plot(xr, reg_g.predict(xr.reshape(-1,1)), color=BTG_NAVY, linestyle='--', alpha=0.4, lw=1.8)
ax1.text(xr[-8], reg_g.predict(xr[-8:].reshape(-1,1))[-1]+0.3,
         f'R²={r2_g:.2f}', fontsize=11, alpha=0.55, color=BTG_NAVY)
plot_zelo(ax1, ZELO_CAGR, zelo_implied)
style_ax(ax1, 'Revenue CAGR 2025–28 (%)', 'EV/EBITDA 2027E', 'Revenue CAGR vs EV/EBITDA 2027E')
ax1.legend(fontsize=7.5, loc='upper left', ncol=2, framealpha=0.7)

# Plot 2 — Predictability
ax2 = axes[0,1]
ax2.set_facecolor('#FAFAFA')
scatter_xy(ax2, 'Predictability', 'EV_EBITDA')
ax2.plot(xr2, reg_p.predict(xr2.reshape(-1,1)), color=BTG_NAVY, linestyle='--', alpha=0.4, lw=1.8)
ax2.text(xr2[-5], reg_p.predict(xr2[-5:].reshape(-1,1))[-1]+0.3,
         f'R²={r2_p:.2f}', fontsize=11, alpha=0.55, color=BTG_NAVY)
plot_zelo(ax2, ZELO_PRED, zelo_implied)
style_ax(ax2, 'Predictability Score', 'EV/EBITDA 2027E', 'Predictability vs EV/EBITDA 2027E')

# Plot 3 — Matriz (no painel)
ax3 = axes[1,0]
ax3.set_facecolor('#FAFAFA')
draw_matrix(ax3, bscale=55, font_in=7, font_name=6.5, quad_fs=11, standalone=False)
style_ax(ax3, 'Revenue CAGR 2025–28 (%)', 'Predictability Score',
         f'2×2 Matrix  |  avg CAGR={avg_growth:.1f}%  Pred={avg_pred:.1f}')

# Plot 4 — Actual vs Predicted
ax4 = axes[1,1]
ax4.set_facecolor('#FAFAFA')
scatter_xy(ax4, 'Predicted', 'EV_EBITDA')
ax4.plot(lr, lr, color=BTG_NAVY, linestyle='--', alpha=0.35, lw=1.8, label='Perfect fit')
ax4.fill_between(lr, lr-1.5, lr+1.5, alpha=0.06, color=BTG_BLUE)
plot_zelo(ax4, zelo_implied, zelo_implied, label=f'Grupo Zelo ({zelo_implied:.1f}x)')
style_ax(ax4, 'Regression-Implied EV/EBITDA 2027E', 'Actual EV/EBITDA 2027E',
         f'Actual vs Predicted  (R²={r2:.2f})')
ax4.legend(fontsize=7.5, loc='upper left', ncol=2, framealpha=0.7)

plt.tight_layout(rect=[0, 0, 1, 0.97])
p = os.path.join(CHART_DIR, 'charts_full.png')
fig.savefig(p, dpi=180, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.show()
print(f"  Saved: {p}")

# =============================================================================
# MATRIZ INDIVIDUAL — FOCO TOTAL (grande, legível, para colar na apresentação)
# =============================================================================
fig_m, ax_m = plt.subplots(figsize=(26, 20))
fig_m.patch.set_facecolor('#F8F9FA')
ax_m.set_facecolor('#FAFAFA')

draw_matrix(ax_m, bscale=90, font_in=9, font_name=8.5, quad_fs=14, standalone=True)

# Anotações extras na matriz individual
ax_m.axhline(y=avg_pred,   color=BTG_GRAY, linestyle='--', lw=0, alpha=0)  # já desenhado dentro
ax_m.axvline(x=avg_growth, color=BTG_GRAY, linestyle='--', lw=0, alpha=0)

# Legenda de categorias
from matplotlib.patches import Patch
legend_handles = [Patch(color=v, label=k) for k, v in cat_colors.items()
                  if k in df['Category'].unique()]
legend_handles.append(Patch(color=BTG_GOLD, label='Grupo Zelo (target)'))
ax_m.legend(handles=legend_handles, fontsize=9, loc='lower right',
            framealpha=0.85, title='Category', title_fontsize=10, ncol=2)

style_ax(ax_m, 'Revenue CAGR 2025–28 (%)', 'Predictability Score',
         f'2×2 Matrix  |  avg CAGR = {avg_growth:.1f}%  |  avg Pred = {avg_pred:.1f}  |  bubble = EV/EBITDA 2027E')

p_m = os.path.join(CHART_DIR, 'chart_matrix.png')
fig_m.savefig(p_m, dpi=200, bbox_inches='tight', facecolor=fig_m.get_facecolor())
plt.show()
print(f"  Saved: {p_m}")

# =============================================================================
# OUTROS GRÁFICOS INDIVIDUAIS
# =============================================================================
for plot_id in ['growth', 'pred', 'avp']:
    fig_s, ax_s = plt.subplots(figsize=(18, 13))
    fig_s.patch.set_facecolor('#F8F9FA')
    ax_s.set_facecolor('#FAFAFA')

    if plot_id == 'growth':
        scatter_xy(ax_s, 'Revenue_CAGR', 'EV_EBITDA', s=1200, fi=FONT_IN_S, fn=FONT_NAME_S)
        ax_s.plot(xr, reg_g.predict(xr.reshape(-1,1)), color=BTG_NAVY, linestyle='--', alpha=0.4, lw=2)
        ax_s.text(xr[-8], reg_g.predict(xr[-8:].reshape(-1,1))[-1]+0.3,
                  f'R²={r2_g:.2f}', fontsize=13, alpha=0.55, color=BTG_NAVY)
        plot_zelo(ax_s, ZELO_CAGR, zelo_implied, s=1200, fi=FONT_IN_S, fn=FONT_NAME_S)
        style_ax(ax_s, 'Revenue CAGR 2025–28 (%)', 'EV/EBITDA 2027E',
                 f'Revenue CAGR vs EV/EBITDA 2027E  (R²={r2_g:.2f})')
        ax_s.legend(fontsize=9, loc='upper left', ncol=2, framealpha=0.7)

    elif plot_id == 'pred':
        scatter_xy(ax_s, 'Predictability', 'EV_EBITDA', s=1200, fi=FONT_IN_S, fn=FONT_NAME_S)
        ax_s.plot(xr2, reg_p.predict(xr2.reshape(-1,1)), color=BTG_NAVY, linestyle='--', alpha=0.4, lw=2)
        ax_s.text(xr2[-5], reg_p.predict(xr2[-5:].reshape(-1,1))[-1]+0.3,
                  f'R²={r2_p:.2f}', fontsize=13, alpha=0.55, color=BTG_NAVY)
        plot_zelo(ax_s, ZELO_PRED, zelo_implied, s=1200, fi=FONT_IN_S, fn=FONT_NAME_S)
        style_ax(ax_s, 'Predictability Score', 'EV/EBITDA 2027E',
                 f'Predictability vs EV/EBITDA 2027E  (R²={r2_p:.2f})')

    elif plot_id == 'avp':
        scatter_xy(ax_s, 'Predicted', 'EV_EBITDA', s=1200, fi=FONT_IN_S, fn=FONT_NAME_S)
        ax_s.plot(lr, lr, color=BTG_NAVY, linestyle='--', alpha=0.35, lw=2, label='Perfect fit')
        ax_s.fill_between(lr, lr-1.5, lr+1.5, alpha=0.06, color=BTG_BLUE)
        plot_zelo(ax_s, zelo_implied, zelo_implied,
                  label=f'Grupo Zelo ({zelo_implied:.1f}x)', s=1200, fi=FONT_IN_S, fn=FONT_NAME_S)
        style_ax(ax_s, 'Regression-Implied EV/EBITDA 2027E', 'Actual EV/EBITDA 2027E',
                 f'Actual vs Predicted  (R²={r2:.2f})')
        ax_s.legend(fontsize=9, loc='upper left', ncol=2, framealpha=0.7)

    plt.tight_layout()
    path = os.path.join(CHART_DIR, f'chart_{plot_id}.png')
    fig_s.savefig(path, dpi=180, bbox_inches='tight', facecolor=fig_s.get_facecolor())
    plt.show()
    print(f"  Saved: {path}")

print(f"\nDONE. Charts saved in: {CHART_DIR}")
print(f"\nSUMMARY:")
print(f"  Grupo Zelo  CAGR={ZELO_CAGR:.0f}%  Pred={ZELO_PRED:.1f}  →  {zelo_implied:.1f}x EV/EBITDA 2027E")
print(f"  Médias: CAGR={avg_growth:.1f}%  Pred={avg_pred:.1f}")
print(f"  Quadrante: HG/HP (superior direito) ✓")
