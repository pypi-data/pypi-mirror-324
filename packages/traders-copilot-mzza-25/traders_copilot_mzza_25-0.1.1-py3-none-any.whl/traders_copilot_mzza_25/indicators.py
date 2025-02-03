import pandas as pd
import numpy as np

#SMA
def calculate_sma(data, window=50, fillna=False):
    """Calculate the Simple Moving Average (SMA) for the given data.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing stock price data with a 'Close' column.
    window : int, optional
        The number of periods to calculate the SMA (default is 50).
    fillna : bool, optional
        Whether to fill NaN values (default is False).

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional column for the SMA.

    Examples
    --------
    >>> data = pd.DataFrame({'Close': [100, 102, 104, 106, 108]})
    >>> result = calculate_sma(data, window=3)
    >>> print(result['SMA_3'])
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The input data must be a pandas DataFrame.")
    
    if 'Close' not in data.columns:
        raise ValueError("The input DataFrame must contain a 'Close' column.")
    
    if data.empty:
        return data
    
    data[f'SMA_{window}'] = data['Close'].rolling(window=window).mean()
    
    if fillna:
        data[f'SMA_{window}'] = data[f'SMA_{window}'].bfill()  
    
    return data


#RSI 
def calculate_rsi(data, window=14, fillna=False):
    """Calculate the Relative Strength Index (RSI) measuring the speed and change of price movements.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing stock price data with a 'Close' column.
    window : int, optional
        Number of periods for RSI calculation (default is 14).
    fillna : bool, optional
        Whether to fill NaN values (default is False).

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional column for RSI.
    
    Examples
    --------
    >>> data = pd.DataFrame({'Close': [100, 102, 104, 106, 108]})
    >>> result = calculate_rsi(data, window=3)
    >>> print(result['RSI'])
    """
        
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The input data must be a pandas DataFrame.")
    
    if 'Close' not in data.columns:
        raise ValueError("The input DataFrame must contain a 'Close' column.")
    
    # Handle empty data
    if data.empty:
        return data
    
    delta = data['Close'].diff()
    
    # Separate gains and losses
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    
    data['RSI'] = 100 - (100 / (1 + rs))
    
    if fillna:
        data['RSI'] = data['RSI'].bfill()  
    
    return data
