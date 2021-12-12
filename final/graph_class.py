from algorithms import dijkstras_searching, dijistras_short
import json

class Vertex:
    def __init__(self, id, name, display_name, total_lines, rail):
        # Adding details of station to and as vertex.
        self.id = id
        self.name = name
        self.display_name = display_name
        self.total_lines = total_lines
        self.rail = rail
        self.adjacent = []  # Adjacency list

    def __str__(self):
        return str(self.name)

    def addNeighbour(self, neighbour, weight=0):
        self.adjacent[neighbour] = weight

    def getConnections(self):
        edges = self.adjacent
        connections = []
        for edge in edges:
            connections.append(
                edge.get_connection(self)
            )
        return connections

    def getId(self):
        return self.id

    # def getWeight(self, neighbour):
    #     return self.adjacent

class Train:
    trains = {}

    def __init__(self, id, name, colour, stripe):
        self.name = name
        self.id = id
        self.colour = colour
        self.stripe = stripe

        Train.trains.update({
            id: self
        })

    def get_train(id):
        return Train.trains[id]


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
        if vertex == self.vertices[0]:
            neighbour = self.vertices[1]
        else:
            neighbour = self.vertices[0]
        return int(self.duration), neighbour.id

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
        # print(self.vertDict[vertex_1],
        # self.vertDict[vertex_2])
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

    def search_dijistras(self, start, destination):
        start = self.vertDict[start]
        destination = self.vertDict[destination]
        dijkstras_searching(self, start, destination)

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
        print(f'distance: {path_searched["distances"][destination]}')
        path1 = self.build_path(start, destination, path_searched['parents'])
        print(path1)
        print(path1.pop())

    def build_path(self, start, destination, parents):
        current_vertex = destination
        path = []
        while start != current_vertex:
            path.append(current_vertex)
            current_vertex = parents[current_vertex]
        path.append(start)
        return path
        # print(short_paths)
