# Project layout (no files renamed)

```
.
├── archives/                    # ZIP archives and snapshots
├── data/
│   ├── raw/                     # Source inputs by season/gender (Scraping/, WBB_Data/, rankings, teams, select_sun, season CSVs)
│   └── processed/               # Combined/cleaned datasets ready for modeling (ncaa_data_all*)
├── docs/                        # Supporting documents (A10 Work.pdf)
├── models/                      # Saved model artifacts and data splits (*.joblib)
├── notebooks/                   # Analysis, scraping, and modeling notebooks (incl. deep learning)
├── reports/
│   ├── figures/                 # Visual assets and dashboards (root PNGs + Visualizations/)
│   ├── outputs/                 # Prediction CSVs and test outputs
│   └── Deep Learning Results/   # DL-specific plots and predictions
└── src/                         # Python scripts (ncaa-basketball-analysis.py)
```

Notes
- Raw data is grouped under `data/raw` by source/season; processed datasets live in `data/processed`.
- Visuals are consolidated under `reports/figures`; model outputs under `reports/outputs`.
- Serialized models are in `models/`; notebooks live in `notebooks/` (deep learning work kept under `notebooks/deep learning/`).
