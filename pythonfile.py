import json
import os

file = "last5_builds.json3"

if not os.path.exists(file):
    raise Exception("JSON file not found")

if os.path.getsize(file) == 0:
    raise Exception("JSON file is empty – Jenkins API fetch failed")

with open(file, "r") as f:
    data = json.load(f)

builds = data.get("builds", [])

total = len(builds)
success = sum(1 for b in builds if b["result"] == "SUCCESS")
avg_duration = sum(b["duration"] for b in builds) / total if total else 0

summary = {
    "total_builds": total,
    "success_count": success,
    "failure_count": total - success,
    "success_rate": round((success / total) * 100, 2),
    "average_duration_ms": round(avg_duration, 2)
}

with open("build_analytics_summary.json", "w") as f:
    json.dump(summary, f, indent=4)

print("✔ Build analytics generated successfully")
print(summary)
