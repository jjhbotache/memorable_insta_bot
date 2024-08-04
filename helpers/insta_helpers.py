from selenium import webdriver

from helpers.config import DEBUG

def get_data_from_insta_user(username):
  if DEBUG:
    print(f"Getting data from Instagram user: {username}")
  # haedless driver
  edge_options = webdriver.EdgeOptions()
  edge_options.add_argument("--headless")
  edge_options.add_argument("--disable-gpu")
  driver = webdriver.Edge(options=edge_options)
  driver.implicitly_wait(10)
  
  driver.get(f"https://www.instagram.com/{username}/")
  user_info_to_return = {}
  
  user_info_to_return["username"] = driver.find_element("xpath",'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section/div[1]/div[1]/h2').text
  user_info_to_return["posts_amount"] =int(  driver.find_element("xpath",'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section/div[3]/ul/li[1]/div/button/span/span').text.replace(",",""))
  user_info_to_return["followers_amount"] =int(  driver.find_element("xpath",'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section/div[3]/ul/li[2]/div/button/span/span').text.replace(",",""))
  user_info_to_return["followed_amount"] =int( driver.find_element("xpath",'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section/div[3]/ul/li[3]/div/button/span/span').text.replace(",",""))
  user_info_to_return["real_name"] = driver.find_element("xpath",'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section/div[4]/div[1]/span').text
  try: user_info_to_return["description"] = driver.find_element("xpath",'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section/div[4]/span').text
  except: user_info_to_return["description"] = None
  user_info_to_return["stared_stories"] =[(s.text if len(s.text)>1 else "-") for s in driver.find_elements("xpath",'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/div[1]/div/div/div[1]/div/ul/li')]
  user_info_to_return["imgs"] = [img.get_attribute("src") for img in driver.find_elements("tag name","img") if not img.get_attribute("src").startswith("data")]
  user_info_to_return["profile_picture"] = user_info_to_return["imgs"][0] ; user_info_to_return["imgs"].pop(0)

  
  if DEBUG: print("profile info gotten")
  return user_info_to_return
  
  
if __name__ == "__main__":
  get_data_from_insta_user(input("Ingresa un usuario: "))