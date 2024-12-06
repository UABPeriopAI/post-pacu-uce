# Post-PACU Escalation Prediction

This project aims to predict escalations of care after Post-Anesthesia Care Unit (PACU) discharge using patient demographics, medical histories, and intra-PACU signals. An escalation of care is defined as any of the following events occurring within three midnights of PACU discharge:

- **Medical Emergency Team (MET) call**
- **Unplanned Intensive Care Unit (ICU) admission**
- **Unplanned transfer from general care to step-down unit**

The model leverages an elastic-net-regularized logistic regression and utilizes the `optbinning` package to create a scorecard for risk prediction.

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
├── data/                   # Data files (not included)
├── notebooks/              # Jupyter notebooks for exploratory analysis
├── src/                    # Source code for the project
│   ├── config/             # Configuration files
│   ├── postpacu/           # Main package
│   ├── tests/              # Unit tests
│   └── README.md           # Additional documentation
├── README.md               # Project overview (this file)
├── setup.py                # Installation script
└── requirements.txt        # Python dependencies
```

## Getting Started

### Prerequisites

- **Python 3.7+**
- **pip** (Python package installer)
- **R** (for initial data cleaning)
  - Ensure that required R packages are installed.

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

Navigate to the `src/` directory and install the package:

```bash
cd src
pip install --upgrade pip setuptools wheel
pip install -e .
```

For development (includes additional dependencies for testing and code quality):

```bash
pip install -e ".[dev]"
```

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
    --new-args-fp="config/optimized_args.json" \
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
    --new-X="path/to/new_observations.csv" \
    --output="path/to/risk_scores.csv"
```

*Ensure that `new_X` matches the expected input format of the model. This typically includes the same features used during training.*

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style and Linting

```bash
flake8 src/
```

### Building Documentation

*Documentation guidelines and generation scripts go here, if applicable.*

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
