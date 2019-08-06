from  material import *
import pygame
from pygame.locals import *
a=Atlas()
# print(a.atlas)
pygame.init()
screen=pygame.display.set_mode((400,400))
font=pygame.font.Font(None, 36)
flag1=False
clock=pygame.time.Clock()
used=[]
while True:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()
        if event.type==MOUSEMOTION:
            mouse_pos=(event.pos[0]//40,event.pos[1]//40)
            if event.pos[0]<5 or event.pos[0]>395 or event.pos[1]<5 or event.pos[1]>395 or mouse_pos not in a.grass:
                flag1=False
            else:
                flag1=True
        if event.type==MOUSEBUTTONDOWN:
            a.judge((event.pos[0]//40,event.pos[1]//40))

    for i,j in a.atlas.items():
        if j>0:
            pygame.draw.rect(screen, (255, 0, 255), (i[0] * 40, i[1] * 40, 39, 39))
            num_text =font.render(str(j), True, (0, 0, 0))
            screen.blit(num_text,(i[0]*40+15,i[1]*40+10))
        if j ==0:
            pygame.draw.rect(screen, (200,200,200), (i[0] * 40, i[1] * 40, 39, 39))
        if j<0:
             pygame.draw.rect(screen,(255,0,0),(i[0]*40,i[1]*40,39,39))
        for i,j in a.grass.items():
            pygame.draw.rect(screen, (255,255, 255), (i[0] * 40, i[1] * 40, 39, 39))
        if flag1:
            pygame.draw.rect(screen, (0, 0, 255), ( mouse_pos[0] * 40,  mouse_pos[1] * 40, 39, 39))
        pygame.display.update()