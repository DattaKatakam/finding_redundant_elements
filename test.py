from sympy import symbols
from sympy.logic.boolalg import Or, And, Implies, Not
from src.formula_conversions import formula_conversions
from src.dimac_solver import *
import numpy as np

A, B, C = symbols('A, B, C')
sat_formula = And(
    Or(A, B),
    Or(B, C),
    Or(A, B)
)
f_c = formula_conversions()

dimac_formula = [[3, 1], [1, 2], [3, 1]]
print(dimac_formula)
temp_cnf = f_c.get_cnf_from_dimac(dimac_formula)
print(temp_cnf)

sat = check_satisfiability(dimac_formula)
if sat != "UNSAT":
    all_models = get_models(dimac_formula)
    print(f"dimac structure of the sat is {dimac_formula}")
    print("\nchecking sematic entailment for variables in the clause.....")
    listC = check_dimac_semantic_entailment(dimac_formula)
    if listC:
        print("redundant sub formulas in the main formula is/are: ")
        for listInst in listC:
            print(listInst)
        print("these are individually redundant at a time i.e when one is not present then only these particular sub "
              "formulas are redundant")
    else:
        print("there are no redundant individual elements")
