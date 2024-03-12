from src.dimac_solver import *

f_c = formula_conversions()

dimac_formula = [[3, 1], [1, 2], [3, 1]]
# dimac_formula = [[1, 3, 2, -2], [1, 3, -1, -2], [1, 3, -3, -2]]
print(f"Given dimac formula: {dimac_formula}")
temp_cnf = f_c.get_cnf_from_dimac(dimac_formula)
print(f"writing cnf formula from Dimac: {temp_cnf}")

sat = check_satisfiability(dimac_formula)
if sat != "UNSAT":
    print("\nSatisfiable")
    all_models = get_models(dimac_formula)
    print(f"dimac structure of the sat is {dimac_formula}")
    print("\nchecking sematic entailment for variables in the clause.....")
    listC = check_dimac_cnf_redundant_elements(dimac_formula)
    if listC:
        print("redundant sub formulas in the main formula is/are: ")
        for listInst in listC:
            print(listInst)
        print("these are individually redundant at a time i.e when one is not present then only these particular sub "
              "formulas are redundant")
    else:
        print("there are no redundant individual elements")
