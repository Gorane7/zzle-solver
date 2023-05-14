import time

import solvers


if __name__ == '__main__':
    # solvers.solve_specific("maps/basic.txt", [[(0, 0), (1, 3), (6, 0)]])
    # solvers.timed_comparison("maps/basic.txt")
    success, solution, time_taken = solvers.solve_with_dfs("maps/4_0.txt")
    print(f"Solution was {solution}")
    print(f"Finding solution took {time_taken} seconds")
