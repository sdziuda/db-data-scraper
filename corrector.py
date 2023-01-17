import csv
import numpy as np

inputCsv = open("res/locales.csv", "r", encoding="utf-8")
outputCsv = open("res/locales_corrected.csv", "w", encoding="utf-8")
writer = csv.writer(outputCsv)
correctLocales = {}

for r in inputCsv:
    r = r.strip()
    if len(r) > 0:
        localeId = r.split(",")[0]
        regionId = r.split(",")[1]
        localeName = ""
        for i in range(2, len(r.split(","))):
            localeName += r.split(",")[i] + ","
        localeName = localeName[:-1]
        correctLocales[(regionId, localeName)] = localeId

for key in correctLocales:
    if key[1] == "siedziba":
        writer.writerow((correctLocales[key], key[0], key[1]))
    else:
        writer.writerow((correctLocales[key], key[0], key[1][1:-1]))

inputCsv.close()
outputCsv.close()
inputCsv = np.loadtxt("res/results.csv", delimiter=",", dtype=str, skiprows=1, encoding="utf-8")
outputCsv = open("res/results_corrected.csv", "w", encoding="utf-8")
writer = csv.writer(outputCsv)
writer.writerow(("id_lokalu", "id_kandydata", "ile"))
correctResults = {}

for r in inputCsv:
    if (r[0], r[1]) not in correctResults:
        correctResults[(r[0], r[1])] = int(r[2])
    else:
        correctResults[(r[0], r[1])] += int(r[2])

for key in correctResults:
    writer.writerow((key[0], key[1], correctResults[key]))

