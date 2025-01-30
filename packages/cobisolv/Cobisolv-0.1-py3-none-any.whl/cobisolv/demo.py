from formulate import OptimizationProblem
import numpy as np

prob1 = OptimizationProblem()
N = 5
x = prob1.add_variable("x", 0, 1, N)
Q = [[ 2, -1,  0, -2,  3],
    [-1,  2, -1,  0, -1],
    [ 0, -1,  1,  2, -2],
    [-2,  0,  2,  3, -1],
    [ 3, -1, -2, -1,  2]]
prob1.set_objective(x.T @ Q @ x)
sol, obj, feas = prob1.solve()
print(sol, obj, feas)
if np.array_equal(sol, np.array([0, 1, 1, 0, 1])) and obj == np.float64(-3.0) and feas:
    print("Prob 1 True")

prob2 = OptimizationProblem()
N = 3
x = prob2.add_variable("x", 0, 7, N)
A = np.array([
    [2, 1, 3], 
    [1, 2, 2],  
])
b = np.array([20, 15])  
c = np.array([-3,-5,-4]) 
prob2.set_objective(c @ x)
prob2.add_constraint(A @ x, "<=", b)
sol, obj, feas = prob2.solve()
print(sol, obj, feas)
if np.array_equal(sol, [7,4,0]) and obj == -41 and feas:
    print("Prob 2 True")

prob3 = OptimizationProblem()
x = prob3.add_variable("x", 0, 1)
y = prob3.add_variable("y", 0, 1)
z = prob3.add_variable("z", 0, 1)
prob3.set_objective(2*z*z*x - 3*x*y*z - 2*y*z*z)
prob3.add_constraint(x+y+z, "<=", 2)
prob3.add_constraint(x+z, "=", 1)
sol, obj, feas = prob3.solve(lam = 10)
print(sol, obj, feas)
if np.array_equal(sol, [0, 1, 1]) and obj == -2 and feas:
    print("Prob 3 True")

prob4 = OptimizationProblem()
N = 3
x = prob4.add_variable("x", 0, 7, N)
A = np.array([
    [2, 2, 3], 
    [1, 2, 1],  
])
b = np.array([20, 15])
Q = np.array([[-3,5,4],
            [2,-1,0],
            [4,-4,6]])
y = prob4.add_variable("y", 0, 1)
z = prob4.add_variable("z", 0, 1)

prob4.set_objective(x.T @ Q @ x - x[0]*y*z - x[1]*y*y - x[2]*z*z)
prob4.add_constraint(A @ x, "<=", b)
sol, obj, feas = prob4.solve(lam = 10)
print(sol, obj, feas) # [7, 0, 0, 1, 1] -154 True
if np.array_equal(sol, [7, 0, 0, 1, 1]) and obj == -154 and feas:
    print("Prob 4 True")