from game_material import *
# import pygame
class Game():
    def __init__(self):
        #初始化屏幕
        self.screen=pygame.display.set_mode(SCREEN_RECT.size)
        #游戏时钟
        self.clock=pygame.time.Clock()
        #生成snake 和food
        self.__create()
        #计分牌
        self.score=0
        #开始游戏
    def __create(self):
        self.game_snake=Snake()
        self.game_food=Food(self.game_snake.snake)
    def start_game(self):
        delay=0
        level=9
        while True:
            #设置刷新帧率
            self.clock.tick(30)
            #游戏事件监测
            self.__event_handle()
            # 碰撞检测
            self.__collide()
            self.screen.fill(BALCK)
            if self.game_snake.active:
                #绘制 snake food
                if not delay%level:
                    self.game_snake.move()
                for i in self.game_snake.snake:
                    if i==self.game_snake.snake[0]:
                        color=RED
                    else:
                        color=WHITE
                    pygame.draw.rect(self.screen,color,(i[0]*30,i[1]*30,30,30))
                pygame.draw.rect(self.screen,BULUE,(self.game_food.food[0]*30,self.game_food.food[1]*30,30,30))
            else:
                #游戏结束，结束画面
                print("game over")

            #刷新屏幕
            pygame.display.update()
            delay=(delay+1)%6
    def __collide(self):
        self.game_snake.judge()
        if self.game_snake.snake[0]==self.game_food.food:
            self.game_food.reset(self.game_snake.snake)
            self.score+=1
            self.game_snake.elongate()
        # if self.score>
    def __event_handle(self):
        for event in pygame.event.get():
            if event.type==QUIT:
                Game.__game_over()
            if event.type==KEYDOWN:
                if event.key==K_UP and self.game_snake.direction!=[0,1]:
                    self.game_snake.direction=[0,-1]
                elif event.key==K_DOWN and self.game_snake.direction!=[0,-1]:
                    self.game_snake.direction=[0,1]
                elif event.key==K_LEFT and self.game_snake.direction!=[1,0]:
                    self.game_snake.direction=[-1,0]
                elif event.key==K_RIGHT and self.game_snake.direction!=[-1,0]:
                    self.game_snake.direction=[1,0]
    @staticmethod
    def __game_over():
        pygame.quit()
        exit()



if __name__ == '__main__':
    game=Game()
    game.start_game()