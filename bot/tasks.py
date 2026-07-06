import replicate
import requests
import tempfile
from config import REPLICATE_API_TOKEN

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

def generate_animation(image_url: str, category: str, style: str, user_id: int) -> str:
    # Используем Stable Video Diffusion — официальную модель Stability AI
    output = replicate_client.run(
        "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
        input={
            "cond_image": image_url,
            "motion_bucket_id": 80,
            "fps": 15,
            "decoding_t": 4,
        }
    )
    video_url = output
    response = requests.get(video_url)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tmp.write(response.content)
    tmp.close()
    return tmp.name
