import time

import parsers
import deque
import sol_gen
import simulator


def timed_comparison(filename):
    start = time.time()
    success, message = solve_with_dfs(filename)
    print(f"DFS took {time.time() - start} seconds and found solution {message}")
    
    start = time.time()
    success, message = solve_with_bfs(filename)
    print(f"BFS took {time.time() - start} seconds and found solution {message}")

    start = time.time()
    success, message = solve_with_random(filename)
    print(f"Random took {time.time() - start} seconds and found solution {message}")


def solve_specific(filename, solution):
    task_map, functions = parsers.textfile_parser(filename)
    success, message = simulator.try_solve([
        {key: val for key, val in task_map[0].items()},
        {x for x in task_map[1]},
        task_map[2]
    ], solution, True)
    print([success, message])


def solve_with_dfs(filename):
    start = time.time()
    task_map, functions = parsers.textfile_parser(filename)
    i = 0
    print_every = 10000
    sol = sol_gen.gen_empty_sol(functions)
    success, solution = do_dfs(task_map, sol, functions)
    time_taken = time.time() - start
    simulator.try_solve([
        {key: val for key, val in task_map[0].items()},
        {x for x in task_map[1]},
        task_map[2]
    ], sol, True)
    return success, solution, time_taken


def do_dfs(task_map, current_sol, function_sizes):
    success, message = simulator.try_solve([
        {key: val for key, val in task_map[0].items()},
        {x for x in task_map[1]},
        task_map[2]
    ], current_sol, False)
    if success:
        return success, current_sol
    to_mod = min([x for x in function_sizes.keys() if function_sizes[x] > len(current_sol[x])] + [1024])
    if to_mod == 1024:
        return False, "Fully mapped functions"
    action_amount = 6 + len(function_sizes.keys())
    for conditional in range(4):
        for action in range(action_amount):
            current_sol[to_mod].append((action, conditional))
            success, message_or_sol = do_dfs(task_map, current_sol, function_sizes)
            if success:
                return success, message_or_sol
            current_sol[to_mod].pop()
    return False, "Iterated through all solutions"


def solve_with_bfs(filename):
    task_map, functions = parsers.textfile_parser(filename)
    solutions = deque.Deque()
    solutions.add(sol_gen.gen_empty_sol(functions))
    i = 0
    print_every = 10000
    while True:
        if i % print_every == 0:
            start = time.time()
        if solutions.size():
            sol = solutions.get()
        else:
            print(f"ERROR: Tried all possible solutions ({i}), but none worked")
            return
        success, message = simulator.try_solve([
            {key: val for key, val in task_map[0].items()},
            {x for x in task_map[1]},
            task_map[2]
        ], sol)
        if success:
            print(sol)
            break
        for new_sol in sol_gen.gen_additional_sols(functions, sol):
            solutions.add(new_sol)
        if i % print_every == print_every - 1:
            dur = time.time() - start
            print(f"Checking {print_every} solutions took {dur} seconds, solution stack size: {solutions.size()}")
        i += 1
    """simulator.try_solve([
        {key: val for key, val in task_map[0].items()},
        {x for x in task_map[1]},
        task_map[2]
    ], sol, True)"""
    return success, message


def solve_with_random(filename):
    task_map, functions = parsers.textfile_parser(filename)
    i = 0
    print_every = 10000
    while True:
        if i % print_every == 0:
            start = time.time()
        sol = sol_gen.gen_sol(functions)
        success, message = simulator.try_solve([
            {key: val for key, val in task_map[0].items()},
            {x for x in task_map[1]},
            task_map[2]
        ], sol)
        if success:
            print(sol)
            break
        if i % print_every == print_every - 1:
            dur = time.time() - start
            print(f"Checking {print_every} solutions took {dur} seconds")
        i += 1
    return success, message