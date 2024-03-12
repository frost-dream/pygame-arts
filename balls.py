import pygame
from random import randint
pygame.init()
screen = pygame.display.set_mode((500, 500))
TILE_SIZE = 20
particles = []
tile_map = {}
for i in range(2,14):
    tile_map[f'{i};{i + 8}'] = [i, i + 8, (255, 255, 0)]
for i in range(10,14):
    tile_map[f'15;{i}'] = [15, i, (0, 0, 255)]
for i in range(5,8):
    tile_map[f'{i};10'] = [i,10, (255,255,255)]
tile_map['11;11'] = [11, 11, (0, 255, 255)]
clicking = False
while True:
    screen.fill((0,0,0))
    if clicking:
        for i in range(30):
            particles.append([list(pygame.mouse.get_pos()), [randint(0, 42) / 6 - 3.5, randint(0, 42) / 6 - 3.5], randint(4, 6), (randint(0,255),randint(0,255),randint(0,255))])
    for particle in particles:
        particle[0][0] += particle[1][0]
        if str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE)) in tile_map:
            particle[1][0] = -0.7 * particle[1][0]
            particle[1][1] *= 0.95
            particle[0][0] += particle[1][0] * 2
        particle[0][1] += particle[1][1]
        if str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE)) in tile_map:
            particle[1][1] = -0.7 * particle[1][1]
            particle[1][0] *= 0.95
            particle[0][1] += particle[1][1] * 2
        particle[2] -= 0.035
        particle[1][1] += 0.15
        pygame.draw.circle(screen, particle[3], [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)
    for tile in tile_map:
        pygame.draw.rect(screen, tile_map[tile][2], pygame.Rect(tile_map[tile][0] * TILE_SIZE, tile_map[tile][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    for event in pygame.event.get((pygame.QUIT,pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP)):
        match event.type:
            case pygame.QUIT:
                quit()
            case pygame.MOUSEBUTTONDOWN:
                clicking = True
            case pygame.MOUSEBUTTONUP:
                clicking = False
    pygame.display.flip()
    pygame.time.wait(3)