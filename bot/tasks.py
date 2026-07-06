import replicate
import requests
import tempfile
from config import REPLICATE_API_TOKEN

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

def generate_animation(image_url: str, category: str, style: str, user_id: int) -> str:
    prompts = {
        "portrait": {
            "лесной дух": "portrait of a person, forest spirit, leaves around, gentle breeze moving hair, dappled light, soft focus background, studio ghibli style, warm colors, hand-drawn animation",
            "default": "soft portrait, gentle smile, warm light, animated hair movement, ghibli style"
        },
        "nature": {
            "закат над водой": "sunset over lake, calm water ripples, glowing sun, silhouettes of trees, soft pastel, studio ghibli style, animated",
            "default": "beautiful nature landscape, soft wind, moving clouds, ghibli style"
        },
    }
    prompt = prompts.get(category, {}).get(style, "warm animated scene, studio ghibli style, masterpiece")

    output = replicate_client.run(
        "lucataco/animate-diff:be4e5a38e6f96f5a4c4b6b2b9c2c0a5b7e3a2f0a9d9f0e3f5c1b3e6c8d7f6a4",
        input={
            "image": image_url,
            "prompt": prompt,
            "num_frames": 24,
            "fps": 15,
            "guidance_scale": 7.5,
        }
    )
    video_url = output
    response = requests.get(video_url)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tmp.write(response.content)
    tmp.close()
    return tmp.name
