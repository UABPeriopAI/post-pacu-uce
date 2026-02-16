# Post-PACU Escalation Prediction

This project aims to predict escalations of care after Post-Anesthesia Care Unit (PACU) discharge
using patient demographics, medical histories, and intra-PACU signals. An escalation of care is
defined as any of the following events occurring within three midnights of PACU discharge:

- **Medical Emergency Team (MET) call**
- **Unplanned Intensive Care Unit (ICU) admission**
- **Unplanned transfer from general care to step-down unit**

The model leverages an elastic-net-regularized logistic regression and utilizes the `optbinning`
package to create a scorecard for risk prediction.

## Table of Contents

- [Background](#background)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Data Preparation](#data-preparation)
- [Usage](#usage)
  - [Training the Model](#training-the-model)
  - [Optimizing Hyperparameters](#optimizing-hyperparameters)
  - [Making Predictions](#making-predictions)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

[Data Dictionary](docs/data_dictionary.md)

## Background

Patients discharged from the PACU may experience unexpected deteriorations requiring escalations of care. Early prediction of such events can enhance patient outcomes and optimize resource allocation. This project develops a predictive model based on comprehensive patient data to identify individuals at risk and facilitate timely interventions.

*For detailed methodology and results, please refer to the associated manuscript.*

## Project Structure

```plaintext
├── .devcontainer/          # Devcontainer definition (Dockerfile + VS Code config)
├── Docker/                 # Container startup scripts
├── config/                 # Runtime configuration and args JSON
├── data/                   # Data files (not included)
├── docs/                   # MkDocs sources and data dictionary
├── llm_utils/              # Shared utilities (vendored dependency)
├── postpacu/               # Main package and R entrypoints
│   ├── r/                   # R utilities for statistical tests
│   ├── preprocess_data.R    # R-based preprocessing
│   └── main.py              # Typer CLI entrypoint
├── site/                   # Generated MkDocs site output
├── mkdocs.yml              # MkDocs configuration
├── pyproject.toml          # Tooling configuration
├── requirements.txt        # Python dependencies
├── setup.py                # Package metadata / install
└── README.md               # Project overview (this file)
```

## Getting Started

### Prerequisites

- **Python 3.11+**
- **pip** (Python package installer)
- **R** (for data cleaning and statistical tests)
  - Install required R packages (see `docs/packages.sh`).
- **Docker** (optional, for devcontainer workflow)

### Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

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

## Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository.
2. **Clone** your fork: `git clone https://github.com/yourusername/yourrepository.git`
3. **Create a branch** for your feature or bug fix: `git checkout -b feature/your-feature`
4. **Commit** your changes: `git commit -am 'Add new feature'`
5. **Push** to the branch: `git push origin feature/your-feature`
6. **Submit a pull request**.

### Open Issues

- [ ] **Defining Input for New Observations**: Determine the required format and preprocessing steps for new data when making predictions.
- [ ] **Improving Documentation**: Expand the README and code comments for better clarity.
- [ ] **Automating R Dependencies**: Integrate R dependency checks and installations within the setup process.

## License

This project is licensed under the [GPLv3](LICENSE).

## References

- *[Link to the associated manuscript detailing the methodology and findings.](#)*
- *Relevant publications and resources.*

---

*Please note that sensitive patient data must be handled in compliance with all applicable regulations and institutional policies. Ensure that all data processing and analysis adhere to ethical guidelines.*
