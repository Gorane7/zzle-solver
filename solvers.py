import time

import parsers
import deque
import sol_gen
import simulator


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
            break
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
    print(success, message)


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
    print(success, message)