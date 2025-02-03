# traders_copilot_mzza_25

[![Documentation Status](https://readthedocs.org/projects/traders-copilot-mzza-25/badge/?version=latest)](https://traders-copilot-mzza-25.readthedocs.io/en/latest/?badge=latest)

This package is a streamlined application designed to assist in investment decision-making. It provides trading signals for stock markets by leveraging two key technical indicators: Simple Moving Average (SMA), which smooths price data to identify trends, and Relative Strength Index (RSI), which measures the speed and magnitude of price movements to determine overbought or oversold conditions.

## Contributors

Mingyang Zhang, Zanan Pech, Ziyuan Zhao and Abeba Nigussie Turi

## Installation

1.  Clone the Repository git clone <https://github.com/UBC-MDS/traders_copilot_mzza_25.git> cd traders_copilot_mzza_25

2.  Install the Package: \$ pip install traders_copilot_mzza_25

## Features

traders_copilot_mzza_25 package is a specialized tool for traders and investors fitting into a Python ecosystem of a similar vein. The package augments the existing trading and financial analysis packages like TA-Lib, Backtrader, and PyAlgoTrade by combining trading signal generation, strategy optimization, and built-in visualization tools into one place for a comprehensive trading workflow.

-   **simulate_market_data:** Simulates stock market data for analysis and testing.
-   **Technical Indicators:** Implements:
    -   Simple Moving Average (SMA): Smooths price data to identify trends.
    -   Relative Strength Index (RSI): Measures the speed and magnitude of price movements to assess overbought/oversold conditions.
-   **generate_signals:** Identifies buy/sell signals based on SMA and RSI thresholds:
    -   **Buy Signal:**
        -   SMA_50 \> SMA_200 (short-term trend is stronger)
        -   RSI \< 30 (stock is oversold)
    -   **Sell Signal:**
        -   SMA_50 \< SMA_200 (long-term trend is stronger)
        -   RSI \> 70 (stock is overbought)
-   **plot_signals:** Visualizes stock data with buy/sell signals marked on the chart.

## Usage

`traders_copilot_mzza_25` can be used to simulate market data, generate trading signals, and visualize results. Here are examples of usage:

### Simulate Market Data

``` python
from traders_copilot_mzza_25 import simulate_market_data

data = generate_synthetic_data("2021-01-01", "2021-12-31", num_records=252, seed=40)
print(data.head())
```

### Calculate Indicators

``` python
from traders_copilot_mzza_25 import calculate_sma, calculate_rsi

data = pd.DataFrame({'Close': [100, 102, 104, 106, 108]})
result = calculate_sma(data, window=3)
print(result['SMA_3'])

data = pd.DataFrame({'Close': [100, 102, 104, 106, 108]})
result = calculate_rsi(data, window=3)
print(result['RSI'])
```

### Generate Trading Signals

``` python
from traders_copilot_mzza_25 import generate_signals

data = pd.DataFrame({
'SMA_50': [100, 102, 104, 106, 108],
'SMA_200': [98, 99, 100, 101, 102],
'RSI': [25, 30, 35, 40, 45]
})
result = generate_signals(data)
print(result['Signal'])
```

### Visualize Signals

``` python
from traders_copilot_mzza_25 import plot_signals

data = pd.DataFrame({"Date": ["2023-01-01", "2023-01-02", "2023-01-03"], 
                     "Close": [100, 102, 104]})
fig = plot_signals(data)
fig.show()
```

## Python Ecosystem

The traders_copilot_mzza_25 package positions itself within the Python ecosystem as a practical and user-friendly tool tailored to traders and investors seeking to make informed decisions in the stock market. While the ecosystem already includes powerful libraries like TA-Lib, Backtrader, and PyAlgoTrade, this package stands out by combining trading signal generation, strategy optimization, and visualization into an integrated workflow. With intuitive function names such as simulate_market_data, generate_signals, and plot_signals, it simplifies the process of applying technical indicators like SMA and RSI for both novice and experienced traders. This package is not only a comprehensive resource for trading strategies but also a hands-on tool for Python enthusiasts eager to deepen their skills in financial analysis and programming, making it a versatile addition to the Python finance ecosystem.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`traders_copilot_mzza_25` was created by Mingyang Zhang, Zanan Pech, Ziyuan Zhao and Abeba Nigussie Turi. It is licensed under the terms of the MIT license.

## Credits

`traders_copilot_mzza_25` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
