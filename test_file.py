print("testing")
# figuring out how to read CSV
import csv
london_connections_file = 'data/londonconnections.csv'
london_lines_file = 'data/londonlines.csv'
london_stations_file = 'data/londonstations.csv'

# reading london stations
with open(london_stations_file, newline='') as csvfile:
    spam_reader = csv.reader(csvfile, delimiter=' ', quotechar = '|')
    for row in spam_reader:
        print(row)
        print(', '.join(row))

# reading london lines
with open(london_lines_file, newline='') as csvfile:
    spam_reader = csv.reader(csvfile, delimiter=' ', quotechar = '|')
    for row in spam_reader:
        print(row)
        print(', '.join(row))