import matplotlib.pyplot as plt
import numpy as np

vector = (3, 3)
matrix = [[-1, 3], [1, 1], [1, 0], [0, 1]]
right_part = [20, 20, 5, 5]
sign = ['<=', '<=', '<=', '>=']

x1 = np.linspace(-20, 20, 1000)

intersection_points = []

# Find intersection points
for i in range(len(matrix)):
    for j in range(i + 1, len(matrix)):
        A = np.array([[matrix[i][0], matrix[i][1]], [matrix[j][0], matrix[j][1]]])
        B = np.array([right_part[i], right_part[j]])
        intersection_point = np.linalg.solve(A, B)
        intersection_points.append(intersection_point)

# Plot lines and fill areas
for i in range(len(matrix)):
    if matrix[i][1] != 0:
        lambdas = lambda x: (right_part[i] - matrix[i][0] * x) / matrix[i][1]
        y = lambdas(x1)
        if sign[i] == '<=':
            plt.plot(x1, y, label=f'{matrix[i][0]}x1 + {matrix[i][1]}x2 <= {right_part[i]}', color='royalblue')
            plt.fill_between(x1, y, np.full_like(x1, 20), color='aqua', alpha=0.5)
        else:
            plt.plot(x1, y, label=f'{matrix[i][0]}x1 + {matrix[i][1]}x2 >= {right_part[i]}', color='hotpink')
            plt.fill_between(x1, y, np.full_like(x1, -20), color='pink', alpha=0.5)
    else:
        if sign[i] == '<=':
            plt.axvline(x=right_part[i] / matrix[i][0], color='royalblue',
                        label=f'{matrix[i][0]}x1 + {matrix[i][1]}x2 <= {right_part[i]}')
            plt.fill_between(x1, -20, 20, where=(x1 >= right_part[i] / matrix[i][0]), color='aqua', alpha=0.5)
        else:
            plt.axvline(x=right_part[i] / matrix[i][0], color='hotpink',
                        label=f'{matrix[i][0]}x1 + {matrix[i][1]}x2 >= {right_part[i]}')
            plt.fill_between(x1, -20, 20, where=(x1 <= right_part[i] / matrix[i][0]), color='pink', alpha=0.5)

# Check intersection points against inequalities
for point in intersection_points:
    satisfied = True
    for i in range(len(matrix)):
        if matrix[i][1] != 0:
            if sign[i] == '<=':
                if matrix[i][0] * point[0] + matrix[i][1] * point[1] > right_part[i]:
                    satisfied = False
                    break
            else:
                if matrix[i][0] * point[0] + matrix[i][1] * point[1] < right_part[i]:
                    satisfied = False
                    break
        else:
            if sign[i] == '<=':
                if point[0] > right_part[i] / matrix[i][0]:
                    satisfied = False
                    break
            else:
                if point[0] < right_part[i] / matrix[i][0]:
                    satisfied = False
                    break
    if satisfied:

        plt.plot(point[0], point[1], 'go')

# Plotting the vector
plt.arrow(0, 0, vector[0], vector[1], head_width=0.5, head_length=0.7, color='green', alpha=0.7)

# Finding the slope of the vector
slope = vector[1] / vector[0]

# Finding the slope of the perpendicular line
perpendicular_slope = -1 / slope

# Plotting the perpendicular line passing through the endpoint of the vector
x_endpoint = vector[0]
y_endpoint = vector[1]
x_perpendicular = np.linspace(-20, 20, 1000)
y_perpendicular = perpendicular_slope * (x_perpendicular - x_endpoint) + y_endpoint
plt.plot(x_perpendicular, y_perpendicular, '--', color='orange', label='Perpendicular')
plt.xlabel('x1')
plt.ylabel('x2')
plt.xlim(-20, 20)
plt.ylim(-20, 20)
plt.legend()
plt.grid(True)
plt.show()
