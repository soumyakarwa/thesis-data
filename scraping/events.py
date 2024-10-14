import requests
from bs4 import BeautifulSoup
import createJSON
import json

# Set start and end years
year = 2000
lastYear = 2021
eventData = {}

def main():
    for curr in range(year, lastYear+1):
        print(curr)
        eventData.update(createJSON.create_yearly_structure(curr))
        url = f'https://en.wikipedia.org/wiki/{curr}_in_India'  # Format URL with year
        print(url)
        # Fetch the webpage content
        response = requests.get(url)
        if response.status_code == 200:  # Check if request was successful
            web_content = response.content

            # Parse the webpage content with BeautifulSoup
            soup = BeautifulSoup(web_content, 'html.parser')

            # Print the parsed HTML content (you can modify this to extract specific data)
            eventH2 = soup.find('h2', id='Events')
            
            if eventH2:
                # Get the parent <h2> tag for the "Events" section
                h2Parent = eventH2.find_parent()
                # Now, find the next sibling that contains the events list (usually <ul> or <p>)
                next_sibling = h2Parent.find_next_sibling()
                
                
                while next_sibling:
                    # Stop if we reach a <div> with class 'section-heading' (indicating a new section)
                    if next_sibling.name == 'div' and 'mw-heading2' in next_sibling.get('class', []):
                        break  # Stop the loop when reaching the next section

                    # If it's a <ul> (unordered list), extract all <li> tags within
                    if next_sibling.name == 'ul':
                        for li in next_sibling.find_all('li'):
                            # print(li)
                            currentText = (li.get_text())  # Extract text from <li> tags
                            createJSON.addEvent(eventData, curr, currentText)

                    # Move to the next sibling
                    next_sibling = next_sibling.find_next_sibling()
            else:
                print(f"No 'Events' section found for the year {curr}")
        else:
            print(f"Failed to retrieve data for the year {year}. HTTP Status Code: {response.status_code}")

    with open('output.json', 'w') as json_file:
        json.dump(eventData, json_file, indent=4)

    print("JSON data has been written to output.json")

if __name__ == "__main__":
    main()
