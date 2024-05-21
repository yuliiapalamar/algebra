from LinearEquationSystem import LinearEquationSystem
from sparse import SparseMatrix
from classes import Vector

# 1 2 3        1
# 2 3(-1) 4    1
# 3 4 1(-8)    1
# temp = ["2", "1", "1", "4", "3"]
# temp = ["3", "1", "1", "2", "3", "3", "4"]
# temp = ["3", "2", "1", "2", "3", "3", "4", "1"]
# temp = ["4", "2", "1", "2", "3", "3", "4", "1", "3", "2", "1"]
temp = ["5", "1", "1", "3", "4", "5", "2", "2", "6", "1", "1"]


spM = SparseMatrix(temp)
print(spM)
v = Vector([8, 24, 18, 18, 4])
# v = Vector([1, 1, 1, 1, 1])
r = LinearEquationSystem.gaussian_sparse_matrix(spM, v)
print(r.data)
