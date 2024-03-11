import string
import random
from sympy import symbols


def get_unique_values(dimac_formula):
    flattened_list = [value for sublist in dimac_formula for value in sublist if value >= 0]
    unique_values = set(flattened_list)
    charset = list(string.ascii_letters)
    random.shuffle(charset)
    value_mapping = {value: symbols(charset[i]) for i, value in enumerate(unique_values)}
    return value_mapping


def get_var_mapping(cnf_formula):
    value_to_index = {}
    variables = set(cnf_formula.atoms())
    index = 1
    for value in variables:
        value_to_index[value] = index
        index += 1
    # print(f"Variables Mapping: {value_to_index}")
    return value_to_index


def get_val_mapping(variables):
    index_to_value = {}
    index = 1
    for value in variables:
        index_to_value[index] = value
        index += 1
    # print(f"index to values mapping: {index_to_value}\n")
    return index_to_value
