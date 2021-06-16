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

# Enemy
# creating lists to store multiple enemy entities
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_o_enemy = 8
enemies = ["images/004-alien.png", "images/014-alien-6.png", "images/013-silly-1.png", "images/009-alien-3.png"]

# loop to put enemies in lists
for i in range(no_o_enemy):
    enemyImg.append(pygame.image.load(random.choice(enemies)))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
# ready state means we can't see the bullet on screen.
# fire state means that bullet is fired and is moving.
bullet_state = "ready"

# score
SCORE = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(SCORE), True, (255, 255, 255))
    screen.blit(score, (x, y))


# player function
def player(x, y):
    # .blit() method draws images on screen
    screen.blit(playerImg, (x, y))


# enemy function
def enemy(x, y, k):
    screen.blit(enemyImg[k], (x, y))


# bullet state stores weather a bullet is on screen or not
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    # reason of adding 16 and 10 to x and y axis respectively is to make bullet appear from center of ship.
    screen.blit(bulletImg, (x + 16, y + 10))


def collision(xe, ye, xb, yb):
    distance = math.sqrt(math.pow((xe - xb), 2) + math.pow((ye - yb), 2))
    if distance < 27:
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
                playerX_change = -2

            if event.key == pygame.K_RIGHT:
                playerX_change = 2

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
        if enemyY[i] > 440:
            for j in range(no_o_enemy):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
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

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fired":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
