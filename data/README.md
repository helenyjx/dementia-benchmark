# Input data (not included)

Place the raw HRS files in `data/original data/`. These are the RAND HRS longitudinal file, the HRS core interview files and the HRS 2022 Tracker (`trk2022tr_r.dta`). The HRS does not allow redistribution of its files, so each user must register on the HRS data portal (https://hrsdata.isr.umich.edu) and download them. Download steps are in `REPRODUCIBILITY.md`, section "Obtaining the HRS data".

The preprocessing notebooks write the wave-level tables to `data/preprocessed data/`. Both folders contain HRS-derived participant-level data and are ignored by Git.
