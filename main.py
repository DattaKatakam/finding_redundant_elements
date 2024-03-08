from sympy import symbols
from sympy.logic.boolalg import Or, And, Implies, Not
from src.formula_conversions import formula_conversions
from src.dimac_solver import *
import numpy as np

# Define the SAT formula
# trainLate, taxi, johnLate = symbols('trainLate taxi johnLate')
# sat_formula = Implies(Implies(And(trainLate, Not(taxi)), johnLate),
#                       Implies(Not(johnLate), Implies(trainLate, taxi)))

A, B, C = symbols('A, B, C')
# sat_formula = And(
#     Or(A, B),
#     Or(B, C)
# )
sat_formula = And(
    Or(A, B),
    Or(Not(A), Not(B)),
    Or(A, C),
    Or(Not(B), C)
)

f_convertor = formula_conversions(sat_formula)

print(f"Sat formula is: {sat_formula}")
variables = f_convertor.get_variables()

print(f"\nwriting cnf formula from sat : {f_convertor.get_cnf_formula()}")

dimac_formula = f_convertor.get_dimac_formula()
print(f"printing dimac formula using dimac convention.py {dimac_formula}")

# print(f"printing cnf from dimac: {f_convertor.get_dimac_to_cnf_formula(dimac_formula)}")

sat = check_satisfiability(dimac_formula)

if sat != "UNSAT":
    print("Satisfiable")

    all_models = get_models(dimac_formula)
    np_all_models = np.array(all_models)
    print("Models:")
    for model in all_models:
        print(model)
    print("\n")
    # after getting sub sets we check semantic entailment of these new subsets to original dimac
    # !( original -> subset) and !(subset -> original) both are unsat then that particular clause is redundant

    print("getting dimac subsets")
    dimac_subsets = get_subsets(dimac_formula)
    for i, inst_subset in enumerate(dimac_subsets):
        semEqui = check_semantic_entailment(dimac_formula, inst_subset)
        # print(inst_subset)
        if semEqui:
            print(f"{dimac_formula[i]} is redundant in formula")
        else:
            print(f"{dimac_formula[i]} is non redundant in formula")
        print("\n")
        instModels = get_models(inst_subset)
        if np.array_equal(np_all_models, np.array(instModels)):
            print(f"{dimac_formula[i]} is having same models")
        else:
            print(f"{dimac_formula[i]} is having different models")
else:
    print("Unsatisfiable")


