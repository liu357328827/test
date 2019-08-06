import pygame
import sys
from pygame.locals import *
from random import *
class BombSupply(pygame.sprite.Sprite):
	"""docstring for supply"""
	def __init__(self, ):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load('images/bomb_supply.png').convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.left,self.rect.top=[randint(0,417),-207]
		self.activate=False
	def move(self):
		self.boundary()
		self.rect.top+=3
	def boundary(self):
		if self.rect.left<0:
			self.rect=0
		if self.rect.right>470: 
			self.right=470
		if self.rect.top>700:
			self.reset()
	def reset(self):
		self.rect.left,self.rect.top=[randint(0,417),-207]
		self.activate=False
			
class BulletSupply(pygame.sprite.Sprite):
	"""docstring for supply"""
	def __init__(self, ):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load('images/bullet_supply.png').convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.left,self.rect.top=[randint(0,417),-207]
		self.activate=False
	def move(self):
		self.boundary()
		self.rect.top+=5
	def boundary(self):
		if self.rect.left<0:
			self.rect=0
		if self.rect.right>470: 
			self.right=470
		if self.rect.top>700:
			self.reset()
	def reset(self):
		self.rect.left,self.rect.top=[randint(0,417),-207]
		self.activate=False
