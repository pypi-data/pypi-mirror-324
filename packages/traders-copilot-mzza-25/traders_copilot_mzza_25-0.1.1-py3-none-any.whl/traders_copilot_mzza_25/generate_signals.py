import pandas as pd

def generate_signals(data):
    """Generate buy/sell signals based on Simple Moving Averages (SMA) and Relative Strength Index (RSI).

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing 'SMA_50', 'SMA_200', and 'RSI' columns.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional 'Signal' column indicating 'BUY', 'SELL', or 'HOLD' signals.

    Examples
    --------
    >>> data = pd.DataFrame({
    >>>     'SMA_50': [100, 102, 104, 106, 108],
    >>>     'SMA_200': [98, 99, 100, 101, 102],
    >>>     'RSI': [25, 30, 35, 40, 45]
    >>> })
    >>> result = generate_signals(data)
    >>> print(result['Signal'])
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError('Data object is not a type of dataframe.')

    required_columns = ['SMA_50', 'SMA_200', 'RSI']
    if not all(column in data.columns for column in required_columns):
        raise ValueError(f"DataFrame must contain the following columns: {', '.join(required_columns)}")

    data['Signal'] = 'HOLD'
    data.loc[(data['SMA_50'] > data['SMA_200']) & (data['RSI'] < 30), 'Signal'] = 'BUY'
    data.loc[(data['SMA_50'] < data['SMA_200']) & (data['RSI'] > 70), 'Signal'] = 'SELL'

    return data
