#!/usr/bin/env python3
import os
import ccxt
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ----------------------
# 1. Configuration
# ----------------------
API_KEY = os.getenv("KRAKEN_API_KEY")
API_SECRET = os.getenv("KRAKEN_API_SECRET")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

# ----------------------
# 2. Main logic
# ----------------------
def main():
    # (A) Connect to Kraken via ccxt
    kraken = ccxt.kraken({
        'apiKey': API_KEY,
        'secret': API_SECRET
    })

    # (B) Fetch Account Balances
    balance_info = kraken.fetch_balance()
    
    btc_balance = balance_info.get('BTC', {}).get('total', 0)
    usd_balance = balance_info.get('USD', {}).get('total', 0)
    
    # Calculate a rough total of all assets in the account
    total_balance_sum = 0
    for currency, data in balance_info.items():
        if isinstance(data, dict) and 'total' in data:
            total_balance_sum += data['total']
    # Optional: Convert to USD if needed

    # (C) Fetch trades for the last 7 days
    seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    since_ms = int(seven_days_ago.timestamp() * 1000)
    
    trades = kraken.fetch_my_trades(symbol=None, since=since_ms)
    
    # (D) Analyze trades for summary
    trade_count = len(trades)
    trade_table_rows = []
    for t in trades:
        symbol = t.get('symbol', 'N/A')
        amount = t.get('amount', 0)
        fee_cost = t.get('fee', {}).get('cost', 0)
        cost = t.get('cost', 0)

        purchase_price = cost / amount if amount else 0
        fee_percent = (fee_cost / cost * 100) if cost else 0
        
        trade_table_rows.append([
            str(t.get('datetime', 'N/A')),
            str(symbol),
            str(t.get('price', 'N/A')),
            str(amount),
            str(cost),          
            str(round(fee_cost, 4)),
            str(round(fee_percent, 2)) + "%"
        ])

    # (E) Format the email body
    trades_html_table = """
    <table border="1" cellpadding="5" cellspacing="0">
      <tr>
        <th>Date</th>
        <th>Security Purchased</th>
        <th>Price</th>
        <th>Amount</th>
        <th>Cost (USD)</th>
        <th>Fees (USD)</th>
        <th>Fees %</th>
      </tr>
    """
    for row in trade_table_rows:
        trades_html_table += "<tr>"
        trades_html_table += "".join([f"<td>{col}</td>" for col in row])
        trades_html_table += "</tr>"
    trades_html_table += "</table>"

    html_body = f"""
    <h2>Kraken Account Activity (Last 7 Days)</h2>
    <p><strong>Date (UTC):</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <p><strong>Current BTC Balance:</strong> {btc_balance}</p>
    <p><strong>Current USD Balance:</strong> {usd_balance}</p>
    <p><strong>Total Account Balance (raw sum of all currencies):</strong> {total_balance_sum}</p>
    <p><strong>Number of Trades in Last 7 Days:</strong> {trade_count}</p>
    <hr/>
    <h3>Trade Details:</h3>
    {trades_html_table}
    """

    # (F) Construct and send the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Weekly Kraken Report"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    
    # Attach the HTML part
    part = MIMEText(html_body, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1)  # Enable debug output
            server.starttls()          # Upgrade the connection to TLS
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# ----------------------
# 3. Entry point
# ----------------------
if __name__ == "__main__":
    main()