import pygame
import sys
from pygame.locals import *
from random import randint

pygame.init()
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")#大飞机
enemy3_fly_sound.set_volume(0.2)

class SmallEnemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# self.bg_size=bg_size
		self.image = pygame.image.load('images/enemy1.png').convert_alpha()
		self.rect=self.image.get_rect()
		self.speed=[randint(-1,1),randint(1,3)]
		self.rect.left,self.rect.top=[randint(-45,423),randint(-200,-43)]
		self.destory_images=[
							pygame.image.load('images/enemy1_down1.png').convert_alpha(),
							pygame.image.load('images/enemy1_down2.png').convert_alpha(),
							pygame.image.load('images/enemy1_down3.png').convert_alpha(),
							pygame.image.load('images/enemy1_down4.png').convert_alpha(),
							]
		self.death=False
		self.deathindex=0
		self.mask=pygame.mask.from_surface(self.image)
	def move(self):
		self.boundary()
		self.rect.left+=self.speed[0]*2
		self.rect.top+=(self.speed[1]+1)
	#检测飞机出界情况	
	def boundary(self):
		if self.rect.left<-56 or self.rect.left>479 or self.rect.top>700:
			self.reset()
	def reset(self):
		self.death=False
		self.rect.left,self.rect.top=[randint(-55,423),randint(-500,-43)]
		self.speed=self.speed

		
class MidEnemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/enemy2.png').convert_alpha()
		self.image_hit = pygame.image.load("images/enemy2_hit.png").convert_alpha()
		self.rect=self.image.get_rect()
		self.speed=[randint(-3,3),2]
		self.rect.left,self.rect.top=[randint(-50,411),randint(-2100,-100)]
		self.destory_images=[
							pygame.image.load('images/enemy2_down1.png').convert_alpha(),
							pygame.image.load('images/enemy2_down2.png').convert_alpha(),
							pygame.image.load('images/enemy2_down3.png').convert_alpha(),
							pygame.image.load('images/enemy2_down4.png').convert_alpha()
							]
		self.hp=8
		self.death=False
		self.deathindex=0
		self.hit=False
		self.mask=pygame.mask.from_surface(self.image)
	def move(self):
		self.boundary()
		self.rect.left+=self.speed[0]
		self.rect.top+=self.speed[1]
	#检测飞机出界情况	
	def boundary(self):
		if self.rect.left<-20 :
			self.speed[0]=-self.speed[0]
		if self.rect.right>490:
			self.speed[0]=-self.speed[0]
		if self.rect.top>700:
			self.reset()
	def reset(self):
		self.death=False
		self.hp=8
		self.rect.left,self.rect.top=[randint(-50,411),randint(-2100,-100)]
		self.speed=self.speed

class BigEnemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# self.bg_size=bg_size
		self.image1 = pygame.image.load('images/enemy3_n1.png').convert_alpha()
		self.image2 = pygame.image.load('images/enemy3_n2.png').convert_alpha()
		self.image_hit = pygame.image.load("images/enemy3_hit.png").convert_alpha()
		self.rect=self.image1.get_rect()
		self.speed=[0,1]
		self.rect.left,self.rect.top=[randint(0,211),randint(-5000,-3000)]
		self.destory_images=[
							pygame.image.load('images/enemy3_down1.png').convert_alpha(),
							pygame.image.load('images/enemy3_down2.png').convert_alpha(),
							pygame.image.load('images/enemy3_down3.png').convert_alpha(),
							pygame.image.load('images/enemy3_down4.png').convert_alpha(),
							pygame.image.load('images/enemy3_down5.png').convert_alpha(),
							pygame.image.load('images/enemy3_down6.png').convert_alpha()
							]
		self.hp=20
		self.death=False
		self.hit=False
		self.deathindex=0
		self.mask=pygame.mask.from_surface(self.image1)
		self.enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")#大飞机
		self.enemy3_fly_sound.set_volume(0.2)
	def move(self):
		self.boundary()
		self.rect.left+=self.speed[0]
		self.rect.top+=self.speed[1]
		
	def boundary(self):#检测飞机出界情况
		if self.rect.left<0 or self.rect.left>211 or self.rect.top>700:
			self.reset()
	def reset(self):
		self.death=False
		self.hp=20
		self.speed=self.speed
		self.rect.left,self.rect.top=[randint(0,211),randint(-5000,-3000)]
		self.enemy3_fly_sound.stop()



		

		
