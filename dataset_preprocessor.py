import csv

PIB = r".\res\API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4683825.csv"
ATHLETES = r".\res\athlete_events.csv"
ATHLETES_WITH_PIB = r".\res\athlete_events_with_pib.csv"

PIB_C = 0
PIB_CC = 1
PIB_PIBS_START = 4
PIB_PIBS_END = 66

ATHLETES_C = 6
ATHLETES_CC = 7
ATHLETES_YEAR = 9
ATHLETES_PIB = 15

BASE_YEAR = 1960
COUNTRY_CODES_REPLACE = {
    "BAH": "BHS", "BER": "BMU", "BRU": "BRN", "CAM": "KHM", "CGO": "COG", "DEN": "DNK", "GAM": "GMB", "GBS": "GNB",
    "GER": "DEU", "GRE": "GRC", "INA": "IDN", "IRI": "IRN", "ISV": "VIR", "LIB": "LBN", "MON": "MCO", "MYA": "MMR",
    "NED": "NLD", "PHI": "PHL", "POR": "PRT", "RSA": "ZAF", "SKN": "KNA", "SUI": "CHE", "UAR": "ARE", "URU": "URY",
    "VIN": "VCT", "ZIM": "ZWE"
}
COUNTRY_CODES_NO_EXIST = ["URS", "FRG", "GDR", "MAL", "YUG", "TCH", "IOA", "SCG", "ROT",
                          "COK", "TPE", "RHO", "WIF", "PLE", "EUN", "AHO", "YMD", "YAR"]

if __name__ == "__main__":
    bad_countries = set()

    pibs_c = {}
    pibs_cc = {}
    with open(PIB) as pib_file:
        pib_reader = csv.reader(pib_file, delimiter=",")
        counter = 0
        headers = []
        for row in pib_reader:
            if counter == 0:
                headers = row
            else:
                country = row[PIB_C]
                country_code = row[PIB_CC]
                pibs_per_year = {}
                pibs_c[country] = pibs_per_year
                pibs_cc[country_code] = pibs_per_year
                for pib_year in range(PIB_PIBS_START, PIB_PIBS_END):
                    pibs_per_year[headers[pib_year]] = row[pib_year]
            counter += 1

    athletes_with_pib = []
    with open(ATHLETES) as athletes_file:
        athletes_reader = csv.reader(athletes_file, delimiter=",")
        counter = 0
        for row in athletes_reader:
            if counter == 0:
                headers = row
                athletes_with_pib.append(row)
            else:
                year = row[ATHLETES_YEAR]
                if int(year) < BASE_YEAR:
                    continue
                country = row[ATHLETES_C].split("/")[0]
                country_code = COUNTRY_CODES_REPLACE.get(row[ATHLETES_CC], row[ATHLETES_CC])
                apib_c = pibs_c.get(country, None)
                apib_cc = pibs_cc.get(country_code, None)
                if apib_cc:
                    row[ATHLETES_PIB] = apib_cc[year]
                elif apib_c:
                    row[ATHLETES_PIB] = apib_c[year]
                else:
                    print("Rogue country code:", country_code, country)
                    if country_code not in COUNTRY_CODES_NO_EXIST:
                        bad_countries.add(country_code + " " + country)
                athletes_with_pib.append(row)

            counter += 1

    print(bad_countries)

    with open(ATHLETES_WITH_PIB, 'w', newline="") as apib_file:
        apib_writer = csv.writer(apib_file, delimiter=",")
        apib_writer.writerows(athletes_with_pib)
