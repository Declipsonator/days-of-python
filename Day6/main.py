import time

from pygame.rect import RectType

import MazeCell
import random
import pygame

pygame.init()
screen = pygame.display.set_mode((1800, 1000), pygame.RESIZABLE)
my_font = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()
running = True


def generate_maze(width: int, height: int, cell_width, cell_height, delay_seconds):
    """
    :param delay_seconds: float
    :param cell_height: int
    :param cell_width: int
    :param width: int
    :param height: int

    makes a 2D array of MazeCell objects with the given width and height and returns it.
    Follows Prim's Maze Generation Algorithm https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
    """
    maze = []
    for i in range(width):
        maze.append([])
        for j in range(height):
            maze[i].append(MazeCell.MazeCell(True, True, True, True))

    can_choose = [(random.randrange(0, width), random.randrange(0, height))]

    while len(can_choose) > 0:
        chosen_cell = can_choose[random.randrange(0, len(can_choose))]
        can_choose.remove(chosen_cell)

        maze[chosen_cell[0]][chosen_cell[1]].visited = True

        adjacent_visited_cells = []

        # Left Cell
        if chosen_cell[0] != 0 and not maze[chosen_cell[0] - 1][chosen_cell[1]].visited:
            maze[chosen_cell[0] - 1][chosen_cell[1]].visited = True
            can_choose.append((chosen_cell[0] - 1, chosen_cell[1]))
        elif chosen_cell[0] != 0 and not (chosen_cell[0] - 1, chosen_cell[1]) in can_choose:
            adjacent_visited_cells.append((chosen_cell[0] - 1, chosen_cell[1]))

        # Right Cell
        if chosen_cell[0] != width - 1 and not maze[chosen_cell[0] + 1][chosen_cell[1]].visited:
            maze[chosen_cell[0] + 1][chosen_cell[1]].visited = True
            can_choose.append((chosen_cell[0] + 1, chosen_cell[1]))
        elif chosen_cell[0] != width - 1 and not (chosen_cell[0] + 1, chosen_cell[1]) in can_choose:
            adjacent_visited_cells.append((chosen_cell[0] + 1, chosen_cell[1]))

        # Up Cell
        if chosen_cell[1] != 0 and not maze[chosen_cell[0]][chosen_cell[1] - 1].visited:
            maze[chosen_cell[0]][chosen_cell[1] - 1].visited = True
            can_choose.append((chosen_cell[0], chosen_cell[1] - 1))
        elif chosen_cell[1] != 0 and not (chosen_cell[0], chosen_cell[1] - 1) in can_choose:
            adjacent_visited_cells.append((chosen_cell[0], chosen_cell[1] - 1))

        # Down Cell
        if chosen_cell[1] != height - 1 and not maze[chosen_cell[0]][chosen_cell[1] + 1].visited:
            maze[chosen_cell[0]][chosen_cell[1] + 1].visited = True
            can_choose.append((chosen_cell[0], chosen_cell[1] + 1))
        elif chosen_cell[1] != height - 1 and not (chosen_cell[0], chosen_cell[1] + 1) in can_choose:
            adjacent_visited_cells.append((chosen_cell[0], chosen_cell[1] + 1))

        if len(adjacent_visited_cells) > 0:
            remove_wall = adjacent_visited_cells[random.randrange(0, len(adjacent_visited_cells))]
            if remove_wall[0] == chosen_cell[0] + 1:
                maze[remove_wall[0]][remove_wall[1]].left_wall = False
                maze[chosen_cell[0]][chosen_cell[1]].right_wall = False
            if remove_wall[0] == chosen_cell[0] - 1:
                maze[remove_wall[0]][remove_wall[1]].right_wall = False
                maze[chosen_cell[0]][chosen_cell[1]].left_wall = False
            if remove_wall[1] == chosen_cell[1] + 1:
                maze[remove_wall[0]][remove_wall[1]].up_wall = False
                maze[chosen_cell[0]][chosen_cell[1]].down_wall = False
            if remove_wall[1] == chosen_cell[1] - 1:
                maze[remove_wall[0]][remove_wall[1]].down_wall = False
                maze[chosen_cell[0]][chosen_cell[1]].up_wall = False

        screen.fill("purple")
        t_end = time.time() + delay_seconds
        while time.time() < t_end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            for x_cell in range(len(maze)):
                for y_cell in range(len(maze[0])):
                    pygame.draw.rect(screen, "red" if not maze[x_cell][y_cell].visited else (
                        "gray" if (x_cell, y_cell) in can_choose else (
                            "black" if (x_cell, y_cell) == chosen_cell else "white")),
                                     RectType(x_cell * cell_width, y_cell * cell_height, cell_width, cell_height))
                    if maze[x_cell][y_cell].up_wall:
                        pygame.draw.line(screen, "black", (x_cell * cell_width, y_cell * cell_height),
                                         (x_cell * cell_width + cell_width, y_cell * cell_height))
                    if maze[x_cell][y_cell].down_wall:
                        pygame.draw.line(screen, "black", (x_cell * cell_width, y_cell * cell_height + cell_height),
                                         (x_cell * cell_width + cell_width, y_cell * cell_height + cell_height))
                    if maze[x_cell][y_cell].left_wall:
                        pygame.draw.line(screen, "black", (x_cell * cell_width, y_cell * cell_height),
                                         (x_cell * cell_width, y_cell * cell_height + cell_height))
                    if maze[x_cell][y_cell].right_wall:
                        pygame.draw.line(screen, "black", (x_cell * cell_width + cell_width, y_cell * cell_height),
                                         (x_cell * cell_width + cell_width, y_cell * cell_height + cell_height))
            text_surface = my_font.render('Its actually much faster I just slowed it down (:', False, (0, 0, 0))
            screen.blit(text_surface, (width * cell_width / 2, height * cell_height + cell_height))

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

    return maze


box_width = 20
box_height = 20
maze = generate_maze(50, 50, box_width, box_height, 0.00001)

player_pos = (0, 0)

maze[0][0].start = True
maze[len(maze) - 1][len(maze[0]) - 1].end = True
won = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not won:
            if event.key == pygame.K_UP:
                if player_pos[1] == 0 or maze[player_pos[0]][player_pos[1]].up_wall:
                    continue
                else:
                    player_pos = (player_pos[0], player_pos[1] - 1)

            if event.key == pygame.K_DOWN:
                if player_pos[1] == len(maze) - 1 or maze[player_pos[0]][player_pos[1]].down_wall:
                    continue
                else:
                    player_pos = (player_pos[0], player_pos[1] + 1)

            if event.key == pygame.K_LEFT:
                if player_pos[0] == 0 or maze[player_pos[0]][player_pos[1]].left_wall:
                    continue
                else:
                    player_pos = (player_pos[0] - 1, player_pos[1])

            if event.key == pygame.K_RIGHT:
                if player_pos[0] == len(maze[0]) - 1 or maze[player_pos[0]][player_pos[1]].right_wall:
                    continue
                else:
                    player_pos = (player_pos[0] + 1, player_pos[1])

        if maze[player_pos[0]][player_pos[1]].end:
            won = True

    screen.fill("purple")

    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y].start or won:
                pygame.draw.rect(screen, "green", RectType(x * box_width, y * box_height, box_width, box_height))
            elif maze[x][y].end:
                pygame.draw.rect(screen, "red", RectType(x * box_width, y * box_height, box_width, box_height))
            else:
                pygame.draw.rect(screen, "white", RectType(x * box_width, y * box_height, box_width, box_height))
            if maze[x][y].up_wall:
                pygame.draw.line(screen, "black", (x * box_width, y * box_height),
                                 (x * box_width + box_width, y * box_height))
            if maze[x][y].down_wall:
                pygame.draw.line(screen, "black", (x * box_width, y * box_height + box_height),
                                 (x * box_width + box_width, y * box_height + box_height))
            if maze[x][y].left_wall:
                pygame.draw.line(screen, "black", (x * box_width, y * box_height),
                                 (x * box_width, y * box_height + box_height))
            if maze[x][y].right_wall:
                pygame.draw.line(screen, "black", (x * box_width + box_width, y * box_height),
                                 (x * box_width + box_width, y * box_height + box_height))

    pygame.draw.circle(screen, "black",
                       (player_pos[0] * box_width + box_width / 2, player_pos[1] * box_height + box_height / 2),
                       min(box_width, box_height) / 3 + min(box_width, box_height) / 10)
    pygame.draw.circle(screen, "gray",
                       (player_pos[0] * box_width + box_width / 2, player_pos[1] * box_height + box_height / 2),
                       min(box_width, box_height) / 3)

    if won:
        text_surface = my_font.render('You Won!!!!!', False, (0, 0, 0))
        screen.blit(text_surface, (len(maze) * 30 / 2, len(maze[0]) * 30 + 50))
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
