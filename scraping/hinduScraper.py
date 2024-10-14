from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the browser
driver = webdriver.Chrome()

# Navigate to the URL
driver.get("https://www.thehindu.com/archive/web/2009/12/31/")

# Wait for Cloudflare check to finish (or handle CAPTCHA manually if needed)
driver.implicitly_wait(10)

# Extract page content
page_content = driver.page_source
print(page_content)

# Close the browser
driver.quit()