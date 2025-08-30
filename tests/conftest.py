# tests/conftest.py
import sys
from pathlib import Path
import pandas as pd
import warnings

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def pytest_sessionstart(session):
    out_dir = ROOT / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "output.csv"

    if not csv_path.exists():
        dates = pd.date_range("2021-01-10", "2021-01-20", freq="D")
        df = pd.DataFrame({
            "date": dates,
            "sales": [100, 120, 115, 130, 125, 200, 210, 205, 215, 220, 225],
            "region": (["north", "south", "east", "west", "north"] * 3)[:len(dates)],
        })
        df.to_csv(csv_path, index=False)

warnings.filterwarnings("ignore", category=DeprecationWarning, module="selenium")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="urllib3")
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
