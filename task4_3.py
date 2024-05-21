from task4_2 import start_vertex, calculate_eccentricities, find_max_vertex
from matrix import Matrix


def read_data_entry(data_entry):
    data = []

    try:
        lines = data_entry.split("\n")
        for line in lines:
            values = [float(x) for x in line.strip().split()]
            data.append(values)
        return Matrix(data)
    except ValueError as e:
        raise ValueError(f'Помилка типів даних: {e}')
    except Exception as e:
        raise Exception(f'Помилка: {e}')


def matrix_to_graph(matrix):
    graph = {}
    for i in range(len(matrix)):
        connections = []
        for j in range(len(matrix.data[i])):
            if matrix.data[i][j] == 1 and i != j:
                connections.append(j + 1)
        if connections:
            graph[i + 1] = connections
    return graph


def get_neighbors_length(vertex):
    return len(graph[vertex])


def kathie_makki_algorithm(graph, pseudo_peripheral):
    renumbering = [pseudo_peripheral]
    visited = [pseudo_peripheral]

    while len(visited) < len(graph):
        connections = []
        for vertex in renumbering:
            for neighbour in graph[vertex]:
                connections.append(neighbour)

        for vertex in connections:
            if vertex not in visited:
                visited.append(vertex)

        sorted_visited = []
        for vertex in visited:
            if vertex not in sorted_visited:
                sorted_visited.append(vertex)
        sorted_visited.sort(key=get_neighbors_length)

        for vertex in sorted_visited:
            if vertex not in renumbering:
                renumbering.append(vertex)

    renumbered_graph = {}
    for i, vertex in enumerate(renumbering, start=1):
        renumbered_neighbours = []
        for neighbour in graph[vertex]:
            if neighbour in renumbering:
                renumbered_neighbours.append(renumbering.index(neighbour) + 1)
        renumbered_graph[i] = renumbered_neighbours

    return renumbered_graph


def graph_to_matrix(renumbered_graph):
    num_vertices = len(renumbered_graph)
    matrix = []
    for i in range(num_vertices):
        row = []
        for j in range(num_vertices):
            row.append(0)
        matrix.append(row)

    for vertex, neighbours in renumbered_graph.items():
        for neighbour in neighbours:
            matrix[vertex - 1][neighbour - 1] = 1

    for i in range(num_vertices):
        matrix[i][i] = 1

    return matrix


filename = "C:\\Users\\Adminnn\\Desktop\\папочка\\унік\\algebra\\task4_3.txt"
with open(filename, 'r') as file:
    data = file.read()

matrix_from_file = read_data_entry(data)
graph = matrix_to_graph(matrix_from_file)
eccentricities = calculate_eccentricities(graph, start_vertex)
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



renumbered_graph = kathie_makki_algorithm(graph, pseudo_peripheral)

matrix_result = graph_to_matrix(renumbered_graph)

print(renumbered_graph)
print(matrix_result)
