from constraint import Problem, FunctionConstraint, AllDifferentConstraint

# Define time slots
time_slots = ['S1', 'S2', 'S3', 'S4', 'S5', 'M1', 'M2', 'M3', 'M4', 'M5', 
              'T1', 'T2', 'T3', 'W1', 'W2', 'W3', 'W4', 'W5', 'TH1', 'TH2', 
              'TH3', 'TH4', 'TH5']

# Define variables and their domains
variables = {
    'Sécurité_lecture': time_slots,
    'Sécurité_td': time_slots,
    'Méthodes_formelles_lecture': time_slots,
    'Méthodes_formelles_td': time_slots,
    'Analyse_numérique_lecture': time_slots,
    'Analyse_numérique_td': time_slots,
    'Entrepreneuriat_lecture': time_slots,
    'Recherche_opérationnelle_2_lecture': time_slots,
    'Recherche_opérationnelle_2_td': time_slots,
    'Distributed_Architecture_Intensive_Computing_lecture': time_slots,
    'Distributed_Architecture_Intensive_Computing_td': time_slots,
    'Réseaux_2_lecture': time_slots,
    'Réseaux_2_td': time_slots,
    'Réseaux_2_tp': time_slots,
    'Artificial_Intelligence_lecture': time_slots,
    'Artificial_Intelligence_td': time_slots,
    'Artificial_Intelligence_tp': time_slots
}

# Create problem instance
problem = Problem()

# Add variables to the problem
for var, domain in variables.items():
    problem.addVariable(var, domain)

# Define constraints
def not_same_day(a, b):
    return a[0] != b[0]

def not_same_time(a, b):
    return a != b

def all_different(*args):
    return len(args) == len(set(args))

# Add constraints to the problem
problem.addConstraint(AllDifferentConstraint(), list(variables.keys()))

# Add function constraints for not having lectures and TDs on the same day
problem.addConstraint(FunctionConstraint(not_same_day), ('Sécurité_lecture', 'Sécurité_td'))
problem.addConstraint(FunctionConstraint(not_same_day), ('Méthodes_formelles_lecture', 'Méthodes_formelles_td'))
problem.addConstraint(FunctionConstraint(not_same_day), ('Analyse_numérique_lecture', 'Analyse_numérique_td'))
problem.addConstraint(FunctionConstraint(not_same_day), ('Recherche_opérationnelle_2_lecture', 'Recherche_opérationnelle_2_td'))
problem.addConstraint(FunctionConstraint(not_same_day), ('Distributed_Architecture_Intensive_Computing_lecture', 'Distributed_Architecture_Intensive_Computing_td'))
problem.addConstraint(FunctionConstraint(not_same_day), ('Réseaux_2_lecture', 'Réseaux_2_td'))
problem.addConstraint(FunctionConstraint(not_same_day), ('Artificial_Intelligence_lecture', 'Artificial_Intelligence_td'))

# Solve the problem
solution = problem.getSolution()

# Print the solution
print("Solution:")
print(solution)
