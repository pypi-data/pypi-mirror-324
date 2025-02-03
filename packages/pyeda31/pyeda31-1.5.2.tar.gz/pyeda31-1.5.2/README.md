# pyeda31

| Category| Status |
|---------|--------|
| CI-CD | [![ci-cd](https://github.com/UBC-MDS/pyeda/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/pyeda/actions/workflows/ci-cd.yml) |
| Testing | [![codecov](https://codecov.io/gh/UBC-MDS/pyeda/graph/badge.svg?token=7fkP6T1239)](https://codecov.io/gh/UBC-MDS/pyeda) |
| Documentation | [![Documentation Status](https://readthedocs.org/projects/pyeda31/badge/?version=latest)](https://pyeda31.readthedocs.io/en/latest/?badge=latest)|
| Repo Status | [![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/) |
| Package Version | [![PyPI - Version](https://img.shields.io/pypi/v/pyeda31)](https://pypi.org/project/pyeda31/) |
| Python Versions | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyeda31)](https://pypi.org/project/pyeda31/) |

This python package creates an exploratory data analysis utility designed to streamline the initial stages of data exploration and statistic overview. The three core functions are file validation, handling missing values, and generating summary statistics. `pyeda31` offers users a practical toolkit for data preprocessing and exploration, enabling them to work more efficiently with CSV datasets across various projects.

## Contributors

Catherine Meng, Jessie Zhang, Zheng He

## Functions

- **`check_csv`**  
    Check if the given file has a CSV file extension and whether it can be read by the pandas library.
- **`missing_value_summary`**  
    This function is to provide a summary of missing values in the dataset.
- **`get_summary_statistics`**  
    Generate summary statistics for specified columns or all columns if none are provided.

## Contributing to the Python Ecosystem
The `pyeda31` package complements the Python ecosystem by providing simple and efficient tools for users to implement quick EDA in the first step of their analysis. While there are some other similar Python packages such as [Sweetviz](https://pypi.org/project/sweetviz/) (in-depth EDA with a focus on visualization) and [perform-eda](https://pypi.org/project/perform-eda/) (providing comprehensive EDA analysis), these tools can be too heavyweight for quick analysis. Instead, our `pyeda31` package aims for simplicity and efficiency, enabling users to quickly complete the most basic and important steps, including validating dataset formats, checking for missing values, and generating statistical summaries for columns of interest. t is a lightweight alternative for small-scale tasks or for gaining an initial understanding of the dataset before in-depth research.Users can also combine `pyeda31` with other visualization packages for deeper insights.

## Installation

``` bash
$ pip install pyeda31
```

## Usage

`pyeda31` can be used to verify the format of data files and perform basic exploratory data analysis as follows:
```python
from pyeda31.check_csv import check_csv
from pyeda31.pymissing_values_summary import missing_values_summary
from pyeda31.data_summary import get_summary_statistics
```
#### Check if the given data file is in csv format
```python
data_file_path = "docs/sample_data.csv"  # path to your data file
if not check_csv(data_file_path):
    raise TypeError("The given file either does not have a CSV file extension or cannot be read by the pandas library. Please check the printed error message for more details.")
```
#### Check if the data file has a CSV file extension and whether it can be read by the pandas library
```python
df = pd.read_csv(data_file_path)

missing_summary = missing_values_summary(df)
print("Missing Values Summary:")
print(missing_summary)
```
#### Get the data summary for either all columns or the specified columns of our dataset (adjustable decimal precision for mean)
```python
get_summary_statistics(df)
get_summary_statistics(df, col=["numeric", "categorical"]) 
get_summary_statistics(df, col=["numeric"], decimal = 1)  
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pyeda31` was created by Catherine Meng, Jessie Zhang, Zheng He. It is licensed under the terms of the MIT license.

## Credits

`pyeda31` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
