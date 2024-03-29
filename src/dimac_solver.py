import pycosat
import itertools
from src.mappings import *
import copy
from src.formula_conversions import formula_conversions


def get_models(dimacs_form):
    n_models = []
    for model in pycosat.itersolve(dimacs_form):
        model_dict = {}
        for i, var in enumerate(model, start=1):
            model_dict[i] = var > 0
        n_models.append(model_dict)
    return n_models


def check_satisfiability(dimacs_formula):
    return pycosat.solve(dimacs_formula)


def get_subsets(dimac_input_list):
    subset_output_list = []
    for i in range(len(dimac_input_list)):
        sublist = []
        for j in range(len(dimac_input_list)):
            if j != i:
                sublist.append(dimac_input_list[j])
        subset_output_list.append(sublist)
    return subset_output_list


def negated_dimac(dimacs_input_list):
    combinations_maker = list(itertools.product(*dimacs_input_list))
    negated_output_list = []
    for combo in combinations_maker:
        transformed_combo = []
        for x in combo: transformed_combo.append(-x)
        negated_output_list.append(transformed_combo)

    return negated_output_list


def restructure(f1, f2):
    result_formula = []
    for clause in f1: result_formula.append(clause[:])
    for clause in f2: result_formula.append(clause[:])
    return result_formula


def check_semantic_entailment(main_form, sub_form):
    negated_sub_form = negated_dimac(sub_form)
    negated_main_form = negated_dimac(main_form)
    form1 = restructure(main_form, negated_sub_form)
    form2 = restructure(sub_form, negated_main_form)
    satVal_form1 = check_satisfiability(form1)
    satVal_form2 = check_satisfiability(form2)
    if satVal_form1 == "UNSAT" and satVal_form2 == "UNSAT":
        return True
    else:
        return False


def check_dimac_redundant_sub_formulas(dimac_formula):
    print("getting dimac subsets and checking semantic entailment with sub sets generated.....")
    dimac_subsets = get_subsets(dimac_formula)
    redundant_sub_formulas = []
    for i, inst_subset in enumerate(dimac_subsets):
        semEqui = check_semantic_entailment(dimac_formula, inst_subset)
        # print(inst_subset)
        if semEqui:
            # print(f"{dimac_formula[i]} is redundant in formula")
            redundant_sub_formulas.append(inst_subset)
        else:
            print(f"{dimac_formula[i]} is non redundant in formula")
    return redundant_sub_formulas


def check_dimac_cnf_redundant_elements(dimac_formula):
    f_conv = formula_conversions()
    f_conv.get_cnf_from_dimac(dimac_formula)
    return check_dimac_redundant_elements(f_conv, dimac_formula)


def check_dimac_redundant_elements(formula_converter, dimac_formula):
    variables = formula_converter.get_variables()
    var_map = get_var_mapping(formula_converter.get_cnf_formula())
    redundant_elements = []
    print(var_map)
    modified_formula = []
    for var in variables:
        # print(f"var is {var} and var map is {var_map[var]}")
        is_redundant = False
        for varBool in {False, True}:
            sub_redundant = []
            reduced_cnf = copy.deepcopy(dimac_formula)
            checked = False
            # print(f"current reduced cnf is not altered: {reduced_cnf}")
            for j, clause in enumerate(reduced_cnf):
                duplicate_clause = copy.deepcopy(clause)
                # print(f"and j is {j} , clause is : {clause}")
                foundLit = False
                for i, lit in enumerate(clause):
                    # print(f"literal in the clause is : {lit}")
                    if abs(lit) == var_map[var]:
                        foundLit = True
                        if varBool:
                            clause[i] = lit
                        else:
                            clause[i] = -lit
                # print(f"changed the clause: {clause}")
                if not foundLit:
                    # print("couldn't find the literal or formula is same as original form in the clause")
                    # print("\n")
                    continue

                # print(f"changed dimacs for the {var} in dimac is {reduced_cnf}")
                checked = True
                semEqui = check_semantic_entailment(dimac_formula, reduced_cnf)
                # print(reduced_cnf)
                # print(f" the semantic entailment we got is: {semEqui}")
                if semEqui:
                    # print(f"{var} with this {varBool} is redundant in formula")
                    sub_redundant.append(var)
                    sub_redundant.append(varBool)
                    sub_redundant.append(reduced_cnf[j])
                    sub_redundant.append(duplicate_clause)
                    if reduced_cnf[j] != duplicate_clause:
                        # print(f"changed dimacs for the {var} in dimac is {reduced_cnf}")
                        modified_formula.append(copy.deepcopy(reduced_cnf))

                # else:
                # print(f"{var} with this {varBool} is non redundant in formula")
                # print("\n")
                reduced_cnf[j] = duplicate_clause
            if sub_redundant:
                redundant_elements.append(sub_redundant)

            if not checked:
                continue
        # print("\n\n")
    return modified_formula
