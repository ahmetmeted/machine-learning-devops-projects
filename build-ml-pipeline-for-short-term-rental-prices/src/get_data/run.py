import argparse
import os
import shutil
import mlflow

p = argparse.ArgumentParser()
p.add_argument("--input_filename", required=True)
p.add_argument("--output_path", required=True)
args = p.parse_args()

os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
shutil.copyfile(args.input_filename, args.output_path)
mlflow.log_artifact(args.output_path)
print(f"Saved to {args.output_path}")
