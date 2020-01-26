# -*- coding: utf-8 -*-
"""
Created on Sat May 18 16:34:44 2019

@author: chris
"""

import pygame
import random
import time


#color settings
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
grey = (232, 232, 232, 1)

#game display conditions
height = 500
width = 300
fps = 60

#global variable
pause = False

#spaceship conditions
shipImg = pygame.image.load("blueship.png")
shipImg = pygame.transform.scale(shipImg, (50, 50))
#alien conditions
alienImg = pygame.image.load("enemy.png")
alienImg = pygame.transform.scale(alienImg, (50, 50))
#bullet condition
#bulletImg = pygame.image.load("bullets.png")

#initializing the game
pygame.init()
pygame.mixer.init()
monitor = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space shooting")
timing = pygame.time.Clock()

        
#creating a spaceship object     
class spaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = shipImg
        self.rect = self.image.get_rect()
        #self.image.fill(blue)
        #self.radius = 40
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.centerx = width / 2 
        self.rect.centery = height - self.rect.height
        self.speedx = 0
        self.speedy = 0
        
    def update(self):
        self.speedx = 0
        self.speedy = 0
        command = pygame.key.get_pressed()
        if command[pygame.K_RIGHT]:
            self.speedx =  5
        if command[pygame.K_LEFT]:
            self.speedx =  -5
        if command[pygame.K_UP]:
            self.speedy = -5
        if command[pygame.K_DOWN]:
            self.speedy =  5
            
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy
                    
        if self.rect.right > width :
            self.rect.right = width 
        if self.rect.left < 0 :
            self.rect.left = 0 
        if self.rect.bottom > height :
            self.rect.bottom = height 
        if self.rect.top < 0 :
            self.rect.top = 0 
     
    def fire(self):
        Bullets = bullets(self.rect.centerx,self.rect.top)
        every_sprites.add(Bullets)
        Bullet.add(Bullets)
        shooting_sound.play()
        
                       
    
Spaceship = spaceShip()

#creating an alien object
class alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = alienImg
        #self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(35,250)
        self.rect.centery = -100
        self.speedy = 6
        
    
    def update(self):
        self.rect.y = self.rect.y + self.speedy
        if self.rect.top > height + 40:
            self.rect.centerx = random.randrange(35,250)
            self.rect.centery = -100
            self.speedy = self.speedy + 3 
            

    
            

Alien = alien()

#creating bullets
class bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,40))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -5
    
    def update(self):
        self.rect.y = self.rect.y + self.speedy
        if self.rect.bottom < 0:
            self.kill()
    
    
        
    
#sound
shooting_sound = pygame.mixer.Sound("shooting.wav")
exploding_sound = pygame.mixer.Sound("exploding.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
#put every sprite object together so it can update all at once
every_sprites = pygame.sprite.Group()
Bullet = pygame.sprite.Group()
enemy = pygame.sprite.Group()
ship = pygame.sprite.Group()
enemy.add(Alien)
ship.add(Spaceship)
every_sprites.add(Spaceship)
every_sprites.add(Alien)

 
#text display
def lose():
    pygame.font.init()
    Font = pygame.font.SysFont('freesansbold.ttf',50)
    textSurface = Font.render('You Lose',True,white)
    monitor.blit(textSurface,(80,200))
    #Font2 = pygame.font.SysFont('freesansbold.ttf',12)
    #textSurface2 = Font2.render('Press Space to restart',True,black)
    #monitor.blit(textSurface2,(80,300))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()

    
#more enemy
def add():
    newAlien = alien()
    enemy.add(newAlien)
    every_sprites.add(newAlien)
for i in range(5):
    add()
    
#intro
def intro():
    introduction = True
    while introduction:
        monitor.fill(grey)
        pygame.font.init()
        Font_intro = pygame.font.SysFont('freesansbold.ttf',50)
        text_intro = Font_intro.render('Welcome to',True,black)
        monitor.blit(text_intro,(60,150))
        Font_intro2 = pygame.font.SysFont('freesansbold.ttf',50)
        text_intro2 = Font_intro2.render('Space Shooting',True,black)
        monitor.blit(text_intro2,(20,200))
        Font_intro3 = pygame.font.SysFont('freesansbold.ttf',30)
        text_intro3 = Font_intro3.render('Press [SPACE] to begin',True,black)
        monitor.blit(text_intro3,(40,300))
        Font_intro4 = pygame.font.SysFont('freesansbold.ttf',30)
        text_intro4 = Font_intro4.render('Press [p] to pause',True,black)
        monitor.blit(text_intro4,(60,350))
        monitor.blit(shipImg,(125,400))
        monitor.blit(alienImg,(125,50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    introduction = False
                    game()
  
    
#unpause
def unpause():
    global pause
    pause = False
#pause
def paused():
    
    while pause:
        monitor.fill(grey)
        pygame.font.init()
        Font_pause = pygame.font.SysFont('freesansbold.ttf',50)
        text_pause = Font_pause.render('Paused',True,black)
        monitor.blit(text_pause,(90,150))
        Font_pause2 = pygame.font.SysFont('freesansbold.ttf',50)
        text_pause2 = Font_pause2.render('Press [r] to restart',True,black)
        monitor.blit(text_pause2,(2,200))
        monitor.blit(shipImg,(125,400))
        monitor.blit(alienImg,(125,50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    unpause()



        

#game loop
def game():
    kill_count = 0
    global pause
    run = True
    while run:
        # tick can give us the milliseconds
        timing.tick(fps) 
            
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                     Spaceship.fire()
                if event.key == pygame.K_p:
                    pause = True
                    paused()
     
        #updating all the sprites
        every_sprites.update()   
        
        #when alien hit the ship, the game will end
        if pygame.sprite.groupcollide(enemy,ship,True,True):
            game_over_sound.play()
            lose()

        """if Spaceship.rect.top < Alien.rect.bottom:
            if Alien.rect.right > Spaceship.rect.left and Alien.rect.right < Spaceship.rect.right:
                run = False
        if Spaceship.rect.top < Alien.rect.bottom:
            if Alien.rect.left < Spaceship.rect.right and Alien.rect.left > Spaceship.rect.left:
                run = False
        if Alien.rect.top > Spaceship.rect.bottom:
            if Alien.rect.right > Spaceship.rect.left and Alien.rect.right < Spaceship.rect.right:
                run = True
        if Alien.rect.top > Spaceship.rect.bottom:
            if Alien.rect.left < Spaceship.rect.right and Alien.rect.left > Spaceship.rect.left:
                run = True"""
 
        #when bullet hits the alien, the alien will disappear and comes out again
        #when Alien is vanished, there is still a ghost
        killed = pygame.sprite.groupcollide(enemy,Bullet,True,True)
        if killed:
          add()
          kill_count = kill_count + 1
          exploding_sound.play()
          
        #draw on the monitor
        monitor.fill(black)
        pygame.font.init()
        
         
        Font = pygame.font.SysFont('freesansbold.ttf',30)
        textSurface = Font.render("kill count: " + str(kill_count),True,white)
        monitor.blit(textSurface,(5,5))
        every_sprites.draw(monitor)        
        #update the monitor
        pygame.display.flip()


intro()            
game()
pygame.quit()







