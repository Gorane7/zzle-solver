import solvers


if __name__ == '__main__':
    # solvers.solve_specific("maps/basic.txt", [[(0, 0), (1, 3), (6, 0)]])
    solvers.solve_with_dfs("maps/basic.txt")
    # solvers.solve_with_bfs("maps/basic.txt")
    # solvers.solve_with_random("maps/basic.txt")
