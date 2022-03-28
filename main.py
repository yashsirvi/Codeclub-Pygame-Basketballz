import numpy as np
import pygame
import random


pygame.init()
screen = pygame.display.set_mode((1000,600))

# variables
boardend = 930
clock = pygame.time.Clock()
fps = 30
pos = 0
score = 0
validthrow = False
gotscore = False
showText = pygame.font.Font(None, 45).render("Score: 0", 1, (255, 208, 0))
# importing images
pygame.display.set_caption("basketballz")
icon = pygame.image.load('images/screeniconbasketball.png')
pygame.display.set_icon(icon)
dot = pygame.image.load("images/dot.png")
dot = pygame.transform.scale(dot, (5,5))
bg = pygame.image.load("images/bg.png")
bg = pygame.transform.scale(bg, (1000,600))
# Hoop
hooptemp = pygame.image.load("images/hoop.png")
hoopsize1, hoopsize2 = hooptemp.get_size()
hoop = pygame.transform.scale(hooptemp, (int(hoopsize1*0.35), int(hoopsize2*.35)))

# Movmement of ball
ball = pygame.transform.scale(icon, (64, 64))
def ballpos():
    xball = random.randint(200,400)
    yball = random.randint(300,460)
    return xball, yball

# states
ballstate = "ready"
clicked = False

# tracking path
def trackpath(pos):
    mx, my = pos
    dx = (mx-xball)
    dy = (my-yball)

    if dx != 0:
        theta = np.pi - np.arctan(dy/dx)
    else:
        theta = np.pi/2

    distance = np.sqrt((mx-xball)**2 + (my-yball)**2)

    if distance >=300:
        distance = 300

    vel = distance
    g = 10

    trackx = np.arange(xball +30, 800, 20)
    calcx = trackx - xball-30
    tracky = 20+yball - (calcx*np.tan(theta) - g*(calcx**2)/(2*(vel**2)*(np.cos(theta))**2))
    trackx[trackx > boardend] = 2*boardend-trackx[trackx>boardend]

    for i in range(len(trackx)):
        screen.blit(dot, (trackx[i], tracky[i]) )

def moveball(pos, xball, yball):
    mx, my = pos
    dx = (mx-xball)
    dy = (my-yball)

    if dx != 0:
        theta = np.pi - np.arctan(dy/dx)
    else:
        theta = np.pi/2

    distance = np.sqrt((mx-xball)**2 + (my-yball)**2)

    if distance >=300:
        distance = 300

    vel = distance
    g = 10

    trackx = np.arange(xball, 1500, 5)
    calcx = trackx - xball
    tracky = yball - (calcx*np.tan(theta) - g*(calcx**2)/(2*(vel**2)*(np.cos(theta))**2))
    trackx[trackx > boardend] = 2*boardend-trackx[trackx>boardend]

    return trackx, tracky

def distance(xball, yball):
    return np.sqrt((xball-860)**2 + (yball-130)**2)


running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
                posrelease = pygame.mouse.get_pos()
                xballin, yballin = xball, yball
                ballstate = "released"
                clicked = False


    screen.blit(bg,(0,0))
    screen.blit(hoop,(860,100))
    #screen.fill((255,0,0),((860,150),(5,5)))
    if clicked:
        pos = pygame.mouse.get_pos()
        trackpath(pos)
    if ballstate == "ready":
        xball, yball = ballpos()
        gotscore = False
        ballstate= "ready2"
    if ballstate == "released":
        validthrow = False
        trackx, tracky = moveball(posrelease, xballin, yballin)
        for i in range(len(trackx)):
            xball, yball = trackx[i], tracky[i]
            pygame.display.update()
            if yball < 100 and xball > 820:
                validthrow = True
            if distance(xball, yball) < 45 and validthrow and gotscore == False:
                score += 1
                textfont = pygame.font.Font(None, 45)
                showText = textfont.render("Score: " +str(score), 1, (255, 208, 0))
                gotscore = True
                validthrow = False
            clock.tick(fps*3)
            screen.blit(bg,(0,0))
            screen.blit(ball, ( xball, yball))
            screen.blit(hoop,(860,100))
            screen.blit(showText,(50,50))
        ballstate = "ready"

    screen.blit(ball,(xball,yball))
    screen.blit(showText,(50,50))
    pygame.display.update()
    clock.tick(fps)