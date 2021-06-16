import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# adding the screen
# make sure to pass tuple in set_mode
# set_mode(width, height)
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("images/background.png")

# background music
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("images/player.png")
playerX = 370
playerY = 500
playerX_change = 0


# BOSS
bossImg = pygame.image.load("images/006-ufo.png")
bossX = 370
bossY = 30
bossx_change = 0.1
bossX_change = 0.1

# Enemy
# creating lists to store multiple enemy entities
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_o_enemy = 8
enemies = ["images/004-alien.png", "images/014-alien-6.png", "images/013-silly-1.png",
           "images/009-alien-3.png", "images/enemy.png"]
enemyx_change = 1
enemyy_change = 40


# loop to put enemies in lists
def add_enemy(enemy_no):
    for _ in range(enemy_no):
        enemyImg.append(pygame.image.load(random.choice(enemies)))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(enemyx_change)
        enemyY_change.append(enemyy_change)


# function to create enemies as program starts
add_enemy(no_o_enemy)

# Bullet
bulletImg = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5

# ready state means we can't see the bullet on screen.
# fire state means that bullet is fired and is moving.
bullet_state = "ready"

# boss bullet
bossbulletImg = pygame.image.load("images/bullet3.png")
bossbulletX = 0
bossbulletY = 30
bossbulletX_change = 0
bossbulletY_change = 5
bossbullet_state = "ready"


# score
SCORE = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = textY = 10


# timing or boss bullets
starttime = 0
endtime = 0


def show_score(x, y):
    score = font.render("Score: " + str(SCORE), True, (255, 255, 255))
    screen.blit(score, (x, y))


# player function
def player(x, y):
    # .blit() method draws images on screen
    screen.blit(playerImg, (x, y))


# enemy function
def enemy(x, y, e):
    screen.blit(enemyImg[e], (x, y))
    

def boss(x, y):
    screen.blit(bossImg, (x, y))


# bullet state stores weather a bullet is on screen or not
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    # reason of adding 16 and 10 to x and y axis respectively is to make bullet appear from center of ship.
    screen.blit(bulletImg, (x+16, y+10))


def fire_boss_bullet(x, y):
    global bossbullet_state
    bossbullet_state = "fired"
    screen.blit(bossbulletImg, (x+16, y+20))


def collision(xe, ye, xb, yb):
    distance = math.sqrt(math.pow((xe - xb), 2) + math.pow((ye - yb), 2))
    if distance < 27:
        return True
    else:
        return False


# boss hit function
def bosshit(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
    if distance < 30:
        return True
    else:
        return False


# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Game Loop
running = True
while running:
    if SCORE == 5:
        enemyx_change = 1.5
        add_enemy(3)
        bulletY_change = 7

    # anything we want on screen to stay persistent should be in the for loop
    # fills screen with rgb colors
    # (0, 0, 0) is black fill
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    # this checks all event happening in pygame window i.e. press of a key on keyboard or mouse click
    for event in pygame.event.get():
        # checks if close button is pressed
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check for left or right keystroke
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -3

            if event.key == pygame.K_RIGHT:
                playerX_change = 3

            if event.key == pygame.K_SPACE:
                bull_sound = mixer.Sound("sounds/laser.wav")
                bull_sound.play()
                bulletX = playerX
                fire_bullet(bulletX, playerY)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # call player after fill() function otherwise screen will be drawn over the player and it will never be visible
    playerX += playerX_change

    # adding boundaries in screen by restricting ships movements
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    else:
        pass

    # enemy movements
    for i in range(no_o_enemy):

        # Game Over
        k = False
        if bossbullet_state == "fired":
            k = bosshit(playerX, playerY, bossbulletX, bossbulletY)

        if enemyY[i] > 440 or k:
            for j in range(no_o_enemy):
                enemyY[j] = 2000
            bossX = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = enemyx_change
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemyx_change
            enemyY[i] += enemyY_change[i]
        else:
            pass
        
        # Boss movements
        if SCORE > 10:
            bossX += bossX_change
            if bossX <= 0:
                bossX_change = bossx_change
            elif bossX >= 736:
                bossX_change = -bossx_change
            else:
                pass

        # collision
        collided = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collided:
            explosion = mixer.Sound("sounds/explosion.wav")
            explosion.play()
            bulletY = 480
            bullet_state = "ready"
            SCORE += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            enemyImg[i] = pygame.image.load(random.choice(enemies))
     
        # calling enemy function
        enemy(enemyX[i], enemyY[i], i)
        
        # calling boss function
        if SCORE > 10:
            boss(bossX, bossY)

            # Boss bullet calling
            n = random.randint(1, 5)
            if n == 1 and bossbullet_state == "ready":
                bossbulletX = bossX
                fire_boss_bullet(bossbulletX, bossY)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fired":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # boss bullet movement
    if bossbulletY >= 600:
        bossbulletY = 0
        bossbullet_state = "ready"

    if bossbullet_state == "fired":
        fire_boss_bullet(bossbulletX, bossbulletY)
        bossbulletY += bossbulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
