import json

# Load JSON data
with open("college_scraper/output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract text and URLs
documents = []
for entry in data:
    url = entry.get("url", "")
    text = entry.get("text", "").replace("\n", " ").strip()

    if text:  # Ensure non-empty text
        documents.append({"url": url, "text": text})

# Save cleaned data
with open("cleaned_data.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=4)
