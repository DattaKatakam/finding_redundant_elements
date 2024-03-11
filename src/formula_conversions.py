from sympy.logic.boolalg import to_cnf, Not, And, Or
from src.mappings import *


class formula_conversions:
    def __init__(self, formula=None):
        if formula is not None:
            self.sat_formula = formula
            self.cnf_formula = to_cnf(self.sat_formula)
            self.variables = set(self.cnf_formula.atoms())

    def get_dimac_formula(self):
        var_mapping = get_var_mapping(self.cnf_formula)
        dimacs_formula = []

        for clause in self.cnf_formula.args:
            dimacs_clause = []
            for literal in clause.args:
                if literal.is_Not:
                    dimacs_clause.append(-var_mapping[literal.args[0]])
                else:
                    dimacs_clause.append(var_mapping[literal])
            dimacs_formula.append(dimacs_clause)
        return dimacs_formula

    def get_cnf_formula(self):
        return self.cnf_formula

    def set_cnf(self, t_cnf_formula):
        self.cnf_formula = t_cnf_formula
        self.variables = set(self.cnf_formula.atoms())

    def get_variables(self):
        return self.variables

    def get_dimac_to_cnf_formula(self, dimacs_formula):
        disjunctions = []
        var_mapping = get_val_mapping(self.variables)
        for clause in dimacs_formula:
            literals = []
            for literal in clause:
                if literal < 0:
                    symbol = Not(var_mapping[literal * -1])
                else:
                    symbol = var_mapping[literal]
                literals.append(symbol)
            disjunctions.append(Or(*literals))
        cnf_formulaD = And(*disjunctions)
        return cnf_formulaD

    def get_cnf_from_dimac(self, dimac_formula):
        disjunctions = []
        var_mapping = get_unique_values(dimac_formula)
        for clause in dimac_formula:
            literals = []
            for literal in clause:
                if literal < 0:
                    symbol = Not(var_mapping[literal * -1])
                else:
                    symbol = var_mapping[literal]
                literals.append(symbol)
            disjunctions.append(Or(*literals))
        cnf_formulaD = And(*disjunctions)
        self.set_cnf(cnf_formulaD)
        return cnf_formulaD
