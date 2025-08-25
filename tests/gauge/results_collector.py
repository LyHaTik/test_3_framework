# tests/gauge/results_collector.py
import csv
import os

results = []

def record_result(app, step_name, duration, status):
    results.append({
        "App": app,
        "Step": step_name,
        "Duration_ms": round(duration * 1000, 2),
        "Status": status
    })

def save_results(filename="results.csv"):
    if not results:
        return

    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["App", "Step", "Duration_ms", "Status"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(results)
    results.clear()