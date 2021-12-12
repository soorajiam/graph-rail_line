# import sys.max
import queue
import heapq


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
    flag = 1
    while (flag):
        start = input("start: ")
        end = input("end: ")
        print(parents[start])
        print(distances[start])
        print(parents[end])
        print(distances[end])
        flag = int(input("continue:(0/1)"))
    # print(distance)


def dijistras_short(graph, start, destination=None):
    distances = {vertex: float('inf') for vertex in graph.getVertices()}
    distances[start.id] = 0
    parents = {vertex: None for vertex in graph.getVertices()}
    queue = [(0, start.id)]
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        # relaxation
        for weight, next_node in graph.vertDict[current_node].getConnections():
            distance_temp = current_distance + weight
            if distance_temp < distances[next_node]:
                distances[next_node] = distance_temp
                parents[next_node] = current_node
                heapq.heappush(queue, (distance_temp, next_node))
    return distances, parents
