

def try_solve(task, sol):
    stack = []
    stack += sol[0][::-1]
    # screen = setup_display(task)
    # render_frame(task, screen)
    # time.sleep(0.1)
    dir_map = {
        "U": (0, -1),
        "L": (1, 0),
        "D": (0, 1),
        "R": (-1, 0)
    }
    rotate_right_map = {
        "U": "R",
        "R": "D",
        "D": "L",
        "L": "U"
    }
    rotate_left_map = {
        "U": "L",
        "L": "D",
        "D": "R",
        "R": "U"
    }
    c = 0
    while True:
        c += 1
        if c > 1000:
            return False, "out of time"
        if not stack:
            return False, "stack empty"
        action, condition = stack.pop()
        if condition == "A" or task[0] == condition:
            if isinstance(action, int):
                stack += sol[action][::-1]
            elif action == "M":
                x, y, dir = task[2]
                dx, dy = dir_map[dir]
                new_x, new_y = x + dx, y + dy
                task[2] = (new_x, new_y, dir)
                if (new_x, new_y) not in task[0].keys():
                    return False, "invalid location"
                if (new_x, new_y) in task[1]:
                    task[1].remove((new_x, new_y))
                    if not task[1]:
                        break
            elif action == "R":
                x, y, dir = task[2]
                task[2] = (x, y, rotate_right_map[dir])
            elif action == "L":
                x, y, dir = task[2]
                task[2] = (x, y, rotate_left_map[dir])
            elif action[0] == "C":
                x, y, dir = task[2]
                task[0][(x, y)] = action[1]
            else:
                print("ERROR: parser should not reach this statement")
                exit()
        # render_frame(task, screen)
        # time.sleep(0.1)
    return True, "Success"