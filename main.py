#py -m pip install pygame
import pygame
pygame.init()

#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
gray = (128,128,128)
background = pygame.image.load('background.png')

#screen constants
width = 500
height = 600
background = pygame.transform.scale(background, (width, height))
player = pygame.image.load('player.png')
icon = pygame.image.load('icon.jpg')
fps = 60
font = pygame.font.Font('freesansbold.ttf', 16)
timer = pygame.time.Clock()

#screen 
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Doodle Jump')
pygame.display.set_icon(icon)

#event handler
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0,0))
    pygame.display.flip()
    timer.tick(fps)
pygame.quit()
