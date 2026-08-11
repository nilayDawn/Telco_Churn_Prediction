## Folder structure

```
my_ml_project/
├── .github/
│   └── workflows/
│       ├── ci.yaml                # Linter, tests, and code checks on PR/Push
│       └── cd.yaml                # Automated build and deployment pipeline
├── .gitignore
├── README.md
├── pyproject.toml                 # uv configuration & project metadata
├── uv.lock                        # Lockfile for exact, reproducible builds
├── Dockerfile                     # Container definition for deployment
├── docker-compose.yaml            # Optional: Local container setup (App + MLflow)
│
├── config/
│   ├── config.yaml                # General parameters (data paths, model params)
│   └── logging_config.yaml        # Logging formatters and handlers configuration
│
├── data/                          # Keep OUT of git (.gitignore)
│   ├── raw/                       # Unprocessed, immutable source data
│   ├── processed/                 # Cleaned and feature-engineered datasets
│   └── external/                  # Third-party baseline data
│
├── logs/                          # Directory for file log outputs (.gitignore)
│   └── app.log
│
├── artifacts/                     # Directory for exported models/encoders (.gitignore)
│   ├── model.pkl
│   └── scaler.pkl
│
├── mlruns/                        # Local MLflow run metadata and metrics (.gitignore)
│
├── great_expectations/            # Data validation suites and checkpoints
│   ├── expectations/
│   └── great_expectations.yml
│
├── notebooks/                     # Exploratory Data Analysis (EDA) only
│   ├── 01_eda.ipynb
│   └── 02_model_experiments.ipynb
│
├── src/                           # Source code modular package
│   ├── __init__.py
│   ├── data/                      # Data ingestion and validation logic
│   │   ├── __init__.py
│   │   ├── load_data.py
│   │   └── validate_data.py
│   ├── features/                  # Feature engineering transformers
│   │   ├── __init__.py
│   │   └── build_features.py
│   ├── models/                    # Training and inference scripts
│   │   ├── __init__.py
│   │   ├── train.py
│   │   └── predict.py
│   └── utils/                     # Helper tools (logger setup, custom metrics)
│       ├── __init__.py
│       └── logger.py
│
├── app/                           # Production API or Web Interface
│   ├── __init__.py
│   ├── main.py                    # FastAPI app or Streamlit frontend
│   └── schema.py                  # Input/output Pydantic schemas for API
│
├── tests/                         # Unit and integration test suite
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_features.py
│   └── test_models.py
│
└── scripts/                       # Execution entry points for pipelines
    ├── run_pipeline.py
    └── evaluate.py