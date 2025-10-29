# Stock Trades Downloader

This script downloads all trades for a specified ticker within a date range and saves them to a Parquet file.

## Features

- Downloads all trades for a ticker within a specified date range
- Handles API pagination automatically (50,000 records per request limit)
- Saves data in efficient Parquet format
- Progress tracking with per-day trade counts
- Error handling for API issues

## Requirements

- Python 3.10 or higher
- Valid Polygon.io API key
- Required packages: `polygon-api-client`, `pandas`, `pyarrow`

## Configuration

Edit the following variables in `stocks-trades.py`:

```python
TICKER = "IREN"           # Stock ticker symbol
START_DATE = "2025-01-01" # Start date (YYYY-MM-DD)
END_DATE = "2025-12-31"   # End date (YYYY-MM-DD)
```

## Usage

1. Set your Polygon.io API key as an environment variable:
   ```bash
   export POLYGON_API_KEY="your_api_key_here"
   ```

2. Run the script:
   ```bash
   cd examples/rest
   python stocks-trades.py
   ```

3. The script will:
   - Fetch trades for each day in the date range
   - Display progress for each day
   - Save all trades to a Parquet file named: `{TICKER}_trades_{START_DATE}_to_{END_DATE}.parquet`

## Output

The script generates a Parquet file containing the following fields for each trade:

- `conditions`: List of trade conditions
- `correction`: Trade correction indicator
- `exchange`: Exchange ID
- `id`: Trade ID
- `participant_timestamp`: Participant timestamp
- `price`: Trade price
- `sequence_number`: Sequence number
- `sip_timestamp`: SIP timestamp
- `size`: Trade size
- `tape`: Tape
- `trf_id`: TRF ID
- `trf_timestamp`: TRF timestamp

## Example Output

```
Downloading trades for IREN from 2025-01-01 to 2025-12-31...
This may take some time due to API rate limits and pagination...
Fetching trades for 2025-01-01... 1234 trades
Fetching trades for 2025-01-02... 2345 trades
...
Total trades downloaded: 123456
Saving to IREN_trades_2025-01-01_to_2025-12-31.parquet...
Successfully saved 123456 trades to IREN_trades_2025-01-01_to_2025-12-31.parquet
File size: 5.67 MB
```

## Notes

- The API has a limit of 50,000 records per request. The script handles pagination automatically.
- For large date ranges, the script may take significant time to complete.
- The script processes one day at a time to manage memory efficiently.
- Output files are excluded from git via `.gitignore`.

## Reading the Parquet File

You can read the generated Parquet file using pandas:

```python
import pandas as pd

# Read the parquet file
df = pd.read_parquet("IREN_trades_2025-01-01_to_2025-12-31.parquet")

# Display basic statistics
print(df.head())
print(f"Total trades: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
```
