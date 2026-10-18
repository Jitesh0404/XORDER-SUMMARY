#!/usr/bin/env python3
import json
import sys
from pathlib import Path

source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("cypressResults.json")
output_path = Path("assesment_result.json")

status = "FAILURE"
passed = 0
total = 0

if source_path.exists():
    try:
        with source_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
        status_value = payload.get("status") or payload.get("TEST_STATUS") or payload.get("result") or ""
        passed = int(payload.get("passed", 0) or 0)
        total = int(payload.get("total", 0) or 0)
        if str(status_value).lower() in {"success", "passed", "ok", "true"}:
            status = "SUCCESS"
        elif str(status_value).upper() == "FAILURE":
            status = "FAILURE"
    except Exception:
        status = "FAILURE"

result = {
    "status": status,
    "TEST_STATUS": status,
    "TEST_STATUS_SUCCESS": status == "SUCCESS",
    "passed": passed,
    "total": total,
}

with output_path.open("w", encoding="utf-8") as fh:
    json.dump(result, fh, indent=2)
    fh.write("\n")

print(json.dumps(result))
