import pygame



def setup_display(task):
    # TODO: somewhat missing compatibility with latest data structures
    pygame.init()
    pygame.display.set_caption("Zzle")
    max_x = max([x[0] for x in task[0].keys()])
    min_x = min([x[0] for x in task[0].keys()])
    max_y = max([x[1] for x in task[0].keys()])
    min_y = min([x[1] for x in task[0].keys()])
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
    # TODO: somewhat missing compatibility with latest data structures
    background_colour = (0, 0, 0)
    colours = {
        1: (255, 165, 0),
        2: (0, 128, 128),
        3: (128, 0, 128),
        0: (128, 128, 128)
    }
    max_x = max([x[0] for x in task[0].keys()])
    min_x = min([x[0] for x in task[0].keys()])
    max_y = max([x[1] for x in task[0].keys()])
    min_y = min([x[1] for x in task[0].keys()])
    tile_size = 30
    border_size = 3
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill(background_colour)
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            if (x, y) in task[0].keys():
                colour = colours[task[0][(x, y)]]
            else:
                colour = colours[0]
            pygame.draw.rect(screen, colour, (((x - min_x + 1) * (tile_size + border_size) + border_size, (y - min_y + 1) * (tile_size + border_size) + border_size), (tile_size, tile_size)))
            if (x, y) in task[1]:
                circle_pos = ((x - min_x + 1) * (tile_size + border_size) + border_size + int(tile_size / 2), (y - min_y + 1) * (tile_size + border_size) + border_size + int(tile_size / 2))
                pygame.draw.circle(screen, (0, 0, 0), circle_pos, int(tile_size / 3))
    x, y, dir = task[2]
    cx, cy = (x - min_x + 1) * (tile_size + border_size) + border_size + tile_size / 2, (y - min_y + 1) * (tile_size + border_size) + border_size + tile_size / 2
    long_diff = tile_size / 3
    short_diff = tile_size / 6
    point_list = [[cx, cy] for _ in range(3)]
    if dir % 2 == 0:
        point_list[0][1] += (1 if dir == 2 else -1) * long_diff
        for i in range(1, 3):
            point_list[i][1] += (1 if dir == 0 else -1) * long_diff
        point_list[1][0] -= short_diff
        point_list[2][0] += short_diff
    if dir % 2 == 1:
        point_list[0][0] += (1 if dir == 1 else -1) * long_diff
        for i in range(1, 3):
            point_list[i][0] += (1 if dir == 3 else -1) * long_diff
        point_list[1][1] -= short_diff
        point_list[2][1] += short_diff
    pygame.draw.polygon(screen, (255, 255, 255), point_list)
    pygame.display.update()