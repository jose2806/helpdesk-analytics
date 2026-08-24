from pathlib import Path
import pandas as pd

def load_csv(file_name:str,data_dir:Path) -> pd.DataFrame:
  """
    Load a CSV file from the raw data directory.
  """
  file_path = data_dir / file_name

  if not file_path.exists():
    raise FileNotFoundError( f"Data file not found: {file_path}")

  return pd.read_csv(file_path)