# Saved aggregate results

| Folder | Contents |
| --- | --- |
| `tables/audited_sources/` | Final aggregate CSV sources: performance with intervals, paired differences, calibration, decision curves, overlap, importance and runtime tables, plus `supplementary/` with the manuscript Table 1 (hyperparameter search space, selected values and decision thresholds), Supplementary Tables S1–S26 and `performance_all.csv`, the internal and temporal performance tables combined |
| `tables/outcome_flow/` | Supplementary Table S1 (final audited counts for the four windows) |
| `tables/manuscript_format/` | Supplementary Tables S1, S9, S10 and S12 in the layout printed in the supplement (text labels, rounding and category names), built by `inference/supplementary_tables.py` from the audited sources |
| `tables/runtime/` | Measured runtime summary, the editable workbook with the idealized hardware-normalized estimates, and `S19_FP32_equivalent.csv`, the Supplementary Table S19 printed in the manuscript (primary outcome; time per training epoch, total training time and total inference time, converted to a common reference GPU, an NVIDIA GeForce RTX 5070 Ti; built by `inference/supplementary_tables.py`) |
| `verification/` | Saved completion, source, model, comparison and cross-device acceptance reports from the full run |
| `MANIFEST.json` | SHA-256 and size of every file in this folder |

The cohort sizes (analytic samples 13,246 and 12,236 in 2000; 14,123 and 11,603 in 2010) and all numbers in the manuscript tables come from these files. They contain aggregate results only. The normalized runtime columns are idealized estimates, not same-device measurements. Run `python tools/verify_delivery.py` to check the files against their recorded hashes.
