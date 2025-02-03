import numpy as np
from cobiformulate.formulate import OptimizationHelper, Constraint
import cobiformulate.cobi_cloud.cobi_cloud as cloud

class OptimizationProblem(OptimizationHelper):
    def __init__(self):
        super().__init__()
        self.variables = []
        self.constraints = []
        self.objective = None
        self.variable_names = []  # To store variable names
        self.full_variable_names = []  # To store all binary variables
        self.user_variable_count = 0
 
    def add_variable(self, base_name, lower_bound=0, upper_bound=1, count=1):
        self.user_variable_count += count
        if count == 1:
            return self._add_variable_helper(base_name, lower_bound, upper_bound)
        return np.array([self._add_variable_helper(f"{base_name}{i}", lower_bound, upper_bound) for i in range(count)])

    def set_objective(self, expr):
        self.objective = expr

    def add_constraint(self, lhs, operator, rhs):
        if isinstance(lhs, np.ndarray) and isinstance(rhs, np.ndarray):
            if len(lhs) != len(rhs):
                raise ValueError("The number of expressions and constants must be the same.")
            for expr, const in zip(lhs, rhs):
                constraint = Constraint(expr, operator, float(const))
                self.constraints.append(constraint)
                self.original_constraints.append(constraint) # Used for validating constraints
        else:
            constraint = Constraint(lhs, operator, rhs)
            self.constraints.append(constraint)
            self.original_constraints.append(constraint) # Used for validating constraints

    def solve(self, timeoutSec = 1, target = None, lam=None):
        qubo = self._create_qubo(lam)
        solution = cloud.send_problem(qubo)
        solution=solution[0]
        variable_values = self._spins_to_variables(solution)
        obj_value = self._compute_objective_value(solution)
        feasible = self._check_constraints(solution)
        sol = [value for key, value in variable_values.items()][:self.user_variable_count]
        return sol, obj_value, feasible

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
    
if __name__ == "__main__":
    import cobiformulate as cobi
    prob5 = cobi.OptimizationProblem()
    N = 2
    x = prob5.add_variable("x", 0, 1)
    y = prob5.add_variable("y", 0, 1)
    prob5.set_objective(3*x + 5*y + x*x +  2*x*y + x*x*x + y*y*y*y)
    prob5.add_constraint(2*x + 4*y, "<=", 10)
    prob5.add_constraint(x + 3*y + x*y, "<=", 8)
    sol, obj, feas = prob5.solve()
    print(sol, obj, feas)