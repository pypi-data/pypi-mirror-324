## Contributors 
[![Documentation Status](https://readthedocs.org/projects/datpro/badge/?version=latest)](https://datpro.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/github/UBC-MDS/dataprofiler_group-30/graph/badge.svg?token=scTqjqGrog)](https://codecov.io/github/UBC-MDS/dataprofiler_group-30)
[![ci-cd](https://github.com/UBC-MDS/dataprofiler_group-30/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/dataprofiler_group-30/actions/workflows/ci-cd.yml)

Dongchun Chen, Ismail (Husain) Bhinderwala, Jingyuan Wang

## 🚀 Meet `datpro` : Your Data’s Best Friend  

If you’ve ever worked with raw data, you know the struggle—messy columns, missing values, outliers lurking where you least expect them. Before you can even start your analysis, you spend hours cleaning, summarizing, and trying to make sense of what’s in front of you.  

That’s why we built `datpro`—a simple yet powerful Python package that makes data profiling **fast, easy, and intuitive**. Whether you're trying to **spot anomalies**, **summarize key statistics**, or **visualize your dataset**, `datpro` does the heavy lifting so you can focus on **what really matters—getting insights**.  

### ✨ Why Use `datpro`?  
Imagine you're working on a new dataset. You want to quickly:  
✅ Understand the structure and key statistics  
✅ Find missing values, duplicates, and outliers  
✅ Generate visualizations without writing long scripts  

Instead of juggling multiple tools, `datpro` lets you do all of this with just a few lines of code. It’s **lightweight, flexible, and fits right into your workflow**.  

### 🔍 What Can `datpro` Do? 

- `summarize_data()`: Summarizes numeric columns in a given DataFrame by calculating key statistical metrics.This function gives an overview of key statistics of numeric columns. It returns a summary DataFrame containing the minimum, 25th percentile (Q1), median (50th percentile), 75th percentile (Q3), and maximum values for each numeric column.

- `detect_anomalies()`: Detects anomalies in a dataset by identifying missing values, outliers, and duplicates. It calculates the percentage of missing data for each column, detects numerical outliers using the interquartile range (IQR) method, and identifies duplicate rows. The function also allows users to specify a particular anomaly type to focus on, making it flexible for targeted data quality checks. If no specific type is provided, all anomaly categories are analyzed by default. This helps in understanding and addressing potential data quality issues efficiently.

- `plotify()`: A versatile function that simplifies DataFrame visualization by automatically generating appropriate plots based on the data types of your columns. It supports various plot types, including histograms and density plots for numeric data, bar charts for categorical data, scatter plots for pairwise numeric relationships, correlation heatmaps for exploring numeric variable relationships, and box plots for numeric vs. categorical comparisons. For pairwise categorical columns, it generates stacked bar charts. The function dynamically analyzes your DataFrame and provides insightful visualizations tailored to your data structure, making exploratory data analysis efficient and comprehensive.

While tools like [`ydata-profiling`](https://docs.profiling.ydata.ai/latest/) provide auto-generated reports, `datpro` is designed to be **modular**—so you can use only what you need, when you need it.

## 📦 Installation  

```bash
$ pip install datpro
```

## Usage
Let’s say you're analyzing employee data and need a quick overview. Instead of manually checking each column, let datpro do the work:

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
And just like that, you get a clear, structured summary, an anomaly report, and meaningful visualizations without spending hours on manual data exploration.

## Run the tests

Run the following command in terminal to execute the tests:
```bash
$ pytest tests/
```

## 🤝 Want to Contribute?

We’d love your help in improving datpro! If you have ideas, bug fixes, or feature suggestions, check out our contribution guidelines.

By contributing, you agree to follow our Code of Conduct—we’re all about collaboration and respect.

## 📜 License

`datpro` was created by Dongchun Chen, Ismail (Husain) Bhinderwala, and Jingyuan Wang. It's open-source and licensed under MIT, so feel free to use and improve it!

## Credits

`datpro` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
