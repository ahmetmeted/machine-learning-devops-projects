import argparse
import sys
import mlflow
import pandas as pd
import logging
from test_data import test_row_count, test_price_range, test_proper_boundaries

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

ap = argparse.ArgumentParser()
ap.add_argument("--csv_path", required=True, type=str, help="Input CSV file path")
ap.add_argument("--min_rows", type=int, required=True, help="Minimum number of rows")
ap.add_argument("--max_rows", type=int, required=True, help="Maximum number of rows")
ap.add_argument("--min_price", type=float, required=True, help="Minimum price")
ap.add_argument("--max_price", type=float, required=True, help="Maximum price")
args = ap.parse_args()

logger.info("Reading CSV file")
df = pd.read_csv(args.csv_path)

logger.info("Running data quality tests")
# Update test_row_count to use config parameters
def test_row_count_config(data, min_rows, max_rows):
    assert min_rows < data.shape[0] < max_rows, f"Dataset has {data.shape[0]} rows, which is not in the expected range ({min_rows}, {max_rows})"

test_row_count_config(df, args.min_rows, args.max_rows)
test_price_range(df, args.min_price, args.max_price)
test_proper_boundaries(df)

logger.info("Data checks passed")
