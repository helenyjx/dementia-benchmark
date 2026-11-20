# Reproducibility notes

## Environment

Python 3.12 and `requirements-revised.txt` (NumPy 1.26.4, scikit-learn 1.6.1, miceforest 6.0.3, LightGBM 4.5.0, CatBoost 1.2.8, pytabkit 1.6.1, TabICL 0.1.3, PyTorch Geometric 2.6.1, shap 0.46.0). Install a PyTorch build for your device; the recorded local run used PyTorch 2.8.0 with CUDA 12.8. LightGBM GPU fits need an OpenCL-enabled build. TabICL uses the public pretrained checkpoint `tabicl-classifier-v1.1-0506.ckpt` from the Hugging Face cache (`HF_HUB_OFFLINE=1` is set by the coordinator). Seeds: internal splits 0–9; training-only imputation seed 42 + repeat; temporal imputation seed 999; stochastic models 42 (GAT restarts 43–45); bootstrap and KernelSHAP seed 2026.

## Obtaining the HRS data

No HRS file is included in this repository, and none may be added to it. The HRS distributes its data under its Conditions of Use. Registered users agree not to transfer the files to third parties and not to try to identify participants. We therefore cannot redistribute any HRS file, including the Tracker. The Tracker (`trk2022tr_r.dta`) also holds participant-level information such as vital status and death dates, so it needs the same care as the other HRS files. Every user must obtain the files from the HRS under their own registration.

1. Register for a free account on the HRS data portal (https://hrsdata.isr.umich.edu), accept the Conditions of Use and log in.
2. In the data products section of the portal, open the 2022 Tracker file and download the Stata version, `trk2022tr_r.dta`.
3. From the same portal, download the HRS 2022 core interview files that contain the "don't do" items.
4. Download the RAND HRS Longitudinal File 2022 (V2) from RAND (https://www.rand.org/health/surveys/hrs/hrs-data.html).
5. Place all raw files in `data/original data/`. This folder is ignored by Git.

The layout of the HRS and RAND sites may change, so follow the current instructions on those sites. Questions about access go to the HRS (hrsquestions@umich.edu).

## Inputs and order of execution

1. Obtain the raw HRS files as described in "Obtaining the HRS data" above and place them in `data/original data/`.
2. Run `preprocess_2000.ipynb`, `preprocess_2002-2016.ipynb` and `preprocess_2018-2020.ipynb` (they use `dont_do.py`) to write the wave-level tables to `data/preprocessed data/`.
3. Run `all_y.ipynb`, then `data_management (2000-2006).ipynb` and `data_management (2000-2008).ipynb`. They write the encoded predictor files that define the 94 model inputs. Cohorts and outcome labels are **not** taken from these notebooks; `train/cohorts.py` rebuilds them from the Tracker.
4. Run the benchmark from the repository root:

```sh
python run_benchmark.py --tracker /path/to/trk2022tr_r.dta --prepare-only
python run_benchmark.py --tracker /path/to/trk2022tr_r.dta
python run_table_sources.py
python -m inference.death_audit --tracker /path/to/trk2022tr_r.dta
```

The coordinator reproduces the recorded lane plan (LR, GNB and DT on CPU; LightGBM and TabICL on GPU 0; CatBoost, RealMLP and GAT on GPU 1). On other hardware, call the stages directly:

```sh
python -m train.cohorts --tracker /path/to/trk2022tr_r.dta
python -m train.imputation --horizon 6 --outcome final     # also: --horizon 8, and --outcome any
python -m inference.verify --prepared-only
python -m train.benchmark --model LR --horizon 6 --outcome final --device cpu
python -m inference.predict --model LR --horizon 6 --outcome final
python -m inference.importance --model LR
```

Repeat the training and prediction commands for every model, horizon and outcome (`--device 0` for GPU models). Completed stages are reused only when their input receipts match.

## Outputs

Everything is written under `artifacts/`: `cohorts/` (four primary and four sensitivity cohorts with label audit ledgers), `imputation/` (one training-only cache per repeat plus the temporal imputation model), `checkpoints/`, `predictions/`, `importance/`, `imputation_comparison/` (mean-imputation and complete-case runs for the 6-year horizon) and `tables/` (cohort flow, death audit, performance with intervals, paired differences, calibration, decision curves, runtime, importance and `tables/supplementary/` with Table 1 and Supplementary Tables S1–S26). `artifacts/source_status.json` records the hash of every final table and `artifacts/completion_audit.json` is written only when the full scope passes.

## Verification and hardware notes

`python tools/verify_delivery.py` checks `delivery/` (hashes, S1 counts against the audited source, runtime totals) without HRS data. The completed run used CPU for LR, GNB and DT, an RTX 3070 Ti for CatBoost and RealMLP, an RTX 5070 Ti for LightGBM and TabICL, and an RTX 5070 Ti or an NVIDIA L40S for GAT, as recorded per run in the runtime tables. The formal TabICL KernelSHAP was split across an RTX 5070 Ti and an L40S; the distributed dispatch scripts used for that split are not part of this repository. A strict elementwise cross-device check of TabICL predictions did not pass its original tolerance, and production results were accepted under recorded per-job probability, SHAP and ranking checks; this is not a claim of numerical equivalence across devices. GPU computations are not guaranteed to be bit-for-bit deterministic.
