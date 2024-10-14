import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage you want to scrape
url = 'https://timesofindia.indiatimes.com/2021/5/15/archivelist/year-2021,month-5,starttime-44331.cms'

# Fetch the webpage content
response = requests.get(url)
web_content = response.content

# Parse the webpage content with BeautifulSoup
soup = BeautifulSoup(web_content, 'html.parser')

# Find the <tr> with class "rightColWrap"
right_col_wrap = soup.find('tr', class_='rightColWrap')

# List to store href and text as dictionaries
links_data = []

if right_col_wrap:
    # Find all <td> tags inside the found <tr> tag
    td_tags = right_col_wrap.find_all('td')
    
    # Extract all <a> tags within the <td> tags
    for td in td_tags:
        a_tags = td.find_all('a')
        for a in a_tags:
            # Check if 'href' attribute exists
            if 'href' in a.attrs:
                href = a['href']
                text = a.get_text(strip=True)  # Get the text inside the <a> tag
                # Append href and text as a dictionary to the list
                links_data.append({
                    "href": href,
                    "text": text
                })
else:
    print("No <tr> with class 'rightColWrap' found")

# Store the result in a JSON file
with open('links_data.json', 'w') as json_file:
    json.dump(links_data, json_file, indent=4)

print("Data has been saved to links_data.json")
