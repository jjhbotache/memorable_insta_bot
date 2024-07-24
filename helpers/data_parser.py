import os
import random
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO
import json

from config import BUYER_DESCRIPTION, DEBUG
from helpers.str_helpers import trim_json_str

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel(model_name='gemini-1.5-flash')



def url_img_to_description(img_url):
  img_data = requests.get(img_url).content
  temp_img = Image.open(BytesIO(img_data))
  response = model.generate_content([
    temp_img,
    "Describe this image in detail"
  ])
  return response.text
  
def user_data_to_potential_buyer(user_data):
  """Returns according to a user_data, if it's possible that the user buy

  Args:
      user_data (dict): dict of the user_data
  """
  # choose random 4 images (if exists)
  
  print("Analysing user ", user_data["username"]," . . .")
  
  imgs_to_choose = len(user_data['imgs']) if len(user_data['imgs']) < 5 else 4
  url_imgs_to_get_descriptions = []
  
  print("Chosing random imgs to analyse . . .")
  while len(url_imgs_to_get_descriptions) < imgs_to_choose:
    random_img_url = user_data['imgs'][:20][random.randint(0, len(user_data['imgs']) - 1)]
    if random_img_url not in url_imgs_to_get_descriptions:
      url_imgs_to_get_descriptions.append(random_img_url)
  
  print(f"{len(url_imgs_to_get_descriptions)} imgs choosed")
  
  # starting to create descriptions from the imgs
  user_data["imgs_descripted"] = []
  for url in url_imgs_to_get_descriptions:
    description = url_img_to_description(url)
    user_data["imgs_descripted"].append( description )
    if DEBUG: print("img descripted: ",user_data["imgs_descripted"][-1])
    
  # also descript the profile pic
  user_data["profile_picture_description"] = url_img_to_description(user_data["profile_picture"])
  if DEBUG: print("profile img descripted: ",user_data["profile_picture_description"])
  
  # checking if it's possible to buy based on the user data
  string_data = json.dumps(user_data)
  
  prompt = f"""Here is a description of a potential buyer: {BUYER_DESCRIPTION}
    According to this user data: {string_data}
    Answer with a JSON following this schema:
    {{
      "is_possible_to_buy": true/false,
      "reason": "the reason why it's possible to buy"
    }}"""
    
  response = model.generate_content(prompt)
  data = json.loads(trim_json_str(response.text))
  
  print("Result: ", data)
  user_data["analysis_result"] = data
  return data
  
      
  
  
if __name__ == '__main__':
  url_img_to_description("https://storage.googleapis.com/generativeai-downloads/images/piranha.jpg")