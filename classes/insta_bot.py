import random
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from helpers.insta_helpers import get_data_from_insta_user
from helpers.data_parser import local_url_img_to_description, url_img_to_description, user_data_to_potential_buyer, would_person_be_interested
import time
import threading

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
            center_x, center_y = self.get_mid_points()
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

  def get_mid_points(self):
      window_size = self.driver.get_window_size()
      center_x = window_size['width'] / 2
      center_y = window_size['height'] / 2
      return center_x,center_y


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