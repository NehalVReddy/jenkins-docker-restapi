import json
import glob

files = glob.glob("last5_builds.json*")

total = success = failure = 0
durations = []

for file in files:
    with open(file) as f:
        data = json.load(f)
        for b in data["builds"]:
            total += 1
            durations.append(b["duration"])
            if b["result"] == "SUCCESS":
                success += 1
            else:
                failure += 1

success_rate = (success / total) * 100 if total > 0 else 0

print("Total builds:", total)
print("Success:", success)
print("Failures:", failure)
print("Success rate:", round(success_rate, 2), "%")
print("Average duration:", sum(durations) / len(durations))
