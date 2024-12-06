# config.py
import logging
import sys
from pathlib import Path

import mlflow
from rich.logging import RichHandler

# Directories
BASE_DIR = Path(__file__).parent.parent.absolute()
CONFIG_DIR = Path(BASE_DIR, "config")
DATA_DIR = Path("/data/DATASCI")
RAW_DATA = Path(DATA_DIR, "raw")
INTERMEDIATE_DATA = Path(DATA_DIR, "intermediate")
RESULTS = Path(DATA_DIR, "results")

# Assets
RAW_DATA = Path(RAW_DATA, "EscalationsAt3Days.xlsx")
PLOT_STYLE = Path(CONFIG_DIR, "anes_pub.mplstyle")

# Intermediate
SCORECARD_DATA = Path(INTERMEDIATE_DATA, "variable_setup_for_scorecard_3days.csv")
ALT_MODEL_DATA = Path(INTERMEDIATE_DATA, "variable_setup_3days.csv")

# Results
SCORECARD_MISSINGNESS = Path(RESULTS, "scorecard_missingness_report_3days.csv")
ALT_MODEL_MISSINGNESS = Path(RESULTS, "missingness_report_3days.csv")
COMPARISON_TESTS = Path(RESULTS, "comparison_tests_3days.csv")

# Train/test split size
TEST_SIZE = 0.2

# Random seed
RANDOM_STATE = 42

# Plot Title
PLOT_TITLE = "ROC Curve - Escalation within 3 days"

# numeric variables
numeric_variables_all = [
    "Age",
    "BMI",
    "MinPACULastHour_SpO2",
    "LastPACU_SpO2",
    "MaxPACULastHour_O2FlowRate",
    "LastPACU_O2FlowRate",
    "MaxPACULastHour_SBP",
    "LastPACU_SBP",
    "MinPACULastHour_MAP",
    "MaxPACULastHour_MAP",
    "LastPACU_MAP",
    "MaxPACULastHour_RR",
    "LastPACU_RR",
    "MaxPACULastHour_PainScore",
    "LastPACU_PainScore",
    "MinPACULastHour_Aldrete",
    "LastPACU_Aldrete",
    "AlbuminLevel",
    "MACE_Score",
    "EBL",
    "Urine",
    "PACU_Urine_mL",
    "SugammadexAmount",
    "NeostigmineAmount",
    "RBCs",
    "NaCl",
    "Normosol",
    "Albumin",
    "LR",
    "Isolyte",
    "BloodProductsTotal",
    "CrystalloidsTotal",
    "LastPACU_Temp",
    "MinPACULastHour_Temp",
    "anes_duration",
    "procedure_duration",
    "PreOpPlatelets",
    "anes_surgical_duration_diff",
    "MaxPACULastHour_HR",
    "LastPACU_HR",
    "MinPACULastHour_SBP",
    "PreOpGlucose",
    "PreOpBicarb",
    "PreOpHemoglobin",
    "PreOpHematocrit",
    "PostOpGlucose",
    "MinPACUTemp",
    "MaxPACUTemp",
    "Total_NonBloodFluids",
    "FFP",
    "Cryo",
    "Platelets",
    "CellSaver",
    "D5and10",
    "WholeBlood",
]
NUMERIC_VARIABLES = list(set(numeric_variables_all))

# Experiment tracking
mlflow.set_tracking_uri("http://localhost:5000")
# if not using docker setup:
# STORES_DIR = Path(BASE_DIR, "stores")
# MODEL_REGISTRY = Path(STORES_DIR, "model")
# MODEL_REGISTRY.mkdir(parents=True, exist_ok=True)
# mlflow.set_tracking_uri("file://" + str(MODEL_REGISTRY.absolute()))

print("registry_uri: {}".format(mlflow.get_registry_uri()))
print("tracking_uri: {}".format(mlflow.get_tracking_uri()))

# logging
LOGS_DIR = Path(BASE_DIR, "logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# config/config.py
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {
            "format": "%(levelname)s %(asctime)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)d]\n \
            %(message)s\n"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "root": {
        "handlers": ["console", "info", "error"],
        "level": logging.INFO,
        "propagate": True,
    },
}

# config/config.py

logging.config.dictConfig(logging_config)
logger = logging.getLogger()
logger.handlers[0] = RichHandler(markup=True)  # pretty formatting
