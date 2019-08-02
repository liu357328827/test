import pygame
from pygame.locals import *
from random import *

SCREEN_RECT=pygame.Rect(0,0,600,600)
WHITE=(255,255,255)
RED=(255,0,0)
BULUE=(0,0,255)
BALCK=(0,0,0)
class Snake():

    def __init__(self):
        self.snake=[[11,10],[10,10],[9,10]]
        self.direction=[1,0]
        self.change=True
        self.active = True
    def move(self):
        temp=self.snake[0].copy()
        temp[0] += self.direction[0]
        temp[1] += self.direction[1]
        self.snake.insert(0,temp)
        self.snake.pop()
    def elongate(self):
        temp=self.snake[-1].copy()
        self.snake.append(temp)

    def judge(self):
        print(self.snake[0])
        if self.snake[0][0]<0 or self.snake[0][0]>19:
            self.active=False
        if self.snake[0] in self.snake[1:]:
            self.active=False
class Food():
    def __init__(self,snake):
        self.food=[randint(0,20),randint(0,20)]
        while self.food in snake:
            self.food = [randint(0, 20), randint(0, 20)]
    def reset(self,snake):
        while self.food in snake:
            self.food = [randint(0, 20), randint(0, 20)]
