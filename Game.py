import pygame
import random

#Initialize PyGame
pygame.init()

#Creating screen
screen = pygame.display.set_mode((800,600))

#Background
background = pygame.image.load('Background.jpg')
background = pygame.transform.scale(background, (800,600))

#BGM
pygame.mixer.music.load("Megalovania2.mp3")
pygame.mixer.music.play(-1)

#Title and Logo
pygame.display.set_caption("Alien Invasion")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

#Player
playerimg = pygame.image.load('spaceship.png')
playerimg = pygame.transform.scale(playerimg,(60,64))
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimage = pygame.image.load('enemyship.png')
    enemyimg.append(pygame.transform.scale(enemyimage,(60,64)))
    enemyX.append(random.randint(0,735)) 
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

#Bullet
#Ready - bullet can't be seen on screen
#Fire - bullet is currently moving
bulletimg = pygame.image.load('bullet.png')
bulletimg = pygame.transform.scale(bulletimg,(32,32))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.7
bullet_state = 'ready'

#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

#Game over text
over_font =  pygame.font.Font("freesansbold.ttf",64)

def show_score(x,y):
    score = font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))
def player(x,y):
    screen.blit(playerimg,(x,y))
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg,(x+16,y+10))
def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = ((enemyX[i]-bulletX)**2 + (enemyY[i]-bulletY)**2)**0.5
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:
    #Color Scheme - R,G,B
    screen.fill((5,5,10))
    #Background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Keyboard commands 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX+=playerX_change

    #Boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    #enemy movement
    for i in range(num_of_enemies):
        #game over
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i]+=enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i]+=enemyY_change[i]
        #Collision
        collision = iscollision(enemyX,enemyY,bulletX,bulletY)
        if collision:
            bulletY=480
            bullet_state='ready'
            score_value+=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i], i)    

    #bullet movement
    if bulletY <= 0:
        bulletY=480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
