import z3
from z3 import Bool, And, Not, Solver, sat

print("=" * 60)
print("  Exercise 2: Z3 Satisfiability Checker")
print("  Formula: p ∧ ¬¬(¬q ∧ ¬¬p)")
print("=" * 60)


p = Bool('p')
q = Bool('q')

print("\n Step -1 Variables declared: p, q")


formula = And(
    p,
    Not(Not(And(
        Not(q),
        Not(Not(p))
    )))
)

print(f"\n Step -2 Formula constructed:")
print(f"  {formula}")


s = Solver()
s.add(formula)

print("\n Step -3 Formula added to Z3 Solver.")


result = s.check()

print("\n Step -4 Checking satisfiability...")
print(f"\n  Result : {str(result).upper()}")

if result == sat:
    model = s.model()
    print(f"  Model  : {model}")
    print("\n  Interpretation:")
    for decl in model.decls():
        print(f"    {decl.name()} = {model[decl]}")
else:
    print("  The formula is UNSATISFIABLE.")
    print("  No truth assignment can make the formula True.")


print("\n Step -5 Manual Verification:")
print("  p=True, q=False:")
print("    p                    → True")
print("    ¬q                   → ¬False = True")
print("    ¬¬p                  → ¬¬True = True")
print("    ¬q ∧ ¬¬p            → True ∧ True = True")
print("    ¬¬(¬q ∧ ¬¬p)       → ¬¬True = True")
print("    p ∧ ¬¬(¬q ∧ ¬¬p)  → True ∧ True = True  ✓")

print("\n" + "=" * 60)
print("  Z3 Exercise Complete.")
print("=" * 60)
