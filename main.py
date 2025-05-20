from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import make_interp_spline
import numpy as np
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

db = sqlite3.connect('backset.db')
cursor = db.cursor()

country_of_interest = 'United States' 
def get_data(country_of_interest):
    # Schema is {
    # year: (spending, emmissions)   
    #}
    data_by_year = {}

    cursor.execute(f'SELECT * FROM main where country = "{country_of_interest}"')
    rows = cursor.fetchall()
    for row in rows:
        year = row[3]
        emmis_per_year = cursor.execute(f'SELECT quantity FROM co2e where country = "{country_of_interest}" and year = {year}').fetchall()
        if len(emmis_per_year) == 0:
            continue
        data_by_year[row[3]] = (int(str(row[5]).replace(" ", "")), (emmis_per_year)[0][0])


    # Sort data by year to ensure proper plotting
    years = sorted(list(data_by_year.keys()))
    # Convert years to integers for plotting
    years_numeric = [int(year) for year in years]
    # Get spending and emissions data
    spending = [data_by_year[year][0] for year in years]
    emissions = [data_by_year[year][1] for year in years]
    return years_numeric, spending, emissions

countries_of_interest = ['United States', 'China', 'India', 'Germany', 'France', 'Brazil', 'Japan', 'Russia', 'South Korea', 'Canada']
data_by_country = {}
for country in countries_of_interest:
    data_by_country[country] = get_data(country)
# Create a 3d plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Set the title and labels
ax.set_title('Spending vs Emissions')
ax.set_xlabel('Year')
ax.set_ylabel('Spending')
ax.set_zlabel('Emissions')
# Set the x, y, and z limits
ax.set_xlim([2000, 2025])
ax.set_ylim([0, 2000000000])
ax.set_zlim([0, 2000000000])
# Set the x, y, and z ticks
ax.set_xticks(np.arange(2000, 2025, 1))
ax.set_yticks(np.arange(0, 2000000000, 500000000))
ax.set_zticks(np.arange(0, 2000000000, 500000000))
# Set the x, y, and z tick labels
ax.set_xticklabels(np.arange(2000, 2025, 1))
ax.set_yticklabels(np.arange(0, 2000000000, 500000000))
ax.set_zticklabels(np.arange(0, 2000000000, 500000000))
# Plot the data
for country, data in data_by_country.items():
    years, spending, emissions = data
    # Plot the data directly without using spline interpolation
    ax.plot(years, spending, emissions, label=country)
# Add a legend
ax.legend()
# Show the plot
plt.show()
# Close the database connection
db.close()