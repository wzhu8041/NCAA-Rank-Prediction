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

## Running the notebooks

### Prerequisites

Install Python 3.10+ and the packages commonly used across the notebooks:

```
pip install jupyterlab pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm catboost joblib
pip install torch torchvision torchaudio  # only required for deep learning notebooks
```

If you plan to re-run scraping notebooks, you may also need:

```
pip install requests beautifulsoup4 lxml
```

### Recommended execution order

The notebooks build on each other. If you start from raw data, run them in this order:

1. **Scraping/collection notebooks** (if you want to refresh raw data)
   - Look for notebooks in `notebooks/` with names referencing "scrape", "data collection", or "rankings".
   - These populate or update `data/raw/` folders.
2. **Data cleaning and feature engineering**
   - Notebooks that read from `data/raw/` and write consolidated CSVs into `data/processed/` (often named with "clean", "prep", or "feature").
   - Output is usually one or more `ncaa_data_all*.csv` files in `data/processed/`.
3. **Model training & evaluation**
   - Notebooks that load from `data/processed/` and write results to `reports/outputs/` and model artifacts to `models/`.
   - Deep learning notebooks are under `notebooks/deep learning/` and write plots to `reports/Deep Learning Results/`.
4. **Visualization & reporting**
   - Notebooks that read predictions or evaluation CSVs and write figures to `reports/figures/`.

### Getting results from the notebooks

After running each stage, outputs should appear in these locations:

- **Processed datasets:** `data/processed/` (look for `ncaa_data_all*.csv`).
- **Model artifacts:** `models/` (joblib files for classical models).
- **Predictions & metrics:** `reports/outputs/` (CSV outputs of model runs and evaluation).
- **Figures:** `reports/figures/` and `reports/Deep Learning Results/` (plots, dashboards, and DL outputs).

If you only want to reproduce results without re-running scraping:

1. Start from the **data cleaning** notebooks that build `data/processed/` from the existing `data/raw/`.
2. Run the **model training** notebooks to generate models and predictions.
3. Run **visualization** notebooks if you want updated figures.

### Model overview

The notebooks typically train and compare multiple model families:

- **Tree-based models:** Random Forest, Gradient Boosting, XGBoost, LightGBM, and CatBoost. These are saved as `.joblib` artifacts under `models/` and produce prediction CSVs in `reports/outputs/`.
- **Linear/regularized models:** Logistic Regression or related baselines for ranking/classification tasks.
- **Deep learning models:** PyTorch-based networks in `notebooks/deep learning/`, with outputs in `reports/Deep Learning Results/`.

Look for notebook sections labeled *Model*, *Training*, or *Evaluation* to see each model's specific hyperparameters and metrics.
