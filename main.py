import requests
import regex as re
import xlsxwriter
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Taj_Mahal"
API_URL = "https://en.wikipedia.org/w/api.php"

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

title = soup.find(id="firstHeading")
title=title.string

img="https://"
for raw_img in soup.find_all('img'):
   link = raw_img.get('src')
   # The first image on the page with the URL strucutre below is usually 
   # the image inside the infobox. We exlcude any .svg images, as they are 
   # vector graphics common to all Wikipedia pages
   if re.search('wikipedia/.*/thumb/', link) and not re.search('.svg', link):
     img += link[2:]
     # Once the first image has been found, we break out of the loop and search the next page
     break

response = requests.get(
    API_URL,
    params={
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
    }).json()

page = next(iter(response['query']['pages'].values()))
summary = page['extract']
paragraph=""
for char in summary:
    if char=='\n':
        break
    paragraph += char

# write Scraped Data to Excel Worksheet
workbook   = xlsxwriter.Workbook('scraped_data.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, "Title")
worksheet.write(0, 1, "Paragraph")
worksheet.write(0, 2, "Image URL")
worksheet.write(1, 0, title)
worksheet.write(1, 1, paragraph)
worksheet.write(1, 2, img)
workbook.close()
