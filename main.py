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
pygame.display.set_caption("俄罗斯方块")
font = pygame.font.SysFont("impact", 24)
FPS = 30

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
	new_matrix = []
	full_number = 0
	for i in matrix:
		if any(i) is None:
			new_matrix.append(matrix)
		else:
			score += 100
	new_matrix = [[None] * G_w_num for i in range(G_h_num - len(new_matrix))].extend(new_matrix)

	return new_matrix, score

def main():
	pygame.mixer.music.play(-1)
	clock = pygame.time.Clock()
	# 使用矩阵记录方格是否为空
	matrix = [[None] * G_w_num for i in range(G_h_num)]

	# 分数
	score = 0

	live_cube = cube.Cube()
	next_cube = cube.Cube()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key in [K_LEFT, K_a]:
					live_cube.moveLeft(matrix)
				elif event.key in [K_RIGHT, K_d]:
					live_cube.moveRight(matrix)
				elif event.key in [K_RIGHT, K_d]:
					live_cube.moveRight(matrix)
				# elif event.key in [K_DOWN, K_s]:
				# 	live_cube.moveDown()
				elif event.key in [K_UP, K_w]:
					live_cube.rotate(matrix)
				elif event.key == K_SPACE:
					live_cube.moveDown()
				elif event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()

		keys = pygame.key.get_pressed()
		if keys[K_DOWN] or keys[K_s]:
			live_cube.moveDown(matrix)

		matrix, score = clear_full(matrix, score)

		screen.fill(BLACK)
		draw_grid()
		live_cube.draw_in_left(screen)
		next_cube.draw_in_right(screen)
		pygame.display.update()
		clock.tick(FPS)

if __name__ == "__main__":
	main()
