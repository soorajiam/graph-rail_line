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
    return distances, parents
    # print(distance)


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


def dfs(graph, node):
    visited = [node]
    stack = [node]
    while stack:
        node = stack[-1]
        if node not in visited:
            visited.extend(node)
        remove_from_stack = True
        for next in graph[node]:
            if next not in visited:
                stack.extend(next)
                remove_from_stack = False
                break
        if remove_from_stack:
            stack.pop()
    return visited


def get_chain_d(argDict):
    def each_path(i, caller_chain):
        a = []
        caller_chain.append(i)
        b = argDict.get(i, [])
        for j in b:
            if j not in caller_chain:
                a.append(j)
                a.extend(each_path(j, caller_chain))
        return a

    return {i: each_path(i, []) for i in argDict}


dependecyDict = {'A': ['D'], 'B': ['A', 'E'], 'C': ['B'], 'D': ['C'], 'G': ['H']}

print(get_chain_d(dependecyDict))


def paths(graph, v):
    """Generate the maximal cycle-free paths in graph starting at v.
    graph must be a mapping from vertices to collections of
    neighbouring vertices.

    >>> g = {1: [2, 3], 2: [3, 4], 3: [1], 4: []}
    >>> sorted(paths(g, 1))
    [[1, 2, 3], [1, 2, 4], [1, 3]]
    >>> sorted(paths(g, 3))
    [[3, 1, 2, 4]]

    """
    path = [v]  # path traversed so far
    seen = {v}  # set of vertices in path

    def search():
        dead_end = True
        for neighbour in graph[path[-1]]:
            if neighbour not in seen:
                dead_end = False
                seen.add(neighbour)
                path.append(neighbour)
                yield from search()
                path.pop()
                seen.remove(neighbour)
        if dead_end:
            yield list(path)

    yield from search()
