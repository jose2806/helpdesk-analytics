from pathlib import Path

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]

# Directorios de datos
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"