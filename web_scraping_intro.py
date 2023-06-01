#install libraries
pip install pandas
pip install beautifulsoup4 # library to scrape data from websites
pip install lxml # beautiful soup requires a parser

import urllib.request as urlib
import bs4 as bs

# Data source used: https://manchestersquare.ca/directory/
source = urlib.urlopen("https://manchestersquare.ca/directory/").read()

# Create the soup object
soup = bs.BeautifulSoup(source, 'lxml')

# Check soup object
print('title of the page: ', soup.title)
print('values: ', soup.title.string)

# Get all text from all soup
print(soup.get_text())

# Extract hyperlinks
print(soup.find_all("a"))

# As you can see from the output above, html tags sometimes come with attributes. 
# These attributes provide additional information about html elements. 
# You can use a for loop and the get('"href") method to extract and print out only hyperlinks.
all_links = soup.find_all("a")
for link in all_links:
    print(link.get("href"))
    
# perhaps the business is only interested in extracting social media urls like instagram. 
# we could use regex to find these links and then add them to a list

import re 
instagram_list = []

all_links = soup.find_all("a")
for link in all_links:
    cell_value = link.get("href")
    if bool(re.search("instagram.com", cell_value)):
      instagram_list.append(cell_value)
print(instagram_list)

# We can create a dataframe from this list.
df = pd.DataFrame(instagram_list, columns=['instagram_url'])
df

# We could remove the forwardslash at the end of the string, and then retrieve the company name from the instagram link.

df['instagram_url'] = df['instagram_url'].str.rstrip('/')
df['Company_Name'] = df['instagram_url'].str.split('/').str[-1]
df

# Extension Exercise
# Extract the paragraph tags and put them in a list (address, company name) and add them to the previous data frame!
body = soup.body
for paragraph in body.find_all('p'): #paragraph tags
    print(paragraph.text)
    
 
# We can also extract data from tables on the web
# Source: https://www.ontario.ca/page/2022-23-third-quarter-finances

source = urlib.urlopen("https://www.ontario.ca/page/2022-23-third-quarter-finances").read()
soup = bs.BeautifulSoup(source, 'lxml')

# Check to see if page has a table
table = soup.find('table')

# Find the table headers
col_labels = soup.find_all('th')
col_labels

# Print rows to ensure nothing went awry
rows = soup.find_all('tr')
print(rows[:5])

# Convert the table into a dataframe
table = soup.find_all('table')
df = pd.read_html(str(table))[0] # prints first table

# Convert your dataframe into a csv file.
df.to_csv('table.csv', index=False, encoding='utf-8')


# For those using Google Colab, you will need
# from google.colab import drive
# drive.mount('drive')
# df.to_csv('table.csv', index=False, encoding='utf-8')
# !cp table.csv "drive/My Drive"
