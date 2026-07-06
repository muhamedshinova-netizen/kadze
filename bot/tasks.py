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
        "lucataco/hotshot-xl:78b4e0a22f8b8b1d7c3b0e8d6a5c3a0d5b2c7e1f6e9a2b4d7c8f1e0a3b5c6d8",
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
