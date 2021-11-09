import pygame
import random
import math
from pygame import mixer

def main():
    ## initializing the game
    pygame.init()


    ## creating the screen
    screen = pygame.display.set_mode((800, 600))

    ## background
    background = pygame.image.load('background.jpg')

    ## background sound
    mixer.music.load('background.wav')
    mixer.music.play(-1)

    ## setting the title and icon
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load('spaceship.png')
    pygame.display.set_icon(icon)

    ## Player

    playerimage = pygame.image.load('rocket.png')
    playerX = 370
    playerY = 480
    player_change = 0

    ## Enemy

    enemyimage = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyimage.append(pygame.image.load('alien.png'))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(1)
        enemyY_change.append(20)

    ## Bullet

    bulletimage = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 1
    bulletY_change = 5
    global bullet_state
    bullet_state = "ready"

    ## Score
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf',32)
    textX = 10
    textY = 10

    ## Game over text
    over_font = pygame.font.Font('freesansbold.ttf',64)

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200,250))

    def show_score(x,y):
        score = font.render("Score :"+ str(score_value), True, (255, 255, 255))
        screen.blit(score, (x,y))

    def player(x,y):
        screen.blit(playerimage,(x,y))

    def enemy(x,y,i):
        screen.blit(enemyimage[i],(x,y))

    def fire_bullet(x,y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletimage, (x+16 ,y+10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
        if distance < 27:
            return True
        else:
            return False


    ## game loop
    running = True
    while running:
        #RGB - Red, Green, Blue
        screen.fill((0,128,128))
        screen.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_change = -0.6
                if event.key == pygame.K_RIGHT:
                    player_change = 0.6
                if event.key == pygame.K_SPACE:
                    if bullet_state =="ready":
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_change = 0


        ## Checking the boundaries for players
        playerX += player_change
        if(playerX <= 0):
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        ## Making the enemy move
        for i in range(num_of_enemies): 

            ## Game over 
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break


            enemyX[i] += enemyX_change[i]
            if(enemyX[i] <= 0):
                enemyX_change[i] = 1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1
                enemyY[i] += enemyY_change[i]

            ## Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

        ## Bullet movement 
        if bulletY <=0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        
  


        player(playerX, playerY)
        show_score(textX,textY)
        pygame.display.update()

if __name__ == "__main__":
    main()