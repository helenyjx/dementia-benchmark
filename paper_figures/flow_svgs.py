"""Fig. 1 (study workflow) and Supplementary Fig. S1 (participant flow).

The two drawings are editable SVG templates. This script replaces every count in them with the audited
values from ``participant_flow.csv`` (and the split sizes derived from them), rebuilds the 3 x 3 grid of the most
important predictors in Fig. 1 from ``importance_permutation_h6.csv``, and rasterizes the SVGs with a headless
Chromium-based browser when one is available (``--chrome`` or the CHROME environment variable).
"""
import math
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from common import *

TEMPLATES = Path(__file__).parent / 'templates'
LABEL = {'ageym': ['Age'], 'edstg': ['Education'], 'raceeth': ['Race/ethnicity'], 'gender': ['Sex'],
         'mapa': ['Difficulty using', 'a map'], 'shlt': ['Self-rated health'], 'slfmem': ['Self-rated memory'],
         'doctim': ['Doctor visits', '(previous 2 years)'], 'nrstim': ['Nursing-home stays', '(previous 2 years)'],
         'nrsnit': ['Nursing-home nights', '(previous 2 years)'], 'livpar': ['Living parents'],
         'livsib': ['Living siblings'], 'weight': ['Weight'], 'height': ['Height'], 'drink': ['Ever drinks alcohol'],
         'proxy': ['Proxy interview'], 'adl5a': ['ADL difficulties (0-5)'], 'lbrf': ['Labor force status'],
         'mstat': ['Marital status'], 'stroke': ['Stroke'], 'effort': ['CES-D: effort'],
         'depres': ['CES-D: depressed'], 'flone': ['CES-D: lonely'], 'grossa': ['Gross-motor', 'difficulties (0-5)'],
         'momage': ["Mother's age"], 'dadage': ["Father's age"], 'cendiv': ['Census division']}
GRID_FILL = [['#138341', '#6db944', '#6db944'], ['#6db944', '#8cc888', '#8cc888'], ['#a8d3a0'] * 3]
GRID_X = [1847.0, 2016.3, 2185.7]
GRID_Y = [410, 466, 522]
CELL_W, CELL_H = 165.3, 52


def n(x):
    return f'{int(x):,}'


def flow_table():
    f = pd.read_csv(A + 'participant_flow.csv')
    return {(r['cohort'], int(r['horizon (years)'])): r for _, r in f.iterrows()}


def seq(svg, pattern, values, flags=0):
    it = iter(values)
    return re.sub(pattern, lambda m: next(it), svg, flags=flags)


def top_predictors(k=9):
    p = pd.read_csv(A + 'importance_permutation_h6.csv')
    g = p.groupby('variable').agg(rank=('rank', 'mean'), drop=('importance_AUPRC_drop', 'mean'))
    return list(g.sort_values(['rank', 'drop'], ascending=[True, False]).index[:k])


def grid_svg(variables):
    out = []
    for i, v in enumerate(variables):
        r, c = divmod(i, 3)
        x, y = GRID_X[c], GRID_Y[r]
        lines = LABEL.get(v, [v])
        cx = x + CELL_W / 2
        out.append(f'<rect x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" fill="{GRID_FILL[r][c]}" stroke="#ffffff" stroke-width="1.5"/>')
        color = '#ffffff' if i == 0 else '#1c1c1c'
        if len(lines) == 2:
            for j, t in enumerate(lines):
                out.append(f'<text x="{cx:.1f}" y="{y + 23 + 20 * j}" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="{color}" text-anchor="middle">{t}</text>')
        else:
            size = 20.5 if len(lines[0]) <= 14 else 16.5
            out.append(f'<text x="{cx:.1f}" y="{y + 33}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}" text-anchor="middle">{lines[0]}</text>')
    return '\n'.join(out) + '\n'


def fig1():
    flow = flow_table()
    svg = (TEMPLATES / 'Fig1_template.svg').read_text(encoding='utf-8')
    a6, a8 = int(flow[('2000 baseline', 6)]['analytic cohort']), int(flow[('2000 baseline', 8)]['analytic cohort'])
    t6, t8 = int(flow[('2010 baseline', 6)]['analytic cohort']), int(flow[('2010 baseline', 8)]['analytic cohort'])

    def split(total):  # 60/20/20: test = ceil(0.2 n), validation = ceil(0.25 of the remainder)
        test = math.ceil(0.2 * total)
        val = math.ceil(0.25 * (total - test))
        return total - test - val, val, test
    s6, s8 = split(a6), split(a8)
    vals = [f'(n = {n(a6)} / {n(a8)})'] + [f'(n = {n(s6[i])} / {n(s8[i])})' for i in range(3)]
    svg = seq(svg, r'\(n = [\d,]+ / [\d,]+\)', vals)
    svg = seq(svg, r'6-Year Prediction \(n = [\d,]+\)', [f'6-Year Prediction (n = {n(a6)})', f'6-Year Prediction (n = {n(t6)})'])
    svg = seq(svg, r'8-Year Prediction \(n = [\d,]+\)', [f'8-Year Prediction (n = {n(a8)})', f'8-Year Prediction (n = {n(t8)})'])
    start = svg.index('<rect x="1847.0" y="410"')
    end = svg.index('<path d="M1840,400V581H2359.0"')
    svg = svg[:start] + grid_svg(top_predictors()) + svg[end:]
    return svg, (2400, 680, 2)


def s1():
    flow = flow_table()
    svg = (TEMPLATES / 'S1_template.svg').read_text(encoding='utf-8')
    order = [('2000 baseline', 6), ('2000 baseline', 8), ('2010 baseline', 6), ('2010 baseline', 8)]
    base = [('2000 baseline', 6), ('2010 baseline', 6)]
    svg = seq(svg, r'interviewed, n = [\d,]+', [f'interviewed, n = {n(flow[k]["interviewed at baseline"])}' for k in base])
    svg = seq(svg, r'Aged 50 or younger: [\d,]+ \| Dementia at baseline: [\d,]+',
              [f'Aged 50 or younger: {n(flow[k]["excluded: age <= 50"])} | Dementia at baseline: {n(flow[k]["excluded: dementia at baseline"])}' for k in base])
    svg = seq(svg, r'Baseline dementia status unknown: [\d,]+', [f'Baseline dementia status unknown: {n(flow[k]["excluded: baseline dementia status unknown"])}' for k in base])
    svg = seq(svg, r'>n = [\d,]+<', [f'>n = {n(flow[k]["eligible"])}<' for k in base])
    svg = seq(svg, r'regardless of dementia: [\d,]+', [f'regardless of dementia: {n(flow[k]["excluded: died by final wave"])}' for k in order])
    svg = seq(svg, r'Not assessed or unresolved: [\d,]+',
              [f'Not assessed or unresolved: {n(int(flow[k]["excluded: loss to follow-up"]) + int(flow[k]["excluded: unresolved after final interview"]))}' for k in order])
    svg = seq(svg, r'n = [\d,]+ \| Incident dementia: [\d,]+',
              [f'n = {n(flow[k]["analytic cohort"])} | Incident dementia: {n(flow[k]["incident dementia"])}' for k in order])
    return svg, (1704.4, 709.6, 2.5)


def find_chrome(explicit=None):
    for c in [explicit, os.environ.get('CHROME'), '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
              shutil.which('google-chrome'), shutil.which('chromium'), shutil.which('chromium-browser')]:
        if c and Path(c).exists():
            return c
    return None


def rasterize(svg_path, png_path, width, height, scale, chrome):
    tmp = Path(tempfile.mkdtemp()) / 'page.html'
    tmp.write_text(f'<html><body style="margin:0;background:#fff"><img src="file://{svg_path}" width="{width}" '
                   f'height="{height}" style="display:block"></body></html>', encoding='utf-8')
    subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--force-device-scale-factor={scale}',
                    f'--window-size={int(round(width))},{int(round(height))}', f'--screenshot={png_path}', f'file://{tmp}'],
                   check=True, capture_output=True)


def main(which=('fig1', 's1'), chrome=None):
    chrome = find_chrome(chrome)
    jobs = {'fig1': (fig1, Path(OUT_F) / 'Fig1_workflow'), 's1': (s1, Path(OUT_S) / 'S1_sample_flow')}
    for key in which:
        build, stem = jobs[key]
        svg, (w, h, sc) = build()
        stem.with_suffix('.svg').write_text(svg, encoding='utf-8')
        if chrome:
            rasterize(stem.with_suffix('.svg').resolve(), stem.with_suffix('.png').resolve(), w, h, sc, chrome)
        else:
            print(f'{key}: SVG written; no Chromium/Chrome found for the PNG (set --chrome or CHROME)')


if __name__ == '__main__':
    main()
