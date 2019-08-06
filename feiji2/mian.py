import pygame
from random import *
from pygame.locals import *
from plane_sprites import *

class PlaneGame():
    def __init__(self):
        #1.创建游戏窗口
        self.screen=pygame.display.set_mode(SCREEN_RECT.size)
        #2.创建时钟
        self.clock=pygame.time.Clock()
        #3.调用私有方法，创建精灵、精灵组
        self.__create_sprites()
        pygame.time.set_timer(CREATE_ENEMY_EVEN,1000)#设置定时器时间，创建敌机,1s出现一个
        pygame.time.set_timer(BULLET_FREE, 300)#设置子弹发射间隔0.1s
        pygame.time.set_timer(SUPPLY_TIME, 5000)#设置补给发放间隔30s
    def __create_sprites(self):
        #创建背景精灵、精灵组
        bg1=Background()
        bg2 = Background(True)
        self.bg_group=pygame.sprite.Group(bg1,bg2)
        #创建敌机精灵组
        self.enemies_group=pygame.sprite.Group()
        #创建我方飞机
        self.me=Myplane()
        self.me_group=pygame.sprite.Group(self.me)
        #创建子弹精灵列表
        # self.bullet1=[]
        self.bullets_group=pygame.sprite.Group()
        # for i in range(4):
        #     X=Bullet1(self.me.rect.midtop)
        #     self.bullet1.append(X)
        #     self.bullets_group.add(X)
        #创建补给精灵组
        self.supply_group=pygame.sprite.Group()

    def start_game(self):
        while True:
            #设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #事件监听
            self.__event_handler()
            #碰撞检测
            self.__check_collide()
            #更新、绘制精灵组
            self.__update_sprites()
            #刷新屏幕
            pygame.display.update()
    def __event_handler(self):
        for event in pygame.event.get():
            if event.type==QUIT:#判断是否退出游戏
                PlaneGame.__game_over()
            elif event.type==CREATE_ENEMY_EVEN:
                # self.enemies_group.add(SmallEnemy())
                # self.enemies_group.add(MidEnemy())

                self.enemies_group.add(BigEnemy())
                pygame.time.set_timer(CREATE_ENEMY_EVEN, 0)
            elif event.type==MOUSEMOTION:
                self.me.rect.centerx, self.me.rect.centery=event.pos
            elif event.type==BULLET_FREE:
                # self.bullets_group.add(Bullet1(self.me.rect.midtop))
                self.bullets_group.add(Bullet2((self.me.rect.centerx+10,self.me.rect.top)))
                self.bullets_group.add(Bullet2((self.me.rect.centerx -10, self.me.rect.top)))
            elif event.type==SUPPLY_TIME:
                if choice([True,False]):
                    self.supply_group.add(BulletSupply())
                else:
                    self.supply_group.add(BombSupply())
    def __check_collide(self):
        # enemy_down=pygame.sprite.spritecollide(self.me,self.enemies_group,True,pygame.sprite.collide_mask)#敌机与我方飞机碰撞检测
        bullet_down=pygame.sprite.groupcollide(self.bullets_group,self.enemies_group,True,False,pygame.sprite.collide_mask)
        if bullet_down:
            for x,y in bullet_down.items():
                y[0].hit=True

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)

        self.enemies_group.update()
        self.enemies_group.draw(self.screen)
        self.me_group.update()
        self.me_group.draw(self.screen)
        self.bullets_group.update()
        self.bullets_group.draw(self.screen)
        self.supply_group.update()
        self.supply_group.draw(self.screen)
    @staticmethod
    def __game_over():
        pygame.quit()
        sys.exit()

if __name__== '__main__':
    game=PlaneGame()
    game.start_game()