# postpacu/main.py
import json
import subprocess
import tempfile
import warnings
from argparse import Namespace
from pathlib import Path

import mlflow
import typer
from mlflow.tracking import MlflowClient
from numpyencoder import NumpyEncoder
from optbinning import BinningProcess, Scorecard
from tableone import TableOne

from config import config
from config.config import logger
from postpacu import data, evaluate, predict, train, utils

app = typer.Typer()
warnings.filterwarnings("ignore")


def load_config_dict(filepath):
    """
    Load a dictionary from a JSON's filepath.

    Args:
      filepath: The filepath to the JSON file.

    Returns:
      A dictionary.
    """

    with open(filepath, "r") as fp:
        d = json.load(fp)
    return d


@app.command()
def load_data():
    """
    > Load data from MS SQL
    """
    # Currently Dave provides query, and we run externally
    # should this be done using a Python+SQL interface?
    # Probably....
    # submerge details in "data" module, and call something here like
    # data.execute_sql() or data.pull()?
    raise NotImplementedError


@app.command()
def clean_data():
    data.r_clean_data(config)
    logger.info("✅ Data cleaned using R script.")


@app.command()
def train_model(
    args_fp: str = "config/args.json",
    experiment_name: str = "current candidate",
    run_name: str = "en no cv",
    test_run: bool = False,
) -> None:
    """
    `train_model` takes a json file with model parameters, and trains a model with those parameters, and
    logs the model and performance metrics to mlflow

    Args:
      args_fp (str): Path to args file. Defaults to configs/args.json
      experiment_name (str): MLFlow experiment name. Defaults to current candidate
      run_name (str): MLFlow run name. Defaults to en no cv
      test_run (bool): Disable MLFlow?. Defaults to False
    """

    # r-cleaned data
    X, y = data.preprocess(config.SCORECARD_DATA.absolute())

    # Train
    args = Namespace(**utils.load_dict(filepath=args_fp))
    mlflow.set_experiment(experiment_name=experiment_name)
    experiment = mlflow.set_experiment(experiment_name=experiment_name)
    utils.print_experiment_info(experiment)
    with mlflow.start_run(run_name=run_name) as run:
        utils.print_run_info(run)
        run_id = mlflow.active_run().info.run_id
        # madewithml tutorial makes and logs all artifacts in main,
        # but if you're making plots, it seems like that should be in
        # train.py, so that's how I did it here. -RM
        artifacts = train.train(
            X=X,
            y=y,
            numeric_vars=config.NUMERIC_VARIABLES,
            args=args,
            trial=test_run,
            test_size=config.TEST_SIZE,
        )
        performance = artifacts["performance"]
        model = artifacts["scorecard_model"]
        with tempfile.TemporaryDirectory() as dp:
            utils.save_dict(performance, Path(dp, "performance.json"))
            model.save(str(Path(dp, "scorecard_model.pkl")))
            mlflow.log_artifact(args_fp)
            mlflow.log_artifacts(dp)

    print(json.dumps(performance, indent=2))

    # Save to config
    open(Path(config.CONFIG_DIR, "run_id.txt"), "w", encoding="utf-8").write(run_id)
    utils.save_dict(performance, Path(config.CONFIG_DIR, "performance.json"))

    logger.info("✅ Model trained with fixed parameters in args.")


@app.command()
def optimize(
    args_fp: str = "config/args.json",
    new_args_fp: str = "config/new_args.json",
    experiment_name: str = "Optimize LR",
    run_name: str = "en cv",
) -> None:
    """
    > Optimize the hyperparameters of the ElasticNet model using the `train.optimize_lr` function

    Args:
      args_fp (str): Path to args file. Defaults to configs/args.json
      new_args_fp (str): Where to store best model parameters. Defaults to
    configs/new_candidate_args.json
      experiment_name (str): MLFlow experiment name. Defaults to Optimize LR
      run_name (str): MLFlow run name. Defaults to en cv
    """
    # load data
    X, y = data.preprocess(config.SCORECARD_DATA.absolute())
    args = Namespace(**utils.load_dict(filepath=args_fp))
    mlflow.set_experiment(experiment_name=experiment_name)
    experiment = mlflow.set_experiment(experiment_name=experiment_name)
    utils.print_experiment_info(experiment)
    mlflow.sklearn.autolog()
    # optimize
    with mlflow.start_run(run_name=run_name) as run:
        utils.print_run_info(run)
        opt_model, _, coef_table = train.optimize_lr(
            X=X, y=y, numeric_vars=config.NUMERIC_VARIABLES, args=args, test_size=config.TEST_SIZE
        )

        best_args = {"C": opt_model.C_, "l1_ratio": opt_model.l1_ratio_}
        mlflow.log_params(best_args)
        mlflow.sklearn.log_model(opt_model, "EN CV")
        with tempfile.TemporaryDirectory() as dp:
            coef_table.to_csv(Path(dp, "coefs.csv"))
            mlflow.log_artifacts(dp)

    # tutorial automatically overwrites args_fp
    # I think a human should manually do this
    # unless we're building a continuously learning
    # or auto-updating model, so instead
    # make a json file with name new_args_fp
    utils.save_dict({**best_args}, new_args_fp, cls=NumpyEncoder)

    logger.info("✅ LR Model optimized. Best parameters in new_args_fp.")


@app.command()
def predict_risk(new_X, run_id=None):
    """
    It loads the artifacts from the run_id, and then uses the predict function to make a prediction.

    Args:
      new_X (pd.DataFrame): a pandas dataframe with the same columns as the training data
      run_id: The run_id of the model you want to use to make predictions.

    Returns:
      A list of dictionaries, each containing the input data and the predicted probability.
    """
    # need to think about the best way to get new_X in there. Excel?
    if not run_id:
        run_id = open(Path(config.CONFIG_DIR, "run_id.txt"), encoding="utf8").read()
    artifacts = load_artifacts(run_id=run_id)
    prediction = predict.predict(X=new_X, artifacts=artifacts)
    print(json.dumps(prediction, indent=2))
    return prediction


@app.command()
def get_comparison_tests():
    rscript_path = Path(config.BASE_DIR, "postpacu/chi_and_t_no_identical_filtering.R")
    subprocess.call(
        [
            "/usr/bin/Rscript",
            "--vanilla",
            str(rscript_path.absolute()),
            str(config.ALT_MODEL_DATA.absolute()),
            str(config.COMPARISON_TESTS.absolute()),
        ]
    )
    logger.info("✅ Saved comparison tests")


# TODO Should this be a command?
def generate_tableone():
    df, y = data.preprocess(str(config.ALT_MODEL_DATA.absolute()))
    df["escalation"] = y
    num_vars = config.NUMERIC_VARIABLES
    num_vars = [x for x in num_vars if x in df.columns]
    cat_vars = [col for col in df.columns if col not in num_vars]
    mytable = TableOne(
        df,
        categorical=cat_vars,
        groupby=["escalation"],
        pval=True,
        htest_name=True,
        dip_test=True,
        normal_test=True,
        tukey_test=True,
        pval_adjust="hommel",
    )
    mytable.to_excel(Path(config.RESULTS, "tableone.xlsx"))
    logger.info("✅ Saved Tableone")


def load_artifacts(run_id):
    """
    Downloads the artifacts from the run with the given run_id, and returns a dictionary with the
    model, performance, and arguments

    Args:
      run_id: The run_id of the run you want to load.

    Returns:
      A dictionary with the model, performance, and args
    """
    with tempfile.TemporaryDirectory() as dp:
        client = MlflowClient()
        client.download_artifacts(run_id, "scorecard_model.pkl", dp)
        client.download_artifacts(run_id, "performance.json", dp)
        client.download_artifacts(run_id, "args.json", dp)
        model = Scorecard.load(str(Path(dp, "scorecard_model.pkl")))
        performance = utils.load_dict(filepath=Path(dp, "performance.json"))
        args = utils.load_dict(filepath=Path(dp, "args.json"))

    return {"args": args, "model": model, "performance": performance}


@app.command()
# It's evaluating the model.
def evaluate_model(
    run_id,
    args_fp: str = "config/args.json",
    experiment_name: str = "current candidate",
    run_name: str = "3-day evaluation",
) -> None:
    """
    It loads the model and data, and then evaluates the model on the data

    :param run_id: The run_id of the model you want to evaluate
    :param experiment_name: The name of the experiment you want to evaluate, defaults to current
    candidate
    :type experiment_name: str (optional)
    :param run_name: The name of the run, defaults to 3-day auc
    :type run_name: str (optional)
    """
    args = load_config_dict(filepath=args_fp)

    experiment = mlflow.set_experiment(experiment_name=experiment_name)

    utils.print_experiment_info(experiment)
    if not run_id:
        run_id = open(Path(config.CONFIG_DIR, "run_id.txt")).read()
    X, y = data.preprocess(config.SCORECARD_DATA.absolute())
    # Split ####
    X_train, X_test, y_train, y_test = data.get_data_splits(
        X, y, test_frac=config.TEST_SIZE, seed=config.RANDOM_STATE
    )
    artifacts = load_artifacts(run_id=run_id)
    print(artifacts)
    numeric_vars = config.NUMERIC_VARIABLES
    # get categorical and numeric vars
    categorical_variables = [col for col in X.columns if col not in numeric_vars]
    # Define the feature list from dataset (including categorical and numerical)
    list_features = X.columns.values

    # Define selection criteria for BinningProcess
    selection_criteria = {
        "iv": {"min": args["iv_min"], "max": args["iv_max"], "strategy": args["iv_strategy"]}
    }
    # Instatiate BinningProcess
    binning_process = BinningProcess(
        categorical_variables=categorical_variables,
        variable_names=list_features,
        selection_criteria=selection_criteria,
        special_codes=[args["special_code"]],
    )

    # get binned data
    X_train_binned = binning_process.fit_transform(
        X_train,
        y_train,
        sample_weight=args["binning_sample_weight"],
        metric=args["binning_metric"],
        metric_special=args["binning_metric_special"],
        metric_missing=args["binning_metric_missing"],
        show_digits=args["binning_show_digits"],
        check_input=args["binning_check_input"],
    )

    X_test_binned = binning_process.transform(
        X_test,
        metric=args["binning_metric"],
        metric_special=args["binning_metric_special"],
        metric_missing=args["binning_metric_missing"],
        show_digits=args["binning_show_digits"],
        check_input=args["binning_check_input"],
    )

    with mlflow.start_run(run_name=run_name):
        evaluate_sc = evaluate.get_scorecard_metrics(
            artifacts["model"],
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
        )

        print(json.dumps(evaluate_sc, indent=2))

        evaluate_lr = evaluate.get_lr_metrics(
            lr_model=artifacts["model"].estimator_,
            X_train_binned=X_test_binned,
            X_test_binned=X_test_binned,
            y_train=y_train,
            y_test=y_test,
            N_feat=args["N_top_features"],
        )

    # return evaluate_sc


if __name__ == "__main__":
    app()
