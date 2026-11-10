# Manuscript figures

The final figures used in the manuscript are stored in `figures/` and `figures/supplementary/` at the repository root. `make_paper_figures.py` (repository root) rebuilds Fig. 1, 3, 4, 5 and Supplementary Fig. S1–S9 from the saved results; Fig. 2 (model categories) is a static drawing in `templates/`.

```sh
python -m pip install -r paper_figures/requirements.txt
python make_paper_figures.py --result /path/to/result --output outputs/paper_figures
```

`--result` is a folder with `tables/audited_sources/` (or `tables/`), `predictions/final/h{6,8}/<model>/metrics.csv` and `imputation_comparison/final/h6/<model>/*.csv`, i.e. the saved result package or the `artifacts/` tree of a full run. Figures whose inputs are missing are skipped. Fig. 3, S2 and S5 need the per-split metrics; Fig. 4, 5 and S3, S4, S6–S9 need only the audited tables (S6 also the temporal metrics). Fig. 1 and S1 are editable SVG templates whose counts, split sizes and predictor grid are filled from `participant_flow.csv` and `importance_permutation_h6.csv`; PNG versions need a headless Chrome/Chromium (`--chrome` or the `CHROME` variable). Use `--only fig4,s3` to build a subset.
