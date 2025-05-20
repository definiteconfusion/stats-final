import sqlite3
import csv

db = sqlite3.connect('backset.db')
c = db.cursor()

stat_data = {}

with open('co2em.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[0] in stat_data:
            stat_data[row[0]].append((row[1], row[25]))
        else:
            stat_data[row[0]] = [(row[1], row[25])]
        
for key in stat_data:
    for item in stat_data[key]:
        c.execute('''INSERT INTO co2e (country, year, quantity) VALUES (?, ?, ?)''', (key, item[0], item[1]))
        
db.commit()