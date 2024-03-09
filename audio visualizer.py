from math import sin
import pygame
from pyaudio import PyAudio,paInt16
from colorsys import hls_to_rgb
screen_width = 500
screen_height = 500
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height),pygame.RESIZABLE)
clock = pygame.time.Clock()
stream = PyAudio().open(format=paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
hue = 0
while True:
    for event in pygame.event.get((pygame.QUIT,pygame.VIDEORESIZE)):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            screen_width,screen_height = event.w,event.h
    clock.tick(60)
    data = stream.read(1024)
    rms = 0
    for i in range(0,len(data),2):
        rms += int.from_bytes(data[i:i + 2], byteorder='little',signed=True) ** 2
    rms = (rms / 512) ** .5 / 50
    screen.fill((0,0,0))
    points = []
    for x in range(screen_width):
        y = screen_height/2 + int(rms * sin(x * .02))
        points.append((x,y))
    pygame.draw.lines(screen,[i * 255 for i in hls_to_rgb(hue / 360, 0.5, 1)],False,points,2)
    pygame.display.flip()
    hue += 1
