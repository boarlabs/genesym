from enum import Enum, auto
from typing import Dict, Optional, List

from cvxpy import Expression
from cvxpy import Minimize
from cvxpy import Problem
from cvxpy import Variable
from cvxpy.constraints.constraint import Constraint

class VarType(Enum):
    REAL = auto()
    BOOLEAN = auto()


class Model:
    
    def __init__(self) -> None:        
        self._constraints: Dict[str, Constraint] = dict()
        self._objective: Optional[Expression] = None
        self._vars: Dict[str, Variable] = dict()
        
    @property
    def objective(self) -> Expression:
        return self._objective
    
    def add_objective_terms(self, objective_terms: Expression) -> None:
        if self._objective is None:
            self._objective = objective_terms
        else:
            self._objective += objective_terms
            
    def get_objective_value(self) -> float:
        return self.objective.value

    def add_var(
        self,
        name: str,
        var_type: VarType,
        lb: Optional[float] = None,
        ub: Optional[float] = None,
    ) -> Variable:

        if var_type == VarType.REAL:
            var: Variable = Variable(name=name)
        elif var_type == VarType.BOOLEAN:
            var = Variable(name=name, boolean=True)
        else:
            raise ValueError("the Variable type is not supported")

        if ub is not None:
            self._constraints[f"{name}_upper_bound"] = var <= ub
        if lb is not None:
            self._constraints[f"{name}_lower_bound"] = var >= lb
        
        self._vars[name] = var
        return var
    
    def get_var(self, name: str) -> Optional[Variable]:
        return self._vars.get(name, None)
        # return self._vars[name]
    
    def sum_vars(self, variables: List[Optional[Variable]], coefs: Optional[List[float]]= None) -> Expression:
        if coefs is None:
            non_null_vars = [var for var in variables if var is not None]
            return sum(non_null_vars)
        else:
            return sum([(var * coef if var is not None else 0) for var, coef in zip(variables, coefs)])
        
 
    def get_var_value(self, var: Variable) -> float:
        return var.value


    def add_constraint(self, name: str, constraint: Constraint) -> None:
        self._constraints[name] = constraint
    
    def get_constraints(self, names: Optional[List[str]] = None) -> List[Constraint]:
        if names is None:
            return list(self._constraints.values())
        else:
            return [self._constraints[name] for name in names]
    

    def solve(self, solver: str = "CBC", verbose: bool = True) -> None:
        self._problem = Problem(Minimize(self.objective), self.get_constraints())
        self._problem.solve(solver=solver, verbose=verbose)

  
    def get_all_var_values(self) -> Dict[str, float]:
        return {name: var.value for name, var in self._vars.items()}
    
    
    def get_dual_var_values(self) -> Dict[str, float]:
        dual_vars = dict()
        for index, key in enumerate(self._constraints):
            
            # dual_vars[key] = self._problem.constraints[index].dual_value
            if self._problem.constraints[index].dual_value is not None:
                dual_vars[key] = self._problem.constraints[index].dual_value
                
        return dual_vars