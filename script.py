import numpy as np
import cv2


def rgb_images(image):
	red = np.zeros(image.shape[:2] , np.uint8)
	green = np.zeros(image.shape[:2] , np.uint8)
	blue = np.zeros(image.shape[:2] , np.uint8)
	for line in xrange(0 , image.shape[0]):
		for col in xrange(0,image.shape[1]):
			red.itemset((line , col) , image.item(line , col , 2))
			green.itemset((line , col) , image.item(line , col , 1))
			blue.itemset((line , col) , image.item(line , col , 0))
	return red , green , blue


image_path = "images/10_cents.JPG"
image = cv2.imread(image_path)
red , green , blue = rgb_images(image)


cv2.imshow('image' , image)
cv2.imshow('red' , red)
cv2.imshow('green' , green)
cv2.imshow('blue' , blue)
cv2.waitKey(0)
