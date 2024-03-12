from math import sin, cos
import pygame
worldMap =  [
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 3, 0, 0, 2],
            [2, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 3, 1, 0, 0, 2, 0, 0, 0, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 2, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 1, 2, 0, 1],
            [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 2],
            [2, 3, 1, 0, 0, 2, 0, 0, 2, 1, 3, 2, 0, 2, 0, 0, 3, 0, 3, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 2, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 3, 0, 1, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
            [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]]
pygame.init()
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
showShadow = True
positionX = 3.0
positionY = 7.0
directionX = 1.0
directionY = 0.0
planeX = 0.0
planeY = 0.5
ray = 2
ROTATIONSPEED = 0.02
MOVESPEED = 0.03
TGM = (cos(ROTATIONSPEED), sin(ROTATIONSPEED))
ITGM = (cos(-ROTATIONSPEED), sin(-ROTATIONSPEED))
COS, SIN = (0,1)
while True:
    for event in pygame.event.get(pygame.QUIT):
        exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        oldDirectionX = directionX
        directionX = directionX * ITGM[COS] - directionY * ITGM[SIN]
        directionY = oldDirectionX * ITGM[SIN] + directionY * ITGM[COS]
        oldPlaneX = planeX
        planeX = planeX * ITGM[COS] - planeY * ITGM[SIN]
        planeY = oldPlaneX * ITGM[SIN] + planeY * ITGM[COS]
    if keys[pygame.K_RIGHT]:
        oldDirectionX = directionX
        directionX = directionX * TGM[COS] - directionY * TGM[SIN]
        directionY = oldDirectionX * TGM[SIN] + directionY * TGM[COS]
        oldPlaneX = planeX
        planeX = planeX * TGM[COS] - planeY * TGM[SIN]
        planeY = oldPlaneX * TGM[SIN] + planeY * TGM[COS]    
    if keys[pygame.K_UP]:
        if not worldMap[int(positionX + directionX * MOVESPEED)][int(positionY)]:
            positionX += directionX * MOVESPEED
        if not worldMap[int(positionX)][int(positionY + directionY * MOVESPEED)]:
            positionY += directionY * MOVESPEED
    if keys[pygame.K_DOWN]:
        if not worldMap[int(positionX - directionX * MOVESPEED)][int(positionY)]:
            positionX -= directionX * MOVESPEED
        if not worldMap[int(positionX)][int(positionY - directionY * MOVESPEED)]:
            positionY -= directionY * MOVESPEED
    if keys[pygame.K_s]:
        showShadow = not showShadow
        pygame.time.wait(300)
    screen.fill((25,25,25))
    for column in range(0,WIDTH,ray):
        cameraX = 2.0 * column / WIDTH - 1.0
        rayPositionX = positionX
        rayPositionY = positionY
        rayDirectionX = directionX + planeX * cameraX
        rayDirectionY = directionY + planeY * cameraX + .0001
        mapX = int(rayPositionX)
        mapY = int(rayPositionY)
        deltaDistanceX = (1.0 + (rayDirectionY * rayDirectionY) / (rayDirectionX * rayDirectionX)) ** .5
        deltaDistanceY = (1.0 + (rayDirectionX * rayDirectionX) / (rayDirectionY * rayDirectionY)) ** .5
        if (rayDirectionX < 0):
            stepX = -1
            sideDistanceX = (rayPositionX - mapX) * deltaDistanceX
        else:
            stepX = 1
            sideDistanceX = (mapX + 1.0 - rayPositionX) * deltaDistanceX
        if (rayDirectionY < 0):
            stepY = -1
            sideDistanceY = (rayPositionY - mapY) * deltaDistanceY
        else:
            stepY = 1
            sideDistanceY = (mapY + 1.0 - rayPositionY) * deltaDistanceY
        while not (worldMap[mapX][mapY] > 0):
            if (sideDistanceX < sideDistanceY):
                sideDistanceX += deltaDistanceX
                mapX += stepX
                side = True
            else:
                sideDistanceY += deltaDistanceY
                mapY += stepY
                side = False
        if side:
            perpWallDistance = abs((mapX - rayPositionX + ( 1.0 - stepX ) / 2.0) / rayDirectionX)
        else:
            perpWallDistance = abs((mapY - rayPositionY + ( 1.0 - stepY ) / 2.0) / rayDirectionY)
        lineHEIGHT = abs(int(HEIGHT / (perpWallDistance+.0000001)))
        drawStart = -lineHEIGHT / 2.0 + HEIGHT / 2.0
        if (drawStart < 0):
            drawStart = 0
        drawEnd = lineHEIGHT / 2.0 + HEIGHT / 2.0
        if (drawEnd >= HEIGHT):
            drawEnd = HEIGHT - 1
        wallcolors = [ [], [150,0,0], [0,150,0], [0,0,150] ]
        color = wallcolors[ worldMap[mapX][mapY] ]                                  
        if showShadow:
            if side:
                for i,v in enumerate(color):
                    color[i] = int(v / 1.2)                    
        pygame.draw.line(screen, color, (column,drawStart), (column, drawEnd), ray)
    pygame.display.flip()
    pygame.time.Clock().tick(300)