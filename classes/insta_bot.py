from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from helpers.insta_helpers import get_data_from_insta_user
from helpers.data_parser import user_data_to_potential_buyer
from time import sleep

perfil_path = "/home/juan/.config/microsoft-edge/Default"


class Bot():
  def __init__(self) -> None:
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument(f"user-data-dir={perfil_path}")
    self.driver = webdriver.Edge(options=edge_options)
    self.driver.implicitly_wait(10)
    self.driver.maximize_window()
    self.actions = ActionChains(self.driver)  
    
  def check_instagram(self):
      self.driver.get("https://www.instagram.com")
      window_size = self.driver.get_window_size()
      center_x = window_size['width']/2
      center_y = window_size['height']/2
      # Calcula las coordenadas del centro de la pantalla
      for _ in range(30):
        
        
        element_at_center:WebElement = self.driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]).parentNode;", center_x, center_y)
        
          
        try:
          imgs = element_at_center.find_elements("tag name","img")
          vids = element_at_center.find_elements("tag name","video")
          media=imgs + vids
        except Exception: print("Error con el elemento, saltando . . .");continue
        
        
        print("videos:", len(vids))
        if len(media)==1:
          element:WebElement = media[0]
          if element.tag_name=="video":
            element.screenshot("ss.png")
            print("video found")
          else:
            self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick', { bubbles: true }));", element)
            print("img liked")

        else:
          # scroll to the closest element
          try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", media[0])
            print("scrolled to element")
          except:
            print("Error al scrollear al elemento. . .")
            self.driver.execute_script("window.scrollBy({top: 100,behavior: 'smooth'});")
        
        
        self.driver.execute_script("window.scrollBy({top: 870,behavior: 'smooth'});")
        sleep(1)

  def bot_quit(self):
    self.driver.quit()