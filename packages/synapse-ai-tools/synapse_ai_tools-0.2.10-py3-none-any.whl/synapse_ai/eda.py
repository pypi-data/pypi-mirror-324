import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os




def nulls(data:pd.DataFrame, column:str) -> None:
    """
    Analyzes and prints the number and percentage of null values in a specified column of a DataFrame.

    This function calculates the total count and percentage of missing (null) values in a given column 
    of a Pandas DataFrame. The results are displayed in a formatted string.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data to analyze.
        column (str): The name of the column to check for null values.

    Returns:
        None: The function directly prints the analysis results.

    Features:
        - Calculates the total number of null values in the specified column using `isnull()`.
        - Computes the percentage of null values relative to the total number of rows in the DataFrame.
        - Displays the results in a clear, formatted string with column name, null count, and percentage.

    Example:
        Analyzing a single column:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A': [1, None, 3, 4], 'B': [None, None, 3, 4]})
        >>> nulls(df, 'A')
        Column: A                              Amount of nulls: 1            Percentage of nulls: 25.00 %
        
        Analyzing multiple columns:
        >>> for column in df.columns:
        ...     nulls(df, column)
        Column: A                              Amount of nulls: 1            Percentage of nulls: 25.00 %
        Column: B                              Amount of nulls: 2            Percentage of nulls: 50.00 %

    Notes:
        - If the column name provided does not exist in the DataFrame, the function will raise a KeyError.
        - The function assumes the input data is a valid Pandas DataFrame.

    Limitations:
        - The function does not handle cases where the DataFrame is empty. Ensure the DataFrame has data before use.
        - Works on one column at a time. For analyzing multiple columns, use a loop as shown in the example.

    Customizations:
        - To handle missing values programmatically instead of printing results, return the calculated null count and percentage.
    """

    nulls_ = data[column].isnull().sum()
    percentage = round(nulls_/len(data)*100, 2)
    print(f'Column: {column:30}   Amount of nulls: {nulls_:<10}   Percentage of nulls: {percentage:.2f} %')



def outliers(data:pd.DataFrame, column:str, color:str='violet', fig_size:tuple[int, int]=(15,4)) -> None:
    """
    Analyzes numerical outliers in a specified column of a DataFrame, visualizing its distribution, 
    boxplot, and basic statistics.

    This function provides a graphical and statistical analysis of a numerical column, including 
    histograms, boxplots, and key statistical metrics (quartiles, mean, median, mode, and IQR). 
    It is intended to identify potential outliers and assess the distribution of data.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data to analyze.
        column (str): The name of the column to analyze. Must contain numerical data.
        color (str): The color for the histogram and boxplot. Defaults to 'violet'.
        fig_size (tuple[int, int]): The size of the figure for the visualizations. Defaults to (15, 4).

    Returns:
        None: The function generates plots and prints statistical metrics directly.

    Features:
        - Converts the column to numeric, coercing non-numeric values to NaN.
        - Creates three subplots:
            1. A histogram with a KDE overlay for visualizing the distribution.
            2. A boxplot for identifying outliers.
            3. A textual summary of key statistics (Q1, Q2, Q3, Q4, mean, median, mode, and IQR).
        - Handles missing values by dropping NaN values before calculations.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A': [1, 2, 2, 3, 100]})
        >>> outliers(df, column='A')
        
        For multiple columns:
        >>> for column in df.select_dtypes(include=['number']).columns:
        ...     outliers(df, column)

    Notes:
        - The specified column must contain numeric data. Non-numeric columns will be coerced to NaN.
        - If the column is empty or contains only NaN values after coercion, the function does not 
          generate statistics or visualizations for that column.
        - The `color` parameter accepts any valid Matplotlib or Seaborn color specification.
        - The third subplot includes textual statistics aligned within the plot area.

    Limitations:
        - Designed for numerical columns only. Non-numerical columns will not produce meaningful results.
        - When using in a script or notebook with many visualizations, consider adding `plt.close(fig)` 
          after `plt.show()` to avoid excessive memory usage.

    Customizations:
        - Customize `color` to match the desired color palette for your project.
        - Adjust `fig_size` to better fit your screen or reporting requirements.

    Improvements:
        - Add `plt.close(fig)` at the end of the function to avoid memory leaks in scenarios with frequent plotting.
    """

    data[column] = pd.to_numeric(data[column], errors='coerce')
    fig, axes = plt.subplots(1, 3, figsize=fig_size) 
    fig.suptitle(f'Analysis for column {column}')
    sns.histplot(data=data, x=column, kde=True, ax=axes[0], color=color)
    axes[0].set_title('Distribution')
    sns.boxplot(data=data, y=column, ax=axes[1], color=color)
    axes[1].set_title('Boxplot')
    data = data[column].dropna()  
    if not data.empty:
        q1 = np.percentile(data, 25)
        q2 = np.percentile(data, 50)  
        q3 = np.percentile(data, 75)
        q4 = np.percentile(data, 100) 
        mean = np.mean(data)
        median = np.median(data)
        mode = data.mode()[0] if not data.mode().empty else "No mode"
        iqr = q3 - q1
        axes[2].text(0.1, 0.9, f'Q1: {q1:.2f}', transform=axes[2].transAxes)
        axes[2].text(0.1, 0.8, f'Q2: {q2:.2f}', transform=axes[2].transAxes)
        axes[2].text(0.1, 0.7, f'Q3: {q3:.2f}', transform=axes[2].transAxes)
        axes[2].text(0.1, 0.6, f'Q4: {q4:.2f}', transform=axes[2].transAxes) 
        axes[2].text(0.1, 0.5, f'Mean: {mean:.2f}', transform=axes[2].transAxes)
        axes[2].text(0.1, 0.4, f'Median: {median:.2f}', transform=axes[2].transAxes)
        axes[2].text(0.1, 0.3, f'Mode: {mode:.2f}', transform=axes[2].transAxes)
        axes[2].text(0.1, 0.2, f'IQR: {iqr:.2f}', transform=axes[2].transAxes)
        axes[2].set_title('Descriptive Statistics')
        axes[2].axis('off')  
    plt.tight_layout()
    plt.show()
    plt.close(fig)



def heatmap_correlation(data:pd.DataFrame, columns:list, title:str='', output_dir:str='', name:str='Heatmap', correlation_type:str='spearman', fig_size:tuple[int, int]=(12,10), cmap:str='coolwarm', linewidths:float=0.5, fontsize:int=10, fontsize_title:int=14, show:bool=True, save:bool=False) -> None:
    """
    Generates and optionally saves a heatmap of correlation values for selected columns in a DataFrame.

    This function computes the correlation matrix for the specified columns using the chosen 
    correlation method ('pearson' or 'spearman') and visualizes it as a heatmap. The plot 
    can be saved to a specified directory or displayed interactively. 

    **Note**: The specified columns must contain numeric data. Non-numeric columns should be excluded 
    from the correlation analysis beforehand.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data to analyze.
        columns (list): A list of column names (must be numeric) to include in the correlation analysis.
        title (str): The title of the heatmap.
        output_dir (str): The directory where the heatmap image will be saved, if `save` is True. 
            Defaults to an empty string (current working directory).
        name (str): The name of the saved image file (without extension). Defaults to 'Heatmap'.
        correlation_type (str): The type of correlation to compute ('pearson' or 'spearman'). 
            Defaults to 'spearman'.
        fig_size (tuple[int, int]): The size of the figure. Defaults to (12, 10).
        cmap (str): The colormap for the heatmap. Defaults to 'coolwarm'.
        linewidths (float): The width of the lines separating cells in the heatmap. Defaults to 0.5.
        fontsize (int): The font size for tick labels. Defaults to 10.
        fontsize_title (int): The font size for the title. Defaults to 14.
        show (bool): Whether to display the heatmap interactively. Defaults to True.
        save (bool): Whether to save the heatmap as an image file. Defaults to False.

    Returns:
        None: The function either displays the heatmap interactively or saves it as an image file.

    Raises:
        ValueError: If `correlation_type` is not 'pearson' or 'spearman', or if any of the 
            specified columns are not present in the DataFrame.

    Example:
        >>> import pandas as pd
        >>> import numpy as np
        >>> df = pd.DataFrame(np.random.rand(100, 4), columns=['A', 'B', 'C', 'D'])
        >>> heatmap_correlation(
        ...     data=df, 
        ...     columns=['A', 'B', 'C', 'D'], 
        ...     title='Correlation Heatmap', 
        ...     output_dir='./plots', 
        ...     name='heatmap_example', 
        ...     correlation_type='pearson', 
        ...     show=True, 
        ...     save=True
        ... )
    """

    df = data[columns]
    if correlation_type == 'pearson':
        correlacion = df.corr(method='pearson')
    elif correlation_type == 'spearman':
        correlacion = df.corr(method='spearman')
    else:
        raise ValueError("The correlation type must be 'pearson' or 'spearman'.")
    plt.figure(figsize=fig_size)
    sns.heatmap(correlacion, annot=True, cmap=cmap, linewidths=linewidths, annot_kws={"size": 10}, 
                cbar_kws={"shrink": .8}, fmt=".2f", center=0)
    plt.xticks(fontsize=fontsize, rotation=45, ha='right')
    plt.yticks(fontsize=fontsize, rotation=0)
    plt.title(title, fontsize=fontsize_title)
    plt.tight_layout()
    if save:
        output_path = os.path.join(output_dir, f'{name}.png')
        plt.savefig(output_path)
    if show:
        plt.show() 
    if save or show:
        plt.close()


