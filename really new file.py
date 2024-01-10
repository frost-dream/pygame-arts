from pygame import init, QUIT
from pygame.draw import line as l, circle
from pygame.time import Clock
from pygame.display import set_mode, flip
from pygame.event import get
from pygame.mouse import get_pos
from random import randint, random, uniform
from math import sin, cos, dist, atan2
from os import _exit
init()
def connect_lines(line, other_line):
    x1 = line['x'] + line['timer'] // 5 * cos(line['angle'])
    y1 = line['y'] + line['timer'] // 5 * sin(line['angle'])
    x2 = other_line['x'] + other_line['timer'] // 5 * cos(other_line['angle'])
    y2 = other_line['y'] + other_line['timer'] // 5 * sin(other_line['angle'])
    distance = dist((line['x'], line['y']), (other_line['x'], other_line['y']))
    if distance < 50:
        alpha = min([255, line['timer']])
        l(screen, (alpha, alpha, alpha), (line['x'], line['y']), (other_line['x'], other_line['y']), 1)
        circle(screen, (alpha, alpha, alpha), (line['x'], line['y']), 2)
        circle(screen, (alpha, alpha, alpha), (other_line['x'], other_line['y']), 2)
        return
    distance = dist((line['x'], line['y']), (x2, y2))
    if distance < 50:
        alpha = min([255, line['timer']])
        l(screen, (alpha, alpha, alpha), (line['x'], line['y']), (x2, y2), 1)
        circle(screen, (alpha, alpha, alpha), (line['x'], line['y']), 2)
        circle(screen, (alpha, alpha, alpha), (x2, y2), 2)
        return
    distance = dist((x1, y1), (x2, y2))
    if distance < 50:
        alpha = min([255, line['timer']])
        l(screen, (alpha, alpha, alpha), (x1, y1), (x2, y2), 1)
        circle(screen, (alpha, alpha, alpha), (x1, y1), 2)
        circle(screen, (alpha, alpha, alpha), (x2, y2), 2)
        return
    distance = dist((x1, y1), (other_line['x'], other_line['y']))
    if distance < 50:
        alpha = min([255, line['timer']])
        l(screen, (alpha, alpha, alpha), (x1, y1), (other_line['x'], other_line['y']), 1)
        circle(screen, (alpha, alpha, alpha), (x1, y1), 2)
        circle(screen, (alpha, alpha, alpha), (other_line['x'], other_line['y']), 2)
lines = []
screen = set_mode((1500, 700))
clock = Clock()
while True:
    for event in get():
        if event.type == QUIT:
            _exit(0)
    screen.fill((0, 0, 0))
    if random() < 0.07:
        lines.append({'x': randint(0, 1500),'y': randint(0, 700), 'fade-out': False, 'angle': uniform(0, 2 * 3.141592653589793), 'timer': 1, 'rotation_speed': uniform(-0.01, 0.01)})
    for line in lines:
        line['angle'] += line['rotation_speed']
        if line['angle'] > 2 * 3.141592653589793:
            line['angle'] -= 2 * 3.141592653589793
        if line['timer'] == 0:
            lines.remove(line)
            continue
        alpha = min([255, line['timer']])
        end_x = line['x'] + line['timer'] // 5 * cos(line['angle'])
        end_y = line['y'] + line['timer'] // 5 * sin(line['angle'])
        l(screen, (alpha, alpha, alpha), (line['x'], line['y']), (end_x, end_y), 1)
        for other_line in lines:
            if line != other_line:
                connect_lines(line, other_line)
        line['x'] += cos(line['angle'])
        line['y'] += sin(line['angle'])
        if line['x'] < 0 or line['x'] > 1500 or line['y'] < 0 or line['y'] > 700:
            lines.remove(line)
            continue
        if line['timer'] > 500:
            line['fade-out'] = True
        if line['fade-out']:
            line['timer'] -= 1
        else:
            line['timer'] += 1
        mouse_x, mouse_y = get_pos()
        distance_to_mouse = dist((line['x'], line['y']), (mouse_x, mouse_y))
        if distance_to_mouse < 100:
            line['fade-out'] = False
            angle_to_mouse = atan2(mouse_y - line['y'], mouse_x - line['x'])
            line['x'] += cos(angle_to_mouse) * 5
            line['y'] += sin(angle_to_mouse) * 5
    flip()
    clock.tick(100)