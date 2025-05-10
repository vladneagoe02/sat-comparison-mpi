import sys
import random
from cnf import CNF
from collections import defaultdict, deque

class DPLLSolver:
    def __init__(self, cnf):
        self.cnf = cnf.copy()
        self.assign = {}       # var → True/False
        self.level = {}        # var → decision level
        self.watches = defaultdict(list)
        self.decision_level = 0
        self.trail = []

        # initialize watches
        for i, cl in enumerate(self.cnf.clauses):
            if len(cl) >= 1:
                self.watches[cl[0]].append(i)
                if len(cl) > 1:
                    self.watches[cl[1]].append(i)

    def pick_branching_variable(self):
        """VSIDS-like: random unassigned variable."""
        unassigned = [v for v in range(1, self.cnf.n_vars+1) if v not in self.assign]
        return random.choice(unassigned) if unassigned else None

    def propagate(self):
        """Simple unit propagation."""
        queue = deque([lit for lit in self.assign if self.assign[lit]])
        while queue:
            lit = queue.popleft()
            opp = -lit
            for ci in list(self.watches[opp]):
                cl = self.cnf.clauses[ci]
                # check if clause is satisfied
                if any(self.assign.get(l, False) for l in cl):
                    continue
                # find new watch
                for l in cl:
                    if l != opp and not self.assign.get(-l, False):
                        self.watches[l].append(ci)
                        self.watches[opp].remove(ci)
                        break
                else:
                    # unit or conflict
                    unassigned = [l for l in cl if l not in self.assign and -l not in self.assign]
                    if not unassigned:
                        return False
                    if len(unassigned) == 1:
                        self.assign[unassigned[0]] = True
                        self.level[unassigned[0]] = self.decision_level
                        queue.append(unassigned[0])
        return True

    def backtrack(self, level):
        """Undo assignments down to given level."""
        for v in list(self.trail)[::-1]:
            if self.level[v] > level:
                self.assign.pop(v, None)
                self.level.pop(v, None)
                self.trail.remove(v)
        self.decision_level = level

    def solve(self):
        if not self.propagate():
            return False
        var = self.pick_branching_variable()
        if var is None:
            return True
        # decision
        self.decision_level += 1
        for value in [True, False]:
            self.assign[var if value else -var] = True
            self.level[var if value else -var] = self.decision_level
            self.trail.append(var if value else -var)
            if self.solve():
                return True
            self.backtrack(self.decision_level - 1)
        return False

if __name__ == "__main__":
    cnf = CNF()
    cnf.load(sys.argv[1])
    solver = DPLLSolver(cnf)
    res = solver.solve()
    print("UNSAT" if not res else "SAT")
