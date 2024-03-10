# Import the Selenium library
from selenium import webdriver
from selenium.webdriver.common.by import By

# Create a driver object that can control the browser
# You can use other browsers such as Firefox, Chrome, etc.
driver = webdriver.Chrome()

# Go to the website you want to access
# Replace this with the actual website URL
driver.get(
    "https://mynoise.net/NoiseMachines/anamnesisSoundscapeGenerator.php")

# Find the button element you want to click by its ID, name, class, or other attribute
# Replace this with the actual button attribute

but = driver.find_element(
    By.ID, "fftCanvas") or driver.find_element(By.ID, "mute")

# Click the button
but.click()

# Close the driver and the browser
# driver.close()
