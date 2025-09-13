import argparse
import os
import mlflow
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

ap = argparse.ArgumentParser()
ap.add_argument("--input_path", required=True, type=str, help="Input CSV file path")
ap.add_argument("--output_path", required=True, type=str, help="Output CSV file path")
ap.add_argument("--min_price", type=float, required=True, help="Minimum price")
ap.add_argument("--max_price", type=float, required=True, help="Maximum price")
ap.add_argument("--apply_geofence", type=str, default="false", help="Apply geofence filter")
ap.add_argument("--lon_min", type=float, required=True, help="Longitude minimum")
ap.add_argument("--lon_max", type=float, required=True, help="Longitude maximum")
ap.add_argument("--lat_min", type=float, required=True, help="Latitude minimum")
ap.add_argument("--lat_max", type=float, required=True, help="Latitude maximum")
args = ap.parse_args()

logger.info("Reading input data")
df = pd.read_csv(args.input_path)

logger.info("Dropping outliers")
idx = df['price'].between(args.min_price, args.max_price)
df = df[idx].copy()

logger.info("Converting last_review to datetime")
if "last_review" in df.columns:
    df['last_review'] = pd.to_datetime(df['last_review'], errors="coerce")

if args.apply_geofence.lower() == "true":
    logger.info("Applying geofence filter")
    in_box = df["longitude"].between(args.lon_min, args.lon_max) & df["latitude"].between(args.lat_min, args.lat_max)
    df = df[in_box].copy()

logger.info("Saving cleaned data")
os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
df.to_csv(args.output_path, index=False)

logger.info("Logging artifact to MLflow")
mlflow.log_artifact(args.output_path)

logger.info(f"Cleaned -> {args.output_path}, rows={len(df)}")
