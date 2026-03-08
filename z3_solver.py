from z3 import *
import re
import sys

def parse_formula(expr, variables):
    expr = expr.strip()

    # Remove outer parentheses
    while expr.startswith('(') and expr.endswith(')'):
        depth = 0
        balanced = True
        for i, c in enumerate(expr):
            if c == '(': depth += 1
            elif c == ')': depth -= 1
            if depth == 0 and i < len(expr) - 1:
                balanced = False
                break
        if balanced:
            expr = expr[1:-1].strip()
        else:
            break

    # Handle ¬ (negation) at the start
    if expr.startswith('¬') or expr.startswith('~'):
        return Not(parse_formula(expr[1:].strip(), variables))

    for op_sym, op_fn in [('∨', Or), ('∧', And)]:
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            if expr[i] == ')': depth += 1
            elif expr[i] == '(': depth -= 1
            elif depth == 0 and expr[i] == op_sym:
                left  = expr[:i].strip()
                right = expr[i+1:].strip()
                return op_fn(parse_formula(left, variables),
                             parse_formula(right, variables))

    # It's a variable
    name = expr.strip()
    if name not in variables:
        variables[name] = Bool(name)
    return variables[name]


def extract_variables(expr):
    return sorted(set(re.findall(r'\b[a-zA-Z_]\w*\b', expr)))


def main():
    print("\nZ3 Satisfiability Checker")
    print("-" * 40)
    print("Supported operators:  ¬ or ~  (NOT),  ∧  (AND),  ∨  (OR)")
    print("Example input:  p ∧ ¬¬(¬q ∧ ¬¬p)")
    print("-" * 40)

    raw = input("\nEnter formula: ").strip()
    if not raw:
        print("No formula entered.")
        sys.exit(1)

    variables = {}
    try:
        formula = parse_formula(raw, variables)
    except Exception as e:
        print(f"Could not parse formula: {e}")
        sys.exit(1)

    print(f"\nParsed formula : {formula}")
    print(f"Variables found: {', '.join(sorted(variables.keys()))}")

    s = Solver()
    s.add(formula)
    result = s.check()

    print(f"\nResult : {str(result).upper()}")

    if result == sat:
        model = s.model()
        print(f"Model  : {model}")
    else:
        print("No satisfying assignment exists.")

    print()

if __name__ == "__main__":
    main()