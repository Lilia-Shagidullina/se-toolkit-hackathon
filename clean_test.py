import json

# Clean jokes.json
with open("jokes.json","r") as f:
    data = json.load(f)
for cat in data:
    data[cat] = [j for j in data[cat] if j.get("text") not in ["Test joke","New test joke","Test"]]
with open("jokes.json","w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Clean pending_jokes.json
with open("pending_jokes.json","r") as f:
    pending = json.load(f)
pending = [j for j in pending if j.get("text") not in ["Test joke","New test joke","Test"]]
with open("pending_jokes.json","w") as f:
    json.dump(pending, f, ensure_ascii=False, indent=2)

print("Cleaned")
