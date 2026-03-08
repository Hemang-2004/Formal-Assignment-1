def simplify(formula, literal):
    new_formula = []
    for clause in formula:
        if literal in clause:
            continue
        new_clause = [l for l in clause if l != -literal]
        new_formula.append(new_clause)
    return new_formula


def unit_propagate(formula, assignment):
    changed = True
    while changed:
        changed = False
        for clause in formula:
            if len(clause) == 0:
                return None, None  # Empty clause = contradiction
            if len(clause) == 1:
                unit = clause[0]
                var = abs(unit)
                val = unit > 0
                if var in assignment:
                    if assignment[var] != val:
                        return None, None  # Contradiction
                else:
                    assignment[var] = val
                    formula = simplify(formula, unit)
                    changed = True
                    break
    return formula, assignment


def pure_literal_eliminate(formula, assignment):
    all_literals = [l for clause in formula for l in clause]
    literals_set = set(all_literals)

    for literal in literals_set:
        if -literal not in literals_set:
            var = abs(literal)
            val = literal > 0
            assignment[var] = val
            formula = simplify(formula, literal)

    return formula, assignment


def dpll(formula, assignment={}):

    assignment = dict(assignment)  # copy to avoid mutation across branches

    # Unit Propagation
    formula, assignment = unit_propagate(formula, assignment)
    if formula is None:
        return False, {}  # Contradiction found

    # Pure Literal Elimination
    formula, assignment = pure_literal_eliminate(formula, assignment)

    # Base cases
    if len(formula) == 0:
        return True, assignment  

    if any(len(clause) == 0 for clause in formula):
        return False, {} 

    var = abs(formula[0][0])

    # Try assigning True
    result, model = dpll(simplify(formula, var), {**assignment, var: True})
    if result:
        return True, model

    # Try assigning False (backtrack)
    result, model = dpll(simplify(formula, -var), {**assignment, var: False})
    if result:
        return True, model

    return False, {}

def var_name(lit, var_map_inv):
    name = var_map_inv.get(abs(lit), f"x{abs(lit)}")
    return f"¬{name}" if lit < 0 else name


def print_formula(formula, var_map_inv):
    clauses_str = []
    for clause in formula:
        lits = " ∨ ".join(var_name(l, var_map_inv) for l in clause)
        clauses_str.append(f"({lits})")
    print("  CNF Formula: " + " ∧ ".join(clauses_str))


if __name__ == "__main__":
    print("=" * 60)
    print("  DPLL Algorithm - Satisfiability Checker")
    print("=" * 60)
    print("\n[Example 1]")
    print("Formula: (A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ ¬C)")
    var_map_inv_1 = {1: "A", 2: "B", 3: "C"}

    formula1 = [
        [1, 2],       # A ∨ B
        [-1, 3],      # ¬A ∨ C
        [-2, -3],     # ¬B ∨ ¬C
    ]
    print_formula(formula1, var_map_inv_1)
    sat, model = dpll(formula1)
    if sat:
        print("  Result : SAT")
        print("  Model  :", {var_map_inv_1[k]: v for k, v in model.items()})
    else:
        print("  Result : UNSAT")


    print("\n[Example 2]")
    print("Formula: (P) ∧ (¬P)  — should be UNSAT")
    var_map_inv_2 = {1: "P"}
    formula2 = [
        [1],    # P
        [-1],   # ¬P
    ]
    print_formula(formula2, var_map_inv_2)
    sat, model = dpll(formula2)
    print("  Result :", "SAT" if sat else "UNSAT")
    print("\n[Example 3 — Assignment formula]")
    print("Formula: p ∧ ¬¬(¬q ∧ ¬¬p)")
    print("Simplified CNF: (p) ∧ (¬q) ∧ (p)")
    var_map_inv_3 = {1: "p", 2: "q"}
    formula3 = [
        [1],    # p
        [-2],   # ¬q
        [1],    # p  (from ¬¬p)
    ]
    print_formula(formula3, var_map_inv_3)
    sat, model = dpll(formula3)
    if sat:
        print("  Result : SAT")
        print("  Model  :", {var_map_inv_3[k]: v for k, v in model.items()})
    else:
        print("  Result : UNSAT")

    print("\n" + "=" * 60)
    print("  DPLL Complete.")
    print("=" * 60)
