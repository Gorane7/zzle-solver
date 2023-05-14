import random


def gen_sol(functions):
    # conditionals = ["A", "O", "T", "P"]
    # actions = ["M", "R", "L", "CO", "CT", "CP"]
    # for key in functions.keys():
        # actions.append(key)
    action_amount = 6 + len(functions.keys()) - 1
    sol = {}
    for key, val in functions.items():
        chosen_len = random.randint(0, val)
        this_func = []
        for i in range(chosen_len):
            # action, conditional
            this_func.append((random.randint(0, action_amount), random.randint(0, 3)))
        sol[key] = this_func
    return sol


def gen_empty_sol(functions):
    return {key: [] for key in functions.keys()}


def gen_additional_sols(functions, sol):
    # conditionals = ["A", "O", "T", "P"]
    # actions = ["M", "R", "L", "CO", "CT", "CP"]
    # for key in sol.keys():
        # actions.append(key)
    action_amount = 6 + len(functions.keys())
    new_sols = []    
    for key in sol.keys():
        if len(sol[key]) == functions[key]:
            continue
        for conditional in range(4):
            for action in range(action_amount):
                new_sol = {key1: [x for x in val] for key1, val in sol.items()}
                new_sol[key].append((action, conditional))
                new_sols.append(new_sol)
    # print(new_sols)
    return new_sols