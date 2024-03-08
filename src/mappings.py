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
