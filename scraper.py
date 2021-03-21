import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

data = {"month":[], "advances":[], "declines":[], "ratio":[]}
opts = Options()
opts.add_argument("--headless")



driver = webdriver.Chrome()
driver.get("https://www1.nseindia.com/products/content/equities/equities/historical_advdeclines.htm")
soup_file = driver.page_source
soup = BeautifulSoup(soup_file, parser="html.parser")
table = soup.find('tbody')
rows = table.find_all('tr')
for r in rows[1:]:
    a = r.find_all('td')
    #print(a)

    month, advance, decline, ratio = a[0].text, a[1].text, a[2].text, a[3].text
    data["month"].append(month)
    data["advances"].append(advance)
    data["declines"].append(decline)
    data["ratio"].append(ratio)


df = pd.DataFrame.from_dict(data)

print(df.head(40))


    

