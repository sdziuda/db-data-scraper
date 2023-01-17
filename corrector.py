import csv

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
        writer.writerow((key[0], correctLocales[key], key[1]))
    else:
        writer.writerow((key[0], correctLocales[key], key[1][1:-1]))
