## Contributors 
[![Documentation Status](https://readthedocs.org/projects/datpro/badge/?version=latest)](https://datpro.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/github/UBC-MDS/dataprofiler_group-30/graph/badge.svg?token=scTqjqGrog)](https://codecov.io/github/UBC-MDS/dataprofiler_group-30)
[![ci-cd](https://github.com/UBC-MDS/dataprofiler_group-30/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/dataprofiler_group-30/actions/workflows/ci-cd.yml)

Dongchun Chen, Ismail (Husain) Bhinderwala, Jingyuan Wang

## datpro

The `datpro` package simplifies data profiling by providing essential functions for comprehensive dataset exploration and quality checks. This package offers tools to generate detailed summaries, detect anomalies, and create intuitive visualizations, making it easier to uncover key patterns and insights in your data with minimal effort.

- `summarize_data()`: Summarizes numeric columns in a given DataFrame by calculating key statistical metrics.This function gives an overview of key statistics of numeric columns. It returns a summary DataFrame containing the minimum, 25th percentile (Q1), median (50th percentile), 75th percentile (Q3), and maximum values for each numeric column.

- `detect_anomalies()`: Detects anomalies in a dataset by identifying missing values, outliers, and duplicates. It calculates the percentage of missing data for each column, detects numerical outliers using the interquartile range (IQR) method, and identifies duplicate rows. The function also allows users to specify a particular anomaly type to focus on, making it flexible for targeted data quality checks. If no specific type is provided, all anomaly categories are analyzed by default. This helps in understanding and addressing potential data quality issues efficiently.

- `plotify()`: A versatile function that simplifies DataFrame visualization by automatically generating appropriate plots based on the data types of your columns. It supports various plot types, including histograms and density plots for numeric data, bar charts for categorical data, scatter plots for pairwise numeric relationships, correlation heatmaps for exploring numeric variable relationships, and box plots for numeric vs. categorical comparisons. For pairwise categorical columns, it generates stacked bar charts. The function dynamically analyzes your DataFrame and provides insightful visualizations tailored to your data structure, making exploratory data analysis efficient and comprehensive.

This package provides tools for exploring and cleaning data by summarizing statistics, detecting anomalies, and creating visualizations. While other tools like `ydata-profiling` (https://docs.profiling.ydata.ai/latest/) offer similar functionalities and generate detailed reports, this package focuses on providing modular functions that can be easily integrated into custom workflows.

## Installation

```bash
$ pip install datpro
```

## Usage

```python
import pandas as pd
import datpro as dp

# Example DataFrame
data = {
    'age': [25, 30, 35, None, 40, 30, 35, 100],
    'salary': [50000, 60000, 70000, 80000, 90000, None, 85000, 400000],
    'department': ['HR', 'Finance', 'HR', 'IT', 'Finance', 'IT', 'HR', 'Finance']
}
df = pd.DataFrame(data)

# Summarize numeric data
summary = dp.summarize_data(df)
print("Summary of numeric data:")
print(summary)

# Detect anomalies
anomalies = dp.detect_anomalies(df)
print("Anomaly detection report:")
print(anomalies)

# Visualize data
print("Generating visualizations...")
dp.plotify(df, plot_types=['histogram', 'box', 'correlation'])
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`datpro` was created by Dongchun Chen, Ismail (Husain) Bhinderwala and Jingyuan Wang. It is licensed under the terms of the MIT license.

## Credits

`datpro` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
