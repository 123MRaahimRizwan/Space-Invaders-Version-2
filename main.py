"""
Space Invaders Game
Author : M. Raahim Rizwan 
Credit for this idea goes to this video on Freecodecamp's youtube channel. Below is the link to the video:
https://www.youtube.com/watch?v=FfWpgLFMI7w&t=302s
"""


import pygame
import random
import math
from pygame import mixer

# Initializing pygame
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
title = pygame.display.set_caption("Snake Invaders Game")
icon = pygame.image.load("Assets/ufo.png")
pygame.display.set_icon(icon)
# Background 
background = pygame.image.load("Assets/background.png")
# Background Music
mixer.music.load("Assets/background.wav")
mixer.music.play(-1)
run = True
BLACK = (0,0,0)
ORANGE = (255, 80, 0)
# Player's info
player_img = pygame.image.load("Assets/player.png")
player_x = 370
player_y = 480
player_x_change = 0
# Enemy's info
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load("Assets/enemy.png"))
    enemy_x.append(random.randint(0,735))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# Bullet's info
bullet_img = pygame.image.load("Assets/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render(f"Score: {str(score_value)}", True, ORANGE)
    screen.blit(score, (x, y))

def game_over():
    over_text = over_font.render("GAME OVER !!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x,y):
    screen.blit(player_img, (x, y))

def enemy(x,y,i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x, y))

def isColllide(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x-bullet_x,2)) + (math.pow(enemy_y-bullet_y,2)))
    if distance < 35:
        return True
    else:
        return False
    

# Main Game Function
def main():
    global run, player_x, player_y, player_x_change, enemy_x, enemy_y, enemy_x_change, BLACK, background, bullet_y, bullet_y_change, bullet_state, bullet_x, score_value, number_of_enemies, text_x, text_y
    while run:
        screen.fill(BLACK)
        screen.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -5
                if event.key == pygame.K_RIGHT:
                    player_x_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound("Assets/laser.wav")
                        bullet_sound.play()
                        bullet_x = player_x
                        fire_bullet(bullet_x, bullet_y)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        # Player movement        
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # Enemy movement
        for i in range(number_of_enemies):
            # Game over
            if enemy_y[i] > 440:
                for j in range(number_of_enemies):
                    enemy_y[j] = 2000
                game_over()
                break


            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = 4
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -4
                enemy_y[i] += enemy_y_change[i]

            # Collision
            collision = isColllide(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                enemy_sound = mixer.Sound("Assets/explosion.wav")
                enemy_sound.play()
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                enemy_x[i] = random.randint(0,735)
                enemy_y[i] = random.randint(50,150)

            enemy(enemy_x[i], enemy_y[i], i)


        # Bullet movement
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"
        if bullet_state == 'fire':
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        
        player(player_x, player_y)
        show_score(text_x, text_y)
        pygame.display.update()



if __name__ == '__main__':
    main()
    pygame.quit()
    quit()
