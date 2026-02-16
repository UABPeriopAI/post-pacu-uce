# Post-PACU Escalation Prediction

This project aims to predict escalations of care after Post-Anesthesia Care Unit (PACU) discharge
using patient demographics, medical histories, and intra-PACU signals. An escalation of care is
defined as any of the following events occurring within three midnights of PACU discharge:

- **Medical Emergency Team (MET) call**
- **Unplanned Intensive Care Unit (ICU) admission**
- **Unplanned transfer from general care to step-down unit**

The model leverages an elastic-net-regularized logistic regression and utilizes the `optbinning`
package to create a scorecard for risk prediction.

The repository includes an `llm_utils/` Git submodule for shared LLM utilities. This project
depends on it but does not modify its contents.

## Table of Contents

- [Background](#background)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Devcontainer (Optional)](#devcontainer-optional)
- [Data Preparation](#data-preparation)
- [Usage](#usage)
- [Training the Model](#training-the-model)
- [Optimizing Hyperparameters](#optimizing-hyperparameters)
- [Making Predictions](#making-predictions)
- [Cleaning Data (R)](#cleaning-data-r)
- [Comparison Tests (R)](#comparison-tests-r)
- [CLI Reference](#cli-reference)
- [Data Paths](#data-paths)
- [Development](#development)
- [License](#license)
- [References](#references)

[Data Dictionary](docs/data_dictionary.md)

## Background

Patients discharged from the PACU may experience unexpected deteriorations requiring escalations of care. Early prediction of such events can enhance patient outcomes and optimize resource allocation. This project develops a predictive model based on comprehensive patient data to identify individuals at risk and facilitate timely interventions.

*For detailed methodology and results, please refer to the associated manuscript.*

## Project Structure

```plaintext
.
    .devcontainer/
        Dockerfile
        add-notice.sh
        devcontainer.json
        rocker_scripts/
            install_R_source.sh
            setup_R.sh
    .gitmodules
    .kilocode/
        rules/
            coding_standard.md
            documentation_style.md
            formatting.md
            naming_conventions.md
            restricted_files.md
            security_guidelines.md
    AGENTS.md
    Docker/
        startup.sh
    LICENSE
    Makefile
    README.md
    config/
        anes_pub.mplstyle
        args.json
        config.py
        new_args.json
        performance.json
        run_id.txt
    data/
    docs/
        data_dictionary.docx
        data_dictionary.md
        dev_requirements.txt
        index.md
        packages.sh
        postpacu/
            data.md
            evaluate.md
            main.md
            train.md
            utils.md
        pull_request_template/
            branches/
        serve_docs.sh
        src_setup.sh
    llm_utils/
        .devcontainer/
            Dockerfile
            add-notice.sh
            devcontainer.json
            noop.txt
        .gitignore
        .streamlit/
            config.toml
        .vscode/
            settings.json
        Docker/
            startup.sh
        LICENSE
        Makefile
        README.md
        __init__.py
        aiweb_common/
            ObjectFactory.py
            UML/
            WorkflowHandler.py
            __init__.py
            configurables/
            fastapi/
            file_operations/
            generate/
            report_builder/
            resource/
            streamlit/
        doc_support/
            CreateMDFiles.py
        docker-compose.yml
        docs/
            aiweb_common/
            index.md
            run_aider.sh
        mkdocs.yml
        pyproject.toml
        requirements.txt
        setup.py
        workspace.code-workspace
    mkdocs.yml
    postpacu/
        chi_and_t_no_identical_filtering.R
        data.py
        evaluate.py
        main.py
        predict.py
        preprocess_data.R
        r/
            compare_means.R
            comparison_tests.R
            get_binomial_p.R
        train.py
        utils.py
    pyproject.toml
    requirements.in
    requirements.txt
    setup.py
    workspace.code-workspace
```

## Getting Started

### Prerequisites

- **Python 3.11+**
- **pip** (Python package installer)
- **R** (for data cleaning and statistical tests)
  - Install required R packages (see `docs/packages.sh`).
- **Docker** (optional, for devcontainer workflow)

### Installation

#### Virtual Environment (Optional but Recommended)

Create and activate a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Package Dependencies

Install from the repository root:

```bash
pip install --upgrade pip setuptools wheel
pip install -e .
```

For development (includes additional dependencies for testing and code quality):

```bash
pip install -e ".[dev]"
```

### Devcontainer (Optional)

This repository includes a `.devcontainer/` setup. In VS Code, use
`Dev Containers: Reopen in Container` to build the environment. The container
bootstraps Python dependencies and R packages via `Docker/startup.sh`.

### Data Preparation

Initial data cleaning is performed using R scripts called by Python. Ensure R is installed and accessible from your command line, and that necessary R packages are available.

Place your raw data files in the `data/` directory. Data processing scripts will read from and write to this location.

## Usage

### Training the Model

#### From Python

```python
from config import config
from postpacu import main
from pathlib import Path

args_fp = Path(config.CONFIG_DIR, "args.json")
main.train_model(args_fp)
```

#### From Command Line

```bash
python postpacu/main.py train-model \
    --args-fp="config/args.json" \
    --experiment-name="baseline" \
    --run-name="elasticnet_model"
```

### Optimizing Hyperparameters

#### From Python

```python
from config import config
from postpacu import main
from pathlib import Path

args_fp = Path(config.CONFIG_DIR, "args.json")
main.optimize(args_fp)
```

#### From Command Line

```bash
python postpacu/main.py optimize \
    --args-fp="config/args.json" \
    --new-args-fp="config/new_args.json" \
    --experiment-name="optimization" \
    --run-name="elasticnet_optimization"
```

### Making Predictions

*Note: Defining the input format for new observations is an open issue.*

#### From Python

```python
from postpacu import main
import pandas as pd

# TODO: Define the structure of new_X
new_X = pd.DataFrame({...})

risk_scores = main.predict_risk(new_X)
```

#### From Command Line

```bash
python postpacu/main.py predict-risk \
    --new-X="path/to/new_observations.csv"
```

*Note: The CLI currently accepts `new_X` as a raw argument. It does not yet load a CSV automatically,
so you will likely want to use the Python API for now.*

### Cleaning Data (R)

```bash
python postpacu/main.py clean-data
```

### Comparison Tests (R)

```bash
python postpacu/main.py get-comparison-tests
```

### CLI Reference

All CLI commands are implemented in `postpacu/main.py` via Typer:

1. `load-data` (Not implemented)
1. `clean-data` Run the R preprocessing pipeline.
1. `train-model` Train the scorecard model and log artifacts to MLflow.
1. `optimize` Hyperparameter search for ElasticNet; writes `config/new_args.json`.
1. `predict-risk` Predict risk for a provided dataframe (best via Python API).
1. `get-comparison-tests` Run chi-squared and t-tests and save results.

### Data Paths

Data locations are configured in `config/config.py` and default to `/data/DATASCI`:

1. Raw data: `/data/DATASCI/raw/EscalationsAt3Days.xlsx`
1. Intermediate outputs: `/data/DATASCI/intermediate/`
1. Results: `/data/DATASCI/results/`

If you are not using the shared `/data` volume, update the paths in
`config/config.py` to match your local environment.

## Development

### Running Tests

There is no automated test suite in this repository yet.

### Code Style and Linting

```bash
black --check .
isort --check-only .
autopep8 --diff -a -a .
```

### Building Documentation
The code documentation for this project was automatically created with mkdocs and is available via github-pages:
[https://uabperiopai.github.io/post-pacu-uce/](https://uabperiopai.github.io/post-pacu-uce/)

## License

This project is licensed under the [GPLv3](LICENSE).

## References

- *[Link to the associated manuscript detailing the methodology and findings.](#)*
- *Relevant publications and resources.*

---

*Please note that sensitive patient data must be handled in compliance with all applicable regulations and institutional policies. Ensure that all data processing and analysis adhere to ethical guidelines.*
