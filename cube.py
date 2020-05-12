import pygame
from random import *

class Cube(pygame.sprite.Sprite):
	cube_shapes = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
	cube_colors = [
	(0xcc, 0x99, 0x99), (0xff, 0xff, 0x99), (0x66, 0x66, 0x99),
	(0x99, 0x00, 0x66), (0xff, 0xcc, 0x00), (0xcc, 0x00, 0x33),
	(0xff, 0x00, 0x33), (0x00, 0x66, 0x99), (0xff, 0xff, 0x33),
	(0x99, 0x00, 0x33), (0xcc, 0xff, 0x66), (0xff, 0x99, 0x00)
	]
	# 不同方块对应的形态, (0,0)为中心块, 前面代表行位置(向左减一，向右加一),后面代表列位置(向上减一,向下加一), 列表长度代表形态个数, (,)个数代表方块个数
	I = [[(0, -1), (0, 0), (0, 1), (0, 2)],
		 [(-1, 0), (0, 0), (1, 0), (2, 0)]]
	J = [[(-2, 0), (-1, 0), (0, 0), (0, -1)],
		 [(-1, 0), (0, 0), (0, 1), (0, 2)],
		 [(0, 1), (0, 0), (1, 0), (2, 0)],
		 [(0, -2), (0, -1), (0, 0), (1, 0)]]
	L = [[(-2, 0), (-1, 0), (0, 0), (0, 1)],
		 [(1, 0), (0, 0), (0, 1), (0, 2)],
		 [(0, -1), (0, 0), (1, 0), (2, 0)],
		 [(0, -2), (0, -1), (0, 0), (-1, 0)]]
	O = [[(0, 0), (0, 1), (1, 0), (1, 1)]]
	S = [[(-1, 0), (0, 0), (0, 1), (1, 1)],
		 [(1, -1), (1, 0), (0, 0), (0, 1)]]
	T = [[(0, -1), (0, 0), (0, 1), (-1, 0)],
		 [(-1, 0), (0, 0), (1, 0), (0, 1)],
		 [(0, -1), (0, 0), (0, 1), (1, 0)],
		 [(-1, 0), (0, 0), (1, 0), (0, -1)]]
	Z = [[(0, -1), (0, 0), (1, 0), (1, 1)],
		 [(-1, 0), (0, 0), (0, -1), (1, -1)]]
	#cube形态索引
	cube_form = {
		'I': I, 'J': J, 'L': L, 'O': O, 'S': S, 'T': T, 'Z': Z
	}

	def __init__(self, G_w_num = (400 // 25)):
		super().__init__()
		# cube类型
		self.shape = self.cube_shapes[randint(0, len(self.cube_shapes) - 1)]
		self.form = randint(0, len(self.cube_form[self.shape]) - 1)
		# cube颜色
		self.color = self.cube_colors[randint(0, len(self.cube_colors) - 1)]
		# cube中心位置, 
		self.center = (G_w_num // 2 - 1, 2)
		# self.matrix = matrix

	# 计算cube在左边网格中的位置
	def get_pos1(self, center = None):
		cube_cur = self.cube_form[self.shape][self.form]
		if center is None:
			center = self.center

		return [(cube[0] + center[0], cube[1] + center[1]) for cube in cube_cur]
	# 计算cube在右边预览处的位置
	def get_pos2(self, center = (19.5, 4)):
		cube_cur = self.cube_form[self.shape][self.form]
		
		return [(cube[0] + center[0], cube[1] + center[1]) for cube in cube_cur]

	# 边缘检测
	def conflict(self, center, matrix):
		for cube in self.get_pos1(center):
			# 超出屏幕之外,说明不合法
			if cube[0] < 0 or cube[1] < 0 or cube[0] >= 16 or cube[1] >= 24:
				return True
			# 不为None，说明之前已经有小方块存在了，也不合法
			if matrix[cube[1]][cube[0]]:
				 return True
		return False	

	def draw_in_left(self, screen):
		for cube in self.get_pos1():
			pygame.draw.rect(screen, self.color, (cube[0] * 25, cube[1] * 25, 25, 25))
			pygame.draw.rect(screen, (200, 200, 200), (cube[0] * 25, cube[1] * 25, 25, 25), 2)

	def draw_in_right(self, screen):
		for cube in self.get_pos2():
			pygame.draw.rect(screen, self.color, (cube[0] * 25, cube[1] * 25, 25, 25))
			pygame.draw.rect(screen, (200, 200, 200), (cube[0] * 25, cube[1] * 25, 25, 25), 2)

	def moveLeft(self, matrix):
		center = (self.center[0] - 1, self.center[1])
		if not self.conflict(center, matrix):
			self.center = center

	def moveRight(self, matrix):
		center = (self.center[0] + 1, self.center[1])
		if not self.conflict(center, matrix):
			self.center = center

	def moveDown(self, matrix):
		center = (self.center[0], self.center[1] + 1)
		if not self.conflict(center, matrix):
			self.center = center
			return True
		else:
			return False

	def rotate(self, matrix):
		new_form = (self.form + 1) % len(self.cube_form[self.shape])
		old_form = self.form
		self.form = new_form
		if self.conflict(self.center, matrix):
			self.form = old_form