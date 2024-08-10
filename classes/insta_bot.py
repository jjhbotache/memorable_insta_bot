import random
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from helpers.insta_helpers import get_data_from_insta_user
from helpers.data_parser import local_url_img_to_description, url_img_to_description, user_data_to_potential_buyer, would_person_be_interested
from helpers.config import DEBUG

import time
import threading

from helpers.str_helpers import get_random_syllable
from helpers.webdriver_helpers import find_first_element_from_elements

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
    self.driver.implicitly_wait(3)
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
      def get_mid_points():
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
                print(f"Person interested: {info['reason']} \n🤩\n")
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
                print("not interested 🥱")
            else:
              print("no media ❓")
                
            self.driver.execute_script("window.scrollBy({top: 870,behavior: 'smooth'});")
            time.sleep(1)
            
          except Exception as e:
              if DEBUG:print(f"Error while getting element at center: {str(e)}")
              continue
      
      print("ended", end="\n\n")
      timer_thread.join()

  def follow_random_users_from_page(self, page, amount_to_follow):
    """ Follow a random amount of users from a page.

    Args:
        page (_type_): _description_
        amount_to_follow (_type_): _description_
    """
    
    
    def get_followers_window():
      for _ in range(3):
        try:
          self.driver.get(f"https://www.instagram.com/{page}/followers/")
          self.driver.find_element("xpath", '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a').click()
          time.sleep(4)
          break
        except Exception as e:
          print(f"Error while getting followers window: {str(e)}")
          time.sleep(2)
          continue
    
    def type_random_syllable():
      for _ in range(3):
        try:
          self.driver.find_element("css selector", 'input[aria-label="Search input"]').send_keys("-")      
          self.driver.find_element("css selector", 'input[aria-label="Search input"]').send_keys(Keys.ESCAPE)      
          self.driver.find_element("css selector", 'input[aria-label="Search input"]').send_keys(get_random_syllable())      
          time.sleep(2)
        except Exception as e:
          print(f"Error while typing random syllable: {str(e)}")
          get_followers_window()
          time.sleep(2)
          continue
    
    
    
    already_followed = 0
    followers_data = []
    while already_followed < amount_to_follow:
      get_followers_window()
      type_random_syllable()
      try:
        # get the followers divs
        try:
          try:
            followers_container = find_first_element_from_elements(self.driver, [
              '/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div',
              '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div'
            ])
          except:
            followers_container = None
          
          followers_divs = followers_container.find_elements("xpath", "./div")
        except Exception as e:
          print("No followers found: ", str(e[:300] if len(str(e))>300 else str(e)))
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
          if already_followed >= amount_to_follow:
            break
          followed = self.attemp_to_follow_user(follower["username"])
          if followed:
            print("\n")
            already_followed += 1
          
          
        
      except Exception as e:
        print(f"Error in follow_random_users_from_page : {str(e)}")
        type_random_syllable()
        time.sleep(2)
        continue
      
    return already_followed
    
  def attemp_to_follow_user(self,username):
    print(f"Checking if user {username} is a potential buyer...",end="\n")
    user_info = get_data_from_insta_user(username,self.driver)
    if user_info is None: return False
    
    analyse = user_data_to_potential_buyer(user_info)
    print(f"Analyse result:")
    print("Would person be interested: ", "yes" if analyse["is_possible_to_buy"] == True else "no")
    reason_limit = 400
    print("Reason: ", analyse["reason"] if len(analyse["reason"])<reason_limit else analyse["reason"][:reason_limit]+"...")
    
    # {'is_possible_to_buy': False, 'reason': "The provided user data does not include any information about age, social life, or interest in wine. Therefore, it's not possible to determine if this user is a potential buyer of custom-designed wine bottles."}
    
    if analyse["is_possible_to_buy"]:
      print(f"following ",end="")
      self.driver.get(f"https://www.instagram.com/{username}/")
      follow_button = None
      for _ in range(3):
        try:                                                            
              try:    follow_button = self.driver.find_element("xpath", '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section/div[1]/div/div/div/button')
              except: follow_button = self.driver.find_element("xpath", '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[2]/div/div/div[2]/div/div[1]/button')
              break
        except Exception as e:
          print(f"Error while finding follow button: {str(e)}")
          time.sleep(2)
          continue
      if "follow" in follow_button.text.lower():
        follow_button.click()
        print(f"✅",end="")
        time.sleep(2)
        return True
    else:
      print(f"User {username} is not a potential buyer, skipping... ❌",end="\n\n")
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