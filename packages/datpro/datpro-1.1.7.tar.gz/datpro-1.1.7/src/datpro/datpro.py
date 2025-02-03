import pandas as pd
import numpy as np
import altair as alt
from itertools import combinations
from typing import Dict, Union, Optional, List

def summarize_data(df: pd.DataFrame) -> pd.DataFrame:
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
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = {
    ...     "A": [1, 2, np.nan, 4],
    ...     "B": [100, 200, 300, 400],
    ...     "C": [1, 1, 1, 100]
    ... }
    >>> df = pd.DataFrame(data)
    >>> summarize_data(df)
         min   25%   50%   75%    max
    A    1.0   1.5   2.0   3.0    4.0
    B  100.0  175.0  250.0  325.0  400.0
    C    1.0   1.0   1.0   50.5  100.0
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

def detect_anomalies(df: pd.DataFrame, anomaly_type: Optional[str] = None) -> Dict[str, Union[Dict[str, Dict[str, Union[int, float]]], str]]:
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

def plotify(df: pd.DataFrame, plot_types: Optional[List[str]] = None, save: bool = False, save_path: str = "plots", file_prefix: str = "plot") -> Dict[str, alt.Chart]:
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
    
    save : bool, optional
        If True, saves the plots to the specified path. Default is False.
    
    save_path : str, optional
        The directory where plots should be saved. Default is 'plots'.
    
    file_prefix : str, optional
        The prefix for saved plot filenames. Default is 'plot'.
    
    Returns
    -------
    dict
        A dictionary where keys are plot names and values are Altair Chart objects.
    
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

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': ['x', 'y', 'x', 'y']})
    >>> charts = plotify(df, plot_types=['histogram', 'bar'])
    >>> charts['histogram_A'].show()
    """
    import os
    
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    if save and not os.path.exists(save_path):
        os.makedirs(save_path)

    # Set default plot types if not specified
    if plot_types is None:
        plot_types = ['histogram', 'density', 'bar', 'scatter', 'correlation', 'box', 'stacked_bar']
    
    # Analyze columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    
    plots = {}

    # Individual column visualizations
    if 'histogram' in plot_types or 'density' in plot_types:
        for col in numeric_cols:
            if 'histogram' in plot_types:
                hist_chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X(col, bin=True, title=f"{col} (binned)"),
                    y=alt.Y('count()', title='Count')
                ).properties(title=f"Histogram of {col}")
                plots[f'histogram_{col}'] = hist_chart
                if save:
                    hist_chart.save(f"{save_path}/{file_prefix}_histogram_{col}.html")
            if 'density' in plot_types:
                density_chart = alt.Chart(df).transform_density(
                    col, as_=[col, 'density']
                ).mark_area(opacity=0.5).encode(
                    x=alt.X(col, title=col),
                    y=alt.Y('density:Q', title='Density')
                ).properties(title=f"Density Plot of {col}")
                plots[f'density_{col}'] = density_chart
                if save:
                    density_chart.save(f"{save_path}/{file_prefix}_density_{col}.html")
    
    if 'bar' in plot_types:
        for col in categorical_cols:
            bar_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(col, title=col),
                y=alt.Y('count()', title='Count')
            ).properties(title=f"Bar Chart of {col}")
            plots[f'bar_{col}'] = bar_chart
            if save:
                bar_chart.save(f"{save_path}/{file_prefix}_bar_{col}.html")
    
    if 'scatter' in plot_types:
        for col1, col2 in combinations(numeric_cols, 2):
            scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
                x=alt.X(col1, title=col1),
                y=alt.Y(col2, title=col2),
                tooltip=[col1, col2]
            ).properties(title=f"Scatter Plot: {col1} vs {col2}")
            plots[f'scatter_{col1}_{col2}'] = scatter_chart
            if save:
                scatter_chart.save(f"{save_path}/{file_prefix}_scatter_{col1}_{col2}.html")
    
    if 'correlation' in plot_types and len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr().stack().reset_index()
        corr_matrix.columns = ['Variable 1', 'Variable 2', 'Correlation']
        heatmap = alt.Chart(corr_matrix).mark_rect().encode(
            x=alt.X('Variable 1:N'),
            y=alt.Y('Variable 2:N'),
            color=alt.Color('Correlation:Q', scale=alt.Scale(scheme='viridis'))
        ).properties(title='Correlation Heatmap')
        plots['correlation_heatmap'] = heatmap
        if save:
            heatmap.save(f"{save_path}/{file_prefix}_correlation_heatmap.html")
    
    if 'box' in plot_types:
        for numeric_col in numeric_cols:
            for categorical_col in categorical_cols:
                box_plot = alt.Chart(df).mark_boxplot().encode(
                    x=alt.X(categorical_col, title=categorical_col),
                    y=alt.Y(numeric_col, title=numeric_col)
                ).properties(title=f"Box Plot of {numeric_col} by {categorical_col}")
                plots[f'box_{numeric_col}_{categorical_col}'] = box_plot
                if save:
                    box_plot.save(f"{save_path}/{file_prefix}_box_{numeric_col}_{categorical_col}.html")
    
    if 'stacked_bar' in plot_types:
        for col1, col2 in combinations(categorical_cols, 2):
            stacked_bar_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(col1, title=col1),
                y=alt.Y('count()', title='Count'),
                color=alt.Color(col2, title=col2)
            ).properties(title=f"Stacked Bar Chart of {col1} vs {col2}")
            plots[f'stacked_bar_{col1}_{col2}'] = stacked_bar_chart
            if save:
                stacked_bar_chart.save(f"{save_path}/{file_prefix}_stacked_bar_{col1}_{col2}.html")
    
    return plots