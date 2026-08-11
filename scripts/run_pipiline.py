import sys
from pathlib import Path

# Add project root directory to python path
sys.path.append(str(Path(__file__).resolve().parents[1]))


import yaml
from src.data.load_data import DataLoader
from src.data.validate_data import DataValidator
from src.features.build_features import FeatureEngineeredPreprocessor
from src.models.train import ModelTrainer
from src.utils.logger import logger


def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    logger.info("Starting end-to-end training pipeline...")
    config = load_config()

    # 1. Data Ingestion & Validation
    loader = DataLoader(config)
    raw_df = loader.load_raw_data()

    validator = DataValidator(config)
    validator.validate_raw_schema(raw_df)

    train_path, test_path = loader.split_and_save_data(raw_df)

    # 2. Data Preprocessing & Feature Engineering
    preprocessor = FeatureEngineeredPreprocessor(config)

    import pandas as pd

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    X_train, y_train = preprocessor.fit_transform(train_df)
    X_test, y_test = preprocessor.transform(test_df)

    preprocessor.save_preprocessor()

    # 3. Model Training & Evaluation
    trainer = ModelTrainer(config)
    trainer.train(X_train, y_train)

    metrics = trainer.evaluate(X_test, y_test)
    trainer.save_model()
    trainer.log_to_mlflow(metrics)

    logger.info("Pipeline execution completed successfully!")


if __name__ == "__main__":
    main()