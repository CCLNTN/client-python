from polygon import RESTClient
from polygon.rest.models import Trade
import pandas as pd  # type: ignore
from datetime import datetime, timedelta

# docs
# https://polygon.io/docs/stocks/get_v3_trades__stockticker
# https://polygon-api-client.readthedocs.io/en/latest/Trades.html#polygon.RESTClient.list_trades

# Trade data refers to the tick records of individual transactions that have
# taken place in a financial market, such as the price, size, and time of
# each trade. It provides a high-frequency, granular view of market activity,
# and is used by traders, investors, and researchers to gain insights into
# market behavior and inform their investment decisions.

# Configuration
TICKER = "IREN"
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"
OUTPUT_FILE = f"{TICKER}_trades_{START_DATE}_to_{END_DATE}.parquet"

# client = RESTClient("XXXXXX") # hardcoded api_key is used
client = RESTClient()  # POLYGON_API_KEY environment variable is used

print(f"Downloading trades for {TICKER} from {START_DATE} to {END_DATE}...")
print(f"This may take some time due to API rate limits and pagination...")

all_trades = []
trade_count = 0

# Generate date range to iterate through each day
start = datetime.strptime(START_DATE, "%Y-%m-%d")
end = datetime.strptime(END_DATE, "%Y-%m-%d")
current_date = start

while current_date <= end:
    date_str = current_date.strftime("%Y-%m-%d")
    print(f"Fetching trades for {date_str}...", end=" ")

    day_trades = 0
    try:
        # The API handles pagination automatically when we iterate
        # limit=50000 is the maximum allowed per request
        for t in client.list_trades(TICKER, date_str, limit=50000):
            # Verify this is a Trade object
            if isinstance(t, Trade):
                # Convert trade object to dictionary
                trade_dict = {
                    "conditions": t.conditions,
                    "correction": t.correction,
                    "exchange": t.exchange,
                    "id": t.id,
                    "participant_timestamp": t.participant_timestamp,
                    "price": t.price,
                    "sequence_number": t.sequence_number,
                    "sip_timestamp": t.sip_timestamp,
                    "size": t.size,
                    "tape": t.tape,
                    "trf_id": t.trf_id,
                    "trf_timestamp": t.trf_timestamp,
                }
                all_trades.append(trade_dict)
                day_trades += 1
                trade_count += 1

        print(f"{day_trades} trades")
    except Exception as e:
        print(f"Error: {e}")

    # Move to next day
    current_date += timedelta(days=1)

print(f"\nTotal trades downloaded: {trade_count}")

if trade_count > 0:
    # Convert to pandas DataFrame
    df = pd.DataFrame(all_trades)

    # Save to parquet file
    print(f"Saving to {OUTPUT_FILE}...")
    df.to_parquet(OUTPUT_FILE, index=False)
    print(f"Successfully saved {trade_count} trades to {OUTPUT_FILE}")
    print(
        f"File size: {pd.read_parquet(OUTPUT_FILE).memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
    )
else:
    print("No trades found for the specified period.")
