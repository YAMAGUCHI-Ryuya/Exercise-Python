import random
import pygame
import math
from pygame import mixer

pygame.init()

# 画面
screen = pygame.display.set_mode((800, 600))

# タイトル設定
pygame.display.set_caption('Invaders Game')

# 画像の読み込み
# Player
playerImg = pygame.image.load('player.png')
playerX, playerY = 370, 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change, enemyY_change = 3, 40

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0, 480
bulletX_change, buklletY_change = 0, 3
bullet_state = 'ready'

# Score
scoreValue = 0

# BGM
mixer.Sound('background.wav').play()

# 画像表示
# Player
def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
def enemy(x, y):
    screen.blit(enemyImg, (x, y))
    
# Bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# 画面表示設定
running = True
while running:
    # 背景色の初期化
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Put on key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:# put on left key
                playerX_change -= 1.5
            if event.key == pygame.K_RIGHT:# put on right key
                playerX_change += 1.5
            if event.key == pygame.K_SPACE:# put on space key
                if bullet_state is 'ready':
                    bulletX = playerX
                    mixer.Sound('laser.wav').play()
                    fire_bullet(bulletX, bulletY)
        
        # Put up key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # Player        
    playerX += playerX_change
    # 画面内にplayerを収める
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736   
    
    # Enemy
    if enemyY > 440:
        break
    enemyX += enemyX_change
    # 左端に来たら
    if enemyX <= 0:
        enemyX_change = 3
        enemyY += enemyY_change
    # 右端に来たら
    elif enemyX >= 736:
        enemyX_change = -3
        enemyY += enemyY_change
        
    # Bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
        
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= buklletY_change
    
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    # bullet, enemyの初期化
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        scoreValue += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)
    
    # スコア表示
    font = pygame.font.SysFont(None, 32)#フォントの決定
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))#テキストの情報（表示する文字、　、色）を決定
    screen.blit(score, (20, 50))
            
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    
    pygame.display.update()