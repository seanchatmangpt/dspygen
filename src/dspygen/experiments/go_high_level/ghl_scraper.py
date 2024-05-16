import requests
from bs4 import BeautifulSoup

# URL of the documentation page
url = "https://highlevel.stoplight.io/docs/integrations/0443d7d1a4bd0-overview"

# Fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the relevant sections
# Example: Extracting all headings and paragraphs
headings = soup.find_all(['h1', 'h2', 'h3'])
paragraphs = soup.find_all('p')

# Print the extracted data
for heading in headings:
    print(heading.get_text())
for para in paragraphs:
    print(para.get_text())
