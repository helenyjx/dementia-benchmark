"""Shared paths, colors and helpers for the manuscript figures.

The result root is a folder that contains ``tables/audited_sources`` (or ``tables``),
``predictions/final/h{6,8}/<model>/metrics.csv`` and ``imputation_comparison/final/h6/<model>/*.csv``
(the layout of the saved result package, or the corresponding ``artifacts/`` tree after a full run).
Set it with the environment variable ``HRS_RESULT`` (done by ``make_paper_figures.py --result``).
"""
import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgb

RESULT = Path(os.environ.get('HRS_RESULT', 'artifacts')).resolve()
OUT = Path(os.environ.get('HRS_FIGURE_OUT', 'outputs/paper_figures')).resolve()
A = RESULT / 'tables' / 'audited_sources'
if not A.is_dir():
    A = RESULT / 'tables'
SUPP = A / 'supplementary'
OUT_F = OUT / 'figures'
OUT_S = OUT / 'supplementary_figures'
for _d in (OUT_F, OUT_S):
    _d.mkdir(parents=True, exist_ok=True)
R = RESULT
A = str(A) + os.sep
OUT_F = str(OUT_F) + os.sep
OUT_S = str(OUT_S) + os.sep

MODELS = ['LR', 'GNB', 'DT', 'LightGBM', 'CatBoost', 'GAT', 'RealMLP', 'TabICL']
T10 = plt.cm.tab10.colors
COL = {'LR': T10[0], 'GNB': T10[3], 'DT': T10[2], 'LightGBM': T10[1], 'CatBoost': T10[5],
       'GAT': T10[6], 'RealMLP': T10[7], 'TabICL': T10[9]}


def light(c):
    return tuple((x + 1) / 2 for x in to_rgb(c))


LCOL = {m: light(c) for m, c in COL.items()}
PANEL = ['TabICL', 'CatBoost', 'LightGBM', 'LR', 'RealMLP', 'GAT', 'DT', 'GNB']
PNAME = {'LR': 'Penalized LR', 'DT': 'Decision tree', 'GNB': 'Gaussian NB'}


def pn(m):
    return PNAME.get(m, m)


def per_repeat(h):
    """Ten internal test-split metrics per model (all participants) for horizon h."""
    out = []
    for m in MODELS:
        d = pd.read_csv(R / 'predictions' / 'final' / f'h{h}' / m / 'metrics.csv')
        d = d[(d.setting == 'internal') & (d.population == 'all')].copy()
        d['model'] = m
        out.append(d)
    return pd.concat(out)


def strat(h, s):
    """Per-repeat metrics for imputation strategy s in {'mean', 'complete_case', 'miceforest'}."""
    import glob
    out = []
    for m in MODELS:
        if s == 'miceforest':
            d = pd.read_csv(R / 'predictions' / 'final' / f'h{h}' / m / 'metrics.csv')
            d = d[(d.setting == 'internal') & (d.population == 'all')].copy()
        else:
            fs = sorted(glob.glob(str(R / 'imputation_comparison' / 'final' / f'h{h}' / m / f'{s}-rep?.csv')))
            d = pd.concat([pd.read_csv(f) for f in fs])
        d['model'] = m
        out.append(d)
    return pd.concat(out)


def boxes(ax, data, positions, fc, ec, width=0.5, lw=1.3):
    bp = ax.boxplot(data, positions=positions, widths=width, patch_artist=True, showfliers=True,
                    flierprops=dict(marker='o', markersize=3.5, markerfacecolor='none', markeredgewidth=1.0))
    for i, b in enumerate(bp['boxes']):
        b.set_facecolor(fc[i]); b.set_edgecolor(ec[i]); b.set_linewidth(lw); b.set_alpha(None)
    for k in ('whiskers', 'caps'):
        for j, l in enumerate(bp[k]):
            l.set_color(ec[j // 2]); l.set_linewidth(lw)
    for j, l in enumerate(bp['medians']):
        l.set_color(ec[j]); l.set_linewidth(lw)
    for j, l in enumerate(bp['fliers']):
        l.set_markeredgecolor(ec[j])
    return bp


def style_cat(ax, labels, rot=45):
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=rot, ha='right', rotation_mode='anchor', fontsize=11)
    ax.yaxis.grid(True, ls=':', color='#b6b6b6', lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis='y', labelsize=10)
    for s in ax.spines.values():
        s.set_linewidth(0.8)
