import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

data = {"month":[], "advances":[], "declines":[], "ratio":[]}
#opts = Options()
#opts.add_argument("--headless")

BASE =  "https://www1.nseindia.com/products/content/equities/equities/"


months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

for YEAR in range(2021, 1999, -1):
    print("Fetching for year : " + str(YEAR))
    for MONTH in reversed(months):
        try :
            print("Fetching for month : " + str(MONTH))
            driver.get(BASE + f"eq_advdec{MONTH}{YEAR}.htm")
            soup_file = driver.page_source
            soup = BeautifulSoup(soup_file, parser="html.parser", features="lxml")
            table = soup.find('tbody')
            rows = table.find_all('tr')

            for r in reversed(rows[2:]):
                
                a = r.find_all('td')
                month, advance, decline, ratio = a[0].text, a[1].text, a[2].text, a[3].text
                data["month"].append(month)
                data["advances"].append(advance)
                data["declines"].append(decline)
                data["ratio"].append(float(ratio))

        except :
            print("Failed for month : " + str(MONTH))


df = pd.DataFrame.from_dict(data)

df.to_csv("./market_breadth.csv", index=False)

