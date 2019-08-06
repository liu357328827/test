from material import *
import pygame
class Game():
    def __init__(self):
        # self.atlas
        pygame.init()
        self.clock=pygame.time.Clock()
        self.font=pygame.font.Font(None,36)
        self.game_atlas=Atlas()#生成地图
        self.screen = pygame.display.set_mode((self.game_atlas.atlas_height*40,self.game_atlas.atlas_height*40))
        self.flag1=False#是否被鼠标选定
    def start_game(self):
        while True:
            #设置刷新率
            self.clock.tick(60)
            #事件监测
            self.__event_handle()
            #绘制图像
            self.__draw_image()
            #更新屏幕
            pygame.display.update()
    def __event_handle(self):
        for  event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEMOTION:
                self.mouse_pos = (event.pos[0] // 40, event.pos[1] // 40)
                if event.pos[0] < 5 or event.pos[0] > 395 or event.pos[1] < 5 or event.pos[1] > 395 or self.mouse_pos not in self.game_atlas.grass:
                    self.flag1 = False
                else:
                    self.flag1 = True
            if event.type == MOUSEBUTTONDOWN:
                temp=(event.pos[0] // 40, event.pos[1] // 40)
                if event.button==1:
                    self.game_atlas.judge(temp)
                if event.button==3 and temp in self.game_atlas.grass:
                    self.game_atlas.grass[temp]=not self.game_atlas.grass[temp]
                if len(self.game_atlas.grass)==self.game_atlas.mine_num:
                    print("扫雷成功")
    def __draw_image(self):
        if not self.game_atlas.defeat:#绘制底层
            for i, j in self.game_atlas.atlas.items():
                if j > 0:
                    pygame.draw.rect(self.screen, (255, 0, 255), (i[0] * 40, i[1] * 40, 39, 39))
                    num_text = self.font.render(str(j), True, (0, 0, 0))
                    self.screen.blit(num_text, (i[0] * 40 + 15, i[1] * 40 + 10))
                if j == 0:
                    pygame.draw.rect(self.screen, (200, 200, 200), (i[0] * 40, i[1] * 40, 39, 39))
                if j < 0:
                    pygame.draw.rect(self.screen, (255, 0, 0), (i[0] * 40, i[1] * 40, 39, 39))
            for i, j in self.game_atlas.grass.items():#绘制表层
                if j:
                    pygame.draw.rect(self.screen, (0, 255, 255), (i[0] * 40, i[1] * 40, 39, 39))
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), (i[0] * 40, i[1] * 40, 39, 39))
                    if self.flag1:
                        pygame.draw.rect(self.screen, (0, 0, 255), (self.mouse_pos[0] * 40, self.mouse_pos[1] * 40, 39, 39))
        else:
            game_over_text = self.font.render(str('Game Over'), True, (0, 0, 0))
            game_over_rect=game_over_text.get_rect()
            game_over_rect.centerx,game_over_rect.centery=self.game_atlas.atlas_height*20,self.game_atlas.atlas_height*20
            self.screen.blit(game_over_text,(game_over_rect))
    @staticmethod
    def __game_over():
        pygame.quit()
        exit()
if __name__=='__main__':
    game=Game()
    game.start_game()