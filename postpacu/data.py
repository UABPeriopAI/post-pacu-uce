import subprocess
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from config import config
from config.config import logger


def preprocess(r_cleaned_data):
    """
    It takes in the path to the data that has already been cleaned by R, and returns the X and y
    matrices that are ready to be used in the model

    Args:
      r_cleaned_data: the path to the R-cleaned data.

    Returns:
      X is a dataframe of the features, y is a dataframe of the labels.
    """
    logger.info("Assuming data.r_clean_data() has already been run on most recent data.")
    X, y = py_clean_data(data_path=r_cleaned_data)
    return X, y


def r_clean_data(configuration=config) -> None:
    """
    It runs an R script that cleans the raw data and saves it to the `ALT_MODEL_DATA` and
    `SCORECARD_DATA` directories

    Args:
      configuration: the configuration object, which is the default config.py file
    """
    # this is so specific to this project,
    # I think it's ok to just have the input be "config"
    rscript_path = Path(configuration.BASE_DIR, "postpacu/preprocess_data.R")
    subprocess.call(
        [
            "/usr/bin/Rscript",
            "--vanilla",
            str(rscript_path.absolute()),
            str(configuration.RAW_DATA.absolute()),
            str(configuration.ALT_MODEL_DATA.absolute()),
            str(configuration.SCORECARD_DATA.absolute()),
            str(configuration.ALT_MODEL_MISSINGNESS.absolute()),
            str(configuration.SCORECARD_MISSINGNESS.absolute()),
        ]
    )
    logger.info("✅ Saved data cleaned with R!")


def py_clean_data(data_path: Path):
    """
    We read in the data, remove some variables, and return the X and y dataframes

    Args:
      data_path (Path): Path =
    Path('/Users/joshua/Documents/GitHub/scorecard_modeling/data/data_for_scorecard.csv')

    Returns:
      X and y
    """
    data_for_scorecard = pd.read_csv(data_path)
    # if surgical specialty is a number, mark it as NA
    data_for_scorecard.loc[
        data_for_scorecard.SurgicalSpecialty.str.isdigit()
        | data_for_scorecard.SurgicalSpecialty.isna(),
        "SurgicalSpecialty",
    ] = pd.NA
    # remove some variables per 3/14 modeling meeting
    y_MET = data_for_scorecard["MET_Team"] == 1
    y_ICU = (
        (data_for_scorecard["ICUafterPACU_Days"] == 1) & (data_for_scorecard["ICU_Bed_Order"] == 0)
    ) | (data_for_scorecard["ICU_AfterStepDown_NoOrderBeforePacuDepart_Days"] == 1)
    y_stepdown = pd.notna(data_for_scorecard["StepDownUnitAfterGeneralCareTime_Days"])
    data_for_scorecard.drop(
        [
            "SurgicalSpecialty",
            "LastPACU_HR",
            "LastPACU_SBP",
            "LastPACU_RR",
            "LastPACU_PainScore",
            "LastPACU_Aldrete",
            "SchedRecAnesType",
            "Urine",
            "NaCl",
            "LR",
            "PreOpGlucose",
            "PreOpHematocrit",
            "PostOpGlucose",
            "MinPACUTemp",
            "MaxPACUTemp",
            "LastSpO2lte92",
            "LastSBPlte100",
            "LastSBPgte100",
            "LastPaingte5",
            "anes_duration",
            "procedure_duration",
            "LastO2Flowgt2",
            "LastHRgte90",
            "LastMAPlte60",
            "LastMAPgte85",
            "LastRRgte20",
            "CurrentSmoker",  # counterintuitive results
            "Total_BloodProducts",  # duplicate
            "ICU_AfterStepDown_NoOrderBeforePacuDepart_Days",  # part of response
            "MET_Team",
            "ICUafterPACU_Days",
            "ICU_Bed_Order",
            "StepDownUnitAfterGeneralCareTime_Days",
            "ICU_AfterStepDown_NoOrderBeforePacuDepart",
        ],
        axis=1,
        inplace=True,
    )
    y = data_for_scorecard["escalation"]
    X = data_for_scorecard.drop("escalation", axis=1)
    other_escalations = pd.DataFrame(
        {"pt_idx": X.index, "MET": y_MET, "ICU": y_ICU, "stepdown": y_stepdown}
    )
    other_escalations.to_csv(Path(config.INTERMEDIATE_DATA, "other_escalations.csv"))
    logger.info("Other escalation types saved to intermediate data path.")
    return X, y


def get_data_splits(X, y, test_frac=0.2, seed=42):
    """
    It splits the data into training and test sets, and returns the four resulting arrays

    Args:
      X: The data to split
      y: The target variable.
      test_frac: The fraction of the data that should be in the test set.
      seed: The random seed to use when shuffling the data. Defaults to 42

    Returns:
      X_train, X_test, y_train, y_test
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_frac, random_state=seed
    )
    return X_train, X_test, y_train, y_test
