import csv
import awoc
import pycountry

# Relative paths for CSVs
PIB = r".\res\API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4683825.csv"
ATHLETES = r".\res\athlete_events.csv"
ATHLETES_WITH_PIB = r".\res\athlete_events_with_pib.csv"

# Column index in the PIB CSV
PIB_C = 0
PIB_CC = 1
PIB_PIBS_START = 4
PIB_PIBS_END = 66

# Column index in the athletes CSV
ATHLETES_C = 6
ATHLETES_CC = 7
ATHLETES_YEAR = 9
ATHLETES_PIB = 15
ATHLETES_CONTINENT = 16

# Year in which the PIB data starts
BASE_YEAR = 1960

# Dictionary for country codes in the PIB CSV that need to be replaced for the athletes CSV
COUNTRY_CODES_REPLACE = {
    "BAH": "BHS", "BER": "BMU", "BRU": "BRN", "CAM": "KHM", "CGO": "COG", "DEN": "DNK", "GAM": "GMB", "GBS": "GNB",
    "GER": "DEU", "GRE": "GRC", "INA": "IDN", "IRI": "IRN", "ISV": "VIR", "LIB": "LBN", "MON": "MCO", "MYA": "MMR",
    "NED": "NLD", "PHI": "PHL", "POR": "PRT", "RSA": "ZAF", "SKN": "KNA", "SUI": "CHE", "UAR": "ARE", "URU": "URY",
    "VIN": "VCT", "ZIM": "ZWE"
}
# Countries in the athletes CSV that no longer exist
COUNTRY_CODES_NO_EXIST = ["URS", "FRG", "GDR", "MAL", "YUG", "TCH", "IOA", "SCG", "ROT",
                          "COK", "TPE", "RHO", "WIF", "PLE", "EUN", "AHO", "YMD", "YAR"]


# Creates a dictionary with countries as keys and their continent as the value
# Data pulled from the a-world-of-countries library
CONTINENTS = {}
def load_continents():
    world = awoc.AWOC()
    for world_country in world.get_countries():
        CONTINENTS[world_country["ISO3"]] = world_country["Continent Name"]


# Determines the proper country data using:
# - The country name provided in the athletes CSV
# - The country code provided in the PIB CSV
# - The country code provided in the athletes CSV
# Data pulled from the pycountries library

# Stores the proper country data of a PIB country code
COUNTRY_CACHE = {}
def get_proper_country(athletes_c, pib_cc, athletes_cc):
    # Get country from cache, returning an empty string if it not cached
    proper = COUNTRY_CACHE.get(pib_cc, "")

    # Repeatedly try to get the proper country until it succeeds
    if proper and proper != "":
        return proper
    elif proper != "":
        proper = pycountry.countries.get(alpha_3=pib_cc)
        if not proper:
            proper = pycountry.countries.get(alpha_3=athletes_cc)
        if not proper:
            proper = pycountry.countries.get(common_name=athletes_c)
        if not proper:
            proper = pycountry.countries.get(name=athletes_c)
        if not proper:
            print("Fuzzy on:", athletes_c)
            proper = pycountry.countries.search_fuzzy(athletes_c)[0]
            if proper:
                print("          Found", proper.name)

        COUNTRY_CACHE[pib_cc] = proper
        return proper


if __name__ == "__main__":
    # Obtain country PIBs and store together with the country and country code
    pibs_c = {}
    pibs_cc = {}
    with open(PIB) as pib_file:
        pib_reader = csv.reader(pib_file, delimiter=",")
        counter = 0
        headers = []
        for row in pib_reader:
            # Load headers from row 0
            if counter == 0:
                headers = row
            # Load data from all other rows
            else:
                country = row[PIB_C]
                country_code = row[PIB_CC]
                # Use the same dictionary object for both country and country codes dictionaries
                pibs_per_year = {}
                pibs_c[country] = pibs_per_year
                pibs_cc[country_code] = pibs_per_year
                # Load all PIBs for a country
                for pib_year in range(PIB_PIBS_START, PIB_PIBS_END):
                    pibs_per_year[headers[pib_year]] = row[pib_year]
            counter += 1

    # Generate all final athlete data
    athletes_with_pib = []
    load_continents()
    with open(ATHLETES) as athletes_file:
        athletes_reader = csv.reader(athletes_file, delimiter=",")
        counter = 0
        for row in athletes_reader:
            # Load headers from row 0
            if counter == 0:
                headers = row
                athletes_with_pib.append(row)
            # Load data from all other rows
            else:
                year = row[ATHLETES_YEAR]
                # Only add data from years after the BASE_YEAR
                if int(year) < BASE_YEAR:
                    continue
                # If multi national, take only the first country
                country = row[ATHLETES_C].split("/")[0]
                # Get the PIB country code from the athletes country code
                country_code = COUNTRY_CODES_REPLACE.get(row[ATHLETES_CC], row[ATHLETES_CC])
                apib_c = pibs_c.get(country, None)
                apib_cc = pibs_cc.get(country_code, None)
                pib = apib_c if apib_c else apib_cc
                # If PIB data was found
                if pib:
                    row[ATHLETES_PIB] = pib[year]
                    # Set the proper country data for the athlete
                    c = get_proper_country(country, country_code, row[ATHLETES_CC])
                    if c:
                        # alpha_3 is the 3 letter country code "standard"
                        row[ATHLETES_C] = c.name
                        row[ATHLETES_CC] = c.alpha_3
                        continent = CONTINENTS.get(c.alpha_3, None)
                        # Only add the country to the final CSV if it has all the proper data
                        if continent:
                            row[ATHLETES_CONTINENT] = continent
                            athletes_with_pib.append(row)
                        else:
                            print("Missing continent for:", c.name)
                    # Proper country not found
                    else:
                        print("Non ISO 3166:", country_code, row[ATHLETES_CC], country)
                else:
                    # If the country still exists but no PIB was found
                    if country_code not in COUNTRY_CODES_NO_EXIST:
                        print("Rogue country code:", country_code, country)
            counter += 1

    # Write out final CSV
    with open(ATHLETES_WITH_PIB, 'w', newline="") as apib_file:
        apib_writer = csv.writer(apib_file, delimiter=",")
        apib_writer.writerows(athletes_with_pib)
