

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
    colour_map = {
        "O": 1,
        "T": 2,
        "P": 3
    }
    dir_map = {
        "U": 0,
        "R": 1,
        "D": 2,
        "L": 3
    }
    for y, line in enumerate(map_lines):
        for x, val in enumerate(line.split("|")):
            if not val:
                continue
            locations[(x, y)] = colour_map[val[0]]
            if len(val) > 1:
                if val[1] == "M":
                    marks.add((x, y))
                if val[1] == "S":
                    start_pos = (x, y, dir_map[val[2]])
    return [
        locations,
        marks,
        start_pos
    ], functions