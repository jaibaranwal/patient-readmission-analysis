from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.analysis import analyse
kpis = analyse()
print("KPI report:", ROOT / "reports" / "kpis.json")
for key, value in kpis.items():
    print(f"{key}: {value}")
