import json
from argparse import Namespace
from typing import Dict

import mlflow
import numpy as np
import pandas as pd
from optbinning import BinningProcess, Scorecard
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import StratifiedKFold

from postpacu import data, evaluate, utils


def train(args: Namespace, X, y, numeric_vars, trial=None, test_size=0.2, random_seed=42) -> Dict:
    """
    Train a logistic regression model on binned data, and return the model, the scorecard, and the
    performance metrics

    Args:
      args (Namespace): Namespace
      X: the dataframe of features
      y: the target variable
      numeric_vars: list of numeric variables
      trial: If true, don't log with mlflow
      test_size: the fraction of the data to use for testing
      random_seed: int. Defaults to 42
    """
    # instead of "trial" maybe just "mlflow=False"

    # Setup ####
    utils.set_seeds()

    # get categorical and numeric vars
    categorical_variables = [col for col in X.columns if col not in numeric_vars]
    # Define the feature list from dataset (including categorical and numerical)
    list_features = X.columns.values

    # Define selection criteria for BinningProcess
    selection_criteria = {
        "iv": {"min": args.iv_min, "max": args.iv_max, "strategy": args.iv_strategy}
    }

    # Instantiate BinningProcess
    binning_process = BinningProcess(
        categorical_variables=categorical_variables,
        variable_names=list_features,
        selection_criteria=selection_criteria,
        special_codes=[args.special_code],
    )

    # Split ####
    X_train, X_test, y_train, y_test = data.get_data_splits(
        X, y, test_frac=test_size, seed=random_seed
    )

    # get binned data
    X_train_binned = binning_process.fit_transform(
        X_train,
        y_train,
        sample_weight=args.binning_sample_weight,
        metric=args.binning_metric,
        metric_special=args.binning_metric_special,
        metric_missing=args.binning_metric_missing,
        show_digits=args.binning_show_digits,
        check_input=args.binning_check_input,
    )

    X_test_binned = binning_process.transform(
        X_test,
        metric=args.binning_metric,
        metric_special=args.binning_metric_special,
        metric_missing=args.binning_metric_missing,
        show_digits=args.binning_show_digits,
        check_input=args.binning_check_input,
    )

    lr_model = LogisticRegression(
        penalty=args.lr_penalty,
        C=args.C,
        l1_ratio=args.l1_ratio,
        solver=args.solver,
        max_iter=args.max_iter,
        n_jobs=-1,
    )

    sc_model = Scorecard(
        binning_process=binning_process,
        estimator=lr_model,
        scaling_method=args.scaling_method,
        rounding=args.rounding,
        scaling_method_params={"min": args.scaling_method_min, "max": args.scaling_method_max},
        reverse_scorecard=args.reverse_scorecard,
        intercept_based=args.intercept_based,
    )

    # looks like you have to at least do metric_special if you have special values. "empirical" uses WoE
    sc_model.fit(
        X_train,
        y_train,
        metric_missing=args.binning_metric_missing,
        metric_special=args.binning_metric_special,
    )

    scorecard_metrics = evaluate.get_scorecard_metrics(
        sc_model, X_train, X_test, y_train, y_test, trial
    )
    lr_metrics = evaluate.get_lr_metrics(
        lr_model=sc_model.estimator_,
        X_train_binned=X_train_binned,
        X_test_binned=X_test_binned,
        y_train=y_train,
        y_test=y_test,
        trial=trial,
    )
    performance = {"scorecard": scorecard_metrics, "lr": lr_metrics}
    print(json.dumps(performance, indent=2))

    return {
        "args": args,
        "lr_model": lr_model,
        "scorecard_model": sc_model,
        "performance": performance,
    }


def optimize_lr(args: Namespace, X, y, numeric_vars, test_size=0.2, random_seed=42):
    """
    This function takes in a dataset and arguments for optimizing hyperparemeters, returning optimal parameters

    Args:
      args (Namespace): Namespace containing model arguments
      X: the dataframe of features
      y: the target variable
      numeric_vars: list of numeric variables
      test_size: the fraction of the data to use for testing
      random_seed: int. Defaults to 42

    Returns:
      The optimal model and the metrics
    """

    # There is much repeated from train() here.
    # I think it should be this way, because in principle,
    # more pieces could be optimized than are currently
    # being optimized. So I'm trying to maximally include
    # what *could* be optimized, even if it currently isn't

    # Setup ####
    utils.set_seeds()

    # get categorical and numeric vars
    categorical_variables = [col for col in X.columns if col not in numeric_vars]
    # Define the feature list from dataset (including categorical and numerical)
    list_features = X.columns.values

    # Define selection criteria for BinningProcess
    selection_criteria = {
        "iv": {"min": args.iv_min, "max": args.iv_max, "strategy": args.iv_strategy}
    }

    # Instatiate BinningProcess
    binning_process = BinningProcess(
        categorical_variables=categorical_variables,
        variable_names=list_features,
        selection_criteria=selection_criteria,
        special_codes=[args.special_code],
    )

    # Split ####
    X_train, _, y_train, _ = data.get_data_splits(X, y, test_frac=test_size, seed=random_seed)

    # get binned data
    X_train_binned = binning_process.fit_transform(
        X_train,
        y_train,
        sample_weight=args.binning_sample_weight,
        metric=args.binning_metric,
        metric_special=args.binning_metric_special,
        metric_missing=args.binning_metric_missing,
        show_digits=args.binning_show_digits,
        check_input=args.binning_check_input,
    )

    CE_min, _ = utils.get_lr_penalty(X_train_binned, y_train, min(args.l1_ratio_list))
    _, CE_max = utils.get_lr_penalty(X_train_binned, y_train, max(args.l1_ratio_list))

    en_cv = LogisticRegressionCV(
        penalty=args.lr_penalty,
        Cs=np.logspace(
            np.log10(CE_min), np.log10(CE_max), num=args.lr_num_Cs
        ),  # 100 is default argument for "Cs"
        solver=args.solver,
        cv=StratifiedKFold(10),
        n_jobs=-1,
        max_iter=args.max_iter,
        scoring=args.lr_metric,
        l1_ratios=args.l1_ratio_list
        # balancing classes for an lr model inflates intercept/baseline risk.
        # We are trying to predict probabilities,
        # so I don't think we want this
        # , class_weight = 'balanced'
    )

    en_cv.fit(X=X_train_binned, y=y_train)
    metrics_train = mlflow.sklearn.eval_and_log_metrics(
        en_cv, X_train_binned, y_train, prefix="train_"
    )

    # make coefficient 95% CIs
    idx_l1r = np.where(en_cv.l1_ratios_ == en_cv.l1_ratio_)[0][0]
    idx_C = np.where(en_cv.Cs_ == en_cv.C_)[0][0]
    coefs = en_cv.coef_.flatten()
    coef_cvs = en_cv.coefs_paths_[True][:, idx_C, idx_l1r, :]
    coef_names = en_cv.feature_names_in_
    lci = np.percentile(coef_cvs, 2.5, 0)
    hci = np.percentile(coef_cvs, 97.5, 0)
    # last variable in lci and hci will be intercept
    coef_table = pd.DataFrame(
        {"variable": coef_names, "coefficient": coefs, "lower_ci": lci[:-1], "upper_ci": hci[:-1]}
    )

    return en_cv, metrics_train, coef_table
