from pygame import init,Color
from pygame.math import Vector2
from pygame.mouse import get_pos
from pygame.event import get
from pygame.display import set_mode, flip
from pygame.time import Clock
from pygame.draw import ellipse
from random import randint
init()
screen = set_mode([700, 500])
starfield = []
for i in range(100):
    x = randint(0, 700)
    y = randint(0, 500)
    starfield.append([x, y])
clock = Clock()
while True:
    for i in get():
        pass
    for star in starfield:
        star[1] += 1
        if star[1] > 500:
            star[1] = 0
            star[0] = randint(0, 700)
    screen.fill((0, 0, 0))
    mouse_x, mouse_y = get_pos()
    for star in starfield:
        distance = Vector2(star[0] - mouse_x, star[1] - mouse_y).length()
        if distance < 50:
            color = (255, 255, 255)
        else:
            hue = int(distance) % 360
            color = Color(0, 0, 0)
            color.hsla = (hue, 100, 50, 100)
        ellipse(screen, color, [star[0], star[1], 20, 20])
    flip()
    clock.tick(60)
