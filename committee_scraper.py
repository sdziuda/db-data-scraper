from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/komitety"
driver = webdriver.Chrome()
committeesCsv = open("res/committees.csv", "w", encoding="utf-8")
candidatesCsv = open("res/candidates.csv", "w", encoding="utf-8")

driver.get(url)
time.sleep(1)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
committees_count = 0
candidates_count = 0

# scraping all HTML code containing committees
committees_even = soup.find_all("tr", {"class": "even"})
committees_odd = soup.find_all("tr", {"class": "odd"})
committees = committees_even + committees_odd

# scraping name of each committee that takes part in the elections and writing it to csv file
try:
    writer = csv.writer(committeesCsv)
    writer.writerow(("id", "nazwa"))
    writer = csv.writer(candidatesCsv)
    writer.writerow(("id", "pierwsze_imie", "drugie_imie", "nazwisko", "id_komitetu"))
    for committee in committees:
        writer = csv.writer(committeesCsv)
        number = committee.attrs["data-id"]
        name = committee.findAll("td")[1].text
        takes_part = committee.findAll("td")[0].text

        if takes_part != "999":
            print(name)
            writer.writerow((committees_count, name))

            url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/komitety/" + number + "?wybory=sejm"
            driver.get(url)
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            writer = csv.writer(candidatesCsv)

            # scraping all HTML code containing candidates from this committee
            bodies = soup.findAll("tbody")

            # scraping name of each candidate that takes part in the elections and writing it to csv file
            for body in bodies:
                candidates = body.findAll("tr")
                for candidate in candidates:
                    if candidate.has_attr("role") and candidate.attrs["role"] == "row":
                        name = candidate.findAll("td")[1].text
                        surname = ""
                        first_name = ""
                        second_name = ""

                        for part in name.split(" "):
                            if part == "-":
                                surname = surname[:-1] + part
                            elif part.isupper():
                                surname = surname + part + " "
                            elif first_name == "":
                                first_name = part
                            else:
                                second_name = part

                        writer.writerow((candidates_count, first_name, second_name, surname[:-1], committees_count))

                        candidates_count += 1

            committees_count += 1
finally:
    committeesCsv.close()
