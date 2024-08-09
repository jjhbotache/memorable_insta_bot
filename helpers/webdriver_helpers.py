from selenium.common.exceptions import NoSuchElementException

def find_first_element_from_elements(driver, xpaths):
  for xpath in xpaths:
    try:
      element = driver.find_element("xpath",xpath)
      return element
    except NoSuchElementException:
      pass
  return None