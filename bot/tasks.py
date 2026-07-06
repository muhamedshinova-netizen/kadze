import replicate
import requests
import tempfile
from config import REPLICATE_API_TOKEN

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

def generate_animation(image_url: str, category: str, style: str, user_id: int) -> str:
    # Бесплатная модель стилизации (не видео)
    output = replicate_client.run(
        "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
        input={
            "img": image_url,
            "scale": 2,
            "version": "v1.4"
        }
    )
    # output — это URL улучшенного изображения
    image_url_result = output
    response = requests.get(image_url_result)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    tmp.write(response.content)
    tmp.close()
    return tmp.name
