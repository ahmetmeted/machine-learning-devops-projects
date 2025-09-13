import argparse
import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

ap = argparse.ArgumentParser()
ap.add_argument("--input_artifact", required=True, type=str, help="Input artifact name")
args = ap.parse_args()

logger.info("Starting EDA notebook server")
logger.info("Please open your browser and go to http://localhost:8888")
logger.info("Use the notebook to explore the data and create visualizations")

# Start Jupyter notebook
os.system("jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''")
