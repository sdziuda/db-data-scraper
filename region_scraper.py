from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/organy_wyborcze/obwodowe/pl"
driver = webdriver.Chrome()
voivodeshipsCsv = open("voivodeships.csv", "w")
districtsCsv = open("districts.csv", "w")
municipalitiesCsv = open("municipalities.csv", "w")
localesCsv = open("locales.csv", "w")

driver.get(url)
time.sleep(1)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

voivodeships_count = 0
districts_count = 0
municipalities_count = 0
locales_count = 0

# scraping all HTML code containing voivodeships
body = soup.findAll("tbody")
voivodeships = body[2].findAll("tr")

try:
    writer = csv.writer(voivodeshipsCsv)
    writer.writerow(("id", "nazwa"))
    writer = csv.writer(districtsCsv)
    writer.writerow(("id", "id_wojewodztwa", "nazwa"))
    writer = csv.writer(municipalitiesCsv)
    writer.writerow(("id", "id_powiatu", "nazwa"))
    writer = csv.writer(localesCsv)
    writer.writerow(("id", "id_gminy", "siedziba"))

    for voivodeship in voivodeships:
        writer = csv.writer(voivodeshipsCsv)
        number = voivodeship.attrs["data-id"]
        name = voivodeship.findAll("td")[0].text
        writer.writerow((voivodeships_count, name))

        url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/organy_wyborcze/obwodowe/woj/" + number
        driver.get(url)
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # scraping all HTML code containing districts from this voivodeship
        body = soup.findAll("tbody")
        districts = body[2].findAll("tr")

        for district in districts:
            writer = csv.writer(districtsCsv)
            number = district.attrs["data-id"]
            name = district.findAll("td")[0].text
            writer.writerow((districts_count, voivodeships_count, name))

            if name[0].isupper() and name != "Warszawa":
                writer = csv.writer(municipalitiesCsv)
                writer.writerow((municipalities_count, districts_count, name))

                url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/organy_wyborcze/obwodowe/pow/" + number
                driver.get(url)
                time.sleep(1)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # scraping all HTML code containing locales from this city
                body = soup.findAll("tbody")
                locales = body[2].findAll("tr")

                for locale in locales:
                    writer = csv.writer(localesCsv)
                    name = locale.findAll("td")[1].text
                    writer.writerow((locales_count, municipalities_count, name))
                    locales_count += 1

                municipalities_count += 1
            else:
                url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/organy_wyborcze/obwodowe/pow/" + number
                driver.get(url)
                time.sleep(1)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # scraping all HTML code containing commitees from this district
                body = soup.findAll("tbody")
                municipalities = body[2].findAll("tr")

                for municipality in municipalities:
                    writer = csv.writer(municipalitiesCsv)
                    number = municipality.attrs["data-id"]
                    name = municipality.findAll("td")[0].text
                    writer.writerow((municipalities_count, districts_count, name))

                    url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/organy_wyborcze/obwodowe/gm/" + number
                    driver.get(url)
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    # scraping all HTML code containing locales from this district
                    body = soup.findAll("tbody")
                    locales = body[2].findAll("tr")

                    for locale in locales:
                        writer = csv.writer(localesCsv)
                        name = locale.findAll("td")[1].text
                        writer.writerow((locales_count, municipalities_count, name))
                        locales_count += 1

                    municipalities_count += 1

            districts_count += 1
            percent = string = "{:.2f}".format(municipalities_count / 2495 * 100)
            print(percent + "%")

        voivodeships_count += 1
finally:
    voivodeshipsCsv.close()
    districtsCsv.close()
    municipalitiesCsv.close()
    localesCsv.close()
