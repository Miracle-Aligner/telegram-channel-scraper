class elements_loaded(object):
  """An expectation for checking that new channel messages is loaded.

  locator - used to find the elements
  returns the WebElement once it has the particular css class
  """
  def __init__(self, prev_len):
    self.prev_len = prev_len

  def __call__(self, driver):
    elements = driver.find_elements(By.CLASS_NAME, "tgme_widget_message_bubble")
    if len(elements) > self.prev_len:
        return elements
    else:
        return False