from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://secure-retreat-92358.herokuapp.com/')

# total_articles = driver.find_element(By.XPATH, value='//*[@id="articlecount"]/ul/li[2]/a[1]').text
# total_articles = driver.find_element(By.CSS_SELECTOR, value='#articlecount li:nth-of-type(2) a:nth-of-type(1)')
# total_articles.click()

# all_portals = driver.find_element(By.LINK_TEXT, value='Content portals')
# all_portals.click()

# search = driver.find_element(By.NAME, value='search')
# search.send_keys("Python")
# search.send_keys(Keys.ENTER)

# driver.quit()

first_name = driver.find_element(By.NAME, value='fName')
last_name = driver.find_element(By.NAME, value='lName')
email = driver.find_element(By.NAME, value='email')

first_name.send_keys('Juan')
last_name.send_keys('dela Cruz')
email.send_keys('jdcruz@hello.com')

button = driver.find_element(By.CSS_SELECTOR, value='form button')
button.click()