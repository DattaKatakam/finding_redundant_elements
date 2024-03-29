from sympy.logic.boolalg import Or, And, Implies, Not
from src.dimac_solver import *

# Define the SAT formula
trainLate, taxi, johnLate = symbols('trainLate taxi johnLate')
sat_formula = Implies(Implies(And(trainLate, Not(taxi)), johnLate),
                      Implies(Not(johnLate), Implies(trainLate, taxi)))

# A, B, C = symbols('A, B, C')
# sat_formula = And(
#     Or(A, B),
#     Or(Not(A), Not(B)),
#     Or(A, C),
#     Or(Not(B), C)
# )

# A, B, C = symbols('A, B, C')
# sat_formula = And(
#     Or(A, B),
#     Or(Not(B), C)
# )

f_convertor = formula_conversions(sat_formula)

print(f"Sat formula is: {sat_formula}")
variables = f_convertor.get_variables()

test_cnf_formula = f_convertor.get_cnf_formula()
print(f"writing cnf formula from sat : {test_cnf_formula}")

dimac_formula = f_convertor.get_dimac_formula()
print(f"dimac structure of the sat is {dimac_formula}")
sat = check_satisfiability(dimac_formula)
if sat != "UNSAT":
    print("\nSatisfiable")
    all_models = get_models(dimac_formula)
    print("Models:")
    for model in all_models:
        print(model)
    print("\nchecking sematic entailment for variables in the clause.....")
    listV = check_dimac_redundant_elements(f_convertor, dimac_formula)
    if listV:
        print("original formula is modified after removing the redundant sub formulas is/are: ")
        for listInst in listV:
            print(listInst)
        print("these are individually redundant at a time i.e when one is not present then only these particular sub "
              "formulas are redundant")
    else:
        print("there are no redundant individual elements")

else:
    print("Unsatisfiable")
