import os
import random
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO
import json

from .config import DEBUG, BUYER_DESCRIPTION, PAGE_ROLE
from .str_helpers import trim_json_str

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def url_img_to_description(img_url):
    img_data = requests.get(img_url).content
    temp_img = Image.open(BytesIO(img_data))
    response = model.generate_content([
        temp_img,
        "Describe this image in detail", ],
        safety_settings={
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "block_none",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "block_none",
            "HARM_CATEGORY_HARASSMENT": "block_none",
            "HARM_CATEGORY_HATE_SPEECH": "block_none",          
        }
    )
    return response.text

def local_url_img_to_description(img_path):
    temp_img = Image.open(img_path)
    response = model.generate_content([
        temp_img,
        "Describe this image in detail"],
        safety_settings={
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "block_none",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "block_none",
            "HARM_CATEGORY_HARASSMENT": "block_none",
            "HARM_CATEGORY_HATE_SPEECH": "block_none",          
        }
    )
    return response.text

def user_data_to_potential_buyer(user_data):
    """Returns according to a user_data, if it's possible that the user buy

    Args:
        user_data (dict): dict of the user_data
    """
    # choose random 4 images (if exists)

    

    imgs_to_choose = len(user_data['imgs']) if len(user_data['imgs']) < 5 else 4
    url_imgs_to_get_descriptions = []

    
    while len(url_imgs_to_get_descriptions) < imgs_to_choose:
        random_img_url = user_data['imgs'][:20][random.randint(0, len(user_data['imgs'][:20]) - 1)]
        if random_img_url not in url_imgs_to_get_descriptions:
            url_imgs_to_get_descriptions.append(random_img_url)


    # starting to create descriptions from the imgs
    user_data["imgs_descripted"] = []
    for url in url_imgs_to_get_descriptions:
        description = url_img_to_description(url)
        user_data["imgs_descripted"].append(description)

    # also descript the profile pic
    user_data["profile_picture_description"] = url_img_to_description(user_data["profile_picture"])

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

    user_data["analysis_result"] = data
    return data

def would_person_be_interested(img_description, person_role=PAGE_ROLE):
    """
    Determine if a person with a given role would be interested in an image based on its description.

    Args:
        img_description (str): Description of the image.
        person_role (str): Role of the person (e.g., "photographer", "art enthusiast").

    Returns:
        bool: True if the person would be interested, False otherwise.
    """
    prompt = f"""Based on the following description of an image: "{img_description}", 
    and considering the person has the role of "{person_role}", 
    would this person be interested in the image? 
    Answer with a JSON following this schema:
    {{
      "interested": true/false,
      "reason": "the reason for the interest or lack of interest"
    }}"""

    response = model.generate_content(prompt)
    data = json.loads(trim_json_str(response.text))
    
    return data


if __name__ == '__main__':
  pass
    # Test the functions
    # print(url_img_to_description("https://storage.googleapis.com/generativeai-downloads/images/piranha.jpg"))
    # print(local_url_img_to_description("/home/juan/Documents/dev/memorable_insta_bot/wine.jpg"))  # Reemplaza con la ruta a tu imagen local
    # print(would_person_be_interested(
    #   """On the opposite side of the water, the stick figure sees a sign that says "HOME" with an arrow pointing to the right. This suggests that the fish is swimming toward home, while the stick figure is looking on. The image is drawn in black ink on white paper. The overall tone of the image is light and whimsical.""",
    #   person_role=PAGE_ROLE
    #   ))  # Reemplaza con la ruta a tu imagen local
