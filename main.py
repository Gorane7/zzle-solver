import time
import glob

import solvers


if __name__ == '__main__':
    # solvers.solve_specific("maps/basic.txt", [[(0, 0), (1, 3), (6, 0)]])
    # solvers.timed_comparison("maps/basic.txt")
    for map_name in glob.glob("maps/*"):
        print(f"Doing {map_name}")
        success, solution, time_taken = solvers.solve_with_dfs(map_name)
        print(f"{map_name}: {time_taken} {success} {solution}")
        