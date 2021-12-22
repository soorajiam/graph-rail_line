import csv
import time

# from graph_class import Graph, Vertex, Train
import tkinter as tk
import heapq
import json


def dijkstras_searching(graph, start, destination):
    print("starts search")
    print(f'Graph : {graph.name}')
    print(f'Starts at : {start}')
    print(f'Destination: {destination}')

    distances, parents = dijistras_short(graph, start)

    print(distances)
    print(parents)
    print(parents[destination.id])
    print(distances[destination.id])
    print(parents[start.id])
    print(distances[start.id])
    return distances, parents


def dijistras_short(graph, start, destination=None):
    distances = {vertex: float('inf') for vertex in graph.getVertices()}
    distances[start.id] = 0
    parents = {vertex: None for vertex in graph.getVertices()}
    queue = [(0, start.id)]
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        # relaxation
        if graph.vertDict[current_node].is_active:
            for weight, next_node in graph.vertDict[current_node].getConnections():
                distance_temp = current_distance + weight
                if distance_temp < distances[next_node]:
                    distances[next_node] = distance_temp
                    parents[next_node] = current_node
                    heapq.heappush(queue, (distance_temp, next_node))
    return distances, parents


class Vertex:
    def __init__(self, id, name, display_name, total_lines, rail):
        # Adding details of station to and as vertex.
        self.id = id
        self.name = name
        self.display_name = display_name
        self.total_lines = total_lines
        self.rail = rail
        self.adjacent = []
        self.is_active = True

    def __str__(self):
        return str(self.name)

    def addNeighbour(self, neighbour, weight=0):
        self.adjacent[neighbour] = weight

    def getConnections(self):
        edges = self.adjacent
        connections = []
        for edge in edges:
            edge = edge.get_connection(self)
            if edge:
                connections.append(edge)
        return connections

    def getId(self):
        return self.id

    def toggle_status(self):
        self.is_active = not self.is_active
        print(f'Station status is now {self.is_active}')

    # def getWeight(self, neighbour):
    #     return self.adjacent


class Train:
    trains = {}

    def __init__(self, id, name, colour, stripe):
        self.name = name
        self.id = id
        self.colour = colour
        self.stripe = stripe
        self.is_active = True

        Train.trains.update({
            id: self
        })

    def get_train(id):
        return Train.trains[id]

    def get_object_from_name(name):
        for train_id in Train.trains.keys():
            if name == Train.trains[train_id].name:
                return Train.trains[train_id]
        return None

    def toggle_status(self):
        self.is_active = not self.is_active
        print(f'Train status is now {self.is_active}')


class Edge:
    edges = []

    def check_duplicate(vertices):
        for edge in Edge.edges:
            if vertices == edge.vertices or vertices[::-1] == edge.vertices:
                return edge
            else:
                return False

    def __init__(self, graph, train_id, duration, vertices):
        # value = self.check_duplicate(vertices)
        # if not value:
        self.id = len(self.edges)
        self.graph = graph
        self.train = Train.get_train(train_id)
        self.duration = int(duration)
        self.vertices = vertices
        if self not in vertices[0].adjacent:
            vertices[0].adjacent.append(self)
        if self not in vertices[1].adjacent:
            vertices[1].adjacent.append(self)
        self.edges.append(self)

    def get_connection(self, vertex):
        if self.train.is_active:
            if vertex == self.vertices[0]:
                neighbour = self.vertices[1]
            else:
                neighbour = self.vertices[0]
            return int(self.duration), neighbour.id
        else:
            return None

    def __str__(self):
        return 'edge'


class Graph:
    def __init__(self, name):
        self.name = name
        self.vertDict = {}
        self.numVertices = 0

    def __iter__(self):
        return iter(self.vertDict.values())

    def addVertex(self, vertex):
        self.numVertices += 1
        self.vertDict[vertex.id] = vertex
        return vertex

    def getVertex(self, n):
        if n in self.vertDict:
            return self.vertDict[n]
        else:
            return None

    def print_graph(self):
        for vertex_name in self.getVertices():
            vertex = self.vertDict[vertex_name]
            print(vertex, len(vertex.adjacent), f'\t : {vertex.adjacent}')
            # print(vertex.getConnections())
            # print(vertex.getWeight())

    def getVertices(self):
        return self.vertDict.keys()

    def addEdge(self, vertex_1, vertex_2, train_id, duration=0):

        # since undirected graph, nodes sahll share the same values in both ways
        # creating edge object to better manage
        vertices = [self.vertDict[vertex_1],
                    self.vertDict[vertex_2]]
        edge = Edge.check_duplicate(vertices)
        # print(edge)
        if not edge:
            edge = Edge(graph=self,
                        train_id=train_id,
                        duration=duration,
                        vertices=vertices)
        return edge

    def get_named_dict_of_vertices(self):
        named_dict = {self.vertDict[v].name: self.vertDict[v] for v in self.getVertices()}
        return named_dict

    def search_dijistras(self, start, destination):
        start_vertex = self.vertDict[start]
        destination_vertex = self.vertDict[destination]
        distances, parents = dijkstras_searching(self, start_vertex, destination_vertex)
        distance = distances[destination]
        if distance == float("inf"):
            print("Path does not exist")
            path = []
            distance = "Infinity"
        # print("TESSST",parents)
        else:
            path = self.build_path(start, destination, parents)
            print(path)
        return distance, path

    def build_short_matrix(self):
        short_paths = {}
        for vertex in self.getVertices():
            distances, parents = dijistras_short(self, self.vertDict[vertex])
            short_paths[vertex] = {
                'distances': distances,
                'parents': parents
            }
        with open('data.json', 'w') as fp:
            json.dump(short_paths, fp)
        fp.close()

    def search_after_map_build(self, start, destination):

        with open('data.json', 'r') as f:
            paths = json.load(f)

        f.close()
        path_searched = paths[start]
        distance = path_searched["distances"][destination]
        print(f'distance: {distance}')
        if distance == float("inf"):
            print("Path does not exist")
            path = []
            distance = "Infinity"
        else:
            path = self.build_path(start, destination, path_searched['parents'])
            print(path)
        return distance, path

    def build_path(self, start, destination, parents):
        current_vertex = destination
        path = []
        while start != current_vertex:
            path.append(current_vertex)
            current_vertex = parents[current_vertex]
        path.append(start)
        return path
        # print(short_paths)


class RoutingApp():
    count = 0

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.build_graph()
        print("Graph built")
        self.station_reference = self.graph.get_named_dict_of_vertices()

        self.start = tk.StringVar()
        self.destination = tk.StringVar()
        self.search_in_map = 0

        self.set_ui()
        print("UI built")
        self.manage_window_access = None
        self.window_access_values = {}
        self.draw_manage_buttons()
        print("manage buttons drawn on application")
        self.initialize()
        print("UI ran ")

    def initialize(self):
        self.root.mainloop()

    def manage_window_house_keeping(self):
        if self.manage_window_access:
            self.manage_window_access.destroy()
            self.window_access_values = {}

    def build_graph(self):
        self.graph = build_rail_graph()

    def create_drop_down(self, variable, listing, root=None):
        root = root if root else self.root
        return tk.OptionMenu(root, variable, *listing)

    def create_button(self, text, command=None, root=None):
        root = root if root else self.root
        return tk.Button(root, text=text, command=command)

    def set_ui(self):

        self.stations_list = sorted(self.station_reference.keys())
        self.start.set("--select station--")
        start_station_drop = self.create_drop_down(self.start, self.stations_list)
        start_station_drop.pack()
        # destination_station_drop =

        self.destination.set("--select station--")
        destination_station_drop = self.create_drop_down(self.destination, self.stations_list)
        destination_station_drop.pack()

        search_button = self.create_button(text='search', command=self.search_network).pack()

    def create_manage_station_window(self):
        def station_window_call_back(*args):
            station_name = station_setting.get()
            station = self.station_reference[station_name]
            print(station.is_active)
            button_text = tk.StringVar()
            button_text.set(
                f'Toggle Station status({station.is_active})'
            )
            try:
                if self.window_access_values['status']:
                    print('tries to delete')
                    self.window_access_values['status'].pack_forget()
            except:
                print("element not generated")
            self.window_access_values['status']  = tk.Button(station_window,
                                      text=button_text.get(),
                                      command=lambda: station.toggle_status())
            self.window_access_values['status'].pack()
            print(station.is_active)

            print(station)

        self.manage_window_house_keeping()
        self.manage_window_access = tk.Toplevel(self.root)
        station_window = self.manage_window_access
        station_window.geometry("400x400")

        station_setting = tk.StringVar()
        station_setting.set("--select station--")
        station_setting.trace("w", station_window_call_back)
        station_drop = tk.OptionMenu(station_window, station_setting, *self.stations_list)
        station_drop.pack()

        close_station_button = tk.Button(station_window,
                                         text="cancel",
                                         command=station_window.destroy).pack()

    def create_manage_train_window(self):
        def train_window_call_back(*args):
            train_name = train_setting.get()
            train = Train.get_object_from_name(train_name)
            print(train.is_active)
            button_text = tk.StringVar()
            button_text.set(
                f'Toggle train status({train.is_active})'
            )
            try:
                if self.window_access_values['status']:
                    print('tries to delete')
                    self.window_access_values['status'].pack_forget()
            except:
                print("element not generated")
            self.window_access_values['status'] = tk.Button(train_window,
                                     text=button_text.get(),
                                     command=lambda: train.toggle_status())
            self.window_access_values['status'].pack()
            print(train.is_active)

            print(train)

        self.manage_window_house_keeping()
        self.manage_window_access = tk.Toplevel(self.root)
        train_window = self.manage_window_access
        train_window.geometry("400x400")

        trains = Train.trains
        train_names = [Train.trains[id].name for id in Train.trains.keys()]
        train_setting = tk.StringVar()
        train_setting.set("--select train--")
        train_setting.trace("w", train_window_call_back)
        train_drop = tk.OptionMenu(train_window, train_setting, *train_names)
        train_drop.pack()

        close_train_button = tk.Button(train_window,
                                       text="cancel",
                                       command=train_window.destroy).pack()

    def search_network(self):
        count_begin = time.time()
        start_vertex = self.station_reference[self.start.get()]
        destination_vertex = self.station_reference[self.destination.get()]
        start_text = f'station name{start_vertex.name}   id: {start_vertex.id}'
        destination_text = f'station name{destination_vertex.name}   id: {destination_vertex.id}'
        display_start = tk.Label(text=start_text).pack()
        display_destination = tk.Label(text=destination_text).pack()
        if self.search_in_map:
            distance, path = self.graph.search_after_map_build(
                str(start_vertex.id),
                str(destination_vertex.id))
        else:
            distance, path = self.graph.search_dijistras(
                str(start_vertex.id),
                str(destination_vertex.id))
        shortest_path_duration_text = f'shortest duration : {distance} '
        shortest_path_duration_label = tk.Label(text=shortest_path_duration_text).pack()
        shortest_path_text = f'path: {str(path)} '
        shortest_path_duration_label = tk.Label(text=shortest_path_text).pack()
        count_end = time.time()
        time_for_search = tk.Label(text=str(count_end - count_begin)).pack()

    def draw_manage_buttons(self):
        manage_station_button = tk.Button(self.root,
                                          text="manage stations",
                                          command=self.create_manage_station_window)

        manage_station_button.pack()

        manage_train_button = tk.Button(self.root,
                                        text="manage trains",
                                        command=self.create_manage_train_window)

        manage_train_button.pack()

        close_application_button = tk.Button(self.root,
                                             text="close application",
                                             command=self.root.destroy).pack()


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
                          name=row[1],  # replace('"', ''),
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


instance1 = RoutingApp()
