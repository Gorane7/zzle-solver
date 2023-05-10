import pygame
import random
import time
import copy


def textfile_parser(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    map_lines = [line for line in lines if ":" not in line]
    function_lines = [line for line in lines if ":" in line]
    functions = {int(x[0]): int(x[1]) for x in [a.split(":") for a in function_lines]}
    locations = {}
    marks = set()
    start_pos = None
    for y, line in enumerate(map_lines):
        for x, val in enumerate(line.split("|")):
            if not val:
                continue
            locations[(x, y)] = val[0]
            if len(val) > 1:
                if val[1] == "M":
                    marks.add((x, y))
                if val[1] == "S":
                    start_pos = (x, y, val[2])
    return {
        "locations": locations,
        "marks": marks,
        "start pos": start_pos,
        "functions": functions
    }


def setup_display(task):
    pygame.init()
    pygame.display.set_caption("Zzle")
    max_x = max([x[0] for x in task["locations"].keys()])
    min_x = min([x[0] for x in task["locations"].keys()])
    max_y = max([x[1] for x in task["locations"].keys()])
    min_y = min([x[1] for x in task["locations"].keys()])
    x_size = 3 + max_x - min_x
    y_size = 3 + max_y - min_y
    tile_size = 30
    border_size = 3
    x_len_px = x_size * tile_size + border_size * (x_size + 1)
    y_len_px = y_size * tile_size + border_size * (y_size + 1)
    window_size = (x_len_px, y_len_px)
    screen = pygame.display.set_mode(window_size)
    return screen


def render_frame(task, screen):
    background_colour = (0, 0, 0)
    colours = {
        "O": (255, 165, 0),
        "T": (0, 128, 128),
        "P": (128, 0, 128),
        0: (128, 128, 128)
    }
    max_x = max([x[0] for x in task["locations"].keys()])
    min_x = min([x[0] for x in task["locations"].keys()])
    max_y = max([x[1] for x in task["locations"].keys()])
    min_y = min([x[1] for x in task["locations"].keys()])
    tile_size = 30
    border_size = 3
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill(background_colour)
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            if (x, y) in task["locations"].keys():
                colour = colours[task["locations"][(x, y)]]
            else:
                colour = colours[0]
            pygame.draw.rect(screen, colour, (((x - min_x + 1) * (tile_size + border_size) + border_size, (y - min_y + 1) * (tile_size + border_size) + border_size), (tile_size, tile_size)))
            if (x, y) in task["marks"]:
                circle_pos = ((x - min_x + 1) * (tile_size + border_size) + border_size + int(tile_size / 2), (y - min_y + 1) * (tile_size + border_size) + border_size + int(tile_size / 2))
                pygame.draw.circle(screen, (0, 0, 0), circle_pos, int(tile_size / 3))
    x, y, dir = task["start pos"]
    cx, cy = (x - min_x + 1) * (tile_size + border_size) + border_size + tile_size / 2, (y - min_y + 1) * (tile_size + border_size) + border_size + tile_size / 2
    long_diff = tile_size / 3
    short_diff = tile_size / 6
    point_list = [[cx, cy] for _ in range(3)]
    if dir in "UD":
        point_list[0][1] += (1 if dir == "D" else -1) * long_diff
        for i in range(1, 3):
            point_list[i][1] += (1 if dir == "U" else -1) * long_diff
        point_list[1][0] -= short_diff
        point_list[2][0] += short_diff
    if dir in "LR":
        point_list[0][0] += (1 if dir == "R" else -1) * long_diff
        for i in range(1, 3):
            point_list[i][0] += (1 if dir == "L" else -1) * long_diff
        point_list[1][1] -= short_diff
        point_list[2][1] += short_diff
    pygame.draw.polygon(screen, (255, 255, 255), point_list)
    print(f"Updating with pos: {task['start pos']}")
    pygame.display.update()


def gen_sol(task):
    conditionals = ["A", "O", "T", "P"]
    actions = ["M", "R", "L", "CO", "CT", "CP"]
    for key in task["functions"].keys():
        actions.append(key)
    sol = {}
    for key, val in task["functions"].items():
        chosen_len = random.randint(0, val)
        this_func = []
        for i in range(chosen_len):
            this_func.append((random.choice(actions), random.choice(conditionals)))
        sol[key] = this_func
    return sol


def gen_empty_sol(task):
    return {key: [] for key in task["functions"].keys()}


def gen_additional_sols(task, sol):
    conditionals = ["A", "O", "T", "P"]
    actions = ["M", "R", "L", "CO", "CT", "CP"]
    for key in sol.keys():
        actions.append(key)
    new_sols = []    
    for key in sol.keys():
        if len(sol[key]) == task["functions"][key]:
            continue
        for conditional in conditionals:
            for action in actions:
                new_sol = {key1: [x for x in val] for key1, val in sol.items()}
                new_sol[key].append((action, conditional))
                new_sols.append(new_sol)
    # print(new_sols)
    return new_sols



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


class Deque:
    def __init__(self):
        self.s_in = []
        self.s_out = []
    
    def add(self, val):
        self.s_in.append(val)
    
    def get(self):
        if not self.s_out:
            while self.s_in:
                self.s_out.append(self.s_in.pop())
        return self.s_out.pop()

    def size(self):
        return len(self.s_in) + len(self.s_out)


def solve_with_bfs(filename):
    task = textfile_parser(filename)
    # print(task)
    # print()
    solutions = Deque()
    solutions.add(gen_empty_sol(task))
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
        success, message = try_solve(copy.deepcopy(task), sol)
        if success:
            print(sol)
            break
        for new_sol in gen_additional_sols(task, sol):
            solutions.add(new_sol)
        if i % print_every == print_every - 1:
            dur = time.time() - start
            print(f"Checking {print_every} solutions took {dur} seconds, solution stack size: {solutions.size()}")
        i += 1
    # display(task)
    print(success, message)


def solve_with_random(filename):
    task = textfile_parser(filename)
    # print(task)
    # print()
    i = 0
    print_every = 10000
    while True:
        if i % print_every == 0:
            start = time.time()
        sol = gen_sol(task)
        success, message = try_solve(copy.deepcopy(task), sol)
        if success:
            print(sol)
            break
        if i % print_every == print_every - 1:
            dur = time.time() - start
            print(f"Checking {print_every} solutions took {dur} seconds")
        i += 1
    # display(task)
    print(success, message)


if __name__ == '__main__':
    solve_with_bfs("maps/4_0.txt")
    # solve_with_random("maps/4_0.txt")
