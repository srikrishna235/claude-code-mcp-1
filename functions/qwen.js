import { fal } from "@fal-ai/client";

// Configure with API key
fal.config({
  credentials: "3845a313-cfc9-469b-ac5d-fe354d7106dd:42f4fb3cddc5156df1b724115431bb85"
});

const prompt = "Mount Fuji with cherry blossoms in the foreground, clear sky, peaceful spring day, soft natural light, realistic landscape.";

const result = await fal.subscribe("fal-ai/qwen-image", {
  input: {
    prompt: prompt
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS") {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  },
});

// Extract and display only prompt and URL
console.log("Prompt:", prompt);
console.log("URL:", result.data.images[0].url);