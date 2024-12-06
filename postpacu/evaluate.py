# postpacu/evaluate.py
import json
import tempfile
from pathlib import Path
from typing import Dict

import matplotlib.font_manager
import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
import shap
from optbinning import Scorecard
from optbinning.scorecard import ScorecardMonitoring, plot_auc_roc
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from config import config

# we may want a separate file called "explain.py"
# for some of what I've included here for now.
# Agreed RM - I've added a story to Azure
print(matplotlib.font_manager.fontManager.ttflist)


def get_scorecard_metrics(
    scorecard_model: Scorecard, X_train, X_test, y_train, y_test, trial=None
) -> Dict:
    """
    It takes a scorecard model, the training and test data, and returns a dictionary of metrics

    Args:
      scorecard_model (Scorecard): Scorecard
      X_train: the training data
      X_test: the test data
      y_train: the train set labels
      y_test: the test set labels
      trial: if True, don't log with mlflow

    Returns:
      A dictionary of metrics
    """
    summary = scorecard_model.table(style="detailed").round(3)

    # log with mlflow
    with tempfile.TemporaryDirectory() as dp:
        summary.to_excel(Path(dp, "optbinning_scorecard_en_intercept.xlsx"))
        y_train_pred = scorecard_model.predict_proba(X_train)[:, 1]
        y_test_pred = scorecard_model.predict_proba(X_test)[:, 1]

        style_file_path = str(config.PLOT_STYLE)
        plt.style.use(style_file_path)
        plot_auc_roc(
            y_train,
            y_train_pred,
            title="",
            savefig=False,
            fname=str(Path(dp, "train_roc_en_intercept2.png")),
        )
        ax = plt.gca()
        ax.xaxis.label.set_fontsize(28)
        ax.set_xlabel("False Positive Rate", fontname="Arial", fontsize=28)
        ax.set_ylabel("True Positive Rate", fontname="Arial", fontsize=28)
        for line in ax.get_lines():
            line.set_color("black")

        plt.savefig(fname=str(Path(dp, "train_roc_en_intercept2.png")))
        plt.close()

        plot_auc_roc(
            y_test,
            y_test_pred,
            title="",
            savefig=False,
            fname=str(Path(dp, "test_roc_en_intercept2.png")),
        )
        ax = plt.gca()
        ax.set_xlabel("False Positive Rate", fontname="Arial", fontsize=28)
        ax.set_ylabel("True Positive Rate", fontname="Arial", fontsize=28)
        for line in ax.get_lines():
            line.set_color("black")

        plt.savefig(fname=str(Path(dp, "test_roc_en_intercept2.png")))
        plt.close()

        score = scorecard_model.score(X_train)
        score_test = scorecard_model.score(X_test)
        mask = y_train == 0
        plt.hist(score[mask], label="non-event", color="b", alpha=0.35, density=True)
        plt.hist(score[~mask], label="event", color="r", alpha=0.35, density=True)
        plt.xlabel("score")
        plt.legend()
        plt.savefig(Path(dp, "scores_en_intercept.png"))
        monitoring = ScorecardMonitoring(
            scorecard_model,
            psi_method="cart",
            psi_n_bins=5,
            psi_min_bin_size=0.05,
            show_digits=2,
            verbose=False,
        )
        monitoring.fit(X_test, y_test, X_train, y_train)
        monitoring.psi_plot(str(Path(dp, "psi_en_intercept.png")))
        psi_bins = monitoring.tests_table()
        psi_bins.to_excel(Path(dp, "psi_bins_en_intercept.xlsx"))

        test_score_df = pd.DataFrame({"pt_idx": X_test.index, "score": score_test})
        test_score_df.to_csv(Path(dp, "test_scores.csv"), index=False)

        metrics = monitoring._df_performance.to_dict()

        if not trial:
            mlflow.log_artifacts(dp)
            mlflow.log_param("intercept", scorecard_model.intercept_)
            with tempfile.NamedTemporaryFile(prefix="metrics_", mode="w", suffix=".txt") as f:
                # Note the mode is 'w' so json could be dumped
                # Note the suffix is .txt so the UI will show the file
                json.dump(metrics, f)
                # You cannot close the file as it will be removed-You have to move back to its head
                f.seek(0)
                mlflow.log_artifact(f.name)

    return metrics


def get_lr_metrics(
    lr_model: LogisticRegression, X_train_binned, X_test_binned, y_train, y_test, N_feat, trial=None
):
    """
    > This function takes a logistic regression model, the training and test data, and the number of
    features, and returns a dictionary of metrics for the model

    :param lr_model: LogisticRegression
    :type lr_model: LogisticRegression
    :param X_train_binned: the training data, binned
    :param X_test_binned: the test set, binned
    :param y_train: the training labels
    :param y_test: the test set labels
    :param N_feat: number of features to use in the model
    :param trial: if you're running this in a hyperparameter tuning context, this is the trial object
    :return: A dictionary of metrics for the training and test sets.
    """
    N_feat = N_feat + 1
    # shap
    explainer = shap.Explainer(lr_model, X_train_binned)
    expected_value = explainer.expected_value
    explainer(X_test_binned)

    with tempfile.TemporaryDirectory() as dp:
        # histogram of proba from base EN model
        y_pred = lr_model.predict_proba(X_test_binned)[:, 1]
        plt.hist(y_pred)
        plt.xlabel("Probability of escalation")
        plt.savefig(Path(dp, "logistic_escalation_probability.png"))
        plt.close()

        # decision path for >= 10% probability
        T1 = X_test_binned[y_pred >= 0.1]
        sh1 = explainer.shap_values(T1)  # [1]
        shap.decision_plot(
            expected_value,
            sh1,
            T1,
            # feature_order="hclust",
            feature_display_range=slice(None, -len(config.NUMERIC_VARIABLES) + 1, -1),
            link="logit",
            show=False,
        )
        plt.savefig(Path(dp, "decision_path_gt10pct_all.png"), bbox_inches="tight")
        plt.close()

        # decision path for >= 10% probability -- just top 10
        # TODO: play with Top X #
        shap.decision_plot(
            expected_value,
            sh1,
            T1,
            # TODO: make sure top 1 isn't left out - python "clopen" ranges
            feature_display_range=slice(None, -N_feat, -1),  # selects top 10
            link="logit",
            show=False,
        )
        plt.savefig(Path(dp, "decision_path_gt10percent_topN.png"), bbox_inches="tight")
        plt.close()

        # decision path for >= 20% probability
        # TODO: play with Top X #
        T2 = X_test_binned[y_pred >= 0.2]
        sh2 = explainer.shap_values(T2)  # [1]
        shap.decision_plot(
            expected_value,
            sh2,
            T2,
            # feature_order="hclust",
            # TODO: make sure top 1 isn't left out - python "clopen" ranges
            feature_display_range=slice(None, -len(config.NUMERIC_VARIABLES) + 1, -1),
            link="logit",
            show=False,
        )
        plt.savefig(Path(dp, "decision_path_gt20percent_all.png"), bbox_inches="tight")
        plt.close()

        # decision path for >= 20% probability -- just top 10
        shap.decision_plot(
            expected_value,
            sh2,
            T2,
            feature_display_range=slice(None, -N_feat, -1),
            link="logit",
            show=False,
        )
        plt.savefig(Path(dp, "decision_path_gt20percent_topN.png"), bbox_inches="tight")
        plt.close()

        if not trial:
            mlflow.log_artifacts(dp)
            mlflow.sklearn.log_model(lr_model, "lr model")
            metrics_train = mlflow.sklearn.eval_and_log_metrics(
                lr_model, X_train_binned, y_train, prefix="lr_train_"
            )
            metrics_test = mlflow.sklearn.eval_and_log_metrics(
                lr_model, X_test_binned, y_test, prefix="lr_test_"
            )
            mlflow.log_params(lr_model.get_params())
            mlflow.sklearn.log_model(lr_model, "LR Model")
        else:
            metrics_train = classification_report(
                y_train, lr_model.predict(X_train_binned), output_dict=True
            )
            metrics_test = classification_report(
                y_test, lr_model.predict(X_test_binned), output_dict=True
            )

    metrics = {"lr_train": metrics_train, "lr_test": metrics_test}
    return metrics
