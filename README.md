# Benchmarking long-term prognostic models for dementia risk in the Health and Retirement Study

Analysis code for the manuscript *Benchmarking Performance of Long-Term Prognostic Models for Dementia Risk Using the Health and Retirement Study*. The repository is the revised benchmark (branch `hrs-revised-benchmark`. It covers the full chain from the raw HRS files to the saved aggregate results, the supplementary tables and the manuscript figures.

## Study Design

* **Design.**
* Eight models (penalized logistic regression, Gaussian naïve Bayes, decision tree, LightGBM, CatBoost, RealMLP, graph attention network, TabICL) are compared for incident dementia over 6- and 8-year windows (2000–2006, 2000–2008, 2010–2016, 2010–2018). The 2000 sample is used for internal validation (10 repeated stratified 60/20/20 splits) and for fitting the temporal-validation models; the 2010 sample is used only for temporal evaluation.

* **Outcome and estimand.**
* Vital status comes from the HRS 2022 Tracker. All participants who died before the final wave are excluded, whether or not dementia had been observed, which treats participants with and without dementia in the same way. Among participants alive at the final wave, `y = 1` is a dementia classification at one or more biennial follow-up assessments in the window, and `y = 0` is no observed dementia plus a dementia-free assessment at the final wave. Participants alive at the final wave without a final-wave assessment and without observed dementia are excluded as lost to follow-up, and participants whose outcome otherwise remains unavailable are excluded as outcome not available. Missed intermediate assessments do not by themselves cause exclusion. The estimand is the 6- or 8-year risk of dementia among adults aged ≥51 years who were dementia-free at baseline, given that they were alive at the end of the window and had a known outcome. The sensitivity outcome (`any`) keeps the death exclusion but accepts any dementia-free follow-up assessment for confirmed survivors without observed dementia.

* **Predictors and imputation.**
* 60 predictors give 94 model inputs. All eligible participants with a known outcome are analyzed regardless of predictor missingness. In each split, miceforest is fitted once on the training predictors only (the outcome is never used) and applied unchanged to the validation and test subsets; the final internal model is refitted on the already-imputed training and validation data. For temporal validation the imputer and model are fitted on the full 2000 sample, and the 2010 sample is reserved for evaluation.

* **Selection and evaluation.**
* Hyperparameters (grids in `model/specs.py`, Table 1 of the manuscript) are chosen by validation AUPRC and the decision threshold by validation F1; test data are used once. Internal intervals use the corrected resampled t method; temporal intervals and paired differences use 2,000 household cluster bootstrap resamples. Permutation importance (five permutations, 500 household bootstrap resamples) is computed in the 2010 sample at the 6-year horizon; SHAP is exact where available and KernelSHAP (500 participants, 800 coalitions, 10 background participants) for TabICL, RealMLP and GAT.

## Repository Layout

| Path | Contents |
| --- | --- |
| `preprocess_2000.ipynb`, `preprocess_2002-2016.ipynb`, `preprocess_2018-2020.ipynb`, `dont_do.py` | Raw HRS/RAND files to wave-level predictor tables in `data/preprocessed data/` |
| `all_y.ipynb`, `data_management (2000-2006).ipynb`, `data_management (2000-2008).ipynb` | Wave-level dementia classification and the encoded predictor schema read by `train/cohorts.py` |
| `model/` | Model classes, tuning grids and device settings |
| `train/` | Cohort and outcome construction, training-only imputation, tuning and checkpoint writing |
| `inference/` | Replay of saved models, verification, metrics and intervals, importance, SHAP, cohort and supplementary tables (`supplementary_tables.py` also writes the manuscript layouts of Supplementary Tables S1, S9, S10 and S12, using `manuscript_layout.json`) |
| `run_benchmark.py`, `run_table_sources.py`, `artifact_store.py` | Resumable coordinator (CPU plus two GPU lanes) and the table-source stage |
| `figures/` | Final manuscript figures (Fig. 1–5) and `figures/supplementary/` (Supplementary Fig. S1–S9), PNG and SVG, identical to the figures in the submitted documents |
| `paper_figures/`, `make_paper_figures.py` | Scripts and the editable SVG templates for Fig. 1 and Supplementary Fig. S1 (`paper_figures/templates/`) that rebuild these figures from the saved results |
| `delivery/` | Saved aggregate results: audited source tables (including Table 1 and Supplementary Tables S1–S27), the manuscript layouts of Supplementary Tables S1, S9, S10 and S12, runtime summary and verification evidence |
| `PREDICTOR_DICTIONARY.md` | Definitions, sources and coding of the 60 predictors |
| `artifacts/`, `data/` | Output and input folders (ignored by Git; see their README files) |

## Reproduce

Install the dependencies (`python -m pip install -r requirements-revised.txt`, plus a PyTorch build matching your GPU), obtain the HRS inputs and the TabICL v1.1 checkpoint separately, and run the preprocessing notebooks in the order given in [REPRODUCIBILITY.md](REPRODUCIBILITY.md). Then, from the repository root:

```sh
python run_benchmark.py --tracker /path/to/trk2022tr_r.dta --prepare-only   # cohorts, imputation caches, checks
python run_benchmark.py --tracker /path/to/trk2022tr_r.dta                  # models, metrics, importance, tables
python run_table_sources.py                                                 # missing-data comparison, predictor tables, final table sources
python make_paper_figures.py --result artifacts --output outputs/paper_figures   # rebuilds the figures in figures/
```

Check `--help` before starting and do not run two coordinators at once. `python tools/verify_delivery.py` checks the saved aggregate results in `delivery/` against their recorded hashes without any HRS data.

## Data

HRS data are available to registered researchers at <https://hrs.isr.umich.edu>. Raw HRS files, participant-level predictions, imputation caches and fitted checkpoints are not included in this repository. The saved aggregate results in `delivery/tables/audited_sources/` are sufficient to inspect every number in the manuscript tables; the figure scripts that need per-split metrics read them from the result package or from `artifacts/` after a full run.
