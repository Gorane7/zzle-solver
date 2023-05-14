import time

import display


def try_solve(task, sol, render=False):
    stack = []
    stack += sol[0][::-1]
    if render:
        screen = display.setup_display(task)
        display.render_frame(task, screen)
        time.sleep(0.1)
    dir_map = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0)
    ]
    # dir_map = {
    #     "U": (0, -1),
    #     "R": (1, 0),
    #     "D": (0, 1),
    #     "L": (-1, 0)
    # }
    c = 0
    while True:
        c += 1
        if c > 1000:
            return False, "out of time"
        if not stack:
            return False, "stack empty"
        action, condition = stack.pop()
        x, y, dir = task[2]
        if condition == 0 or task[0][(x, y)] == condition:
            # print(f"Executing: {action}, {condition}")
            if action == 0:
                dx, dy = dir_map[dir]
                new_x, new_y = x + dx, y + dy
                task[2] = (new_x, new_y, dir)
                if (new_x, new_y) not in task[0].keys():
                    return False, "invalid location"
                if (new_x, new_y) in task[1]:
                    task[1].remove((new_x, new_y))
                    if not task[1]:
                        break
            elif action == 1:
                task[2] = (x, y, (dir + 1) % 4)
            elif action == 2:
                task[2] = (x, y, (dir - 1) % 4)
            elif action < 6:
                task[0][(x, y)] = action - 2
            else:
                stack += sol[action - 6][::-1]
        if render:
            display.render_frame(task, screen)
            time.sleep(0.1)
    return True, "Success"