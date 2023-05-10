

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
    while task["marks"]:
        c += 1
        if c > 1000:
            return False, "out of time"
        if not stack:
            return False, "stack empty"
        action, condition = stack.pop()
        if condition == "A" or task["locations"] == condition:
            if isinstance(action, int):
                stack += sol[action][::-1]
            elif action == "M":
                x, y, dir = task["start pos"]
                dx, dy = dir_map[dir]
                task["start pos"] = (x + dx, y + dy, dir)
                if (x + dx, y + dy) not in task["locations"].keys():
                    return False, "invalid location"
            elif action == "R":
                x, y, dir = task["start pos"]
                task["start pos"] = (x, y, rotate_right_map[dir])
            elif action == "L":
                x, y, dir = task["start pos"]
                task["start pos"] = (x, y, rotate_left_map[dir])
            elif action[0] == "C":
                x, y, dir = task["start pos"]
                task["locations"][(x, y)] = action[1]
            else:
                print("ERROR: parser should not reach this statement")
                exit()
        # render_frame(task, screen)
        # time.sleep(0.1)
    return True, "Success"