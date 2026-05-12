import sys
import os
sys.path.append(os.getcwd())

from src.quality.validation import validate_anonymized_data

print("Validating anonymized data function...")
try:
    results = validate_anonymized_data("data/raw/patients_raw.csv")
    print("Validation Results:", results)
    if results["success"]:
        print("OK: Quality tests passed")
    else:
        print("FAIL: Quality tests failed:", results["failed_checks"])

except Exception as e:
    print(f"Error during quality validation: {e}")
