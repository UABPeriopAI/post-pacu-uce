import json
import random
from collections import Counter
from urllib.request import urlopen

import numpy as np
from sklearn.preprocessing import scale


def load_json_from_url(url):
    """
    It takes a URL as input, opens the URL, reads the data, loads the data into a JSON object, and
    returns the JSON object

    Args:
      url: the url of the API endpoint

    Returns:
      A dictionary
    """
    data = json.loads(urlopen(url).read())
    return data


def load_dict(filepath):
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


def save_dict(d, filepath, cls=None, sortkeys=False):
    """
    It saves a dictionary to a specific location.

    Args:
      d: The dictionary to save.
      filepath: The path to the file to save the dictionary to.
      cls: A custom JSONEncoder subclass. If specified, the object will use this encoder instead of the
    default.
      sortkeys: If True, the keys of the dictionary are sorted before writing. Defaults to False
    """

    with open(filepath, "w") as fp:
        json.dump(d, indent=2, fp=fp, cls=cls, sort_keys=sortkeys)


def set_seeds(seed=42):
    """
    `set_seeds` sets the seed for reproducibility

    Args:
      seed: The seed for the random number generator. Defaults to 42
    """

    # Set seeds
    np.random.seed(seed)
    random.seed(seed)


def mysd(y):
    """
    The function mysd takes a vector y as input and returns the standard deviation of y.

    Args:
      y: the array of values

    Returns:
      The standard deviation of the data set.
    """

    return np.sqrt(np.sum(np.square((y - np.mean(y)))) / len(y))


def get_lr_penalty(X, y, alpha=1):
    """
    The function takes in a matrix of predictors and a vector of outcomes, and returns the minimum and
    maximum values of the regularization parameter lambda that should be used in a logistic regression
    model.

    The function is based on the paper [Regularization Paths for Generalized Linear Models via
    Coordinate Descent](http://www.jstatsoft.org/v33/i01/paper) by Friedman, Hastie, and Tibshirani.

    Args:
      X: the data matrix
      y: the target variable
      alpha: the elastic net mixing parameter. Defaults to 1

    Returns:
      the minimum and maximum values of the regularization parameter lambda.
    """
    # recreate lambda.max from R glmnet according to paper description
    # http://www.jstatsoft.org/v33/i01/paper
    # lambda.min in glmnet does not work as paper describes;
    # however, I'm sticking with the paper's description here for lambda_min
    # returns C_min, C_max for use in sklearn logistic regression

    # ensure numeric stability -- matching what glmnet does
    if alpha < 0.000001:
        alpha = 0.000001

    # paper says scale y, but that's for regression
    # I can only recreate glmnet binomial lambda.max result by setting proportions of classes
    # see discussion:
    # https://stackoverflow.com/questions/25257780/how-does-glmnet-compute-the-maximal-lambda-value
    counter = Counter(y)
    negative_prop = counter[0] / (counter[1] + counter[0])
    positive_prop = 1 - negative_prop

    if y.ndim == 1:
        y = np.asarray(y)
        y = y[:, np.newaxis]

    if X.shape[0] < X.shape[1]:
        lambda_min_ratio = 0.01
    else:
        lambda_min_ratio = 1e-04

    sdX = np.apply_along_axis(mysd, 0, X)
    sX = scale(X, with_std=False) / sdX[None, :]
    sy = np.where(y == 0, -1 * positive_prop, negative_prop)[:]
    lambda_max = max(abs(np.sum(sX * sy, axis=0))) / (len(sy) * alpha)
    lambda_min = lambda_min_ratio * lambda_max

    # sklearn "C" and glmnet "lambda" are inverse of one another
    return 1 / lambda_max, 1 / lambda_min


def print_experiment_info(experiment):
    """
    This function prints the name, experiment ID, artifact location, and lifecycle stage of an
    experiment.

    Args:
      experiment: The experiment object that contains the mlflow experiment information.
    """

    print("Name: {}".format(experiment.name))
    print("Experiment ID: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))


def print_run_info(run):
    """
    It prints out the run_id, experiment_id, params, artifact_uri, and status of a run

    Args:
      run: The run object that contains the mlflow run information.
    """

    print("run_id: {}".format(run.info.run_id))
    print("experiment_id: {}".format(run.info.experiment_id))
    print("params: {}".format(run.data.params))
    print("artifact_uri: {}".format(run.info.artifact_uri))
    print("status: {}".format(run.info.status))
