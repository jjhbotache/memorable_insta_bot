import os
import time
from selenium import webdriver
import dotenv
dotenv.load_dotenv()

from helpers.config import DEBUG
from helpers.webdriver_helpers import find_first_element_from_elements

def text_to_integrer(text):
    # Eliminar la parte de "followers" y los espacios
    text = text\
      .strip()\
      .replace(",","")\
      .replace(".","")\
      .split(' ',)[0]\
      .split('\n',)[0]\
      .lower()
    
    # Revisar si el texto contiene 'k' o 'M' para miles o millones
    if 'k' in text:
        # Convertir la parte numérica a flotante y multiplicar por 1000
        number = float(text.replace('k', '').strip()) * 1000
    elif 'm' in text:
        # Convertir la parte numérica a flotante y multiplicar por 1,000,000
        number = float(text.replace('M', '').strip()) * 1000000
    else:
        # Si no contiene 'k' ni 'M', convertir directamente a entero
        number = int(text.strip())
    
    return int(number)

def get_data_from_insta_user(username, given_driver=None):
  try:
  
    if DEBUG:
      print(f"Getting data from Instagram user: {username}")
    
    driver = given_driver
    
    
    if driver == None:
      # headless driver
      edge_options = webdriver.EdgeOptions()
      edge_options.add_argument("--headless")
      edge_options.add_argument("--disable-gpu")
      edge_options.add_argument("--log-level=3")
      
      driver = webdriver.Edge(options=edge_options)
      
      
    driver.implicitly_wait(10)
    driver.get(f"https://www.instagram.com/{username}/")
    
    
    user_info_to_return = {}
    
                                                                    
    for _ in range(3):
      try:
        user_info_to_return["username"] = find_first_element_from_elements(driver, [
          '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section/div[1]/div',
          '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[2]/div/div/div[1]/div/a/h2/span'
        ]).text
        break
      except:
        user_info_to_return["username"] = None
        print("retrying to get username")
        time.sleep(1)
        pass
      
    if user_info_to_return["username"] is None:
      print("the info could not be gotten")
      return None
    user_info_to_return["posts_amount"] =text_to_integrer(  find_first_element_from_elements(driver,[
      '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section/div[2]/ul/li[1]/div/button',
      "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[1]"
      ]).text)
    user_info_to_return["followers_amount"] =text_to_integrer( find_first_element_from_elements(driver,[
      '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section/div[2]/ul/li[2]/div/button',
      "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]"
      ]).text)
    user_info_to_return["followed_amount"] =text_to_integrer( find_first_element_from_elements(driver,[
      '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section/div[2]/ul/li[3]/div/button',
      "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[3]"
      ]).text)
    user_info_to_return["real_name"] = find_first_element_from_elements(driver,[
      "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/div[1]/span",
      "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section/div[3]/div[1]/span"
      ]).text
    try: user_info_to_return["description"] = find_first_element_from_elements(driver,[
      "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/span/div/span",
      ]).text
    except: user_info_to_return["description"] = None
    user_info_to_return["stared_stories"] =[(s.text if len(s.text)>1 else "-") for s in driver.find_elements("xpath",'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/div[1]/div/div/div[1]/div/ul/li')]
    user_info_to_return["imgs"] = [img.get_attribute("src") for img in driver.find_elements("tag name","img") if not img.get_attribute("src").startswith("data")]
    user_info_to_return["profile_picture"] = user_info_to_return["imgs"][0] ; user_info_to_return["imgs"].pop(0)

    if given_driver is None:
      driver.quit()
    return user_info_to_return
  
  except Exception as e:
    print(f"Error in get_data_from_insta_user: {str(e)[:300]}")
    return None
  
if __name__ == "__main__":
  get_data_from_insta_user(input("Ingresa un usuario: "))