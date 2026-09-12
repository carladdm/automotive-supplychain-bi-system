"""Configuration module for paths, database connections, and environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_RAW_DIR: Path = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR: Path = BASE_DIR / "data" / "processed"
REPORTS_DIR: Path = BASE_DIR / "reports"
FIGURES_DIR: Path = REPORTS_DIR / "figures"

DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: str = os.getenv("DB_PORT", "3306")
DB_USER: str = os.getenv("DB_USER", "root")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
DB_NAME: str = os.getenv("DB_NAME", "BBDDCaminosAutopartes")

MYSQL_URI: str = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    if DB_PASSWORD
    else f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
