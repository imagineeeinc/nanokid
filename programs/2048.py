# A 2048 game, use the thumbstick to move the blocks
# Logic from https://www.geeksforgeeks.org/2048-game-in-python/
# CHangwe to root varibale to change the location of the bitmaps (if loading from sd, make sure to init)
root = "cyclone/2048"

import random, time

import displayio, terminalio
from adafruit_display_text import Label

from thunder.display import Display
import thunder.input as controls

display = Display()
screen = display.screen

def start_game():
	mat =[]
	for i in range(4):
		mat.append([0] * 4)
	add_new_2(mat)
	return mat
def add_new_2(mat):
	r = random.randint(0, 3)
	c = random.randint(0, 3)

	while(mat[r][c] != 0):
		r = random.randint(0, 3)
		c = random.randint(0, 3)

	mat[r][c] = 2

# Status: 0 - Game not over, 1 - Win, 2 - Game over
def get_current_state(mat):
	for i in range(4):
		for j in range(4):
			if(mat[i][j]== 4096):
				return 1

	for i in range(4):
		for j in range(4):
			if(mat[i][j]== 0):
				return 0

	for i in range(3):
		for j in range(3):
			if(mat[i][j]== mat[i + 1][j] or mat[i][j]== mat[i][j + 1]):
				return 0

	for j in range(3):
		if(mat[3][j]== mat[3][j + 1]):
			return 0

	for i in range(3):
		if(mat[i][3]== mat[i + 1][3]):
			return 0

	return 2
def compress(mat):
	changed = False
	new_mat = []
	for i in range(4):
		new_mat.append([0] * 4)

	for i in range(4):
		pos = 0
		for j in range(4):
			if(mat[i][j] != 0):
				new_mat[i][pos] = mat[i][j]
				if(j != pos):
					changed = True
				pos += 1
	return new_mat, changed

def merge(mat):
	changed = False
	for i in range(4):
		for j in range(3):
			if(mat[i][j] == mat[i][j + 1] and mat[i][j] != 0):
				mat[i][j] = mat[i][j] * 2
				mat[i][j + 1] = 0
				changed = True

	return mat, changed
def reverse(mat):
	new_mat =[]
	for i in range(4):
		new_mat.append([])
		for j in range(4):
			new_mat[i].append(mat[i][3 - j])
	return new_mat

def transpose(mat):
	new_mat = []
	for i in range(4):
		new_mat.append([])
		for j in range(4):
			new_mat[i].append(mat[j][i])
	return new_mat

def move_left(grid):
	new_grid, changed1 = compress(grid)
	new_grid, changed2 = merge(new_grid)
	changed = changed1 or changed2
	new_grid, temp = compress(new_grid)
	return new_grid, changed

def move_right(grid):
	new_grid = reverse(grid)
	new_grid, changed = move_left(new_grid)
	new_grid = reverse(new_grid)
	return new_grid, changed
def move_up(grid):
	new_grid = transpose(grid)
	new_grid, changed = move_left(new_grid)
	new_grid = transpose(new_grid)
	return new_grid, changed
def move_down(grid):
	new_grid = transpose(grid)
	new_grid, changed = move_right(new_grid)
	new_grid = transpose(new_grid)
	return new_grid, changed

# Init
mat = start_game()
sensitivity = 0.8

blocks = {
	0: displayio.Bitmap(50,50,1),
  2: displayio.OnDiskBitmap(root+"/2.bmp"),
  4: displayio.OnDiskBitmap(root+"/4.bmp"),
  8: displayio.OnDiskBitmap(root+"/8.bmp"),
  16: displayio.OnDiskBitmap(root+"/16.bmp"),
	32: displayio.OnDiskBitmap(root+"/32.bmp"),
	64: displayio.OnDiskBitmap(root+"/64.bmp"),
	128: displayio.OnDiskBitmap(root+"/128.bmp"),
	256: displayio.OnDiskBitmap(root+"/256.bmp"),
	512: displayio.OnDiskBitmap(root+"/512.bmp"),
	1024: displayio.OnDiskBitmap(root+"/1024.bmp"),
	2048: displayio.OnDiskBitmap(root+"/2048.bmp"),
	4096: displayio.OnDiskBitmap(root+"/4096.bmp"),
}
grid = [
	[
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*0, y=60*0),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*1, y=60*0),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*2, y=60*0),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*3, y=60*0)
	],
	[
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*0, y=60*1),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*1, y=60*1),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*2, y=60*1),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*3, y=60*1)
	],
	[
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*0, y=60*2),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*1, y=60*2),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*2, y=60*2),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*3, y=60*2)
	],
	[
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*0, y=60*3),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*1, y=60*3),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*2, y=60*3),
		displayio.TileGrid(blocks[0], pixel_shader=blocks[2].pixel_shader, x=60*3, y=60*3)
	]
]
for row in grid:
	for tile in row:
		screen.append(tile)
for i in range(4):
			row = mat[i]
			for j in range(4):
				tile = row[j]
				grid[i][j].bitmap = blocks[tile]
while(True):
	flag = False
	if controls.get_axis(controls.y_axis) < -sensitivity:
		mat, flag = move_up(mat)

		status = get_current_state(mat)
		if(status == 0):
			add_new_2(mat)
		else:
			break
	elif controls.get_axis(controls.y_axis) > sensitivity:
		mat, flag = move_down(mat)
		status = get_current_state(mat)
		if(status == 0):
			add_new_2(mat)
		else:
			break
	elif controls.get_axis(controls.x_axis) < -sensitivity:
		mat, flag = move_left(mat)
		status = get_current_state(mat)
		if(status == 0):
			add_new_2(mat)
		else:
			break
	elif controls.get_axis(controls.x_axis) > sensitivity:
		mat, flag = move_right(mat)
		status = get_current_state(mat)
		if(status == 0):
			add_new_2(mat)
		else:
			break
	if (flag == True):
		for i in range(4):
			row = mat[i]
			for j in range(4):
				tile = row[j]
				grid[i][j].bitmap = blocks[tile]
		time.sleep(0.1)
while True:
	if controls.get_btn(controls.btnb):
		break