import numpy as np
import pygame
import random


pygame.init()
screen = pygame.display.set_mode((1000,600))


# variables
boardend = 930
clock = pygame.time.Clock()
FPS = 30
pos = 0
score = 0
running = True 
validthrow = False
gotscore = False
start = False
lives = 5
ballstate = "ready"
clicked = False
hoopCorner = (862,135)
hoopBack = (965,135)
guideX = []
guideY = []
collided1 = False
showTextScore = pygame.font.Font(None, 45).render("Score: 0", 1, (255, 208, 0))
showTextLives = pygame.font.Font(None, 45).render("Lives: "+str(lives),1,(245, 66, 99))


# importing images
pygame.display.set_caption("basketballz")
icon = pygame.image.load('images/screeniconbasketball.png')
pygame.display.set_icon(icon)
dot = pygame.image.load("images/dot.png")
dot = pygame.transform.scale(dot, (5,5))
bg = pygame.image.load("images/bg.png")
bg = pygame.transform.scale(bg, (1000,600))
hooptemp = pygame.image.load("images/hoop.png")
hoopsize1, hoopsize2 = hooptemp.get_size()
hoop = pygame.transform.scale(hooptemp, (int(hoopsize1*0.35), int(hoopsize2*.35)))

#importing audio
scoreSound = pygame.mixer.Sound("./sounds/Score.wav")
lossSound = pygame.mixer.Sound("./sounds/loss.wav")
bounce = pygame.mixer.Sound("./sounds/bounce.wav")
bgsound = pygame.mixer.Sound("./sounds/BlackTar.wav")
pygame.mixer.Sound.play(bgsound)
# generating initial position of ball
ball = pygame.transform.scale(icon, (64, 64))
def ballpos():
    xball = random.randint(200,400)
    yball = random.randint(300,460)
    return xball, yball


def distance(xball, yball,x,y):
    return np.sqrt((xball-x)**2 + (yball-y)**2)

# tracking path
def trackpath(pos):
    mx, my = pos
    dx = (mx-xball-32)
    dy = (my-yball-32)
    if dx != 0:
        theta = np.pi - np.arctan(dy/dx)
    else:
        theta = np.pi/2
    distance = np.sqrt((mx-xball)**2 + (my-yball)**2)
    if distance >=300:
        distance = 300
    vel = distance*0.8
    g = 10
    trackx = np.arange(xball +30, 800, 20)
    calcx = trackx - xball-30
    tracky = 20+yball - (calcx*np.tan(theta) - g*(calcx**2)/(2*(vel**2)*(np.cos(theta))**2))
    trackx[trackx > boardend] = 2*boardend-trackx[trackx>boardend]
    return trackx, tracky
    
    
def moveball(pos, xball, yball):
    collided1 = False
    collided2 = False
    mx, my = pos
    dx = (mx-xball-32)
    dy = (my-yball-32)
    if dx != 0:
        theta = np.abs(np.arctan(dy/dx))
    else:
        theta = np.pi/2
    displacement = np.sqrt((mx-xball)**2 + (my-yball)**2)
    if displacement >=300:
        displacement = 300
    vel = displacement*0.8
    g = 10
    dt = 4/FPS
    time = 0
    velx = vel*np.cos(np.abs(theta))
    vely = vel*np.sin(np.abs(theta))
    moveX = [xball]
    moveY = [yball]
    newX = xball
    newY = yball
    while time < 30:
        newX += velx*dt
        newY -= vely*dt
        collisondist = distance(newX+32, newY+32, hoopCorner[0],hoopCorner[1])
        if  collisondist< 25 and collided1 == False:
            collided1 = True
            phi = 0
            dx2 = newX + 32 - hoopCorner[0]
            dy2 = newY + 32 - hoopCorner[1]
            if dx2 == 0:
                phi = np.pi/2
            else:
                phi = np.arctan(dy2/dx2)
            parallelV = -(velx*np.cos(phi) - vely*np.sin(phi))
            perpendicularV = velx*np.sin(phi)+vely*np.cos(phi)
            velx = velx + parallelV*np.cos(phi)*0.6
            vely = vely + parallelV*np.sin(phi)*0.6
            continue
        collisondist = distance(newX+32, newY+32, hoopBack[0],hoopBack[1])
        if collisondist < 15 and collided2 == False:
            phi = 0
            dx2 = newX + 32 - hoopCorner[0]
            dy2 = newY + 32 - hoopCorner[1]
            if dx2 == 0:
                phi = np.pi/2
            else:
                phi = np.arctan(dy2/dx2)
            parallelV = -(velx*np.cos(phi) - vely*np.sin(phi))
            perpendicularV = velx*np.sin(phi)+vely*np.cos(phi)
            velx = velx + parallelV*np.cos(phi)*0.6
            vely = vely + parallelV*np.sin(phi)*0.6
            continue
            collided2 = True
        
        if newX > boardend or newX < 0:
            velx = -velx
        if newY > 600-64 :
            vely = -vely
        moveX.append(newX)
        moveY.append(newY)
        time += dt
        vely -=  g*dt
    return moveX, moveY

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
    # pygame.draw.circle(screen, (255,0,0), (910,175), 5)
    # pygame.draw.circle(screen, (255,0,0), (hoopCorner[0],hoopCorner[1]), 5)
    # pygame.draw.circle(screen, (255,0,0), (hoopBack[0],hoopBack[1]), 5)
    if clicked:
        releasepos = pygame.mouse.get_pos()
        guideX, guideY = trackpath(releasepos)
        for i in range(len(guideX)):
            screen.blit(dot, (guideX[i], guideY[i]) )

    if ballstate == "ready":
        if start:
            if gotscore == False:
                lives -=1
                pygame.mixer.Sound.play(lossSound)
                showTextLives = pygame.font.Font(None, 45).render("Lives: "+str(lives),1,(245, 66, 99))
            if lives == 0:
                screen.blit(pygame.font.Font(None,100).render("Game Over",1,(255,0,0)),(500,200))
                break
        lostlife = False
        xball, yball = ballpos()
        gotscore = False
        collided1 = False
        ballstate= "ready2"

    if ballstate == "released":
        start = True
        validthrow = False
        trackx, tracky = moveball(posrelease, xballin, yballin)
        for i in range(len(trackx)):
            xball, yball = trackx[i], tracky[i]
            pygame.display.update()
            if yball > 536:
                pygame.mixer.Sound.play(bounce)
            if xball>= 1000-70 or xball <= 1:
                pygame.mixer.Sound.play(bounce)
            if yball < 100 and xball > 820:
                validthrow = True
            if hoopCorner[0]+10<xball+32<hoopBack[0]-10 and hoopCorner[1] + 50 > yball+32 > hoopCorner[1] and validthrow and gotscore == False:
                score += 1
                pygame.mixer.Sound.play(scoreSound)
                textfont = pygame.font.Font(None, 45)
                showTextScore = textfont.render("Score: " +str(score), 1, (255, 208, 0))
                gotscore = True
                validthrow = False
            screen.blit(bg,(0,0))
            screen.blit(ball, ( xball, yball))
            screen.blit(hoop,(860,100))
            screen.blit(showTextScore,(50,50))
            screen.blit(showTextLives,(50,100))

        ballstate = "ready"
    screen.blit(ball,(xball,yball))
    screen.blit(showTextScore,(50,50))
    screen.blit(showTextLives,(50,100))
    pygame.display.update()
    clock.tick(FPS)