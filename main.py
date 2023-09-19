import pygame
from pygame.locals import *
import sys
import random


def end_check(event):
    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        plik.close()
        pygame.quit()
        sys.exit()


pygame.init()
timer = pygame.time.Clock()
plik = open("input.dat", 'r')
x_size = 70
y_size = x_size - 1
stay = 0
birth = 0
play = 0
suv_x = 1
scale = 3
click_x = 0
click_y = 0
live = 0
stage = 0
is_active = False
click = False
walls = True
changes = []
checkbox_b = [1, 1, 1, 0, 1, 1, 1, 1, 1]
checkbox_s = [1, 1, 0, 0, 1, 1, 1, 1, 1]
corners = []

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
tit_font = pygame.font.SysFont("Hack", 40)
main_font = pygame.font.SysFont("Hack", 20)

vector = [[length for length in range(2)] for fields in range(x_size * y_size)]
id = 0
for y in range(y_size):
    for x in range(x_size):
        if (x == 0 and y == 0) or (x == x_size - 1 and y == 0) or (x == 0 and y == y_size - 1) or (
                x == x_size - 1 and y == y_size - 1):
            corners.append(id)
        id -= y_size
        if id < 0:
            id += x_size * y_size
    id += x_size

while True:
    id = plik.readline()
    if id == '':
        break
    vector[int(id)][1] = 0
plik.close()

while True:
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        end_check(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
                click_x, click_y = event.pos

        if event.type == MOUSEBUTTONUP:
            click = False
            is_active = False

    id = 0
    for el in changes:
        vector[el][1] = vector[el][1] ^ 1
    changes = []
    live = 0
    for y in range(y_size):
        for x in range(x_size):
            if not vector[id][1]:
                pygame.draw.rect(window, (34, 139, 34),
                                 (100 + x * 25 * scale, 100 + 25 * y * scale, 25 * scale, 25 * scale), 0)
                live += 1
            else:
                pygame.draw.rect(window, (255, 228, 181),
                                 (100 + x * 25 * scale, 100 + 25 * y * scale, 25 * scale, 25 * scale), 1)
            if click and 100 + x * 25 * scale <= click_x <= 100 + (
                    x + 1) * 25 * scale and 100 + 25 * y * scale <= click_y <= 100 + 25 * (
                    y + 1) * scale and click_y < 720:
                vector[id][1] = vector[id][1] ^ 1
                click = False
            vector[id][0] = 0
            id -= y_size
            if id < 0:
                id += x_size * y_size
        id += x_size

    # layout
    title = tit_font.render("Game of life", False, (0, 127, 255))
    title_length = title.get_width()
    window.blit(title, (WINDOW_WIDTH / 2 - title_length / 2, 10))
    title = main_font.render("By KarolWes", False, (0, 127, 255))
    title_length = title.get_width()
    window.blit(title, (WINDOW_WIDTH / 2 - title_length / 2, 60))
    title = main_font.render("Rules:", False, (0, 127, 255))
    window.blit(title, (10, 100))
    title = main_font.render("Survive", False, (0, 127, 255))
    window.blit(title, (10, 150))
    for box in range(9):
        if click and 15 <= click_x <= 35 and 180 + 25 * box <= click_y <= 180 + 25 * box + 20:
            checkbox_s[box] = checkbox_s[box] ^ 1
            click = False
        pygame.draw.rect(window, (0, 128, 128), (15, 180 + 25 * box, 20, 20), checkbox_s[box])
        cap = main_font.render(str(box), False, (0, 128, 128))
        window.blit(cap, (40, 178 + 25 * box))

    title = main_font.render("Born", False, (0, 127, 255))
    window.blit(title, (10, 410))
    for box in range(9):
        if click and 15 <= click_x <= 35 and 440 + 25 * box <= click_y <= 440 + 25 * box + 20:
            checkbox_b[box] = checkbox_b[box] ^ 1
            click = False
        pygame.draw.rect(window, (0, 128, 128), (15, 440 + 25 * box, 20, 20), checkbox_b[box])
        cap = main_font.render(str(box), False, (0, 128, 128))
        window.blit(cap, (40, 438 + 25 * box))

    birth = 0
    stay = 0
    for box in range(9):
        if checkbox_b[box] == 0:
            birth += 2 ** box
        if checkbox_s[box] == 0:
            stay += 2 ** box

    pygame.draw.rect(window, (1, 50, 32), (10, 40, 100, 40), 0)
    if not play:
        title = main_font.render("Start", False, (0, 127, 255))
    else:
        title = main_font.render("Stop", False, (0, 127, 255))
    title_length = title.get_width()
    window.blit(title, (title_length / 2, 45))
    if click and 10 <= click_x <= 110 and 40 <= click_y <= 80:
        click = False
        play = play ^ 1
        stage = 0

    pygame.draw.rect(window, (1, 50, 32), (120, 40, 100, 40), 0)
    title = main_font.render("Random", False, (0, 127, 255))
    title_length = title.get_width()
    window.blit(title, (title_length / 2 + 100, 45))
    if click and 120 <= click_x <= 220 and 40 <= click_y <= 80:
        click = False
        plik = open("plik.txt", 'w')
        for field in range(x_size * y_size):
            if vector[field][1] == 0:
                plik.write(str(field))
                plik.write('\n')
        plik.close()
        for el in range(x_size * y_size):
            vector[el][1] = random.randint(0, 1)

    pygame.draw.rect(window, (1, 50, 32), (800, 40, 100, 40), 0)
    title = main_font.render("Clear", False, (0, 127, 255))
    title_length = title.get_width()
    window.blit(title, (title_length / 2 + 780, 45))
    if click and 800 <= click_x <= 900 and 40 <= click_y <= 80:
        click = False
        plik = open("plik.txt", 'w')
        plik.close()
        for el in range(x_size * y_size):
            vector[el][1] = 1

    pygame.draw.rect(window, (0, 0, 0), (0, 680, 1024, 200), 0)

    title = main_font.render("Scale", False, (0, 127, 255))
    window.blit(title, (20, 690))
    pygame.draw.rect(window, (85, 107, 47), (20, 720, 150, 20), 0)

    pygame.draw.rect(window, (128, 128, 128), (25 + suv_x, 722, 15, 15), 0)
    if is_active:
        click_x = pygame.mouse.get_pos()[0]
        suv_x = click_x - 30
        if suv_x < 0:
            suv_x = 1
        if suv_x >= 121:
            suv_x = 119

    if suv_x > 12:
        scale = 3 / int(suv_x / 12)

    if click and (25 + suv_x <= click_x <= 40 + suv_x and 722 <= click_y <= 740):
        is_active = True

    title = main_font.render("Walls", False, (0, 127, 255))
    window.blit(title, (200, 690))
    pygame.draw.rect(window, (0, 128, 128), (220, 720, 20, 20), not walls)
    if click and 220 <= click_x <= 240 and 720 <= click_y <= 760:
        click = False
        walls ^= 1

    title = main_font.render("Stage: ", False, (0, 127, 255))
    title_length = title.get_width()
    window.blit(title, (280, 690))
    title = main_font.render(str(stage), False, (0, 127, 255))
    window.blit(title, (280 + title_length / 2, 720))

    title = main_font.render("Live cells", False, (0, 127, 255))
    title_length = title.get_width()
    window.blit(title, (400, 690))
    cap = str(live) + "/" + str(x_size * y_size)
    title = main_font.render(cap, False, (0, 127, 255))
    window.blit(title, (400 + title_length / 2, 720))
    cap = str(live / (x_size * y_size) * 100) + "%"
    title = main_font.render(cap, False, (0, 127, 255))
    window.blit(title, (400 + title_length / 2, 740))

    # game
    if play:
        stage += 1
        delay = 10
        plik = open("plik.txt", 'w')
        for field in range(x_size * y_size):
            if vector[field][1] == 0:
                plik.write(str(field))
                plik.write('\n')
        plik.close()

        for field in range(x_size * y_size):
            if walls:
                if vector[field - x_size][1] == 0:
                    vector[field][0] += 1
                if vector[field - x_size - y_size][1] == 0:
                    vector[field][0] += 1
                if vector[field - y_size][1] == 0:
                    vector[field][0] += 1
                if vector[(field + 1) % (x_size * y_size)][1] == 0:
                    vector[field][0] += 1
                if vector[(field + x_size) % (x_size * y_size)][1] == 0:
                    vector[field][0] += 1
                if vector[(field + x_size + y_size) % (x_size * y_size)][1] == 0:
                    vector[field][0] += 1
                if vector[(field + y_size) % (x_size * y_size)][1] == 0:
                    vector[field][0] += 1
                if vector[field - 1][1] == 0:
                    vector[field][0] += 1

            else:
                if field == corners[0]:
                    if vector[field - y_size][1] == 0:
                        vector[field][0] += 1
                    if vector[(field + 1) % (x_size * y_size)][1] == 0:
                        vector[field][0] += 1
                    if vector[(field + x_size) % (x_size * y_size)][1] == 0:
                        vector[field][0] += 1
                elif field == corners[1]:
                    if vector[(field + x_size) % (x_size * y_size)][1] == 0:
                        vector[field][0] += 1
                    if vector[(field + x_size + y_size) % (x_size * y_size)][1] == 0:
                        vector[field][0] += 1
                    if vector[(field + y_size) % (x_size * y_size)][1] == 0:
                        vector[field][0] += 1
                elif field == corners[2]:
                    if vector[field - x_size][1] == 0:
                        vector[field][0] += 1
                    if vector[field - x_size - y_size][1] == 0:
                        vector[field][0] += 1
                    if vector[field - y_size][1] == 0:
                        vector[field][0] += 1
                elif field == corners[3]:
                    if vector[field - x_size][1] == 0:
                        vector[field][0] += 1
                    if vector[(field + y_size) % (x_size * y_size)][1] == 0:
                        vector[field][0] += 1
                    if vector[field - 1][1] == 0:
                        vector[field][0] += 1
                else:
                    if field % y_size == 0:
                        if vector[field - y_size][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + 1) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + x_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + x_size + y_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + y_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                    elif (field + 1) % y_size == 0:
                        if vector[field - x_size][1] == 0:
                            vector[field][0] += 1
                        if vector[field - x_size - y_size][1] == 0:
                            vector[field][0] += 1
                        if vector[field - y_size][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + y_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[field - 1][1] == 0:
                            vector[field][0] += 1
                    elif field % x_size == 0:
                        if vector[field - x_size][1] == 0:
                            vector[field][0] += 1
                        if vector[field - x_size - y_size][1] == 0:
                            vector[field][0] += 1
                        if vector[field - y_size][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + 1) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + x_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                    elif (field + 1) % x_size == 0:
                        if vector[field - x_size][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + x_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + x_size + y_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + y_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[field - 1][1] == 0:
                            vector[field][0] += 1
                    else:
                        if vector[field - x_size][1] == 0:
                            vector[field][0] += 1
                        if vector[field - x_size - y_size][1] == 0:
                            vector[field][0] += 1
                        if vector[field - y_size][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + 1) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + x_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + x_size + y_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[(field + y_size) % (x_size * y_size)][1] == 0:
                            vector[field][0] += 1
                        if vector[field - 1][1] == 0:
                            vector[field][0] += 1

            vector[field][0] = 2 ** vector[field][0]

            if (vector[field][1] == 0 and not (vector[field][0] & stay)) or \
                    (vector[field][1] == 1 and vector[field][0] & birth):
                changes.append(field)

    else:
        delay = 100
    timer.tick(delay)
    pygame.display.flip()

# Coded by KarolWes!
