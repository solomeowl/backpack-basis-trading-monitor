# Backpack Basis Trading Monitor

This project is a Python-based trading monitor that tracks arbitrage opportunities in the cryptocurrency market. It calculates funding rate statistics and monitors potential basis trading opportunities for all available cryptocurrency pairs on Backpack Exchange.

## Features

- Calculates funding rate statistics including:
  - Current rate
  - Last 24-hour average
  - Last 7-day average
  - Minimum and maximum rates over 7 days
  - Percentage of positive rates
- Monitors arbitrage opportunities by comparing spot and perpetual futures prices
- Highlights good trading opportunities based on annualized returns and positive funding rate percentages
- Real-time monitoring of all available trading pairs
- Color-coded output for easy opportunity identification:
  - 🟢 Green: 7-day average APR > 10% AND positive funding rate > 75%
  - 🟡 Yellow: 24h average APR > 10%

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/solomeowl/backpack-basis-trading-monitor.git
   cd backpack-basis-trading-monitor
   ```

2. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Run the monitor:
   ```bash
   python main.py
   ```

## Requirements

- Python 3.7 or higher
- Internet connection for accessing the Backpack Exchange API
- Required packages:
  - backpack-exchange-sdk
  - pandas
  - numpy

## Configuration

- The script automatically monitors all available cryptocurrency pairs on Backpack Exchange
- The minimum annual return threshold for highlighting opportunities can be adjusted by changing the `min_annual_return` parameter (default: 10%)
- Update frequency is set to 10 seconds by default

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational purposes only. Trading cryptocurrencies involves significant risk and may not be suitable for all investors. Please conduct your own research and consult with a financial advisor before making any trading decisions.

## Support 

If this SDK has been helpful to you 🌟 and you haven't signed up for Backpack Exchange yet, please consider using the following referral link to register: [Register on Backpack Exchange](https://backpack.exchange/refer/solomeowl) 🚀.

Using this referral link is a great way to support this project ❤️, as it helps to grow the community and ensures the continued development of the SDK. 🛠️
