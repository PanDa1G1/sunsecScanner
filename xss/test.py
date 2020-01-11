
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
req_url = "https://www.baidu.com"
chrome_options=Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get(req_url)
print(browser.page_source)
browser.close()

