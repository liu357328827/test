import pygame
from random import *
from pygame.locals import *
import sys
#屏幕大小
SCREEN_RECT=pygame.Rect(0,0,480,700)
#刷新的帧率
FRAME_PER_SEC=60

CREATE_ENEMY_EVEN=USEREVENT#创建敌机出现的定时器
BULLET_FREE=USEREVENT+1#创建发射子弹定时器
SUPPLY_TIME=USEREVENT+2#补给发放定时器

class GameSprite(pygame.sprite.Sprite):
    '''飞机大战游戏精灵'''
    def __init__(self,image,speed=1):
        super().__init__()
        self.image=pygame.image.load(image)
        self.rect=self.image.get_rect()
        self.speed=speed
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect.y+=self.speed
class Background(GameSprite):
    def __init__(self,is_alt=False):
        #调用父类方法，创建背景精灵
        super().__init__("./images/background.png")
        #判断是否为交替图像如果是则重新设置初始位置
        if is_alt:
            self.rect.y=-self.rect.height

    def update(self):
        #1调用父类的update方法
        super().update()
        #2判断背景图片是否移出底线
        if self.rect.y>=SCREEN_RECT.height:
            self.rect.y=-self.rect.height
class SmallEnemy(GameSprite):
    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.rect.x,self.rect.y=randint(0,SCREEN_RECT.width-self.rect.width),-self.rect.height
        self.speed = [randint(-3,3),randint(1,5)]
        self.destoryimages=['./images/enemy1_down1.png',
                            './images/enemy1_down2.png',
                            './images/enemy1_down3.png',
                            './images/enemy1_down4.png']
        self.destoryindex=0
        self.active=True
        self.hit=False
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        if self.hit:
            self.active=False
        if self.active:
            if self.rect.y>SCREEN_RECT.height or self.rect.left<(0-self.rect.width) or self.rect.left>(SCREEN_RECT.width-self.rect.width):
                self.kill()
            else:
                self.rect.x+=self.speed[0]
                self.rect.y+=self.speed[1]
        else:
            if self.destoryindex<4:
                self.image=pygame.image.load(self.destoryimages[self.destoryindex])
                self.destoryindex=(self.destoryindex+1)%5
            else:
                super().kill()
    def kill(self):
        self.active=False
class MidEnemy(GameSprite):
    def __init__(self):
        super().__init__("./images/enemy2.png")
        self.rect.x, self.rect.y = randint(0, SCREEN_RECT.width - self.rect.width), 0
        # self.speed=[randint(-1,1),randint(2,3)]-self.rect.height
        self.speed=[0,0]
        self.hit=False
        self.hp=8
        self.active=True
        self.destoryindex=0
        self.destoryimages=['./images/enemy2_down1.png',
                            './images/enemy2_down2.png',
                            './images/enemy2_down3.png',
                            './images/enemy2_down4.png']
    def update(self):
        if self.active :
            if self.hit:
                self.hp-=1
                self.hit=False
                self.image=pygame.image.load("./images/enemy2_hit.png")
                if self.hp<=0:
                    self.active=False
                print(self.hp)
            else:
                self.image=pygame.image.load("./images/enemy2.png")
            if self.rect.left < 0 or self.rect.left > (SCREEN_RECT.width - self.rect.width):
                self.speed[0]=-self.speed[0]
            if self.rect.y > SCREEN_RECT.height:
                self.kill()
            else:
                self.rect.x += self.speed[0]
                self.rect.y += self.speed[1]
            self.mask = pygame.mask.from_surface(self.image)
        else:
            if self.destoryindex<4:
                self.image=pygame.image.load(self.destoryimages[self.destoryindex])
                self.destoryindex=(self.destoryindex+1)%5
            else:
                self.kill()
    # def kill(self):
    #     self.active=False

class BigEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load("./images/enemy3_n1.png")
        self.image2 = pygame.image.load("./images/enemy3_n2.png")
        self.speed = 0
        self.image=self.image1
        self.rect=self.image1.get_rect()
        self.rect.x, self.rect.y = randint(0, SCREEN_RECT.width - self.rect.width), 0
        self.switcher = False
        self.n=0
        self.active=True
        self.hit=False
        self.hp=20
        self.destory_images=[
                            './images/enemy3_down1.png',
                            './images/enemy3_down2.png',
                            './images/enemy3_down3.png',
                            './images/enemy3_down4.png',
                            './images/enemy3_down5.png',
                            './images/enemy3_down6.png'
                        ]
        self.destory_index=0
    def update(self):
        self.n = (self.n + 1) % 3#每5帧切换一次图片-self.rect.height
        if self.active:
            if not self.hit:
                if not self.n:
                    self.switcher=not self.switcher
                if self.switcher:
                    self.image=self.image1
                else:
                    self.image=self.image2
            else:
                self.image=pygame.image.load("./images/enemy3_hit.png")
                self.hit = False
                self.hp -= 1
                print(self.hp)
                if self.hp <= 0:
                    self.active = False
            self.mask = pygame.mask.from_surface(self.image)
            if self.rect.y > SCREEN_RECT.height :
                self.kill()
            else:
                self.rect.y += self.speed
        else:
            if self.destory_index<6:
                self.image=pygame.image.load(self.destory_images[self.destory_index])
                if not self.n:
                    self.destory_index+=1
            else:
                self.kill()
class Myplane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load("./images/me1.png")
        self.image2 = pygame.image.load("./images/me2.png")
        self.speed = 2
        self.rect=self.image1.get_rect()
        self.rect.centerx, self.rect.centery =  SCREEN_RECT.width//2 ,SCREEN_RECT.height//2
        self.switcher = False
        self.n=0
    def update(self,):
        self.n = (self.n + 1) % 5#每5帧切换一次图片
        if not self.n:
            self.switcher=not self.switcher
        if self.switcher:
            self.image=self.image1
        else:
            self.image=self.image2
        self.mask = pygame.mask.from_surface(self.image)
class Bullet1(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load("./images/bullet1.png")
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos
        self.active=True
    def update(self):
        if self.active:
            self.rect.y-=self.speed
        if self.rect.y<0:
            self.active=False
    # def reset(self,pos):
    #     self.active=True
    #     self.rect.centerx, self.rect.centery = pos
class Bullet2(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("./images/bullet2.png")
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos
        self.active = True

    def update(self):
        if self.rect.y > 0 and self.active:
            self.rect.y -= self.speed
        else:
            self.kill()
class Supply(pygame.sprite.Sprite):
    def __init__(self,image,speed=3):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.speed = speed
    def update(self):
        if self.rect.y>SCREEN_RECT.height:
            self.kill()
        else:
            self.rect.y += self.speed
class BombSupply(Supply):
    def __init__(self):
        super().__init__("./images/bomb_supply.png")
class BulletSupply(Supply):
    def __init__(self):
        super().__init__("./images/bullet_supply.png")



