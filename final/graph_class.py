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
        return self.adjacent

    def getId(self):
        return self.id

    # def getWeight(self, neighbour):
    #     return self.adjacent


class Edge:
    edges = []

    def check_duplicate(verices):
        for edge in Edge.edges:
            if verices == edge.vertices or verices[::-1] == edge.vertices:
                return edge
            else:
                return False

    def __init__(self, graph, train_id, duration, vertices):
        # value = self.check_duplicate(vertices)
        # if not value:
        self.id = len(self.edges)
        self.graph = graph
        self.train_id = train_id
        self.duration = duration
        self.vertices = vertices
        if self not in vertices[0].adjacent:
            vertices[0].adjacent.append(self)
        if self not in vertices[1].adjacent:
            vertices[1].adjacent.append(self)
        self.edges.append(self)

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
