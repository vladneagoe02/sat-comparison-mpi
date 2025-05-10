import sys
from cnf import CNF

def resolve(c1, c2, var):
    """Resolve on var: remove var and -var and union clauses."""
    return [l for l in c1 if l != var] + [l for l in c2 if l != -var]

def subsumes(c_big, c_small):
    """Check if c_small subsumes c_big."""
    return set(c_small).issubset(c_big)

def resolution_solve(cnf):
    F = [set(cl) for cl in cnf.clauses]
    new = set()
    while True:
        pairs = [(ci, cj) for i, ci in enumerate(F) for cj in F[i+1:]]
        for ci, cj in pairs:
            for lit in list(ci):
                if -lit in cj:
                    resolvent = set(resolve(list(ci), list(cj), lit))
                    if not resolvent:
                        return False  # unsatisfiable
                    # subsumption pruning
                    if not any(subsumes(r_big, resolvent) for r_big in F+list(new)):
                        new.add(frozenset(resolvent))
        if not new:
            return True  # no new clauses ⇒ satisfiable
        # add new and clear
        for r in new:
            F.append(set(r))
        new.clear()

if __name__ == "__main__":
    cnf = CNF()
    cnf.load(sys.argv[1])
    res = resolution_solve(cnf)
    print("UNSAT" if not res else "SAT")
