def find_max_vertex(eccentricities):
    max_value = float('-inf')
    new_start_vertex = None

    for vertex in eccentricities:
        if eccentricities[vertex] > max_value:
            max_value = eccentricities[vertex]
            new_start_vertex = vertex

    return new_start_vertex


def distances_between_vertices_graph(graph, start):
    visited = set()
    level = {start: 0}
    frontier = [start]
    while frontier:
        next_level = []
        for u in frontier:
            visited.add(u)
            for v in graph[u]:
                if v not in visited and v not in level:
                    level[v] = level[u] + 1
                    next_level.append(v)
        frontier = next_level
    return level


def calculate_eccentricities(graph, start_vertex):
    distances = distances_between_vertices_graph(graph, start_vertex)

    max_level = max(distances.values())
    highest_level_vertices = []
    for vertex, level in distances.items():
        if level == max_level:
            highest_level_vertices.append(vertex)
    # print(highest_level_vertices)
    eccentricities = {}
    for vertex in highest_level_vertices:
        eccentricities[vertex] = max(distances_between_vertices_graph(graph, vertex).values())

    return eccentricities


graph = {
    1: [10, 6],
    2: [9, 4],
    3: [11, 5, 7],
    4: [2, 7],
    5: [8, 3],
    6: [1, 9],
    7: [4, 11, 3],
    8: [5, 11],
    9: [6, 2, 11],
    10: [1, 11],
    11: [9, 10, 7, 8, 3]
}


start_vertex = 10
eccentricities = calculate_eccentricities(graph, start_vertex)
print(eccentricities)
start_vertex = find_max_vertex(eccentricities)

previous_eccentricities_values = None
while True:
    eccentricities = calculate_eccentricities(graph, start_vertex)
    current_values = eccentricities.values()

    if previous_eccentricities_values and list(previous_eccentricities_values)[-1] == list(current_values)[-1]:
        pseudo_peripheral = start_vertex
        break

    start_vertex = find_max_vertex(eccentricities)
    previous_eccentricities_values = current_values

print(pseudo_peripheral)
