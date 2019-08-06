import pygame
import sys
from pygame.locals import *
from random import randint

class Myplane(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image1 = pygame.image.load('images/me1.png').convert_alpha()
		self.rect=self.image1.get_rect()
		self.rect.centerx,self.rect.centery=240,650
		self.image2 = pygame.image.load('images/me2.png').convert_alpha()
		self.destory_images=[
							pygame.image.load('images/me_destroy_1.png').convert_alpha(),
							pygame.image.load('images/me_destroy_2.png').convert_alpha(),
							pygame.image.load('images/me_destroy_3.png').convert_alpha(),
							pygame.image.load('images/me_destroy_4.png').convert_alpha()
							]
		self.deathindex=0
		self.mask=pygame.mask.from_surface(self.image1)
		self.life=3
		self.invincible = False
		self.death=False
	def reset(self):
		self.invincible = True
		self.life-=1
		self.death=False




