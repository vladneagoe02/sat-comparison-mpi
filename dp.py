import sys
from cnf import CNF

def eliminate_variable(F, var):
    """Perform DP elimination of var on formula F (list of lists)."""
    pos = [cl for cl in F if var in cl]
    neg = [cl for cl in F if -var in cl]
    rest = [cl for cl in F if var not in cl and -var not in cl]
    resolvents = []
    for c1 in pos:
        for c2 in neg:
            # resolve on var
            new = [l for l in c1 if l != var] + [l for l in c2 if l != -var]
            # remove duplicates
            resolvents.append(sorted(set(new)))
    return rest + resolvents

def dp_solve(cnf):
    F = [list(cl) for cl in cnf.clauses]
    for v in range(1, cnf.n_vars+1):
        F = eliminate_variable(F, v)
        if [] in F:
            return False
    return True

if __name__ == "__main__":
    cnf = CNF()
    cnf.load(sys.argv[1])
    res = dp_solve(cnf)
    print("UNSAT" if not res else "SAT")
