import pygame
import sys
from pygame.locals import *
from random import *
import myplane
import enemy
import bullet
import supply
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
pygame.init()
#设置屏幕大小背景图片
bg_image='images/background.png'
bg_size=(480,700)
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")
background=pygame.image.load(bg_image).convert()

#载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")#背景音乐
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")#子弹音效
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")#炸弹音效
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")#补齐音效
supply_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")#小飞机被击落
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")#中飞机被击落
enemy2_down_sound.set_volume(0.3)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")#大飞机被击落
enemy3_down_sound.set_volume(0.5)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")#获得炸弹音效
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")#获得子弹
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")#我方飞机被击落
me_down_sound.set_volume(0.2)

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy()
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.MidEnemy()
        group1.add(e1)
        group2.add(e1)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.BigEnemy()
        group1.add(e1)
        group2.add(e1)

def main():
	pygame.mixer.music.play(-1)#循环播放背景音乐
	
	clock=pygame.time.Clock()#设置游戏帧数
	delay=100
	
	me=myplane.Myplane()#生成我方飞机

	all_enemy=pygame.sprite.Group()#生成ALL敌机组
	
	big_enemy=pygame.sprite.Group()#生成大飞机组
	add_big_enemies(all_enemy,big_enemy,1)
	mid_enemy=pygame.sprite.Group()#生成中飞机组
	add_mid_enemies(all_enemy,mid_enemy,3)
	small_enemy=pygame.sprite.Group()#生成小飞机组
	add_small_enemies(all_enemy,small_enemy,10)
	add_s=0
	add_m=0
	add_b=0
	speed_lv=0

	switch_image=False#切换图片

	SUPPLYTIME=USEREVENT#定义补给发放时间
	pygame.time.set_timer(SUPPLYTIME,30*1000)#每30秒投放一个补给包
	INVINCIBLETIME=USEREVENT+1#定义无敌时间

	bullet1=[]#生成单发子弹列表
	bullet_num=5#子弹数量
	bullet1_index=0#子弹索引
	bullet2=[]
	bullet2_num=5#子弹数量
	bullet2_index=0#子弹索引
	supperbullet=False

	score=0 #得分
	score_font=pygame.font.Font('font/font.ttf',36)
	with open("record.txt",'r') as f:
		best_score=int(f.read())
	best_score_text=score_font.render("BEST SCORE:%s"%best_score,True,WHITE)
	best_score_rect=best_score_text.get_rect()
	best_score_rect.left,best_score_rect.top=10,10
	gameover=False
	gameover_font1=pygame.font.Font('font/font.ttf',50)
	

	gameover_font2=pygame.font.Font('font/font.ttf',72)
	gameover_text2=gameover_font2.render("GAME OVER",True,WHITE)
	gameover_text2_rect=gameover_text2.get_rect()
	gameover_text2_rect.centerx,gameover_text2_rect.centery=240,400

	again_image=pygame.image.load("images/again.png")
	again_rect=again_image.get_rect()
	again_rect.centerx,again_rect.centery=240,550

	gameover_image=pygame.image.load("images/gameover.png")
	gameover_image_rect=gameover_image.get_rect()
	gameover_image_rect.centerx,gameover_image_rect.centery=240,600

	life_image=pygame.image.load("images/life.png")
	life_rect=life_image.get_rect()

	bomb_supply=supply.BombSupply()#炸弹补给
	bullet_supply=supply.BulletSupply()
	bomb_image=pygame.image.load("images/bomb.png").convert_alpha()#剩余炸弹
	bomb_num=3
	bomb_font=pygame.font.Font('font/font.ttf',36)

	pause=False
	resume_nor=pygame.image.load("images/resume_nor.png").convert_alpha()
	resume_pressed=pygame.image.load("images/resume_pressed.png").convert_alpha()
	pause_rect=resume_nor.get_rect()
	pause_image=resume_nor	

	for x in range(bullet_num):
		bullet1.append(bullet.Bullet1(me.rect.midtop))
	for x in range(bullet2_num):
		bullet2.append(bullet.Bullet2((me.rect.centerx-10,me.rect.top)))
		bullet2.append(bullet.Bullet2((me.rect.centerx-10,me.rect.top)))

	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==MOUSEMOTION:					  #监控鼠标移动
				if pause_rect.collidepoint(event.pos):
					pause_image=resume_pressed
				else:
					pause_image=resume_nor
					me.rect.centerx,me.rect.centery=event.pos #将鼠标当前位置赋予我方飞机中心	
			elif event.type==MOUSEBUTTONDOWN:
				if event.button==1 :
					if pause_rect.collidepoint(event.pos):
						pause=not pause
					elif again_rect.collidepoint(event.pos):
						main()
					elif gameover_image_rect.collidepoint(event.pos):
						pygame.quit()
						sys.exit()
				if event.button==3:
					if bomb_num >0:
						bomb_num-=1
						bomb_sound.play()
						for e in all_enemy:
						 	if e.rect.bottom>0:
						 		e.death=True
			elif event.type==KEYDOWN:
				if event.key==K_SPACE:
					pause=not pause
			elif event.type==SUPPLYTIME:
				supply_sound.play()
				if choice([True,False]):
					bomb_supply.activate=True
				else:
					bullet_supply.activate=True
			elif event.type==INVINCIBLETIME:
				me.invincible=False
				pygame.time.set_timer(INVINCIBLETIME,0)

		screen.blit(background,(0,0))#绘制背景图
		if not gameover:
			score_text=score_font.render('score:%s' %str(score),True,WHITE)#获取得分
			screen.blit(score_text,(10,5))#绘制分数
			screen.blit(bomb_image,(10,620))#绘制炸弹图片
			bomb_text=bomb_font.render('X %d' %bomb_num,True,WHITE)
			screen.blit(bomb_text,(80,625))

			for l in range(me.life):
				screen.blit(life_image,(480-10 - (l+1)*life_rect.width,700-10-life_rect.height))
			#难度设置
			if score//50-add_s and add_s<=15:#每50分增加一个小飞机，上限25个
					add_s+=1
					add_small_enemies(all_enemy,small_enemy,1)
			if score//150-add_m and add_m<=10:
					add_m+=1
					add_mid_enemies(all_enemy,mid_enemy,1)
			if score//400-add_b and add_b<=4:
					add_b+=1
					add_big_enemies(all_enemy,big_enemy,1)  
			if score//500-speed_lv:#每500分加速
				speed_lv+=1
				for x in all_enemy:
					x.speed[1]+=1
			if not pause:
				
				pygame.mixer.music.unpause()
				pygame.mixer.unpause()
				# pause_rect.left,pause_rect.top=(400,10)
				# screen.blit(pause_image,pause_rect)

				if bomb_supply.activate:#绘制补给
					bomb_supply.move()
					screen.blit(bomb_supply.image,bomb_supply.rect)
					if pygame.sprite.collide_mask(me,bomb_supply):
						get_bomb_sound.play()
						if bomb_num<3:
							bomb_num+=1
						bomb_supply.reset()
				if bullet_supply.activate:#绘制补给
					bullet_supply.move()
					screen.blit(bullet_supply.image,bullet_supply.rect)
					if pygame.sprite.collide_mask(me,bullet_supply):
						get_bullet_sound.play()
						bullet_supply.reset()
						supperbullet=True
				if not delay%10:#每10帧发射一颗子弹
					bullet_sound.play()
					if supperbullet:
						bullet2[bullet2_index].reset((me.rect.centerx-10,me.rect.top))
						bullet2[bullet2_index+1].reset((me.rect.centerx+10,me.rect.top))
						bullet2_index=(bullet2_index+2)%10
						bullets=bullet2
					else:
						bullet1[bullet1_index].reset(me.rect.midtop)
						bullet1_index=(bullet1_index+1)%5
						bullets=bullet1
				for b in bullets:#子弹移动
					if not b.death:
						b.move()
						screen.blit(b.image,b.rect)
						bullet_down=pygame.sprite.spritecollide(b,all_enemy, False, pygame.sprite.collide_mask) #检测子弹是否击中敌机
						if bullet_down:
							b.death=True
							for de in bullet_down:
								if de in big_enemy :#命中大飞机或中飞机
									de.hp-=1	#飞机HP-1  		  
									de.hit=True	  			  #将飞机图片改为受攻击
									if de.hp<=0:#hp归0飞机状态改为死亡
										de.death=True
										all_enemy.remove(de)#被击落的飞机从检测组中移除不再进行检测
								if de in mid_enemy:
									de.hp-=1	#飞机HP-1  		  
									de.hit=True	  			  #将飞机图片改为受攻击
									if de.hp<=0:#hp归0飞机状态改为死亡
										de.death=True
										all_enemy.remove(de)		  
								if de in small_enemy:#命中小飞机
									de.death=True
									all_enemy.remove(de)	
				for be in big_enemy:
					if not be.death:#未被击落
						be.move()
						if be.rect.bottom == -50:#在顶端上方50像素开始播放出场声音
							be.enemy3_fly_sound.play(-1)
						if be.hit:#被击中
							screen.blit(be.image_hit,be.rect)
							be.hit=False
						else:
							if switch_image:#未被击中每5帧切换图片
								screen.blit(be.image2,be.rect)
							else:
								screen.blit(be.image1,be.rect)
					else:
						if not delay%3:#被击落，每3帧绘制一次击落图片，并切换图片
							if be.deathindex==0:
								enemy3_down_sound.play()
							screen.blit(be.destory_images[be.deathindex],be.rect)
							be.deathindex=(be.deathindex+1)%6
							if be.deathindex==0:
								be.enemy3_fly_sound.stop()
								be.reset()
								all_enemy.add(be)
								score+=10
					#绘制血条
					pygame.draw.line(screen,BLACK, (be.rect.left, be.rect.top - 5),(be.rect.right, be.rect.top - 5), 2)
					hp_remain = be.hp/20
					if hp_remain > 0.2:
						hp_color = GREEN
					else:
						hp_color = RED
					pygame.draw.line(screen, hp_color,(be.rect.left, be.rect.top -5),(be.rect.left + be.rect.width * hp_remain, be.rect.top - 5), 2)
								
				for mide in mid_enemy:#绘制中飞机
					if not mide.death:
						mide.move()
						if mide.hit:
							screen.blit(mide.image_hit,mide.rect)
							mide.hit=False
						else:
							screen.blit(mide.image,mide.rect)
					else:
						if not delay%3:
							if mide.deathindex==0:
								enemy2_down_sound.play()
							screen.blit(mide.destory_images[mide.deathindex],mide.rect)	
							mide.deathindex=(mide.deathindex+1)%4	
							if mide.deathindex==0:
								mide.reset()
								score+=3
								all_enemy.add(mide)
					pygame.draw.line(screen,BLACK, (mide.rect.left, mide.rect.top - 5),(mide.rect.right, mide.rect.top - 5), 2)
					hp_remain = mide.hp/8
					if hp_remain > 0.2:
						hp_color = GREEN
					else:
						hp_color = RED
					pygame.draw.line(screen, hp_color,(mide.rect.left, mide.rect.top -5),(mide.rect.left + mide.rect.width * hp_remain, mide.rect.top - 5), 2)
				
				for se in small_enemy:#绘制小飞机
					if not se.death:
						se.move()
						screen.blit(se.image,se.rect)
					else:
						if not delay%3:
							if se.deathindex==0:
								enemy1_down_sound.play()
							screen.blit(se.destory_images[se.deathindex],se.rect)
							se.deathindex=(se.deathindex+1)%4
							if se.deathindex==0:
								se.reset()
								score+=1
								all_enemy.add(se)
				enemy_down=pygame.sprite.spritecollide(me,all_enemy, False, pygame.sprite.collide_mask)
				if enemy_down and not me.invincible:
					me.death=True
					me_down_sound.play()
					for e in enemy_down:
						e.death=True
				if not me.death:
					if switch_image:#未被撞击绘制我方飞机,每5帧切换图
						screen.blit(me.image1,me.rect)
					else:
						screen.blit(me.image2,me.rect)
				else:
					if me.life>1:
						if not delay%3:
							me.deathindex=(me.deathindex+1)%4
							screen.blit(me.destory_images[me.deathindex],me.rect)
							if me.deathindex==0:
								me.reset()
								supperbullet=False
								pygame.time.set_timer(INVINCIBLETIME,3*1000)
					else:
						gameover=True
			else:
				pause_rect.centerx,pause_rect.centery=235,350
				screen.blit(pause_image,pause_rect)
				pygame.mixer.music.pause()
				pygame.mixer.pause()
				pygame.time.set_timer(SUPPLYTIME,0)

			delay-=1
			if not(delay % 5):
				switch_image = not switch_image
			if not delay:
				delay=100
		else:
			pygame.mixer.music.pause()
			pygame.mixer.pause()
			pygame.time.set_timer(SUPPLYTIME,0)

			if score>best_score:
				with open("record.txt","w") as f:
					f.write(str(score))
				best_score_text=score_font.render("BEST SCORE:%s"%score,True,WHITE)
			gameover_text1=gameover_font1.render("YOUR SCORE:%s"%str(score),True,WHITE)
			gameover_text1_rect=gameover_text1.get_rect()
			gameover_text1_rect.centerx,gameover_text1_rect.centery=240,300
			screen.blit(best_score_text,best_score_rect)
			screen.blit(gameover_text1,gameover_text1_rect)
			screen.blit(gameover_text2,gameover_text2_rect)
			screen.blit(again_image,again_rect) 
			screen.blit(gameover_image,gameover_image_rect)
		pygame.display.flip()
		clock.tick(60)
if __name__ == '__main__':
	try:
		main()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()
		input()
    

