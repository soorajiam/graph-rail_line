import csv
from graph_class import Graph, Vertex, Train


# CSV library used to parse csv files

# assigns the file location of each files to variables
def build_rail_graph():
    london_connections_file = 'data/londonconnections.csv'
    london_lines_file = 'data/londonlines.csv'
    london_stations_file = 'data/londonstations.csv'

    # Initializes the rail graph
    rail_graph = Graph("Rail Graph")

    # reading london lines
    with open(london_stations_file, newline='') as csvfile:
        spam_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(spam_reader)
        for row in spam_reader:
            # print(row)
            # new vertex object is created
            new_vertex = Vertex(
                id=row[0],
                name=row[3].replace('"', ''),
                display_name=row[4],
                total_lines=row[5],
                rail=row[6]
            )
            # print(new_vertex)
            # new vertex is added to the graph
            rail_graph.addVertex(new_vertex)

    # # reading london lines
    train_lines = {}
    with open(london_lines_file, newline='') as csvfile:
        spam_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(spam_reader)
        for row in spam_reader:
            # print(row)
            # name_id = row[0].split(',')
            # creating a dictionary reference for train info
            train = Train(id=row[0],
                          name=row[1],#replace('"', ''),
                          colour=row[2],
                          stripe=row[3])
    # print(train_lines)

    # checking uniqueness
    unique_station_lines = []
    duplicate_connections = []

    # reading connections between them
    with open(london_connections_file, newline='') as csvfile:
        spam_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(spam_reader)
        for row in spam_reader:
            # print(row)
            rail_graph.addEdge(
                vertex_1=row[0],
                vertex_2=row[1],
                train_id=row[2],
                duration=row[3]
            )

        rail_graph.print_graph()
        rail_graph.build_short_matrix()
        rail_graph.search_after_map_build('281', '298')
    return rail_graph
