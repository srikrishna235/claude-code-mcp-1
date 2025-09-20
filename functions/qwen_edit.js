import { fal } from "@fal-ai/client";

// Configure with API key
fal.config({
  credentials: "3845a313-cfc9-469b-ac5d-fe354d7106dd:42f4fb3cddc5156df1b724115431bb85"
});

const prompt = "Change bag to apple macbook";
const imageUrl = "https://v3.fal.media/files/koala/oei_-iPIYFnhdB8SxojND_qwen-edit-res.png";

const result = await fal.subscribe("fal-ai/qwen-image-edit", {
  input: {
    prompt: prompt,
    image_url: imageUrl
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS") {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  },
});

// Extract and display only prompt, input image URL, and output URL
console.log("Prompt:", prompt);
console.log("Input Image URL:", imageUrl);
console.log("Output URL:", result.data.images[0].url);