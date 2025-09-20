import os
import fal_client

# Set API key as environment variable
os.environ["FAL_KEY"] = "3845a313-cfc9-469b-ac5d-fe354d7106dd:42f4fb3cddc5156df1b724115431bb85"

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
           print(log["message"])

prompt = "Change bag to apple macbook"
image_url = "https://v3.fal.media/files/koala/oei_-iPIYFnhdB8SxojND_qwen-edit-res.png"

result = fal_client.subscribe(
    "fal-ai/qwen-image-edit",
    arguments={
        "prompt": prompt,
        "image_url": image_url
    },
    with_logs=True,
    on_queue_update=on_queue_update,
)

# Extract and display only prompt, input image URL, and output URL
output_url = result["images"][0]["url"]
print("Prompt:", prompt)
print("Input Image URL:", image_url)
print("Output URL:", output_url)

# Save to log file
import json
from datetime import datetime

log_entry = {
    "timestamp": datetime.now().isoformat(),
    "model": "fal-ai/qwen-image-edit",
    "prompt": prompt,
    "input_image_url": image_url,
    "output_url": output_url
}

# Append to log file
log_file = "generation_log.json"
try:
    with open(log_file, 'r') as f:
        logs = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    logs = []

logs.append(log_entry)

with open(log_file, 'w') as f:
    json.dump(logs, f, indent=2)

print(f"\nSaved to {log_file}")