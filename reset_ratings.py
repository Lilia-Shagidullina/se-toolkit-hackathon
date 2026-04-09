import json
with open("jokes.json","r") as f:
    data = json.load(f)
for cat in data:
    for j in data[cat]:
        j["rating"] = 0
        j["votes"] = 0
with open("jokes.json","w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Reset done")
