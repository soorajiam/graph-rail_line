print("testing")
# figuring out how to read CSV
import csv
london_connections_file = 'data/londonconnections.csv'
london_lines_file = 'data/londonlines.csv'
london_stations_file = 'data/londonstations.csv'

from pyvis.network import Network
rail_network = Network(directed=True)
rail_network.add_node(0)

# reading london stations
with open(london_stations_file, newline='') as csvfile:
    spam_reader = csv.reader(csvfile, delimiter=',', quotechar = '|')
    for row in spam_reader:
        print(row)
#         row = row[0].split(',')
        rail_network.add_node(row[0], title=row[0])

# 
train_lines = {}
with open(london_lines_file, newline='') as csvfile:
    spam_reader = csv.reader(csvfile, delimiter=',', quotechar = '|')
    for row in spam_reader:
        # print(row)
        # name_id = row[0].split(',')
        train_lines.update({row[0]: [row[1], row[2]]})

# checking uniqueness
unique_station_lines = []
duplicate_connections = []
# reading connections between them
with open(london_connections_file, newline='') as csvfile:
    spam_reader = csv.reader(csvfile, delimiter=' ', quotechar = '|')
    for row in spam_reader:
        row = row[0].split(',')
        try:
            connection = [row[0], row[1]]
            if connection not in unique_station_lines:
                unique_station_lines.append(connection)
            else:
                print("OOOYYEE")
                duplicate_connections.append(connection)
                print(connection)
            title = f'{train_lines[row[2]][0]}({row[3]})'
            rail_network.add_edge(
                row[0],
                row[1],
                title=title,
                weight=row[3],
                color=train_lines[row[2]][0]
            )
        except:
            print(row)
        # print(row)
rail_network.show("rail_network.html")

from pyvis.network import Network
net = Network(directed=True)
net.add_node(0)
net.add_node(1)
net.add_edge(0, 1, title='t1')
net.add_edge(0, 0, value=2)
net.add_edge(1, 0,value=5,  title='t2')
net.show("net_example.html")
print(train_lines)
print(duplicate_connections)

# import networkx