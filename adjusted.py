import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

db = sqlite3.connect('backset.db')
cursor = db.cursor()

sr_y = {}
get_spend_ratio = lambda row, sr: (sr + (row[2] / row[4])) / 2
get_em_pp = lambda row, em: (em + (row[3] / row[5])) / 2
for i in range(2020, 2024):
    cursor.execute('SELECT * FROM fullpull WHERE year = ?', (i,))
    rows = cursor.fetchall()
    av_spend_ratio = 0.001
    av_em_pp = 0.001
    for row in rows:
        av_spend_ratio = get_spend_ratio(row, av_spend_ratio)
        av_em_pp = get_em_pp(row, av_em_pp)
    sr_y[i] = (av_spend_ratio, av_em_pp)
for item in sr_y:
    sr_y[item] = (sr_y[item][0] * 100, sr_y[item][1])
[print(sr_y[x]) for x in sr_y]


plt.figure(figsize=(10, 5))
plt.title('Worldwide Percentate of GDP Spent on Green Energy')
plt.xlabel('Year')
plt.ylabel('Percentage of GDP')
plt.xticks(list(sr_y.keys()))
plt.plot(list(sr_y.keys()), [sr_y[x][0] for x in sr_y], label='Percentage', marker='o')
plt.legend()
plt.grid()
plt.show()

from mpl_toolkits.mplot3d import Axes3D

# Extract data for the plot
years = list(sr_y.keys())
gdp_pcts = [sr_y[year][0] for year in years]
em_pp_vals = [sr_y[year][1] for year in years]

# Create a 3D scatter plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the scatter points
sc = ax.scatter(years, gdp_pcts, em_pp_vals, c=years, cmap='viridis', s=100, marker='o')

# Add a line connecting the points
ax.plot(years, gdp_pcts, em_pp_vals, 'r-', linewidth=2, alpha=0.6)

# Add labels and title
ax.set_xlabel('Year')
ax.set_ylabel('GDP Percentage Spent on Green Energy')
ax.set_zlabel('Emissions per Population')
ax.set_title('Year vs GDP % vs Emissions per Population')

# Set specific ticks for the years
ax.set_xticks(years)

# Add text labels to each point
for year, gdp, em in zip(years, gdp_pcts, em_pp_vals):
    ax.text(year, gdp, em, f'{year}', size=10, zorder=1)

plt.tight_layout()
plt.show()

# Create a 3D scatter plot of all countries data
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Get all country data from the database
cursor.execute('SELECT country, year, spending, emissions, gdp, population FROM fullpull')
all_data = cursor.fetchall()

# Calculate ratios for each country
countries = []
years_data = []
spend_gdp_ratios = []
emission_pop_ratios = []

for row in all_data:
    country, year, spend, emissions, gdp, population = row
    if gdp and population:  # Avoid division by zero
        spend_gdp_ratio = spend / gdp * 100  # As percentage
        emission_pop_ratio = emissions / population
        
        countries.append(country)
        years_data.append(int(year))
        spend_gdp_ratios.append(spend_gdp_ratio)
        emission_pop_ratios.append(emission_pop_ratio)

# Create scatter plot with color mapped to year
scatter = ax.scatter(
    emission_pop_ratios, 
    spend_gdp_ratios, 
    years_data, 
    c=years_data, 
    cmap='viridis',
    s=50,
    alpha=0.7
)

# Add labels and title
ax.set_xlabel('Emissions per Population')
ax.set_ylabel('Green Energy Spend (% of GDP)')
ax.set_zlabel('Year')
ax.set_title('3D Scatter: Emissions per Population vs Green Energy Spend vs Year for All Countries')

# Add colorbar
cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label('Year')

# Optionally, highlight specific countries or add annotations for a subset of points
# This is a randomly selected subset to avoid cluttering the plot
for i in range(0, len(countries), 20):
    ax.text(
        emission_pop_ratios[i], 
        spend_gdp_ratios[i], 
        years_data[i], 
        countries[i],
        size=8
    )

plt.tight_layout()
plt.show()