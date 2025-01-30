from optimizationProblem import OptimizationProblem
import numpy as np

##### Test Controls #####
# Small tests: < 100 spins
# Medium tests: 100 - 1000 spins
# Large tests: > 1000 spins
print_test_results = 0
run_small = 1
run_medium = 0
run_large = 0
score = 0

##### Test Fnuctions #####

import testing.labs_ising_formulation as labs
import testing.ILPs as ilps
def test_labs(N):
    prob_labs = OptimizationProblem()
    J, h = labs.master_ising(N, N)
    Q = labs.ising_to_qubo(J, h)
    x = prob_labs.add_variable("x", 0, 1, len(Q))
    prob_labs.set_objective(x.T @ Q @ x)
    sol, obj, feas = prob_labs.solve()
    if print_test_results:
        print(sol, obj, feas)
    energy = labs.calculate_energy(sol[:N])
    if energy <= labs.best_energy[N]:
        print(f"LABS_{N} Test True")
        return True
    print(f"LABS_{N} Test False")
    return False

def test_ILP(prob_num):
    A = ilps.A_matrices[prob_num]
    b = ilps.b_vectors[prob_num]
    c = ilps.c_vectors[prob_num]
    prob_ilp = OptimizationProblem()
    x = prob_ilp.add_variable("x", 0, 15, len(c))
    prob_ilp.set_objective(c @ x)
    prob_ilp.add_constraint(A @ x, "<=", b)
    sol, obj, feas = prob_ilp.solve(100)
    if print_test_results:
        print(sol, obj, feas)
    if obj <= ilps.objs[prob_num] and feas:
        print(f"ILP_{prob_num} Test True")
        return True
    print(f"ILP_{prob_num} Test False")
    return False

##### Test Calls #####

if run_small:
    all_small_pass = True
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
    if print_test_results:
        print(sol, obj, feas)
    if np.array_equal(sol, np.array([0, 1, 1, 0, 1])) and obj == np.float64(-3.0) and feas:
        print("Small Test 1 True")
    else:
        print("Small Test 1 False")
        all_small_pass = False

    # Test 2
    # Linear Integer Program
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
    sol, obj, feas = prob2.solve(10)
    if print_test_results:
        print(sol, obj, feas)
    if np.array_equal(sol, [7,4,0]) and obj == -41 and feas:
        print("Small Test 2 True")
    else:
        print("Small Test 2 False")
        all_small_pass = False

    # Test 3
    # Quadratization
    prob3 = OptimizationProblem()
    x = prob3.add_variable("x", 0, 1)
    y = prob3.add_variable("y", 0, 1)
    z = prob3.add_variable("z", 0, 1)
    prob3.set_objective(2*z*z*x - 3*x*y*z - 2*y*z*z)
    prob3.add_constraint(x+y+z, "<=", 2)
    prob3.add_constraint(x+z, "=", 1)
    sol, obj, feas = prob3.solve(lam = 10)
    if print_test_results:
        print(sol, obj, feas)
    if np.array_equal(sol, [0, 1, 1]) and obj == -2 and feas:
        print("Small Test 3 True")
    else:
        print("Small Test 3 False")
        all_small_pass = False

    # Test 4
    # Integer Program w/ Quadratization
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
    if print_test_results:
        print(sol, obj, feas) # [7, 0, 0, 1, 1] -154 True
    if np.array_equal(sol, [7, 0, 0, 1, 1]) and obj == -154 and feas:
        print("Small Test 4 True")
    else:
        print("Small Test 4 False")
        all_small_pass = False

    # Test 5
    # LABS
    for N in range(3, 11):
        if not test_labs(N):
            all_small_pass = False

    # Test 6
    # ILPs
    for i in range(1, 4):
        if not test_ILP(i):
            all_small_pass = False
    
    print("All small tests pass:", all_small_pass)
    
if run_medium:
    all_medium_pass = True
    for N in range(11, 32):
        if not test_labs(N):
            all_medium_pass = False

    
    print("All medium tests pass:", all_medium_pass)