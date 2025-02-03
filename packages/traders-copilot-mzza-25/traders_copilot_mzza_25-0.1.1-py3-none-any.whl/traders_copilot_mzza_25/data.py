import pandas as pd
import numpy as np
from datetime import datetime

def generate_synthetic_data(start_date, end_date, num_records=252, seed=40):
    """Generate synthetic stock data.

    Parameters
    ----------
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        num_records (int): Number of records to generate 
        (default is 252 trading days in a year in major stock markets).
        seed (int): Random seed for reproducibility.

    Returns
    -------
        pd.DataFrame: A DataFrame containing the generated stock data with 'Date', 'Open', 'High', 'Low', 
        'Close', 'Adj Close', and 'Volume' columns.
   
    Example 
if __name__ == "__main__":
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    num_records = 252
    
    Generate the data
    synthetic_data = generate_synthetic_data(start_date, end_date, num_records)
    print("Synthetic Stock Data:")
    print(synthetic_data.head())
        
    """
    
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
    
    if num_records <= 0:
        raise ValueError("num_records must be greater than 0")
    
    if start_date > end_date:
        raise ValueError("start_date must be before end_date")

    np.random.seed(seed)
    
    dates = pd.date_range(start=start_date, end=end_date, periods=num_records)
    
    prices = np.cumsum(np.random.normal(0, 1, num_records)) + 100  
    
    high = prices + np.random.uniform(0.5, 2.0, num_records)
    low = prices - np.random.uniform(0.5, 2.0, num_records)
    open_price = prices + np.random.uniform(-1.0, 1.0, num_records)
    adj_close = prices * (1 + np.random.uniform(-0.01, 0.01, num_records))
    volume = np.random.randint(1_000_000, 5_000_000, num_records)
    
    stock_data = pd.DataFrame({
        "Date": dates,
        "Open": open_price,
        "High": high,
        "Low": low,
        "Close": prices,
        "Adj Close": adj_close,
        "Volume": volume
    })
    
    stock_data.set_index("Date", inplace=True)
    
    return stock_data

