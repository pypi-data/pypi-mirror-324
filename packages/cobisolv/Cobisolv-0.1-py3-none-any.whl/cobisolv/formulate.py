import numpy as np

class Variable:
    def __init__(self, name, lower_bound=0, upper_bound=1):
        if lower_bound > upper_bound:
            raise ValueError("Lower bound cannot be greater than upper bound.")
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.binary_variables = self._convert_to_binary()

    def _convert_to_binary(self):
        """Converts the integer variable to a sum of binary variables."""
        range_size = self.upper_bound - self.lower_bound
        num_bits = int(np.ceil(np.log2(range_size + 1)) if range_size > 0 else 1)
        binary_vars = []
        for i in range(num_bits - 1):
            binary_vars.append((BinaryVariable(f"{self.name}_{i}"), 2**i))
        last_coeff = range_size - sum(2**i for i in range(num_bits - 1))
        binary_vars.append((BinaryVariable(f"{self.name}_{num_bits-1}"), last_coeff))
        return binary_vars

    def to_expression(self):
        """Generates the equivalent expression for this integer variable."""
        terms = {var: coeff for var, coeff in self.binary_variables}
        return Expression(terms, constant=self.lower_bound)

    def __add__(self, other):
        if isinstance(other, Variable):
            return self.to_expression() + other.to_expression()
        elif isinstance(other, Expression):
            return self.to_expression() + other
        elif isinstance(other, (int, float)):
            return self.to_expression() + other
        else:
            raise ValueError("Invalid type for addition with Variable.")

    def __sub__(self, other):
        if isinstance(other, Variable):
            return self.to_expression() - other.to_expression()
        elif isinstance(other, Expression):
            return self.to_expression() - other
        elif isinstance(other, (int, float)):
            return self.to_expression() - other
        else:
            raise ValueError("Invalid type for subtraction with Variable.")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.to_expression() * other
        elif isinstance(other, Variable):
            return self._multiply_variables(other)
        elif isinstance(other, Expression):
            return self.to_expression() * other
        else:
            raise ValueError("Invalid type for multiplication with Variable.")

    def _multiply_variables(self, other):
        """Handles multiplication of two variables."""
        result_terms = {}
        # Expand the product of two variables
        for var1, coeff1 in self.binary_variables:
            for var2, coeff2 in other.binary_variables:
                product = BinaryVariable(f"({var1.name}*{var2.name})")
                result_terms[(var1, var2)] = result_terms.get((var1, var2), 0) + coeff1 * coeff2
        return Expression(result_terms, constant=self.lower_bound * other.lower_bound)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __repr__(self):
        binary_repr = " + ".join(f"{var}" if coeff == 1 else f"{coeff}*{var}" for var, coeff in self.binary_variables if coeff != 0)
        if self.lower_bound != 0:
            return f"{self.name} = {self.lower_bound} + {binary_repr}"
        return f"{self.name} = {binary_repr}"


class BinaryVariable:
    def __init__(self, name):
        self.name = name
        self.lower_bound = 0
        self.upper_bound = 1

    def __repr__(self):
        return self.name
    

class Expression:
    def __init__(self, terms=None, constant=0):
        self.terms = terms or {}
        self.constant = constant

    def __add__(self, other):
        if isinstance(other, Expression):
            new_terms = self.terms.copy()
            for var, coeff in other.terms.items():
                new_terms[var] = new_terms.get(var, 0) + coeff
            return Expression(new_terms, self.constant + other.constant)
        elif isinstance(other, (int, float)):
            return Expression(self.terms, self.constant + other)
        elif isinstance(other, Variable):
            return self + other.to_expression()
        else:
            raise ValueError("Invalid type for addition.")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Expression):
            new_terms = self.terms.copy()
            for var, coeff in other.terms.items():
                new_terms[var] = new_terms.get(var, 0) - coeff
            return Expression(new_terms, self.constant - other.constant)
        elif isinstance(other, (int, float)):
            return Expression(self.terms, self.constant - other)
        elif isinstance(other, Variable):
            return self - other.to_expression()
        else:
            raise ValueError("Invalid type for subtraction.")

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Expression({var: -coeff for var, coeff in self.terms.items()}, other - self.constant)
        else:
            raise ValueError("Invalid type for reverse subtraction.")

    def __mul__(self, other):
        # Handle multiplication with a scalar (int or float)
        if isinstance(other, (int, float)):
            new_terms = {var: coeff * other for var, coeff in self.terms.items()}
            return Expression(new_terms, self.constant * other)
        
        # Handle multiplication with another Expression
        elif isinstance(other, Expression):
            new_terms = {}
            # Multiply each term by the constant of the other expression
            for var, coeff in self.terms.items():
                new_terms[var] = coeff * other.constant
            for var, coeff in other.terms.items():
                if var in new_terms:
                    new_terms[var] += coeff * self.constant
                else:
                    new_terms[var] = coeff * self.constant
            
            # Multiply each term by each term of the other expression
            for var1, coeff1 in self.terms.items():
                for var2, coeff2 in other.terms.items():
                    key = (var1, var2) if var1 != var2 else (var1, var1)
                    new_terms[key] = new_terms.get(key, 0) + coeff1 * coeff2
            
            return Expression(new_terms, self.constant * other.constant)
        
        # Handle multiplication with a Variable
        elif isinstance(other, Variable):
            return other.to_expression() * self
        
        else:
            raise ValueError("Multiplication is only supported with scalars, Variables, or Expressions.")

    def __rmul__(self, other):
        # Right multiplication calls the same logic as left multiplication
        return self.__mul__(other)

    def find_extreme(self):
        """Finds the minimum and maximum possible value of the expression."""
        min_value = self.constant
        max_value = self.constant

        for term, coeff in self.terms.items():
            if isinstance(term, tuple):
                # Quadratic term
                var1, var2 = term
                if hasattr(var1, "lower_bound") and hasattr(var2, "lower_bound"):
                    possibility_1 = coeff * var1.lower_bound * var2.lower_bound
                    possibility_2 = coeff * var1.lower_bound * var2.upper_bound
                    possibility_3 = coeff * var1.upper_bound * var2.lower_bound
                    possibility_4 = coeff * var1.upper_bound * var2.upper_bound
                    min_value += min(possibility_1, possibility_2, possibility_3, possibility_4)
                    max_value += max(possibility_1, possibility_2, possibility_3, possibility_4)
            elif hasattr(term, "lower_bound"):
                # Linear term
                if coeff > 0:
                    min_value += coeff * term.lower_bound
                    max_value += coeff * term.upper_bound
                else:
                    min_value += coeff * term.upper_bound
                    max_value += coeff * term.lower_bound

        return min_value, max_value

    def __repr__(self):
        parts = []
        for key, coeff in self.terms.items():
            if coeff == 0:
                continue
            if isinstance(key, tuple):
                parts.append(f"{coeff}*({'*'.join(map(str, key))})")
            else:
                parts.append(f"{coeff}*{key}")
            # if coeff == 0:
            #     continue
            # if isinstance(key, tuple):
            #     print(key, coeff, "here")
            #     parts.append(f"{coeff}*({key[0]}*{key[1]})")
            # else:
            #     parts.append(f"{coeff}*{key}")
        if self.constant != 0:
            parts.append(str(self.constant))
        return " + ".join(parts)


class Constraint:
    def __init__(self, lhs, operator, rhs):
        if operator not in {"=", "<=", ">="}:
            raise ValueError("Operator must be '=', '<=', or '>='.")
        if not isinstance(rhs, (int, float)):
            raise ValueError("Right-hand side must be a constant.")
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __repr__(self):
        return f"{self.lhs} {self.operator} {self.rhs}"


class OptimizationHelper(Constraint):
    def __init__(self):
        self.variables = []
        self.constraints = []
        self.objective = None
        self.variable_names = []  # To store variable names
        self.full_variable_names = []  # To store all binary variables
        self.user_variable_count = 0

    def _add_variable_helper(self, name, lower_bound=0, upper_bound=1):
        var = Variable(name, lower_bound, upper_bound)
        self.variables.append(var)
        self.variable_names.append(name)  # Store the variable name
        self.full_variable_names.extend([binary_var.name for binary_var, _ in var.binary_variables])
        return var

    def _expression_to_adjacency(self, expression, use_full_names=False):
        """
        Convert an expression into an adjacency matrix.

        :param expression: The expression to convert.
        :param use_full_names: Whether to use full variable names or variable names.
        :return: Adjacency matrix (2D numpy array).
        """
        if use_full_names:
            variable_list = self.full_variable_names
        else:
            variable_list = self.variable_names

        size = len(variable_list)
        adjacency_matrix = np.zeros((size, size))

        variable_index = {name: idx for idx, name in enumerate(variable_list)}

        for key, coeff in expression.terms.items():
            if isinstance(key, tuple):
                var1, var2 = key
            else:
                var1 = var2 = key

            idx1 = variable_index.get(var1.name if isinstance(var1, BinaryVariable) else var1, None)
            idx2 = variable_index.get(var2.name if isinstance(var2, BinaryVariable) else var2, None)

            if idx1 is not None and idx2 is not None:
                adjacency_matrix[idx1, idx2] += coeff
                if idx1 != idx2:
                    adjacency_matrix[idx2, idx1] += coeff
        
        for i in range(size):
            for j in range(i + 1, size):
                adjacency_matrix[i, j] /= 2
                adjacency_matrix[j, i] /= 2
        return adjacency_matrix

    def _convert_inequality(self, constraint):
        """
        Converts an inequality constraint into an equality constraint by adding a slack variable.
        The slack variable is composed of binary variables.
        """
        if constraint.operator not in {"<=", ">="}:
            raise ValueError("Conversion only applicable for '<=' or '>=' constraints.")

        # Determine the range of the slack variable
        # expr = constraint.lhs - constraint.rhs if constraint.operator == "<=" else constraint.rhs - constraint.lhs
        lb, ub = constraint.lhs.find_extreme()
        b = constraint.rhs
        # Create the slack variable
        slack_var_name = f"s{len(self.variables)}"
        if constraint.operator == "<=":
            slack_var = self.add_variable(slack_var_name, lower_bound=0, upper_bound=int(b-lb))
            self.user_variable_count -= 1
        else: # >=
            slack_var = self.add_variable(slack_var_name, lower_bound=0, upper_bound=int(ub-b))
            self.user_variable_count -= 1
        # Update the constraint to an equality
        if constraint.operator == "<=":
            new_constraint = Constraint(constraint.lhs + slack_var.to_expression(), "=", b)
        else:  # ">="
            new_constraint = Constraint(constraint.lhs - slack_var.to_expression(), "=", b)

        # Replace the old constraint with the new one
        self.constraints.remove(constraint)
        self.constraints.append(new_constraint)

    def _constraint_to_expression(self, constraint):
        if constraint.operator != "=":
            raise ValueError("Conversion to expression only applicable for '=' constraints.")
        temp = constraint.lhs - constraint.rhs
        expr = temp * temp
        return expr

    def _quadratize(self, expr):
        new_expr = Expression()
        def term_degree(term):
            if isinstance(term, tuple):
                degree = 0
                for var in term:
                    if isinstance(var, tuple):
                        degree += term_degree(var)
                    elif isinstance(var, BinaryVariable):
                        degree += 1
                return degree
            return 1

        for term, coeff in expr.terms.items():
            degree = term_degree(term)
            if degree <= 2:
                new_expr.terms[term] = new_expr.terms.get(term, 0) + coeff
            elif degree == 3: # cxyz = c - ac - cx - cy - cz + cax + cay + caz + cxy + cxz + cyz, where c is the coefficient and a is an auxiliary variable
                var1, (var2, var3) = term
                if var1.lower_bound != 0 or var1.upper_bound != 1 or var2.lower_bound != 0 or var2.upper_bound != 1 or var3.lower_bound != 0 or var3.upper_bound != 1:
                    raise ValueError("Only degree 3 binary variables are supported.")
                aux_var = self.add_variable(f"a{len(self.variables)}", 0, 1)
                self.user_variable_count -= 1
                aux_var = aux_var.binary_variables[0][0]
                new_expr.terms[(aux_var)] = new_expr.terms.get((aux_var), 0) - coeff
                new_expr.terms[(var1)] = new_expr.terms.get((var1), 0) - coeff
                new_expr.terms[(var2)] = new_expr.terms.get((var2), 0) - coeff
                new_expr.terms[(var3)] = new_expr.terms.get((var3), 0) - coeff
                new_expr.terms[(aux_var, var1)] = new_expr.terms.get((aux_var, var1), 0) + coeff
                new_expr.terms[(aux_var, var2)] = new_expr.terms.get((aux_var, var2), 0) + coeff
                new_expr.terms[(aux_var, var3)] = new_expr.terms.get((aux_var, var3), 0) + coeff
                new_expr.terms[(var1, var2)] = new_expr.terms.get((var1, var2), 0) + coeff
                new_expr.terms[(var1, var3)] = new_expr.terms.get((var1, var3), 0) + coeff
                new_expr.terms[(var2, var3)] = new_expr.terms.get((var2, var3), 0) + coeff
            else:
                raise ValueError("Only terms of degree 3 and below are supported.")
        return new_expr

    def _create_qubo(self, lam=None):
        if self.objective is None:
            raise ValueError("Objective function is not set.")
        obj = self.objective
        i = 0
        while i < len(self.constraints):
            if self.constraints[i].operator in {"<=", ">="}:
                self._convert_inequality(self.constraints[i])
            else:
                i += 1
        
        for i in range(len(self.constraints)):
            constr_expr = self._constraint_to_expression(self.constraints[i])
            if lam is None:
                max_coeff = abs(max(constr_expr.terms.values(), key=abs))
                lam = max_coeff*5
            obj += lam * constr_expr
        obj = self._quadratize(obj)
        qubo = self._expression_to_adjacency(obj, True)
        return qubo

    def _spins_to_variables(self, spins):
        if len(spins) != len(self.full_variable_names):
            raise ValueError("The number of spins must match the number of binary variables.")

        spin_dict = {name: spin for name, spin in zip(self.full_variable_names, spins)}
        variable_values = {}

        for var in self.variables:
            value = var.lower_bound
            for binary_var, coeff in var.binary_variables:
                value += spin_dict[binary_var.name] * coeff
            variable_values[var.name] = value

        return variable_values


    def _compute_expression_value(self, expression, spins):
            value = expression.constant
            for term, coeff in expression.terms.items():
                if isinstance(term, tuple):
                    if isinstance(term[1], tuple):
                        term_value = coeff
                        var1 = term[0]
                        var2 = term[1][0]
                        var3 = term[1][1]
                        term_value *= spins[self.full_variable_names.index(str(var1))] * spins[self.full_variable_names.index(str(var2))] * spins[self.full_variable_names.index(str(var3))]   
                        value += term_value
                    else:
                        term_value = coeff
                        var1 = term[0]
                        var2 = term[1]
                        term_value *= spins[self.full_variable_names.index(str(var1))] * spins[self.full_variable_names.index(str(var2))]   
                        value += term_value
                else:
                    value += coeff * spins[self.full_variable_names.index(str(term))]
            return value

    def _compute_objective_value(self, spins):
        if self.objective is None:
            raise ValueError("Objective function is not set.")
        return self._compute_expression_value(self.objective, spins)

    def _check_constraints(self, spins):
        for constraint in self.constraints:
            lhs_value = self._compute_expression_value(constraint.lhs, spins)
            if constraint.operator == "=" and not np.isclose(lhs_value, constraint.rhs):
                return False
            elif constraint.operator == "<=" and lhs_value > constraint.rhs:
                return False
            elif constraint.operator == ">=" and lhs_value < constraint.rhs:
                return False
        return True

    def __repr__(self):
        repr_str = "Optimization Problem\n"
        repr_str += "Variables:\n" + "\n".join(str(v) for v in self.variables) + "\n"
        if self.objective:
            repr_str += f"Objective:\n  {self.objective}\n"
        if self.constraints:
            repr_str += "Constraints:\n" + "\n".join(str(c) for c in self.constraints) + "\n"
        repr_str += "Variable Names:\n" + ", ".join(self.variable_names) + "\n"
        repr_str += "Full Variable Names:\n" + ", ".join(self.full_variable_names) + "\n"
        return repr_str


# Example Usage
if __name__ == "__main__":
    from optimizationProblem import OptimizationProblem
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

    # Create QUBO
    vars, obj, feasible = prob2.solve(10)
    print(vars, obj, feasible)
    ##########################################################

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
        print("Test 1 True")

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
        print("Test 2 True")

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
        print("Test 3 True")

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
        print("Test 4 True")