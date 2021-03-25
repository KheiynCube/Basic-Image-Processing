import os
import cv2
import numpy as np

# get image
def load_image(index):
	image_path = os.path.join(root, 'images', files[index])
	image = cv2.imread(image_path)
	image = cv2.resize(image, (h, w))
	return  image

def update_contour(image):
	global contours, points, position

	# convert to gray scale image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# get threshold
	ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

	# get contour
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

	# get all border in list of points
	points = []
	for a in range(len(contours)):
		for b in range(len(contours[a])):
			for c in range(len(contours[a][b])):
				points.append(contours[a][b][c])

	# reset position
	position = 0

def play():
	global canvas, position, is_play

	# response depend on action
	if actions[0] == 'dilate':
		color = (255, 255, 255)
		length = patch_size // 2
	elif actions[0] == 'erode':
		color = (0, 0, 0)
		length = patch_size // 2 - 1
	
	# manipulate pixels patch at specific poisition
	if position == 0:
		position += 1
	elif 0 < position < len(points):
		x1 = points[position-1][0] - length
		y1 = points[position-1][1] - length
		x2 = points[position-1][0] + length
		y2 = points[position-1][1] + length
		cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
		position += 1
	elif position == len(points):
		actions.pop(0)
		if len(actions) == 0:
			is_play = False
		else:
			update_contour(canvas)

def display(image):
	
	if len(actions) > 0:

		# response depend on action
		if actions[0] == 'dilate':
			color = (0, 255, 0)
			length = patch_size // 2
		elif actions[0] == 'erode':
			color = (0, 0, 255)
			length = patch_size // 2 - 1

		# display patch square
		if position < len(points):
			x1 = points[position][0] - length
			y1 = points[position][1] - length
			x2 = points[position][0] + length
			y2 = points[position][1] + length
			cv2.rectangle(image, (x1, y1), (x2, y2), color, -1)
	if is_border:
		cv2.drawContours(image, contours, -1, (255, 0, 0), 1)
	image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation = cv2.INTER_AREA)
	cv2.imshow('display', image)

if __name__ == '__main__':

	# root directory
	root = os.path.dirname(os.path.abspath(__file__))
	files = ['circle.png', 'window.png', 'sky.png', 'butterfly.png', 'board.png', 'deathlyhallows.png',  'text.png']
	modes = [['erode'], ['dilate'], ['erode', 'dilate'], ['dilate', 'erode']]
	total = len(files)

	# parameter
	h, w = 500, 500,
	scale = 2
	index, view = 0, 0
	patch_size = 8
	is_border = True
	is_play = False
	actions = modes[view].copy()
	canvas = load_image(index)
	update_contour(canvas)

	while True:

		# animation
		if is_play and len(actions) > 0: play()

		# display
		display(canvas.copy())

		# user feedback
		key = cv2.waitKeyEx(1)
		if key in [ord('q'), 27]:
			break
		elif key in [ord('a'), 2424832]:
			index = max(index - 1, 0)
			is_play = False
			actions = modes[view].copy()
			canvas = load_image(index)
			update_contour(canvas)
		elif key in [ord('d'), 2555904]:
			index = min(index + 1, total - 1)
			is_play = False
			actions = modes[view].copy()
			canvas = load_image(index)
			actions = modes[view].copy()
			update_contour(canvas)
		elif key in [ord('w'), 2490368]:
			view = max(view - 1, 0)
			is_play = False
			actions = modes[view].copy()
			update_contour(canvas)
		elif key in [ord('s'), 2621440]:
			view = min(view + 1, 4 - 1)
			is_play = False
			actions = modes[view].copy()
			update_contour(canvas)
		elif key in [ord(' ')]:
			is_play = not is_play
		elif key in [ord('b')]:
			is_border = not is_border
		if key in [ord('z')]:
			print('modes', modes)
			print('actions', actions)
