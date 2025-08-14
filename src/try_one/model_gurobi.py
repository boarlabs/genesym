from enum import Enum, auto
from typing import Dict, Optional, List

from gurobipy import LinExpr
from gurobipy import Constr
from gurobipy import Var
from gurobipy import Model as grbModel
from gurobipy import Env
from gurobipy import GRB 

class VarType(Enum):
    REAL = auto()
    BOOLEAN = auto()


class Model:
    
    def __init__(self) -> None:        
        # self._constraints: Dict[str, Constr] = dict()
        self._objective: Optional[LinExpr] = None
        self._vars: Dict[str, Var] = dict()
        self._problem =  grbModel("Optimization Model", env=self.get_gurobi_env())

        
    @property
    def objective(self) -> LinExpr:
        return self._objective
    
    def add_objective_terms(self, objective_terms: LinExpr) -> None:
        if self._objective is None:
            self._objective = objective_terms
        else:
            self._objective += objective_terms
            
    def get_objective_value(self) -> float:
        return self.objective.getValue()

    def add_var(
        self,
        name: str,
        var_type: VarType,
        lb: Optional[float] = None,
        ub: Optional[float] = None,
    ) -> Var:
        
        if lb is None:
            lb = -GRB.INFINITY
        if ub is None:
            ub = GRB.INFINITY

        
        if var_type == VarType.REAL:
           var = self._problem.addVar(vtype=GRB.CONTINUOUS, lb=lb, ub=ub, name=name)
                             
        elif var_type == VarType.BOOLEAN:
            var = self._problem.addVar(vtype=GRB.BINARY, lb=lb, ub=ub, name=name)
    
        self._vars[name] = var
        return var
    
    def get_var(self, name: str) -> Optional[Var]:
        return self._vars.get(name, None)
    
    def sum_vars(self, variables: List[Optional[Var]], coefs: Optional[List[float]]= None) -> LinExpr:
        if coefs is None:
            non_null_vars = [var for var in variables if var is not None]
            return sum(non_null_vars)
        else:
            return sum([(var * coef if var is not None else 0) for var, coef in zip(variables, coefs)])
        
 
    def get_var_value(self, var: Var) -> float:
        self._problem.update()
        return var.x


    def add_constraint(self, name: str, constraint: Constr) -> None:
        self._problem.addConstr(constraint, name)

    
    def get_constraints(self, names: Optional[List[str]] = None) -> List[Constr]:
        self._problem.update()
        if names is None:
            return NotImplementedError
        else:
            return [
                self._problem.getConstrByName(name)
                for name in names
            ]
    

    def solve(self) -> None:
        self._problem.setObjective(self.objective, GRB.MINIMIZE)
        self._problem.optimize()

  
    def get_all_var_values(self) -> Dict[str, float]:
        self._problem.update()
        return {
            name: var.x
                for name, var in self._vars.items()
        }
    
    
    def get_dual_var_values(self) -> Dict[str, float]:
        # works only for non-binary problems apparently.
        dual_vars = dict()
        self._problem.update()
        for constr in self._problem.getConstrs():
            # print(constr.Pi)
            dual_vars[constr.ConstrName] = constr.Pi
        
        
        # for index, key in enumerate(self._constraints):
            
            # # dual_vars[key] = self._problem.constraints[index].dual_value
            # if self._problem.constraints[index].dual_value is not None:
            #     dual_vars[key] = self._problem.constraints[index].dual_value
                
        return dual_vars
    
    
    def get_binding_constraints(self) -> List[str]:
        binding_inequality_constraints = []
        
        self._problem.update()
        for constr in self._problem.getConstrs():
            if (constr.Sense != "=") and constr.Slack == 0:
                binding_inequality_constraints.append(
                    constr.ConstrName
                )
        return binding_inequality_constraints
                
        
        
        
    
    
    
    
    @staticmethod
    def get_gurobi_env(timeout: int = 600, job_priority: int = 0):
        # compute server details are pulled from license file specified in environment variable: GRB_LICENSE_FILE
        return Env.ClientEnv(
            logfilename="",
            computeServer="",
            password="",
            priority=job_priority,
            timeout=timeout,
        )