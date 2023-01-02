from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import numpy as np

inputCsv = np.loadtxt("res/candidates.csv", delimiter=",", dtype=str, skiprows=1, encoding="utf-8")
candidatesToId = {}

for r in inputCsv:
    if r[2] != "":
        candidatesToId[(r[3] + r[1] + r[2]).replace(" ", "").encode()] = r[0]
    else:
        candidatesToId[(r[3] + r[1]).replace(" ", "").encode()] = r[0]

inputCsv = open("res/locales.csv", "r", encoding="utf-8")
localesToId = {}

for r in inputCsv:
    r = r.strip()
    if len(r) > 0:
        localeId = r.split(",")[0]
        localeName = r.split(",")[2:]
        localeName = "".join(localeName)
        localeName = localeName.replace("\"", "")
        localesToId[localeName] = localeId

resultsCsv = open("res/results.csv", "w", encoding="utf-8")
writer = csv.writer(resultsCsv)
writer.writerow(("id_lokalu", "id_kandydata", "ile"))
url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/wyniki/sejm/pl"
driver = webdriver.Chrome()

driver.get(url)
time.sleep(1)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

body = soup.findAll("tbody")
regions = body[4].findAll("tr")
locale_count = 0

for region in regions:
    regionId = region.attrs["data-id"]

    url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/wyniki/sejm/okr/" + regionId

    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    body = soup.findAll("tbody")
    districts = body[4].findAll("tr")

    if regionId == "19":
        districts = districts[0:1]

    for district in districts:
        districtId = district.attrs["data-id"]
        if regionId == "19":
            districtName = district.findAll("td")[0].text
        else:
            districtName = district.findAll("td")[1].text

        url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/wyniki/sejm/pow/" + districtId

        driver.get(url)
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        body = soup.findAll("tbody")

        if districtName[0].isupper() and districtName != "Warszawa":
            locales = body[5].findAll("tr")

            for locale in locales:
                localeName = locale.findAll("td")[1].text
                localeName = localeName.replace(",", "")
                localeName = localeName.replace("\"", "")
                localeId = localesToId[localeName]
                localeWebId = locale.attrs["data-id"]

                url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/wyniki/protokol/sejm/" + localeWebId

                driver.get(url)
                time.sleep(1)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                bodies = soup.findAll("tbody")[5:]
                for body in bodies:
                    candidates = body.findAll("tr")
                    for candidate in candidates:
                        candidateName = candidate.findAll("td")[1].text
                        candidateName = candidateName.replace(" ", "")
                        candidateId = candidatesToId[candidateName.encode()]
                        votes = candidate.findAll("td")[2].getText()
                        votes = votes.lstrip("0")

                        if votes == "":
                            votes = "0"
                        else:
                            votes = votes[0:int(len(votes) / 2)]

                        writer.writerow((localeId, candidateId, votes))
                locale_count += 1
            percent = locale_count / 27187 * 100
            print("Progress: " + str(percent) + "%")
        else:
            municipalities = body[4].findAll("tr")

            for municipality in municipalities:
                municipalityId = municipality.attrs["data-id"]

                url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/wyniki/sejm/gm/" + municipalityId

                driver.get(url)
                time.sleep(1)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                body = soup.findAll("div", {"class": "proto"})
                tables = body[0].findAll("div", {"class": "table-responsive"})

                while len(tables) == 0:
                    time.sleep(0.2)
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    body = soup.findAll("div", {"class": "proto"})
                    tables = body[0].findAll("div", {"class": "table-responsive"})

                locales = tables[0].findAll("tr")

                for locale in locales[1:]:
                    localeName = locale.findAll("td")[1].text
                    localeName = localeName.replace(",", "")
                    localeName = localeName.replace("\"", "")
                    localeId = localesToId[localeName]
                    localeWebId = locale.attrs["data-id"]

                    url = "https://sejmsenat2019.pkw.gov.pl/sejmsenat2019/pl/wyniki/protokol/sejm/" + localeWebId

                    driver.get(url)
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    bodies = soup.findAll("tbody")[5:]
                    for body in bodies:
                        candidates = body.findAll("tr")
                        for candidate in candidates:
                            candidateName = candidate.findAll("td")[1].text
                            candidateName = candidateName.replace(" ", "")
                            candidateId = candidatesToId[candidateName.encode()]
                            votes = candidate.findAll("td")[2].getText()
                            votes = votes.lstrip("0")

                            if votes == "":
                                votes = "0"
                            else:
                                votes = votes[0:int(len(votes) / 2)]

                            writer.writerow((localeId, candidateId, votes))
                    locale_count += 1
                percent = locale_count / 27187 * 100
                print("Progress: " + str(percent) + "%")

resultsCsv.close()
