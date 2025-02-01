import pandas as pd
import numpy as np
import altair as alt
from itertools import combinations

def summarize_data(df):
    """
    Summarizes numeric columns in a given DataFrame by calculating key statistical metrics.

    This function automatically detects numeric columns in the provided DataFrame and 
    returns a summary DataFrame containing the minimum, 25th percentile (Q1), median (50th percentile),
    75th percentile (Q3), and maximum values for each numeric column.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing data to be summarized.

    Returns
    -------
    pandas.DataFrame
        A DataFrame where each row corresponds to a numeric column in the input DataFrame,
        and the columns represent the calculated statistics: min, 25%, 50% (median), 75%, and max.

    Example
    -------
    >>> summarize_data(df)
    """

	# Check if input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("The input DataFrame is empty.")

    # Select numeric columns
    numeric_cols = df.select_dtypes(include=['number'])

    # Check if there are numeric columns
    if numeric_cols.empty:
        raise ValueError("The DataFrame contains no numeric columns.")

    # Calculate summary statistics
    summary = numeric_cols.describe(percentiles=[0.25, 0.5, 0.75]).T

    # Select relevant statistics
    summary = summary[['min', '25%', '50%', '75%', 'max']]

    return summary

def detect_anomalies(df, anomaly_type=None):
    """
    Detect anomalies in a dataframe, including missing values, outliers, and duplicates.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe to analyze.
    anomaly_type : str, optional
        Specify which anomaly to check ('missing_values', 'outliers', or 'duplicates').
        If None, all anomaly types will be checked.
    
    Returns
    -------
    dict
        A dictionary containing detected anomalies based on the specified anomaly_type.
    
    Example
    -------
    >>> import pandas as pd
    >>> data = {'A': [1, 2, np.nan, 4], 'B': [100, 200, 300, 400], 'C': [1, 1, 1, 100]}
    >>> df = pd.DataFrame(data)
    >>> detect_anomalies(df, anomaly_type='missing_values')
    {'missing_values': {'A': {'missing_count': 1, 'missing_percentage': 25.0}}}
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    
    report = {}
    total_rows = len(df)
    
    if anomaly_type is None or anomaly_type == 'missing_values':
        missing_values = df.isnull().sum()
        missing_info = {
            col: {
                "missing_count": int(missing_values[col]),
                "missing_percentage": round((missing_values[col] / total_rows) * 100, 2)
            }
            for col in df.columns if missing_values[col] > 0
        }
        report['missing_values'] = missing_info if missing_info else "No missing values detected."
    
    if anomaly_type is None or anomaly_type == 'outliers':
        outlier_info = {}
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
            if not outliers.empty:
                outlier_info[col] = {
                    "outlier_count": len(outliers),
                    "outlier_percentage": round((len(outliers) / total_rows) * 100, 2)
                }
        report['outliers'] = outlier_info if outlier_info else "No outliers detected."
    
    if anomaly_type is None or anomaly_type == 'duplicates':
        duplicate_count = df.duplicated().sum()
        report['duplicates'] = {
            "duplicate_count": duplicate_count,
            "duplicate_percentage": round((duplicate_count / total_rows) * 100, 2)
        } if duplicate_count > 0 else "No duplicate rows detected."
    
    return report

def plotify(df, plot_types=None):
    """
    Visualize a DataFrame by generating specified plots based on column datatypes.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to be visualized.
    
    plot_types : list of str, optional
        A list of plot types to generate. Available options include:
        - 'histogram' : Plot a histogram for numeric columns.
        - 'density' : Plot a density plot for numeric columns.
        - 'bar' : Plot a bar chart for categorical columns.
        - 'scatter' : Plot scatter plots for pairwise numeric columns.
        - 'correlation' : Plot a correlation heatmap for numeric columns.
        - 'box' : Plot box plots for numeric vs categorical columns.
        - 'stacked_bar' : Plot stacked bar charts for pairwise categorical columns.
        If None, all plot types are generated by default.

    Returns
    -------
    None
        Generates and displays specified plots based on the provided column types.
    
    Raises
    ------
    TypeError
        If the input is not a pandas DataFrame.
    ValueError
        If the input DataFrame is empty.

    Notes
    -----
    - Numeric columns are those of types 'int64', 'float64'.
    - Categorical columns are those of types 'object', 'category', and 'bool'.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    # Set default plot types if not specified
    if plot_types is None:
        plot_types = ['histogram', 'density', 'bar', 'scatter', 'correlation', 'box', 'stacked_bar']

    # Analyze columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    # Individual column visualizations
    if 'histogram' in plot_types or 'density' in plot_types:
        for col in numeric_cols:
            print(f"Visualizing numeric column: {col}")
            if 'histogram' in plot_types:
                hist_chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X(col, bin=True, title=f"{col} (binned)"),
                    y=alt.Y('count()', title='Count')
                ).properties(title=f"Histogram of {col}")
                hist_chart.display()
            if 'density' in plot_types:
                density_chart = alt.Chart(df).transform_density(
                    col, as_=[col, 'density']
                ).mark_area(opacity=0.5).encode(
                    x=alt.X(col, title=col),
                    y=alt.Y('density:Q', title='Density')
                ).properties(title=f"Density Plot of {col}")
                density_chart.display()

    if 'bar' in plot_types:
        for col in categorical_cols:
            print(f"Visualizing categorical column: {col}")
            bar_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(col, title=col),
                y=alt.Y('count()', title='Count')
            ).properties(title=f"Bar Chart of {col}")
            bar_chart.display()

    # Pairwise relationships
    if 'scatter' in plot_types:
        for col1, col2 in combinations(numeric_cols, 2):
            print(f"Visualizing numeric vs numeric: {col1} vs {col2}")
            scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
                x=alt.X(col1, title=col1),
                y=alt.Y(col2, title=col2),
                tooltip=[col1, col2]
            ).properties(title=f"Scatter Plot: {col1} vs {col2}")
            scatter_chart.display()

    if 'correlation' in plot_types and len(numeric_cols) > 1:
        print("Visualizing correlation heatmap")
        corr_matrix = df[numeric_cols].corr().stack().reset_index()
        corr_matrix.columns = ['Variable 1', 'Variable 2', 'Correlation']
        heatmap = alt.Chart(corr_matrix).mark_rect().encode(
            x=alt.X('Variable 1:N'),
            y=alt.Y('Variable 2:N'),
            color=alt.Color('Correlation:Q', scale=alt.Scale(scheme='viridis')),
            tooltip=['Variable 1', 'Variable 2', 'Correlation']
        ).properties(title='Correlation Heatmap')
        heatmap.display()

    if 'box' in plot_types:
        for num_col in numeric_cols:
            for cat_col in categorical_cols:
                print(f"Visualizing numeric vs categorical: {num_col} vs {cat_col}")
                box_plot = alt.Chart(df).mark_boxplot().encode(
                    x=alt.X(cat_col, title=cat_col),
                    y=alt.Y(num_col, title=num_col),
                    color=alt.Color(cat_col, legend=None)
                ).properties(title=f"Box Plot: {num_col} vs {cat_col}")
                box_plot.display()

    if 'stacked_bar' in plot_types:
        for cat_col1, cat_col2 in combinations(categorical_cols, 2):
            print(f"Visualizing categorical vs categorical: {cat_col1} vs {cat_col2}")
            stacked_bar = alt.Chart(df).mark_bar().encode(
                x=alt.X(cat_col1, title=cat_col1),
                y=alt.Y('count()', title='Count'),
                color=alt.Color(cat_col2, title=cat_col2)
            ).properties(title=f"Stacked Bar Chart: {cat_col1} vs {cat_col2}")
            stacked_bar.display()