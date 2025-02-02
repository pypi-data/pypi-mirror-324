# NSE Greeks Calculator

A powerful Python package for real-time calculation of option Greeks for NSE (National Stock Exchange) derivatives. This calculator provides accurate and real-time calculations of Delta, Gamma, Theta, Vega, and Rho for options trading on the National Stock Exchange of India.

## Features
- Real-time Greeks calculation (Delta, Gamma, Theta, Vega, Rho)
- Support for both Call (CE) and Put (PE) options
- Live market data integration with NSE
- Automatic implied volatility calculation
- Real-time monitoring with customizable intervals
- Built-in error handling and debugging information
- Simple and intuitive API

## Installation
```bash
pip install nse-greeks-calculator
```

## Requirements
- Python >=3.7
- nsepython
- pandas
- numpy
- scipy

## Quick Start
```python
from nse_greeks_calculator import NSEGreeksCalculator

# Initialize the calculator with symbol
calculator = NSEGreeksCalculator('NIFTY')

# Monitor Greeks in real-time
calculator.monitor_greeks(
    strike_price=23500,
    expiry_date='27-Mar-2025',
    option_type='CE',  # 'CE' for Call Option, 'PE' for Put Option
    interval=5  # Update interval in seconds
)
```

## Features in Detail

### Greeks Calculation
The calculator provides the following Greeks:
- Delta: Measures the rate of change of option price with respect to the underlying
- Gamma: Measures the rate of change of Delta
- Theta: Measures the rate of change of option value with respect to time
- Vega: Measures sensitivity to volatility
- Rho: Measures sensitivity to interest rate changes

### Real-time Monitoring
The `monitor_greeks()` function provides continuous updates with:
- Current spot price
- Option price
- Implied Volatility (IV)
- All Greeks values
- Timestamp for each update

## Error Handling
The package includes comprehensive error handling for:
- Network connectivity issues
- Invalid market data
- Calculation errors
- Invalid parameters

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Author
Lekshmi

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.