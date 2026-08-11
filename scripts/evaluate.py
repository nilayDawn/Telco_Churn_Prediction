import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


import pandas as pd
import yaml

from src.models.predict import ChurnPredictor
from src.models.train import ModelTrainer
from src.utils.logger import logger


def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    logger.info("Running standalone model evaluation on test set...")
    config = load_config()

    test_path = config["data"]["processed_test_path"]
    if not Path(test_path).exists():
        logger.error(f"Test dataset not found at {test_path}")
        return

    test_df = pd.read_csv(test_path)

    # Initialize predictor
    predictor = ChurnPredictor(config)

    X_test, y_test = predictor.preprocessor.transform(test_df)

    trainer = ModelTrainer(config)
    trainer.model = predictor.model

    metrics = trainer.evaluate(X_test, y_test)
    logger.info(f"Test Set Evaluation Metrics: {metrics}")


if __name__ == "__main__":
    main()