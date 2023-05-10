

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
        "start pos": start_pos
    }, functions