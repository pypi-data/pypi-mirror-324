from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

def validate_columns(data, price_col, time_col):
    """Ensure the DataFrame contains the specified price and time columns."""
    if price_col not in data.columns or time_col not in data.columns:
        raise ValueError(f"The DataFrame must contain '{price_col}' and '{time_col}' columns.")

def validate_lengths(data, price_col, time_col):
    """Ensure the lengths of the price and time columns match."""
    # Count non-missing values in each column
    price_len = data[price_col].notna().sum()
    time_len = data[time_col].notna().sum()
    print(f"Debug: Non-missing Length of {price_col} = {price_len}, Non-missing Length of {time_col} = {time_len}")
    if price_len != time_len:
        raise ValueError("The lengths of 'price' and 'time' columns must match.")

def validate_non_empty(data, price_col, time_col):
    """Ensure both price and time columns are non-empty."""
    if data[price_col].empty or data[time_col].empty:
        raise ValueError("Both 'price' and 'time' columns must be non-empty.")

def validate_dates(data, time_col):
    """Validate that each date in the time column is in the 'YYYY-MM-DD' format."""
    for date in data[time_col]:
        try:
            datetime.strptime(str(date), "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Ensure all dates in '{time_col}' are in 'YYYY-MM-DD' format.")

def generate_plot(price, time):
    """Generate a Matplotlib figure for the price vs. time data."""
    fig, ax = plt.subplots()
    ax.plot(time, price, marker='o')
    ax.set_title("Price vs. Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    plt.xticks(rotation=45)
    return fig

def plot_signals(data, price_col="Close", time_col="Date"):
    """Plot a time series depicting the price at specific timestamps from a DataFrame.
    
    Parameters
    ----------
    data : pandas.DataFrame
        The input DataFrame containing price and time data.
    price_col : str, optional
        The column name for price data (default is "Close").
    time_col : str, optional
        The column name for time data (default is "Date").
    
    Returns
    -------
    matplotlib.figure.Figure
        The Matplotlib figure object containing the time series plot.
    
    Raises
    ------
    ValueError
        If the DataFrame does not contain the specified columns.
        If the lengths of the columns do not match.
        If the columns are empty.
        If any date in the time column is not in the 'YYYY-MM-DD' format.
    
    Examples
    --------
    >>> data = pd.DataFrame({"Date": ["2023-01-01", "2023-01-02", "2023-01-03"], 
    >>>                      "Close": [100, 102, 104]})
    >>> fig = plot_signals(data)
    >>> fig.show()
    """
    validate_columns(data, price_col, time_col)
    validate_lengths(data, price_col, time_col)
    validate_non_empty(data, price_col, time_col)
    validate_dates(data, time_col)
    
    return generate_plot(data[price_col], data[time_col])
