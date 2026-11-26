from pathlib import Path
import argparse, sys, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline import prepare
parser = argparse.ArgumentParser(description="Clean synthetic encounter records and derive 30-day inpatient readmissions.")
parser.add_argument("--input", default="data/sample", help="Folder containing patients.csv, organizations.csv and encounters.csv")
args = parser.parse_args()
source = Path(args.input)
if not source.is_absolute(): source = ROOT / source
result = prepare(source, ROOT / "data" / "clean")
(ROOT / "data" / "clean" / "pipeline_metadata.json").write_text(json.dumps({
    "dataset_mode": "project_generated_synthetic_preview",
    "source_folder": str(source),
    **result
}, indent=2), encoding="utf-8")
print("Pipeline complete:", json.dumps(result, indent=2))
