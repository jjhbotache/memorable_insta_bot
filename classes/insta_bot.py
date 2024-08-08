import random
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from helpers.insta_helpers import get_data_from_insta_user
from helpers.data_parser import local_url_img_to_description, url_img_to_description, user_data_to_potential_buyer, would_person_be_interested

import time
import threading

from helpers.str_helpers import get_random_syllable

perfil_path = "/home/juan/.config/microsoft-edge/Default"


class Bot():
  def __init__(self) -> None:
    """
    Initialize a new instance of the Bot class.

    Parameters:
    None

    Returns:
    None
    """
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument(f"user-data-dir={perfil_path}")
    # edge_options.add_argument(f"--headless")
    self.driver = webdriver.Edge(options=edge_options)
    self.driver.implicitly_wait(10)
    self.actions = ActionChains(self.driver)  
    
  def stop_execution(self):
        self.stop_thread = True

  def check_instagram(self, segs):
      """
      Check Instagram for media and interact with it.

      Parameters:
      segs (int): Number of seconds to run the function

      Returns:
      None
      """
      def get_mid_points(self):
        window_size = self.driver.get_window_size()
        center_x = window_size['width'] / 2
        center_y = window_size['height'] / 2
        return center_x,center_y
      
      self.stop_thread = False
      if segs > 0:
        timer_thread = threading.Timer(segs, self.stop_execution)
        timer_thread.start()

      self.driver.get("https://www.instagram.com")
      

      while not self.stop_thread:
          # ensure thatwe are at home url
          if self.driver.title!= "Instagram":
              self.driver.get("https://www.instagram.com")
              continue

          try:

            print("getting element at center")
            center_x, center_y = get_mid_points()
            element_at_center: WebElement = self.driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]).parentNode;", center_x, center_y)
            el_url = "element_at_center.png"
            element_at_center.screenshot(el_url)
            there_is_media = len(element_at_center.find_elements("css selector", "img, video")) > 0
            
            if there_is_media:
              print("there is media")
              description = local_url_img_to_description(el_url)
              info = would_person_be_interested(description)
              if info["interested"]:
                print(f"Person interested: {info['reason']} \n")
                self.actions.double_click(element_at_center).perform()
                img = len(element_at_center.find_elements("css selector", "img")) > 0
                video = len(element_at_center.find_elements("css selector", "video")) > 0
                
                if img:
                  print("watching img")
                  time.sleep(5)
                if video:
                  watching_time = random.choice([15,25,35])
                  print(f"watching video for {watching_time} seconds")
                  time.sleep(watching_time)
                
                
                print("double clicked")
              else:
                print("not interested")
            else:
              print("no media")
                
            self.driver.execute_script("window.scrollBy({top: 870,behavior: 'smooth'});")
            time.sleep(1)
            
          except Exception as e:
              print(f"Error: {str(e)}")
              continue
      
      print("ended")
      timer_thread.join()

  def follow_random_users_from_page(self, page, amount_to_follow=10):
    """ Follow a random amount of users from a page.

    Args:
        page (_type_): _description_
        amount_to_follow (_type_): _description_
    """
    
    self.driver.get(f"https://www.instagram.com/{page}/followers/")
    self.driver.find_element("xpath", '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a').click()
    time.sleep(4)
    
    def type_random_syllable():
      self.driver.find_element("css selector", 'input[aria-label="Search input"]').send_keys("-")      
      self.driver.find_element("css selector", 'input[aria-label="Search input"]').send_keys(Keys.ESCAPE)      
      self.driver.find_element("css selector", 'input[aria-label="Search input"]').send_keys(get_random_syllable())      
      time.sleep(2)
    
    type_random_syllable()
    
    already_followed = 0
    followers_data = []
    while already_followed < amount_to_follow:
      try:
        # get the followers divs
        try:                                                      
          try:
            followers_container = self.driver.find_element("xpath", '/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div')
          except:
            followers_container = self.driver.find_element("xpath", '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div')
          followers_divs = followers_container.find_elements("xpath", "./div")
        except Exception as e:
          print("No followers found: ", str(e[:300]))
          type_random_syllable()
          continue
          
        # parse the followers data
        followers_data = []
        for d in followers_divs:
          username = d.text.split("\n")[0]
          followed = not ("follow" in d.text.split("\n")[2].lower())
          follower_data = {
            "username": username,
            "followed": followed
          }
          followers_data.append(follower_data)
        
        for follower in followers_data:
          print(f"attemping to follow {follower['username']}")
          followed = self.attemp_to_follow_user(follower["username"])
          if followed:
            already_followed += 1
          
          
        
      except Exception as e:
        print(f"Error: {str(e)}")
        continue
      
    print(*followers_data,sep="\n")

  def attemp_to_follow_user(self,username):
    user_info = get_data_from_insta_user(username)
    if user_info is None: return False
    
    analyse = user_data_to_potential_buyer(user_info)
    print(f"Analyse result: {analyse}")
    {'is_possible_to_buy': False, 'reason': "The provided user data does not include any information about age, social life, or interest in wine. Therefore, it's not possible to determine if this user is a potential buyer of custom-designed wine bottles."}
    
    if analyse["is_possible_to_buy"]:
      self.driver.get(f"https://www.instagram.com/{username}/")
      follow_button = self.driver.find_element("xpath", '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section/div[1]/div/div/div/button')
      if "follow" in follow_button.text.lower():
        follow_button.click()
        return True
    else:
      print(f"User {username} is not a potential buyer: {analyse['reason']}")
      return False
    

  def bot_quit(self):
    """
    Quit the browser session.

    Parameters:
    None

    Returns:
    None
    """
    self.driver.close()
    self.driver.quit()