from bs4 import BeautifulSoup
from selenium import webdriver
import csv

url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/komitety"
driver = webdriver.Chrome()
committeesCsv = open("committees.csv", "w")

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
i = 0

# scraping all HTML code containing committees
committees_even = soup.find_all("tr", {"class": "even"})
committees_odd = soup.find_all("tr", {"class": "odd"})
committees = committees_even + committees_odd

# scraping name of each committee that takes part in the elections and writing it to csv file
try:
    writer = csv.writer(committeesCsv)
    writer.writerow(("id", "nazwa"))
    for committee in committees:
        name = committee.findAll("td")[1].text
        takes_part = committee.findAll("td")[4].text
        if takes_part == "tak":
            print(name)
            writer.writerow((i, name))
            i += 1
finally:
    committeesCsv.close()
