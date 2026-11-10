# Saved aggregate results

| Folder | Contents |
| --- | --- |
| `tables/audited_sources/` | Final aggregate CSV sources: performance with intervals, paired differences, calibration, decision curves, overlap, importance and runtime tables, plus `supplementary/` with the manuscript Table 1 and Supplementary Tables S1–S27 |
| `tables/outcome_flow/` | Supplementary Table S1 (final audited counts for the four windows) |
| `tables/runtime/` | Measured runtime summary, the editable workbook with the idealized hardware-normalized estimates, and `S20_FP32_equivalent.csv`, the Supplementary Table S20 printed in the manuscript (primary outcome; time per training epoch, total training time and total inference time, FP32-equivalent on an RTX 5070 Ti; built by `inference/supplementary_tables.py`) |
| `verification/` | Saved completion, source, model, comparison and cross-device acceptance reports from the full run |
| `MANIFEST.json` | SHA-256 and size of every file in this folder |

The cohort sizes (analytic samples 13,246 and 12,236 in 2000; 14,123 and 11,603 in 2010) and all numbers in the manuscript tables come from these files. They contain aggregate results only. The normalized runtime columns are idealized estimates, not same-device measurements. Run `python tools/verify_delivery.py` to check the files against their recorded hashes.
