"""Rebuild the manuscript figures (Fig. 1, 3-5 and Supplementary Fig. S1-S9) from the saved results.

    python make_paper_figures.py --result /path/to/result --output outputs/paper_figures

``--result`` is the result package (or the ``artifacts/`` tree of a full run) containing ``tables/audited_sources``,
``predictions/final/h{6,8}/<model>/metrics.csv`` and ``imputation_comparison/final/h6/<model>/*.csv``.
Figures whose inputs are missing are skipped with a message. Fig. 2 (model categories) is a static drawing copied from
``paper_figures/templates``. PNG rasterization of Fig. 1 and S1 needs a headless Chrome/Chromium (``--chrome``).
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGES = ['fig1', 'fig3', 'fig4', 'fig5', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--result', type=Path, required=True)
    ap.add_argument('--output', type=Path, default=Path('outputs/paper_figures'))
    ap.add_argument('--only', default=','.join(STAGES), help='comma-separated subset of: ' + ','.join(STAGES))
    ap.add_argument('--chrome', help='Chrome/Chromium executable used to rasterize the two SVG drawings')
    args = ap.parse_args()
    os.environ['HRS_RESULT'] = str(args.result.resolve())
    os.environ['HRS_FIGURE_OUT'] = str(args.output.resolve())
    sys.path.insert(0, str(HERE / 'paper_figures'))
    import common
    import fig_box_bar, fig_supp, fig5, flow_svgs
    jobs = {
        'fig1': lambda: flow_svgs.main(('fig1',), args.chrome),
        'fig3': lambda: fig_box_bar.box_fig(['AUPRC', 'AUROC', 'Accuracy'], ['AUPRC', 'AUROC', 'Accuracy'], common.OUT_F + 'Fig3_internal_boxplots'),
        'fig4': lambda: fig_box_bar.bar_fig(['AUPRC', 'AUROC', 'Accuracy'], ['AUPRC', 'AUROC', 'Accuracy'], common.OUT_F + 'Fig4_temporal_grouped_bars'),
        'fig5': fig5.main,
        's1': lambda: flow_svgs.main(('s1',), args.chrome),
        's5': lambda: fig_box_bar.box_fig(['Precision', 'Recall', 'F1'], ['Precision', 'Recall', 'F1 Score'], common.OUT_S + 'S5_internal_boxplots', prefix=False),
        's6': lambda: fig_box_bar.bar_fig(['Precision', 'Recall', 'F1'], ['Precision', 'Recall', 'F1 Score'], common.OUT_S + 'S6_temporal_grouped_bars', prefix=False),
    }
    for s in ('s2', 's3', 's4', 's7', 's8', 's9'):
        jobs[s] = getattr(fig_supp, s)
    for stage in args.only.split(','):
        try:
            jobs[stage]()
            print(f'{stage}: done', flush=True)
        except FileNotFoundError as error:
            print(f'{stage}: skipped, missing input ({error.filename})', flush=True)
    for ext in ('svg', 'png'):
        shutil.copy(HERE / 'paper_figures' / 'templates' / f'Fig2_model_categories.{ext}', common.OUT_F + f'Fig2_model_categories.{ext}')


if __name__ == '__main__':
    main()
