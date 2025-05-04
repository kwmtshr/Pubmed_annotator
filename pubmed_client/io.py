import pandas as pd
from pathlib import Path

def read_input(path):
    return pd.read_csv(path, dtype=str).fillna("")

def write_output(df, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
