import pygame
from pygame.locals import *
from math import sin,cos
pygame.init()
width,height = 800,600
screen = pygame.display.set_mode((width, height))
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
]
raise_height = 3
vertices = [[x, y + raise_height, z] for x, y, z in vertices]
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]
camera_pos = [0, 0, -5]
amplitude = 10
frequency = 0.02
speed = 0.1
clock = pygame.time.Clock()
angle = 0
time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        angle += 0.05
    if keys[K_RIGHT]:
        angle -= 0.05
    screen.fill((255, 255, 255))
    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex
        new_x = x * cos(angle) - z * sin(angle)
        new_z = x * sin(angle) + z * cos(angle)
        rotated_vertices.append([new_x, y, new_z])
    projected_vertices = []
    for vertex in rotated_vertices:
        x, y, z = vertex
        scale = 200 / (z + 5)  # Perspective projection
        screen_x = int(width / 2 + x * scale)
        screen_y = int(height / 2 - y * scale)
        projected_vertices.append([screen_x, screen_y])
    for edge in edges:
        pygame.draw.line(screen, (0, 0, 0), projected_vertices[edge[0]], projected_vertices[edge[1]], 2)
    for x in range(width):
        y = int(amplitude * sin(frequency * x + speed * time) + height / 2)
        pygame.draw.line(screen, (0, 0, 255), (x, height), (x, y), 1)
    pygame.display.flip()
    clock.tick(60)
    time += 1
