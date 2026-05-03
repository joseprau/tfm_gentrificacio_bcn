import pandas as pd
from pathlib import Path
import json

def load_data(base_dir: Path=Path("..")):

    DATA_DIR = base_dir / "data" / "clustered"
    datasets = {
    "2015": pd.read_csv(DATA_DIR / "df_2015.csv"),
    "2023": pd.read_csv(DATA_DIR / "df_2023.csv"),
    "Deltes": pd.read_csv(DATA_DIR / "df_deltes.csv")
    }

    return datasets


def load_dim_barris(base_dir: Path=Path("..")):
    DATA_DIR = base_dir / "data" / "dimensions"
    return pd.read_csv( DATA_DIR / "BarcelonaCiutat_Barris.csv")


def load_labels_config(base_dir: Path=Path("..")):
    with open(base_dir / "clusters_config.json", "r") as f:
        return json.load(f)
    