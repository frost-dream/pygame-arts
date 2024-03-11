import pygame
from random import randint
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
left = right = up = down = False
while True:
    for event in pygame.event.get(pygame.QUIT):
        quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        left = True
    else:
        left = False
        if keys[pygame.K_RIGHT]:
            right = True
        else:
            right = False
    if keys[pygame.K_UP]:
        up = True
    else:
        up = False
        if keys[pygame.K_DOWN]:
            down = True
        else:
            down = False
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
        if left:
            raindrop.x -= 3
        elif right:
            raindrop.x += 3
        if up:
            raindrop.y -= 3
        elif down:
            raindrop.y += 3
        raindrop.fall()
    if len(raindrops) > 1000:
        screen.blit(Lab, (10, 10))
    pygame.display.flip()
    pygame.time.delay(30)
    screen.fill((0, 0, 0))
