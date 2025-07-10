=======
# Kraken Trading Scripts

This directory contains two Python scripts for interacting with the Kraken cryptocurrency exchange.

## Files

### `daily_trade.py`
A simple script that places a daily market buy order for Bitcoin on Kraken.

**Features:**
- Places a market buy order for 0.00012 BTC
- Uses environment variables for API credentials
- Provides error handling and status messages

**Usage:**
```bash
python3 daily_trade.py
```

### `automail.py`
An automated reporting script that fetches account activity and sends a weekly email summary.

**Features:**
- Fetches current account balances (BTC, USD, and total)
- Retrieves trade history for the last 7 days
- Generates an HTML email report with trade details
- Sends email via SMTP

**Usage:**
```bash
python3 automail.py
```

## Requirements

Install the required dependencies:
```bash
pip install ccxt
```

## Environment Variables

Before running these scripts, you need to set up the following environment variables:

### For Trading (daily_trade.py):
```bash
export KRAKEN_TRADE_API_KEY="your_kraken_api_key"
export KRAKEN_TRADE_API_SECRET="your_kraken_api_secret"
```

### For Reporting (automail.py):
```bash
export KRAKEN_API_KEY="your_kraken_api_key"
export KRAKEN_API_SECRET="your_kraken_api_secret"
export SMTP_SERVER="your_smtp_server"
export SMTP_PORT="587"
export SMTP_USERNAME="your_email_username"
export SMTP_PASSWORD="your_email_password"
export EMAIL_FROM="sender@example.com"
export EMAIL_TO="recipient@example.com"
```

## Security Notes

- **Never commit API keys to version control**
- Use environment variables or a secure secrets management system
- Consider using separate API keys for trading and read-only operations
- The trading script has real money implications - test thoroughly before use

## Kraken API Setup

1. Log into your Kraken account
2. Go to Settings → API
3. Create a new API key with appropriate permissions:
   - For `daily_trade.py`: Trading permissions
   - For `automail.py`: Query funds, Query open/closed orders and trades

## Automation

To run these scripts automatically:

### Daily Trading (Cron Example):
```bash
# Run daily at 9 AM
0 9 * * * /usr/bin/python3 /path/to/daily_trade.py
```

### Weekly Reports (Cron Example):
```bash
# Run weekly on Sundays at 8 AM
0 8 * * 0 /usr/bin/python3 /path/to/automail.py
```

## Disclaimer

These scripts are for educational purposes. Cryptocurrency trading involves risk. Always test with small amounts and understand the code before using with real funds. 
>>>>>>> bafccd9 (made changes to readme.md)
