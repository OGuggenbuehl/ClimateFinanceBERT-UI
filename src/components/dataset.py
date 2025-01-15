import logging

import polars as pl

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FULL_DATASET = None


def load_full_dataset(source, columns):
    global FULL_DATASET
    if FULL_DATASET is None:
        logger.info(f"Loading dataset from {source}")
        FULL_DATASET = pl.read_csv(source=source, columns=columns)
        logger.info("Dataset loaded.")
    return FULL_DATASET


def get_dataset():
    if FULL_DATASET is None:
        raise ValueError("Dataset not loaded. Call `load_dataset` first.")
    return FULL_DATASET
