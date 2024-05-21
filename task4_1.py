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


class Graph:
    def __init__(self, matrix):
        self.matrix = matrix
        self.visited = [False] * len(matrix)
        self.shortest_path_length = float('inf')
        self.shortest_path = []

    def dfs_shortest_path(self, start, end, path, path_length, user_path_length):
        self.visited[start] = True
        path.append(start)

        if start == end and path_length == user_path_length:
            self.shortest_path = path.copy()
            return

        for i in range(len(self.matrix.data)):
            if self.matrix.data[start][i] == 1 and not self.visited[i]:
                self.dfs_shortest_path(i, end, path, path_length + 1,
                                       user_path_length)

        path.pop()
        self.visited[start] = False

    def find_shortest_path(self, i, j, user_path_length):
        if not (0 <= i < len(self.matrix.data)) or not (0 <= j < len(self.matrix.data)):
            return []

        if self.matrix.data[i][j] == 1:
            return [i, j]

        self.visited = [False] * len(self.matrix.data)
        self.shortest_path_length = float('inf')
        self.shortest_path = []

        self.dfs_shortest_path(i, j, [], 0, user_path_length)

        if len(self.shortest_path) == user_path_length + 1:
            self.shortest_path_length = user_path_length
            return self.shortest_path
        else:
            return []


filename = "C:\\Users\\Adminnn\\Desktop\\папочка\\унік\\algebra\\martix4_1.txt"
with open(filename, 'r') as file:
    data = file.read()

matrix_from_file = read_data_entry(data)
print(matrix_from_file.data)
graph = Graph(matrix_from_file)
start_vertex = 3
end_vertex = 0

for i in range(len(matrix_from_file.data)):
    path = graph.find_shortest_path(start_vertex, end_vertex, i)

    if(path) :
        print(path)
        print(graph.shortest_path_length)