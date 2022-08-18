from turtle import down
import wave
import pygame
import time
import os
import random

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")

# --- Load images --- #
# Enemy ship
RED_SPACE_SHIP = pygame.image.load(os.path.join("Image", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("Image", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("Image", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("Image", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("Image", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("Image", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("Image", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("Image", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("Image", "background-black.png")),(WIDTH, HEIGHT))

# --- set up laser --- #
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel
        
    def offScreen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(self, obj)


# --- set up ship --- #
class Ship:
    COOLDOWN = 30
    
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.shipImg = None
        self.laserImg = None
        self.lasers = []
        self.coolDownCounter = 0
    
     # shipを描写    
    def draw(self, window):
        window.blit(self.shipImg, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
            
    def moveLasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offScreen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
                
                
    def cooldown(self):
        if self.coolDownCounter >= self.COOLDOWN:
            self.coolDownCounter = 0
        elif self.coolDownCounter > 0:
            self.coolDownCounter += 1
        
    def shoot(self):
        if self.coolDownCounter == 0:
            laser = Laser(self.x, self.y, self.laserImg)
            self.lasers.append(laser)
            self.coolDownCounter = 1
        
    # shipの幅を取得    
    def getWidth(self):
        return self.shipImg.get_width()
    
    # shipの高さを取得
    def getHeight(self):
        return self.shipImg.get_height()

# --- player set up -- #
class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.shipImg = YELLOW_SPACE_SHIP
        self.laserImg = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.shipImg)
        self.maxHealth = health
        
    def moveLasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offScreen(HEIGHT):
                self.lasers.remove(laser)
            else: 
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        
    def healthBar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.getHeight() + 10, self.getWidth(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.getHeight() + 10, self.getWidth() * (self.health/self.maxHealth), 10))
      
    def draw(self, window):
        super().draw(window)
        self.healthBar(window)  
              
# --- enemy set up --- #
class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.shipImg, self.laserImg = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.shipImg)
        
    def shoot(self):
        if self.coolDownCounter == 0:
            laser = Laser(self.x-20, self.y, self.laserImg)
            self.lasers.append(laser)
            self.coolDownCounter = 1
        
    def move(self, vel):
        self.y += vel
        

def collide(obj1, obj2):
    offsetX = obj2.x - obj1.x
    offsetY = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offsetX, offsetY)) != None

def main():
    # --- setting game --- #
    run = True
    lost = False
    FPS = 60
    level = 1
    lives = 5
    stage = 0
    lost_count = 0
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    
    # --- Laser setting --- #
    laser_vel = 5
    
    # --- Enemies setting --- #
    enemies = []
    wave_length = 5
    enemy_vel = 1

    # --- Player setting(moving speed) --- #
    player_vel = 5
    
    player = Player(300, 630)
    
    clock = pygame.time.Clock()
    
    def redraw_window():
        WINDOW.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        
        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
         # --- Enemy --- #
        for enemy in enemies:
            enemy.draw(WINDOW)
        
        # --- Player --- #
        player.draw(WINDOW)
        
        # --- game over --- #
        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
        
        pygame.display.update()
    
    while run:
        clock.tick(FPS)# 60フレームで描画
        redraw_window()# 背景の再描画
        
        # --- judge game --- #
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
            
        if len(enemies) == 0:
            if stage != 0:
                level += 1
            stage += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "green", "blue"]))
                enemies.append(enemy)
        
        # --- 強制終了 --- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
        # --- player moving with keys --- #
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.getWidth() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.getHeight() + 20 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            
        # --- Enemy moving --- #
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.moveLasers(laser_vel, player)
            
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            
            
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.getHeight() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            
        player.moveLasers(-laser_vel, enemies)
        
        
def mainManue():
    title_font = pygame.font.SysFont("comicsans", 60)
    run = True
    while run:
        WINDOW.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                
    pygame.quit()

mainManue()                