import argparse
import os
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split

ap = argparse.ArgumentParser()
ap.add_argument("--input_path", required=True)
ap.add_argument("--trainval_out", required=True)
ap.add_argument("--test_out", required=True)
ap.add_argument("--test_size", type=float, required=True)
ap.add_argument("--random_seed", type=int, required=True)
ap.add_argument("--stratify_by", type=str, default="")
a = ap.parse_args()

df = pd.read_csv(a.input_path)
stratify = df[a.stratify_by] if a.stratify_by and a.stratify_by in df.columns else None

trainval, test = train_test_split(df, test_size=a.test_size, random_state=a.random_seed, stratify=stratify)

os.makedirs(os.path.dirname(a.trainval_out), exist_ok=True)
trainval.to_csv(a.trainval_out, index=False)
test.to_csv(a.test_out, index=False)

mlflow.log_artifact(a.trainval_out)
mlflow.log_artifact(a.test_out)
print(f"trainval={len(trainval)}, test={len(test)}")
