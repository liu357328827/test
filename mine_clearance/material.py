import pygame
from pygame.locals import *
from random import *
class Atlas():
    def __init__(self,atlas_width=10,atlas_height=10,mine_num=10):
        self.atlas={}
        self.atlas_width=atlas_width
        self.atlas_height=atlas_height
        self.mine_num=mine_num
        self.defeat=False
        for i in range(atlas_width):#土地
            for j in range(atlas_height):
                self.atlas[(i,j)]=0
        self.grass=self.atlas.copy()#草皮
        coordinate_list=list(self.atlas.keys())#坐标列表
        self.mines_coordinate={}
        for i in range(mine_num):#地雷坐标
            temp=choice(coordinate_list)
            self.atlas[temp]=self.mines_coordinate[temp]=-1
            coordinate_list.remove(temp)#无雷坐标列表
        for i in coordinate_list:#计算每个方格周围有多少地雷
            if (i[0]+1,i[1]+1) in self.mines_coordinate:
                self.atlas[i]+=1
            if (i[0] + 1,i[1]) in self.mines_coordinate:
                self.atlas[i]+=1
            if (i[0]+1,i[1]-1) in self.mines_coordinate:
                self.atlas[i]+=1
            if (i[0], i[1]-1) in self.mines_coordinate:
                self.atlas[i] += 1
            if (i[0]-1,i[1]-1) in self.mines_coordinate:
                self.atlas[i]+=1
            if (i[0]-1,i[1]) in self.mines_coordinate:
                self.atlas[i]+=1
            if (i[0]-1,i[1]+1) in self.mines_coordinate:
                self.atlas[i]+=1
            if (i[0],i[1]+1) in self.mines_coordinate:
                self.atlas[i]+=1
    def judge(self,pos):
        if pos in self.grass:
            self.grass.pop(pos)
            if self.atlas[pos]==0:
                if (pos[0]-1,pos[1]) in self.grass and (pos[0]-1,pos[1]) not in self.mines_coordinate:
                    self.judge((pos[0]-1,pos[1]))
                if (pos[0]-1,pos[1]-1) in self.grass and (pos[0]-1,pos[1]-1) not in self.mines_coordinate:
                    self.judge((pos[0]-1,pos[1]-1))
                if (pos[0],pos[1]-1) in self.grass and (pos[0],pos[1]-1) not in self.mines_coordinate:
                    self.judge((pos[0],pos[1]-1))
                if (pos[0]+1,pos[1]-1) in self.grass and (pos[0]+1,pos[1]-1) not in self.mines_coordinate:
                    self.judge((pos[0]+1,pos[1]-1))
                if (pos[0]+1,pos[1]) in self.grass and (pos[0]+1,pos[1]) not in self.mines_coordinate:
                    self.judge((pos[0]+1,pos[1]))
                if (pos[0]+1,pos[1]+1) in self.grass and (pos[0]+1,pos[1]+1) not in self.mines_coordinate:
                    self.judge((pos[0]+1,pos[1]+1))
                if (pos[0],pos[1]+1) in self.grass and (pos[0],pos[1]+1) not in self.mines_coordinate:
                    self.judge((pos[0],pos[1]+1))
                if (pos[0]-1,pos[1]+1) in self.grass and (pos[0]-1,pos[1]+1) not in self.mines_coordinate:
                    self.judge((pos[0]-1,pos[1]+1))
            elif self.atlas[pos]==-1:
                self.defeat=True
                print("游戏结束")