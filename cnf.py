# cnf.py

import sys

class CNF:
    """Simple CNF formula representation."""

    def __init__(self):
        # clauses: list of lists of ints (positive for var, negative for negated var)
        self.clauses = []
        self.n_vars = 0

    def add_clause(self, lits):
        """Add a clause (list of ints)."""
        self.clauses.append(list(lits))
        for v in lits:
            self.n_vars = max(self.n_vars, abs(v))

    def load(self, path):
        """Load from DIMACS .cnf file, skipping comments and end‐of‐formula markers."""
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('c') or line.startswith('%'):
                    continue
                if line.startswith('p'):
                    # p cnf num_vars num_clauses
                    parts = line.split()
                    if len(parts) >= 3:
                        self.n_vars = int(parts[2])
                    continue
                # otherwise it's a clause line ending in 0
                parts = line.split()
                if parts[-1] == '0':
                    lits = list(map(int, parts[:-1]))
                    if lits:
                        self.add_clause(lits)

    def write(self, path):
        """Write to DIMACS .cnf format."""
        with open(path, 'w') as f:
            f.write(f"p cnf {self.n_vars} {len(self.clauses)}\n")
            for cl in self.clauses:
                f.write(" ".join(map(str, cl)) + " 0\n")

    def copy(self):
        """Deep copy."""
        new = CNF()
        new.clauses = [list(cl) for cl in self.clauses]
        new.n_vars = self.n_vars
        return new

if __name__ == "__main__":
    # quick test: prints var/clause counts for a given file
    if len(sys.argv) != 2:
        print("Usage: python cnf.py <file.cnf>")
        sys.exit(1)
    cnf = CNF()
    cnf.load(sys.argv[1])
    print("Vars:", cnf.n_vars, "Clauses:", len(cnf.clauses))
