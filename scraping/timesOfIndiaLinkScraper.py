import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage you want to scrape
url = 'https://timesofindia.indiatimes.com/archive/year-2024,month-8.cms'

# Fetch the webpage content
response = requests.get(url)
web_content = response.content

# Parse the webpage content with BeautifulSoup
soup = BeautifulSoup(web_content, 'html.parser')
# print(soup)

# Dictionary to store the data
archive_data = {
    "year": 2024,
    "august": {}
}

calendar_div = soup.find('div', id='calenderdiv')
print(calendar_div)

# Find all <td> elements with class "center" (those contain the day links)
day_links = soup.find_all('td', align='center')


# Loop through each <td> and extract the day and href link
for td in day_links:
    a_tag = td.find('a')
    if a_tag:
        # Extract the day from the link (the text inside the <a> tag)
        day = a_tag.get_text(strip=True)
        # Extract the href link
        link = a_tag['href']
        # Store the day and link in the august dictionary
        archive_data["august"][day] = f"https://timesofindia.indiatimes.com{link}"

# Save the result as a JSON file
with open('archive_links_2024.json', 'w') as json_file:
    json.dump(archive_data, json_file, indent=4)

print("Data has been saved to archive_links_2024.json")
