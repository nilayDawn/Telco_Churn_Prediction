from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from src.utils.logger import logger


class DataLoader:

    def __init__(self, config: dict):
        self.config = config

    def load_raw_data(self) -> pd.DataFrame:
        raw_path = Path(self.config["data"]["raw_path"])
        if not raw_path.exists():
            logger.error(f"Raw data file not found at {raw_path}")
            raise FileNotFoundError(f"File not found: {raw_path}")

        logger.info(f"Loading raw data from {raw_path}")
        df = pd.read_csv(raw_path)
        return df

    def split_and_save_data(self, df: pd.DataFrame) -> tuple[Path, Path]:
        test_size = self.config["data"]["test_size"]
        random_state = self.config["data"]["random_state"]

        logger.info(
            f"Splitting data into train/test with test_size={test_size}"
        )
        train_df, test_df = train_test_split(
            df, test_size=test_size, random_state=random_state
        )

        train_path = Path(self.config["data"]["processed_train_path"])
        test_path = Path(self.config["data"]["processed_test_path"])

        train_path.parent.mkdir(parents=True, exist_ok=True)

        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)

        logger.info(f"Saved train data to {train_path} ({len(train_df)} rows)")
        logger.info(f"Saved test data to {test_path} ({len(test_df)} rows)")

        return train_path, test_path