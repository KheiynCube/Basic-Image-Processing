import os
import cv2
import numpy as np
import colorama
from colorama import Fore

def concat(canvas, graph_h, graph_v):
	board = np.zeros([height+ay, width+ay, 3], np.uint8)
	board[:height, :width] = canvas
	board[height:, :width] = cv2.flip(graph_h, 0)
	board[:height, width:] = cv2.flip(cv2.rotate(graph_v, cv2.cv2.ROTATE_90_CLOCKWISE), 1)
	cv2.rectangle(board, (0, 0), (width, height), (127, 127, 127), 3)
	return board

def draw(img):
	if modes[view] in ['horizontal', 'both']:
		cv2.line(img, (0, mouse[1]), (width, mouse[1]), (255, 0, 255), 1)
	if modes[view] in ['vertical', 'both']:
		cv2.line(img, (mouse[0], 0), (mouse[0], height), (255, 0, 255), 1)
	return img

def plot(axis, p):
	if axis == 'horizontal':
		data = image[p,:,:]
		ax = width
	elif axis == 'vertical':
		data = image[:,p,:]
		ax = height
	graph = np.zeros([ay, ax, 3], np.uint8)
	if modes[view] in [axis, 'both']:
		for c in range(3):
			for x in range(ax):
				i = int(data[x, c]/255*ay*0.9)
				graph[0:i,x,c] = 255
		return graph
	else:
		return graph

def display(image):
	cv2.imshow('display', image)

def mouse_event(event, x, y, flags, param):
	global mouse

	# update cursor position
	if event == cv2.EVENT_MOUSEMOVE:
		mouse = (x,y)
		if y < height and x < width:
			graph_h = plot('horizontal', mouse[1])
			graph_v = plot('vertical', mouse[0])
			canvas = draw(image.copy())
			display(concat(canvas, graph_h, graph_v))

			b, g, r = image[y, x]
			text = Fore.WHITE
			text += '   X:%4d'%x
			text += '   Y:%4d'%y
			text += Fore.RED + '   R:%4d'%r
			text += Fore.GREEN + '   G:%4d'%g
			text += Fore.BLUE + '   B:%4d'%b
			print(text)

if __name__ == '__main__':

	# root directory
	root = os.path.dirname(os.path.abspath(__file__))
	files = ['sphere.png', 'rainbow.jpg', 'shape.png', 'abdomen.jpg', 'chest.jpg']
	modes = ['horizontal', 'vertical', 'both']
	total = len(files)

	# parameter
	mouse = (0, 0)
	ay = 100
	default_length = 460
	index, view = 0, 0

	# enable color in window command shell
	colorama.init()

	while True:

		# load image + info
		image_path = os.path.join(root, 'images', files[index])
		image = cv2.imread(image_path)

		# resize window
		height, width, _ = image.shape
		length = max(height, width)
		scale = default_length/length
		image = cv2.resize(image, (0, 0), fx=scale, fy=scale)
		height, width, _ = image.shape

		# process
		graph_h = plot('horizontal', mouse[1])
		graph_v = plot('vertical', mouse[0])
		canvas = draw(image.copy())

		# display
		display(concat(canvas, graph_h, graph_v))

		# user feedback
		cv2.setMouseCallback('display', mouse_event)
		key = cv2.waitKeyEx(0)
		if key in [ord('q'), 27]:
			break
		elif key in [ord('a'), 2424832]:
			index = max(index - 1, 0)
		elif key in [ord('d'), 2555904]:
			index = min(index + 1, total - 1)
		elif key in [ord('w'), 2490368]:
			view = max(view - 1, 0)
		elif key in [ord('s'), 2621440]:
			view = min(view + 1, len(modes) - 1)