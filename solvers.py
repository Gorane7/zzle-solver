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


def solve_with_dfs(filename, illustrate=False):
    start = time.time()
    task_map, functions = parsers.textfile_parser(filename)
    i = 0
    print_every = 10000
    sol = sol_gen.gen_empty_sol(functions)
    # success, solution, i = do_dfs_recursive(task_map, sol, functions, 0, time.time())
    success, solution, i = do_dfs_iterative(task_map, sol, functions)
    time_taken = time.time() - start
    if illustrate:
        simulator.try_solve([
            {key: val for key, val in task_map[0].items()},
            {x for x in task_map[1]},
            task_map[2]
        ], sol, True)
    return success, solution, time_taken


def do_dfs_iterative(task_map, current_sol, function_sizes):
    i = 0
    start = time.time()
    sol_stack = []
    full_list = []
    for conditional in range(3, -1, -1):
        for action in range(6 + len(function_sizes.keys()) - 1, -1, -1):
            full_list.append((action, conditional))

    for action, conditional in full_list:
        sol_stack.append((True, action, conditional, 0))

    while sol_stack:
        to_add, action, conditional, position = sol_stack.pop()
        if to_add:
            current_sol[position].append((action, conditional))
            success, message = simulator.try_solve([
                {key: val for key, val in task_map[0].items()},
                {x for x in task_map[1]},
                task_map[2]
            ], current_sol, False)
            i += 1
            if i % 10000 == 0:
                diff = time.time() - start
                print(f"Checked {i / 1000000}M solutions at {round(1000000 * diff / i, 2)} microseconds per solution", end="\r")
            sol_stack.append((False, action, conditional, position))
            if success:
                return success, current_sol, i
            for to_mod in function_sizes.keys():
                if function_sizes[to_mod] > len(current_sol[to_mod]):
                    for action, conditional in full_list:
                        sol_stack.append((True, action, conditional, to_mod))
        else:
            current_sol[position].pop()
    return False, "Tried all solutions", i


def do_dfs_recursive(task_map, current_sol, function_sizes, i, start):
    success, message = simulator.try_solve([
        {key: val for key, val in task_map[0].items()},
        {x for x in task_map[1]},
        task_map[2]
    ], current_sol, False)
    i += 1
    if i % 10000 == 0:
        diff = time.time() - start
        print(f"Checked {i / 1000000}M solutions at {round(1000000 * diff / i, 2)} microseconds per solution", end="\r")
    if success:
        return success, current_sol, i
    
    action_amount = 6 + len(function_sizes.keys())
    for to_mod in function_sizes.keys():
        if function_sizes[to_mod] > len(current_sol[to_mod]):
            for conditional in range(4):
                for action in range(action_amount):
                    current_sol[to_mod].append((action, conditional))
                    success, message_or_sol, i = do_dfs_recursive(task_map, current_sol, function_sizes, i, start)
                    if success:
                        return success, message_or_sol, i
                    current_sol[to_mod].pop()
    return False, "Iterated through all solutions", i


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