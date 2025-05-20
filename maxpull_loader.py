import csv
import sqlite3

# measuring from 2020 to 2025

with open('population_dataset.csv', 'r') as f:
    population_reader = csv.reader(f)
    population_header = next(population_reader)
    population_data = [row for row in population_reader]
    
with open('gdp_dataset.csv', 'r') as f:
    gdp_reader = csv.reader(f)
    gdp_header = next(gdp_reader)
    gdp_data = [row for row in gdp_reader]

db = sqlite3.connect('backset.db')
c = db.cursor()
def get_spending(country_of_interest, year):
    spending = c.execute(f"SELECT budget FROM main WHERE country = '{country_of_interest}' and start_year = '{year}'").fetchall()
    for k in range(len(spending)):
        spending[k] = int(str(spending[k][0]).replace(" ", ""))
    sSpending = sum(spending)
    return sSpending

def get_emissions(country_of_interest, year):
    emissions = c.execute(f"SELECT quantity FROM co2e WHERE country = '{country_of_interest}' and year = '{year}'").fetchall()
    return emissions[0][0] if emissions else 0

# schema: (country, year, spending, emissions, gdp, population)
for set_ind in range(len(population_data)):
    try:
        for year in range(2020, 2026):
            country = population_data[set_ind][0]
            population = population_data[set_ind][year - 2020 + 64]
            gdp = gdp_data[set_ind][year - 2020 + 64]
            spending = get_spending(country, year)
            emissions = get_emissions(country, year)
            c.execute('''INSERT INTO fullpull (country, year, spending, emissions, gdp, population) VALUES (?, ?, ?, ?, ?, ?)''', (country, year, spending, emissions, gdp, population))
    except Exception as e:
        print(f"Error processing data for {population_data[set_ind][0]} in year {year}: {e}")
        continue
db.commit()
db.close()