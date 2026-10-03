"""Load card and merchant CSVs into Azure SQL Database."""
from .load_to_sqlserver import load as _load

def load(output_dir="data/generated"):
    import os
    return _load(output_dir, os.environ["AZURESQL_CONNECTION_STRING"])

if __name__ == "__main__": load()
