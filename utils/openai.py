import os
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key
txt_model = "gpt-4-turbo"


#prompt = "an isometric view of a skyscraper in the style of a city building game. The skyscraper should be in the centre of the image and it should not be cut off."

def generate_image(prompt, size='1024x1024', img_model='dall-e-2'):
    
    return openai.images.generate(
        model=img_model,
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    ).data[0].url

def caption_image(url):

    return openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", 
                     "text": "Write a synthetic description for the following image."},
                        {
                            "type": "image_url",
                            "image_url": {
                            "url": url,
                        },
                    },
                ],
            }
        ],
        max_tokens=50,
    ).choices[0].message.content