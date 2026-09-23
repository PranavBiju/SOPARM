import base64
import os
from openai import OpenAI
from tts2 import tts
from dotenv import load_dotenv

def name_meds():
  load_dotenv()
  client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

  # Function to encode the image
  def encode_image(image_path):
    with open(image_path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

  # Path to your image
  image_path = "/home/alpha3/Desktop/Arm_project/24-25 sem1/Final pipeline/panorama.png"

  # Getting the base64 string
  base64_image = encode_image(image_path)

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "name of the medicine",
          },
          {
            "type": "image_url",
            "image_url": {
              "url":  f"data:image/jpeg;base64,{base64_image}"
            },
          },
        ],
      }
    ],
  )


  print(response.choices[0].message.content)\
  
  #asmit code 
  
  tts(response.choices[0].message.content)
if __name__ == "__main__":
  name_meds()