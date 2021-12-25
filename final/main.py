"""
Written by Sooraj Parakkattil Ravi
Student id: 2102360301
SYSTEM DESIGN AND PROGRAMMING COURSEWORK
written on Python 3.9.9 (main, Dec  2 2021, 14:40:02)
machine: Macbook Air M1 (the ARM version- different execution behaviour is expected.)

Requirements:
    the csv file locations:
        'data/londonconnections.csv'
        'data/londonlines.csv'
        'data/londonstations.csv'
"""
import csv
import heapq
import json
import time
import tkinter as tk
from tkinter import messagebox


def graph_searching(graph, start, destination=None):
    """
    Function to accommodate searching in-case different algorithms
     are used.
     Param:
        graph:(User-defined class) graph data type(
            undirected, weighted)
        start: (Vertex/Node) vertex of graph from which distances
            will be calculated from Dijikstra's
        destination:(Vertex/Node) vertex of graph (end condition for algorithm).

    return:
        distances(dictionary): distance from start -> each node.
                node_id is key
        parents(dictionary): The route taken from each node(node->next node)
                node_id is the key

    """
    distances, parents = dijikstras_short(graph, start)
    return distances, parents


def dijikstras_short(graph, start, destination=None):
    """
    Implementation of Dijikstra's using heap.

     Param:
        graph:(User-defined class) graph data type(
            undirected, weighted)
        start: (Vertex/Node) vertex of graph from which distances
            will be calculated from Dijikstra's
        destination:(Vertex/Node) vertex of graph (end condition for algorithm).

    return:
        distances(dictionary): distance from start -> each node.
                node_id is key
        parents(dictionary): The route taken from each node(node->next node)
                node_id is the key
    """
    # initializes all vertices with the largest distance 'infinity'
    distances = {vertex: float('inf') for vertex in graph.getVertices()}
    # sets the start node as 0
    distances[start.id] = 0
    # makes parent map of vertices to None
    parents = {vertex: None for vertex in graph.getVertices()}
    # initializes the queue
    queue = [(0, start.id)]
    while queue:
        # executes till queue is empty
        current_distance, current_node = heapq.heappop(queue)
        # The pair is added to  heap queue
        if graph.vertDict[current_node].is_active:
            # checks the activeness of station
            for weight, next_node in graph.vertDict[current_node].getConnections():
                # loops through all the edges
                distance_temp = current_distance + weight
                if distance_temp < distances[next_node]:
                    # checks if there is a shorter path
                    distances[next_node] = distance_temp
                    # marks teh shortest distances
                    parents[next_node] = current_node
                    # maps the low-weight nearest neighbour
                    heapq.heappush(queue, (distance_temp, next_node))
                    # pops the next node from the heap queue
    return distances, parents


class Vertex:
    def __init__(self, _id, name, display_name, total_lines, rail):
        """
        Initialize a vertex/Node.

        Param:

            id: (str) StationID
            name: (str) Station name
            display_name: (str) Station display name(but has a lot of issues)
            total_lines: (str) number of lines
            rail: (str) type of rail?(un-used)
        """
        # Adding details of station to and as vertex.
        self.id = _id
        #ID of the node
        self.name = name
        # name of the station
        self.display_name = display_name
        self.total_lines = total_lines
        self.rail = rail
        # adjecency list is kept to store edges
        self.adjacent = []
        # Sets a flag to deactivate the node/ station when toggled
        self.is_active = True

    def __str__(self):
        """
        Names the Class(Dunder method)
        :return:
            name(str): name of the station
        """
        return str(self.name)
    def has_active_edge(self):
        """
        Checks if the edge has active edge(making it accessible)
        :return:
            Bool
        """
        for edge in self.adjacent:
            if edge.train.is_active:
                return True
        return False

    def addNeighbour(self, neighbour, weight=0):
        """
        Adds an edge to the vertex
        Params:
            neighbour(classs): neighbouring vertex
            weight(int): the duration to travel to the neighbour

        :return: None
        """
        self.adjacent[neighbour] = weight

    def getConnections(self):
        """
        Returns the connected vertices
        :return:
            connections(list): list of edges
        """
        edges = self.adjacent
        connections = []
        for edge in edges:
            edge = edge.get_connection(self)
            if edge:
                connections.append(edge)
        return connections

    def toggle_status(self, application):
        """
        Toggles current active state of the station
        Params:
            application(class): The whole application
                is passed to redraw manage window
        :return: None
        """
        self.is_active = not self.is_active
        application.create_manage_station_window()
        # print(f'Station status is now {self.is_active}')

    def get_edge_from_vertex(self, neighbour):
        """
        Returns the edge connected with the neighbour
        Param:
         neighbour(class): Graph vertex object
        return:
            edge(class) : Edge class object
        """
        edges = self.adjacent
        for edge in edges:
            neighbor = edge.get_neighbor(neighbour)
            if neighbor:
                return edge
        return None


class Train:
    """
    Class train
        attributes:
            trains(dict): holds all the train
                objects created with id as key
    """
    trains = {}

    def __init__(self, id, name, colour, stripe):
        """

        :param id:
        :param name:
        :param colour:
        :param stripe:
        """
        #train name
        self.name = name
        #train id
        self.id = id
        #train color
        self.colour = colour
        self.stripe = stripe
        #active status of the train
        self.is_active = True
        #update when new trains are created
        Train.trains.update({
            id: self
        })

    def get_train(_id):
        """
        Returns the train object w.r.t to id

        Params:
            _id(str): the id of the train
        return:
            train(class): Train object
        """
        return Train.trains[_id]

    def get_object_from_name(name):
        """
        Returns the train object w.r.t to name

        Params:
            name(str): name of the train
        returns:
            train(Class): object of train class or None
        """
        for train_id in Train.trains.keys():
            if name == Train.trains[train_id].name:
                return Train.trains[train_id]
        return None

    def toggle_status(self, application):
        """
        Toggles current active state of the train

        Params:
            application(class): The whole application
            is passed to redraw manage window
        :return: None
        """
        self.is_active = not self.is_active
        application.create_manage_train_window()
        # print(f'Train status is now {self.is_active}')


class Edge:
    """
    Edge Class

    Attributes:
        edges(list): list of all object instances
    """
    edges = []

    def check_duplicate(vertices):
        """
        Checks if a duplicate edge exists or not

        Param:
            vertices(list): list of 2 neighbouring vertices
        return:
            edge(class): Edge object or False
        """
        #makes sure the edge is not duplicated.
        for edge in Edge.edges:
            if vertices == edge.vertices or vertices[::-1] == edge.vertices:
                #checks the order
                return edge
            else:
                return False

    def __init__(self, graph, train_id, duration, vertices):
        """

        :param graph:
        :param train_id:
        :param duration:
        :param vertices:
        """
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
        """
        Returns the weight and the neighbouring vertex
        param:
            vertex(class): Vertex class object
        return: None
        """
        if self.train.is_active:
            if vertex == self.vertices[0]:
                neighbour = self.vertices[1]
            else:
                neighbour = self.vertices[0]
            return int(self.duration), neighbour.id
        else:
            return None

    def get_neighbor(self, vertex):
        """
        Returns the neighbouring vertex w.r.t the vertex provided in the edge
        param:
            vertex(class): Vertex class object
        return
            : neighbour vertex or none
        """
        if self.train.is_active:
            neighbour = None
            if vertex == self.vertices[0]:
                neighbour = self.vertices[1]
            else:
                neighbour = self.vertices[0]
            return neighbour
        else:
            return None

    def __str__(self):
        return 'edge'


class Graph:
    """
    Graph Class
    """

    def __init__(self, name):
        """

        :param name:
        """
        self.name = name
        self.vertDict = {}
        self.numVertices = 0

    def __iter__(self):
        return iter(self.vertDict.values())

    def addVertex(self, vertex):
        """
        Adding vertex to the graph
        param:
            vertex(class): Vertex object
        return:
            vertex class object
        """
        self.numVertices += 1
        self.vertDict[vertex.id] = vertex
        return vertex

    def print_graph(self):
        """
        Print the graph
        :return: None
        """
        for vertex_name in self.getVertices():
            vertex = self.vertDict[vertex_name]
            # print(vertex, len(vertex.adjacent), f'\t : {vertex.adjacent}')
            # print(vertex.getConnections())
            # print(vertex.getWeight())

    def getVertices(self):
        """
        Get all the vertex labels
        :return:
            (list): list of station id's
        """
        return self.vertDict.keys()

    def addEdge(self, vertex_1, vertex_2, train_id, duration=0):
        """
        Adding an edge to the graph. Weighted graph
        :param:
            vertex_1(class): vertex object
            vertex_2(class): vertex object
            train_id(str): train id which connects the graph
            duration(int): weight of the edge.
        return:
            edge(class): Edge object
        """

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
        """
        Returns a dictionary with names as keys(vertices)
        :return:
            named_dict(dict): key is names of stations
        """
        named_dict = {self.vertDict[v].name: self.vertDict[v] for v in self.getVertices()}
        return named_dict

    def search_graph(self, start, destination):
        """
        Handling search inside the graph
        param:
            start(str): the id of start station
            destination(str): the id of the destination node
        :return:
            distance(float): distance from start -> destination
            path(list): The route taken for shortest distance
        """
        start_vertex = self.vertDict[start]
        destination_vertex = self.vertDict[destination]
        distances, parents = graph_searching(self, start_vertex, destination_vertex)
        distance = distances[destination]
        if distance == float("inf"):
            # print("Path does not exist")
            path = []
            distance = "Infinity"
        # print("TESSST",parents)
        else:
            path = self.build_path(start, destination, parents)
            # print(path)
        return distance, path

    def build_short_matrix(self):
        """
        Builds the matrix of shortest path for the whole graph
         and saves it as file for later use if required.
        :return:
            None
        """
        short_paths = {}
        for vertex in self.getVertices():
            distances, parents = dijikstras_short(self, self.vertDict[vertex])
            short_paths[vertex] = {
                'distances': distances,
                'parents': parents
            }
        with open('data.json', 'w') as fp:
            json.dump(short_paths, fp)
        fp.close()

    def search_after_map_build(self, start, destination):
        """
        Searches the graph shortest path matrix saved to file.
        :param:
            start(str): the id of start station
            destination(str): the id of the destination node
        :return:
            distance(float): distance from start -> destination
            path(list): The route taken for shortest distance
        """

        with open('data.json', 'r') as f:
            paths = json.load(f)

        f.close()
        path_searched = paths[start]
        distance = path_searched["distances"][destination]
        # print(f'distance: {distance}')
        if distance == float("inf"):
            # print("Path does not exist")
            path = []
            distance = "Infinity"
        else:
            path = self.build_path(start, destination, path_searched['parents'])
            # print(path)
        return distance, path

    def build_path(self, start, destination, parents):
        """
        Builds the shortest path based on the parents(
            which node to travel next)
        :param:
            start(str): the id of start station
            destination(str): the id of the destination node
            parents(dictionary): The route taken from each node(node->next node)
                node_id is the key
        :return:
            path(list): ordered list of path(id of vertex)
        """
        current_vertex = destination
        path = []
        while start != current_vertex:
            path.append(current_vertex)
            current_vertex = parents[current_vertex]
        path.append(start)
        return path


class RoutingApp(tk.Frame):
    """
    UI Class
    """
    count = 0

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        # self = tk.Tk()
        self.winfo_toplevel().title("Rail Line Management")
        self.grid(row=10, column=5)

        self.london_connections_file = 'data/londonconnections.csv'
        self.london_lines_file = 'data/londonlines.csv'
        self.london_stations_file = 'data/londonstations.csv'

        self.build_graph()
        print("Graph built")
        self.station_reference = self.graph.get_named_dict_of_vertices()

        self.start = tk.StringVar()
        self.destination = tk.StringVar()
        self.search_in_map = 0

        self.setting_row = 12
        self.reslut_scale = None
        self.station_name_labeling = None
        self.train_scale = None

        self.set_ui()
        print("UI built")
        self.manage_window_access = None
        self.window_access_values = {}
        self.draw_on_grid()
        print("manage buttons drawn on application")
        self.initialize()
        print("UI ran ")

    def initialize(self):
        """
        Starts the Application
        :return:
        """

        self.mainloop()

    def manage_window_house_keeping(self):
        """
        makes sure resources are shared correctly.
            This method makes sure only 1 secondary window exist
            Resets the values
        :return:
        """
        if self.manage_window_access:
            self.manage_window_access.destroy()
            self.window_access_values = {}

    def build_graph(self):
        """
        Initializes the graph construction
        :return:
            None
        """
        self.graph = self.build_rail_graph()

    def create_drop_down(self, variable, listing, root=None):
        """
        Effort to unify dropdown creation.
        (unsuccessful to implement application fully)
        :param variable:
        :param listing:
        :param root:
        :return:
            tkinter widget.
        """
        root = root if root else self
        return tk.OptionMenu(root, variable, *listing)

    def create_button(self, text, command=None,
                      root=None, active_background=None,
                      background=None):
        """
        Effort to unify dropdown creation.
        (unsuccessful to implement application fully)
        :param variable:
        :param listing:
        :param root:
        :return:
            tkinter widget.
        """
        root = root if root else self
        return tk.Button(root, activebackground='#4287f5',
                         bg=background, text=text, command=command)

    def set_ui(self):
        """
        Initializes the most ui elements(does not place them/draw)
        :return:
            None
        """
        self.stations_list = sorted(self.station_reference.keys())
        self.start.set("--select start station--")
        self.start_station_drop = self.create_drop_down(
            self.start, self.stations_list)
        self.start.trace("w", self.start_station_draw_ui_call_back)

        # destination_station_drop =
        self.destination.set("--select destination station--")
        self.destination_station_drop = self.create_drop_down(
            self.destination, self.stations_list)
        self.destination.trace("w", self.destination_station_draw_ui_call_back)

        self.search_button = self.create_button(
            text='search', command=self.search_network, background="red")

        # self.destination_station_label = tk.Label(text="Station: Not selected")
        # self.destination_station_status_label = tk.Label(text="status: None")

        self.draw_manage_buttons()

    def start_station_draw_ui_call_back(self, *args):
        """
        Callback function to display starting station related update in ui
            -triggered when value is changed in start-dropdown
        """
        station_name = self.start.get()
        station = self.station_reference[station_name]
        if not station.is_active:
            messagebox.showerror("Inactive station", message=f'{station.name} is inactive. please select another one')
            self.start.set('--select start station--')
            self.start_station_label.grid_forget()
            self.start_station_status_label.grid_forget()
            return None
        if not station.has_active_edge():
            messagebox.showerror("rail inactive alert", message=f'All rails connected to {station.name} are inactive. please select another one')
            self.start.set('--select station station--')
            self.start_station_label.grid_forget()
            self.start_station_status_label.grid_forget()
            return None
        station_text = f"[{station.id}] {station.name} is selected. {station.total_lines} rail lines."
        try:
            if self.start_station_label:
                self.start_station_label.grid_forget()
        except:
            print("initial did not exist")
        self.start_station_label = tk.Label(
            self, text=station_text).grid(row=2, column=1, columnspan=3)
        try:
            if self.start_station_status_label:
                self.start_station_status_label.grid_forget()
        except:
            print("status label did not exist")

        status_text = f'status : {"Active" if station.is_active else "inactive"}'
        self.start_station_status_label = tk.Label(
            self, text=status_text).grid(row=3, column=1, columnspan=3)
        # print(station)
        self.draw_on_grid()

    def destination_station_draw_ui_call_back(self, *args):
        """
        Callback function to display destination station related update in ui
            -triggered when value is changed in destination-dropdown
        """
        station_name = self.destination.get()
        station = self.station_reference[station_name]
        if not station.is_active:
            messagebox.showerror("Inactive station", message=f'{station.name} is inactive. please select another one')
            self.destination.set('--select destination station--')
            return None
        if not station.has_active_edge():
            messagebox.showerror("Rail inactive alert", message=f'All rails connected to {station.name} are inactive. please select another one')
            self.destination.set('--select destination station--')
            return None
            # messagebox.showerror("showerror", "Error")
        station_text = f"[{station.id}] {station.name} is selected. {station.total_lines} rail lines.({len(station.adjacent)})"
        try:
            if self.destination_station_label:
                self.destination_station_label.destroy()
        except:
            print("initial did not exist")
        self.destination_station_label = tk.Label(
            self, text=station_text).grid(row=5, column=1, columnspan=3)
        try:
            if self.destination_station_status_label:
                self.destination_station_status_label.destroy()
        except:
            print("status label did not exist")

        status_text = f'status : {"Active" if station.is_active else "inactive"}'
        self.destination_station_status_label = tk.Label(
            self, text=status_text).grid(row=6, column=1, columnspan=3)
        # print(station)
        self.draw_on_grid()

    def draw_on_grid(self):
        """
        Places widgets in ui in Grid.
        :return:
        """
        # for i in range(0,5):
        #     self.grid_rowconfigure(i, weight=1)
        #     self.grid_columnconfigure(i, weight=1)
        if self.start_station_drop:
            self.start_station_drop.grid(row=1, columnspan=5)
        # try:
        #     if self.destination_station_label:
        #         self.destination_station_label.grid(row=2, columnspan=3)
        #     if self.destination_station_status_label:
        #         self.destination_station_status_label.grid(row=3, columnspan=3)
        # except:
        #     print("initial paint")

        if self.destination_station_drop:
            self.destination_station_drop.grid(row=4, columnspan=5)
        if self.search_button:
            self.search_button.grid(row=7, columnspan=5)

        self.results_frame = tk.Frame(self)
        self.results_frame.grid(row=8, columnspan=5)

        if self.manage_train_button.grid:
            self.manage_train_button.grid(row=self.setting_row, column=0, columnspan=1)
        if self.manage_station_button:
            self.manage_station_button.grid(row=self.setting_row, column=1, columnspan=1)
        if self.close_application_button:
            self.close_application_button.grid(row=self.setting_row, column=4, columnspan=1)
        if self.manage_variables_button:
            self.manage_variables_button.grid(row=self.setting_row, column=3, columnspan=1)

    def create_info_window(self):
        """
        writes instructions based on the shortest path
        :return:
        """
        self.manage_window_house_keeping()
        self.manage_window_access = tk.Toplevel(self)
        info_window = self.manage_window_access
        info_window.geometry("400x400")
        current_train = None
        previous_train = None
        prevous_station = None
        current_station = None
        for path in self.shortest_path:
            current_station = self.graph.vertDict[path]
            # label = tk.Label(info_window, text=current_station.name)
            prevous_station = current_station
            previous_train = current_train

            if self.shortest_path.index(path) == 0:
                next_station = self.graph.vertDict[str(
                    self.shortest_path[self.shortest_path.index(path) + 1])]
                edge = current_station.get_edge_from_vertex(next_station)
            else:
                next_station = self.graph.vertDict[str(
                    self.shortest_path[self.shortest_path.index(path) - 1])]
                edge = current_station.get_edge_from_vertex(next_station)
            current_train = edge.train
            if not prevous_station:
                label = tk.Label(info_window, text=f'board {current_train.name} from {current_station}')
                continue
            if previous_train != current_train:
                label = tk.Label(info_window, text=f'board {current_train.name} from {current_station}')
            label.pack()


    def draw_search_results(self):
        """
        Draws the elements that represent the search results
        """

        self.train_scale_var = tk.IntVar()
        self.train_scale_var.set(1)
        self.train_scale_var.trace("w", self.redraw_scale)

        self.shortest_distance_label1 = tk.Label(
            self.results_frame, text="The shortest duration was: ").grid(
            row=0, column=1)

        self.shortest_distance_label2 = tk.Label(self.results_frame, text=f"{self.shortest_path_duration} minutes",
                                                 font=('Helvetica', 18, 'bold')).grid(row=0, column=2)
        self.shortest_distance_label3 = tk.Label(self.results_frame, text='The shortest path:',
                                                 font=('Helvetica', 18, 'bold')).grid(row=2, column=1)
        self.search_instruction = tk.Label(self.results_frame, text='you can scroll the scale to browse stations',
                                                 ).grid(row=3, column=1)
        tk.Button(self.results_frame,
                  text="view travel instruction",
                  command=self.create_info_window
                  ).grid(row=3, column=2)
        # self.train_scale = tk.Scale(self.results_frame, from_=0, to=len(self.shortest_path),
        #                      orient=tk.VERTICAL, variable=self.train_scale_var)
        # self.train_scale.grid(row=3, columnspan=1)
        self.redraw_scale()

    def redraw_scale(self, *args):
        """
        updates the Scale(shows the shortest path)in UI when moved.

        """
        if len(self.shortest_path) > 1:
            current_station = self.graph.vertDict[str(
                self.shortest_path[self.train_scale_var.get() - 1])]
            label = current_station.name
            if self.train_scale_var.get() == 1:
                next_station = self.graph.vertDict[str(
                    self.shortest_path[self.train_scale_var.get()])]
                edge = current_station.get_edge_from_vertex(next_station)
            else:
                next_station = self.graph.vertDict[str(
                    self.shortest_path[self.train_scale_var.get() - 2])]
                edge = current_station.get_edge_from_vertex(next_station)

            if self.train_scale:
                # print('forgets')
                self.train_scale.destroy()
            if self.station_name_labeling:
                self.station_name_labeling.grid_forget()
            train_colour = edge.train.colour
            stripe = ''
            if '#' not in train_colour:
                train_colour = '#' + train_colour
            if edge.train.stripe:
                stripe = 'red'
            self.train_scale = tk.Scale(
                self.results_frame, from_=1, to=len(self.shortest_path), bg=train_colour,
                orient=tk.VERTICAL, variable=self.train_scale_var, label=edge.train.name,
                length=200, troughcolor=stripe)
            self.station_name_labeling = tk.Label(self.results_frame, text=label)
            self.train_scale.grid(row=4, columnspan=3)
            self.station_name_labeling.grid(row=4, columnspan=2)

    def create_manage_station_window(self):
        """
        Creates a secondary window to manage stations
        """

        def station_window_call_back(*args):
            """
            When a station is selected this create the required widgets.
            """
            station_name = station_setting.get()
            station = self.station_reference[station_name]
            # print(station.is_active)
            button_text = tk.StringVar()
            button_text.set(
                'Deactivate station' if station.is_active else 'Activate station'
            )
            try:
                if self.window_access_values['status']:
                    # print('tries to delete')
                    self.window_access_values['status'].pack_forget()
            except:
                print("element not generated")
            self.window_access_values['status'] = tk.Button(station_window,
                                                            text=button_text.get(),
                                                            command=lambda: station.toggle_status(self))
            self.window_access_values['status'].pack()
            # print(station.is_active)

            # print(station)

        self.manage_window_house_keeping()
        self.manage_window_access = tk.Toplevel(self)
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
        """
        Creates a secondary window to manage Trains
        """

        def train_window_call_back(*args):
            """
            When a train is selected this create the required widgets.
            """
            train_name = train_setting.get()
            train = Train.get_object_from_name(train_name)
            # print(train.is_active)
            button_text = tk.StringVar()
            button_text.set(
                'deactivate train' if train.is_active else 'Activate train'
            )
            try:
                if self.window_access_values['status']:
                    # print('tries to delete')
                    self.window_access_values['status'].grid_forget()
            except:
                print("element not generated")
            self.window_access_values['status'] = tk.Button(train_window,
                                                            text=button_text.get(),
                                                            command=lambda: train.toggle_status(self))
            self.window_access_values['status'].grid(row=3, column=1, columnspan=5)
            # print(train.is_active)

            print(train)

        self.manage_window_house_keeping()
        self.manage_window_access = tk.Toplevel(self)
        train_window = self.manage_window_access
        train_window.geometry("400x400")

        train_names = [Train.trains[id_].name for id_ in Train.trains.keys()]
        train_setting = tk.StringVar()
        train_setting.set("--select train--")
        train_setting.trace("w", train_window_call_back)
        train_drop = tk.OptionMenu(train_window, train_setting, *train_names)
        train_drop.grid(row=0, column=1, columnspan=5)

        close_train_button = tk.Button(train_window,
                                       text="cancel",
                                       command=train_window.destroy).grid(row=5, column=1, columnspan=5)

    def search_network(self):
        """
        When search is triggered in the ui.
        This segment facilitates and creates new ui for the search
        :return:
            None
        """
        count_begin = time.time()
        start_vertex = self.station_reference[self.start.get()]
        destination_vertex = self.station_reference[self.destination.get()]
        # start_text = f'station name{start_vertex.name}   id: {start_vertex.id}'
        # destination_text = f'station name{destination_vertex.name}   id: {destination_vertex.id}'
        # display_start = tk.Label(text=start_text).pack()
        # display_destination = tk.Label(text=destination_text).pack()
        if self.search_in_map:
            distance, path = self.graph.search_after_map_build(
                str(start_vertex.id),
                str(destination_vertex.id))
        else:
            distance, path = self.graph.search_graph(
                str(start_vertex.id),
                str(destination_vertex.id))
        shortest_path_duration_text = f'shortest duration : {distance} '
        self.shortest_path_duration = distance
        self.shortest_path = path[::-1]
        # self.shortest_path_duration_label = tk.Label(text=shortest_path_text).pack()
        count_end = time.time()
        self.time_for_search = str(round(count_end - count_begin, 2))
        print(f'time to search: {self.time_for_search}')
        self.draw_search_results()

    def draw_manage_buttons(self):
        """
        initializes the bottom level setting buttons.
        :return:
        """
        self.manage_station_button = tk.Button(self,
                                               text="manage stations",
                                               command=self.create_manage_station_window)

        self.manage_train_button = tk.Button(self,
                                             text="manage trains",
                                             command=self.create_manage_train_window)

        self.close_application_button = tk.Button(self,
                                                  text="close application",
                                                  command=self.quit)
        self.manage_variables_button = tk.Button(self,
                                                 text="settings(not-implemented)",
                                                 command=self.quit)
        # planning to switch between algorithm,
        # ability to do dynamic search or search in pre-built map
        # showing results via time,stations or switching trainlines

    def build_rail_graph(self):
        """
        Reads the data from the files provided and builds the Graph
         and the related classes
        """

        # Initializes the rail graph
        rail_graph = Graph("Rail Graph")

        # reading london lines
        with open(self.london_stations_file, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csv_reader)
            for row in csv_reader:
                # print(row)
                # new vertex object is created
                new_vertex = Vertex(
                    _id=row[0],
                    name=row[3].replace('"', ''),
                    display_name=row[4],
                    total_lines=row[5],
                    rail=row[6]
                )
                # print(new_vertex)
                # new vertex is added to the graph
                rail_graph.addVertex(new_vertex)
            csvfile.close()

        # # reading london lines
        train_lines = {}
        with open(self.london_lines_file, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csv_reader)
            for row in csv_reader:
                # print(row)
                # name_id = row[0].split(',')
                # creating train objects
                train = Train(id=row[0],
                              name=row[1],  # replace('"', ''),
                              colour=row[2],
                              stripe=row[3])
            csvfile.close()
        # print(train_lines)

        # reading connections between them and creating edges of graph
        with open(self.london_connections_file, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csv_reader)
            for row in csv_reader:
                # print(row)
                rail_graph.addEdge(
                    vertex_1=row[0],
                    vertex_2=row[1],
                    train_id=row[2],
                    duration=row[3]
                )
            csvfile.close()
            rail_graph.print_graph()
            rail_graph.build_short_matrix()
            # rail_graph.search_after_map_build('281', '298')
        return rail_graph


instance = RoutingApp()
