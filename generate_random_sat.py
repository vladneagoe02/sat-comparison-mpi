# generate_random_sat.py
import random
from cnf import CNF

def random_3sat(n_vars, n_clauses):
    cnf = CNF()
    for _ in range(n_clauses):
        clause = random.sample(range(1, n_vars+1), 3)
        clause = [(v if random.random()<0.5 else -v) for v in clause]
        cnf.add_clause(clause)
    return cnf

if __name__=='__main__':
    cnf = random_3sat(100, 430)
    cnf.write('instances/random3sat.cnf')