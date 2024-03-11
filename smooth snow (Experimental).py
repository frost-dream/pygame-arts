import pygame
from random import randint
from time import time
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1200
pygame.init()
screen = pygame.display.set_mode((1500, 700))
class Raindrop:
    def __init__(self):
        self.x = randint(0, SCREEN_WIDTH)
        self.y = randint(-SCREEN_HEIGHT, 0)
        self.speed = randint(2, 10)
        self.size = randint(1, 3)
        self.color = [randint(150,255)] * 3
        self.wind = randint(-3, 3)
    def fall(self):
        self.y += self.speed
        self.x += self.wind
        if self.y > SCREEN_HEIGHT:
            self.y = randint(-SCREEN_HEIGHT, 0)
            self.x = randint(0, SCREEN_WIDTH)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
raindrops = [Raindrop() for _ in range(600)]
fpsLab = pygame.font.SysFont("monospace", 200).render("Empty", 1, (255,255,0))
Lab = pygame.font.SysFont("monospace", 20).render("Warning!", 1, (255,0,0))
left = right = False
t = time()
while True:
    for event in pygame.event.get(pygame.QUIT):
        quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        left = True
        right = False
        for raindrop in raindrops:
            raindrop.x -= min((time() - t) * 3, 5)
    else:
        if left:
            for i in range(10,int((time() - t) * 10)):
                for raindrop in raindrops:
                    raindrop.x -= 5 / (i / 10)
                    raindrop.fall()
                if len(raindrops) > 500:
                    screen.blit(Lab, (10, 10))
                pygame.display.flip()
                pygame.time.delay(30)
                screen.fill((0, 0, 0))
            left = False
        if keys[pygame.K_RIGHT]:
            right = True
            left = False
            for raindrop in raindrops:
                raindrop.x += min((time() - t) * 3, 5)
        else:
            if right:
                for i in range(10,int((time() - t) * 10)):
                    for raindrop in raindrops:
                        raindrop.x += 5 / (i / 10)
                        raindrop.fall()
                    if len(raindrops) > 500:
                        screen.blit(Lab, (10, 10))
                    pygame.display.flip()
                    pygame.time.delay(30)
                    screen.fill((0, 0, 0))
                right = False
            else:
                t = time()
    if keys[pygame.K_q]:
        try:
            for i in range(10):
                raindrops.pop()
        except:
            screen.blit(fpsLab, (500, 250))
    elif keys[pygame.K_w]:
        for i in range(10):
            raindrops.append(Raindrop())
    for raindrop in raindrops:
        raindrop.fall()
    if len(raindrops) > 1000:
        screen.blit(Lab, (10, 10))
    pygame.display.flip()
    pygame.time.delay(30)
    screen.fill((0, 0, 0))
