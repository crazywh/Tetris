import pygame, sys, os
from pygame.locals import *
from random import randint

import cube

# 设置窗口打开位置
os.environ['SDL_VIDEO_WINDOW_POS'] = "400, 100"

# 初始化
pygame.init()
pygame.mixer.init()
size = w, h = 600, 600
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("俄罗斯方块 Q:控制音乐; 空格：快速下落; 鼠标点击暂停; E改变落地颜色")
font = pygame.font.SysFont("impact", 24)
FPS = 30
running = False
# 格子大小
G_SIZE = 25
G_w_num = (w - 200) // 25
G_h_num = h // 25

# 加载音乐
pygame.mixer.music.load('sound/bg.mp3')
pygame.mixer.music.set_volume(0.5)

# 颜色
WHITE1 = (255, 255, 255)
WHITE2 = (75, 75, 75)
BLACK = (0, 0, 0)
BULE = (0, 0, 180)

#文字绘制
def print_text(font, x, y, text, color = WHITE1):
	ti = font.render(text, True, color)
	screen.blit(ti, (x, y))

# 绘制网格
def draw_grid():
	for i in range((w - 200) // G_SIZE):
		pygame.draw.line(screen, WHITE2, (i * G_SIZE, 0), (i * G_SIZE, 600), 1)
	for i in range(h // G_SIZE):
		pygame.draw.line(screen, WHITE2, (0, i * G_SIZE), (400, i * G_SIZE), 1)
	pygame.draw.line(screen, WHITE1, (400, 0), (400, 600), 2)

def clear_full(matrix, score):
	extra_matrix = []
	full_number = 0
	for i in matrix:
		if None in i:
			extra_matrix.append(i)
		else:
			score += 100
	new_matrix = [[None] * G_w_num for i in range(G_h_num - len(extra_matrix))]
	new_matrix.extend(extra_matrix)

	return new_matrix, score

def draw_matrix(matrix, c):
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			# print(matrix[i][j])
			if matrix[i][j]:
				if c:
					pygame.draw.rect(screen, matrix[i][j], (j * 25, i * 25, 25, 25))
				else:
					pygame.draw.rect(screen, BULE, (j * 25, i * 25, 25, 25))
				pygame.draw.rect(screen, WHITE1, (j * 25, i * 25, 25, 25), 2)

def draw_gameover():
	print_text(font, 275, 300, "Game Over!!")
	print_text(font, 250, 350, "Press R To Restart")


def main():
	global running
	clock = pygame.time.Clock()
	# 使用矩阵记录方格是否为空
	matrix = [[None] * G_w_num for i in range(G_h_num)]
	# 分数
	score = 0
	level = 1
	# 停止标志
	gameover = False
	pause = False
	# 颜色标志
	c = True
	# 音乐控制
	sound = True
	# 下降延迟辅助
	delay = 0
	live_cube = cube.Cube()
	next_cube = cube.Cube()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN and not gameover and running:
				if event.key in [K_LEFT, K_a]:
					live_cube.moveLeft(matrix)
				elif event.key in [K_RIGHT, K_d]:
					live_cube.moveRight(matrix)
				elif event.key in [K_RIGHT, K_d]:
					live_cube.moveRight(matrix)
				elif event.key in [K_UP, K_w]:
					live_cube.rotate(matrix)
				elif event.key == K_SPACE:
					while live_cube.moveDown(matrix):
						pass
				elif event.key == K_q:
					sound = not sound
				elif event.key == K_e:
					c = not c
				elif event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			elif event.type == MOUSEBUTTONDOWN and running:
				pause = not pause
			elif event.type == KEYDOWN and not running:
				running = True
				pygame.mixer.music.play(-1)

		if not pause and running:
			keys = pygame.key.get_pressed()
			if (keys[K_DOWN] or keys[K_s]) and not gameover:
				live_cube.moveDown(matrix)
			elif keys[K_r] and gameover:
				pygame.mixer.music.play(-1)
				main()
			if not gameover and delay % (FPS // level) == 0:
				# 音乐控制
				if sound:
					pygame.mixer.music.unpause()
				else:
					pygame.mixer.music.pause()
				
				if not live_cube.moveDown(matrix):
					for grid in live_cube.get_pos1():
						matrix[grid[1]][grid[0]] = live_cube.color
					live_cube = next_cube
					next_cube = cube.Cube()
					# 更新新的cube出现冲突，则游戏结束
					if live_cube.conflict(live_cube.center, matrix):
						gameover = True
						live_cube = None
						pygame.mixer.music.stop()

		matrix, score = clear_full(matrix, score)
		delay += 1
		level = score // 2000 + 1
		screen.fill(BLACK)
		draw_grid()
		if not gameover:
			live_cube.draw_in_left(screen)
		else:
			draw_gameover()
		if pause:
			print_text(font, 475, 400, "Pause")
		
		if not running:
			print_text(font, 200, 300, "Press Any Key To Start !")

		print_text(font, 475, 200, "level: " + str(level))
		print_text(font, 470, 250, "score: " + str(score))
		next_cube.draw_in_right(screen)
		draw_matrix(matrix, c)

		pygame.display.update()
		clock.tick(FPS)

if __name__ == "__main__":
	main()