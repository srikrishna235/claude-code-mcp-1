import os
import fal_client

# Set API key as environment variable
os.environ["FAL_KEY"] = "3845a313-cfc9-469b-ac5d-fe354d7106dd:42f4fb3cddc5156df1b724115431bb85"

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
           print(log["message"])

text = "I just found a hidden treasure in the backyard! Check it out!"

result = fal_client.subscribe(
    "fal-ai/chatterbox/text-to-speech",
    arguments={
        "text": text
    },
    with_logs=True,
    on_queue_update=on_queue_update,
)

# Extract and display only text and audio URL
print("Text:", text)
print("Audio URL:", result["audio"]["url"])