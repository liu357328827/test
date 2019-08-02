import pygame
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode((600,600))
snake=[[-1,0],[9,10],[9,10],[9,10],[10,10]]
def move_up(snake_list):
    if not snake[0]==[0,1]:
        snake[0]=[0,-1]
    temp=snake_list[1].copy()
    temp[1]-=1
    snake_list.insert(1,temp)
    snake_list.pop()
def move_down(snake_list):
    if not snake[0] == [0, -1]:
        snake[0]=[0,1]
    temp=snake_list[1].copy()
    temp[1]+=1
    snake_list.insert(1,temp)
    snake_list.pop()
def move_left(snake_list):
    if not snake[0] == [1, 0]:
        snake[0]=[-1,0]
    temp=snake_list[1].copy()
    temp[0]-=1
    snake_list.insert(1,temp)
    snake_list.pop()
def move_right(snake_list):
    # if not snake[0] == [-1,0]:
    snake[0]=[1,0]
    temp=snake_list[1].copy()
    temp[0]+=1
    snake_list.insert(1,temp)
    snake_list.pop()
def move(snake_list):
    temp = snake_list[1].copy()
    temp[0]+=snake_list[0][0]
    temp[1]+=snake_list[0][1]
    snake_list.insert(1, temp)
    snake_list.pop()

clock = pygame.time.Clock()
delay=100
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()
        elif event.type==KEYDOWN:
            if event.key==K_UP:
                if not snake[0]==[0,1]:
                    move_up(snake)
            elif event.key==K_LEFT:
                if not snake[0] == [1, 0]:
                    move_left(snake)
            elif event.key==K_DOWN:
                if not snake[0] == [0, -1]:
                    move_down(snake)
            elif event.key==K_RIGHT:
                if not snake[0] == [-1, 0]:
                    move_right(snake)
    screen.fill((0,0,0))
    if not delay%10:
        move(snake)
    for i in snake:
        if i==snake[1]:
            scolor=(255,0,130)
        else:
            scolor=(0,130,220)
        if not i==snake[0]:
            pygame.draw.rect(screen,scolor,(i[0]*30,i[1]*30,30,30))
    pygame.display.update()
    delay-=1
    if not delay:
        delay=100