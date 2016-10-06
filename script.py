import numpy as np
import cv2


def flood(image , value = 0 , single_seed = None):
	height , width = image.shape[:2]
	floodfill_image = image.copy()                                                          #cria uma copia da imagem recebida para que a mesma nao seja alterada, uma vez que a funcao cv2.floodFill() altera a imagem recebida como parametro ao inves de retornar uma nova imagem com o filtro aplicado
	mask = np.zeros((height + 2 , width + 2) , np.uint8)                          #cria a mascara exigida pela funcao cv2.floodFill()                      
	if single_seed == None:                                                                 #coloca sementes nas extremidades da imagem
		seeds = []                                                                          #lista com todas as sementes
		for x in xrange(0 , width , 5):                                                #definindo as coordenadas das sementes 
			seeds.append(tuple([0 , x]))
			seeds.append(tuple([height - 5 , x]))
			seeds.append(tuple([x , 0]))
			seeds.append(tuple([x , width - 5]))
		for seed in seeds:
			cv2.floodFill(floodfill_image , mask , seed , value , loDiff = 2 , upDiff = 2)  #aplica a funcao cv2.floodFill() para cada semente criada
	else:
		seed = single_seed
		cv2.floodFill(floodfill_image , mask , seed , value , loDiff = 2 , upDiff = 2)
	white = 0 
	for x in xrange(0,image.shape[0]):                                                      #verifica o numero de px com o valor 255 (branco) apos a aplicacao da funcao cv2.floodFill(), usado futuramente para verificar se houve um erro ou nao 
		for y in xrange(0,image.shape[1]):
			if floodfill_image.item(x,y) == 255:
				white += 1
	if white > ((image.shape[0] * image.shape[1] * 80) / 100):                              #verifica se mais de 80% da imagem ficou branca, o que claramente indica um erro tendo em vista que nenhuma celula ocupa esse tamanho na imagem, caso isso seja verdade invertese a imagem 
		floodfill_image = cv2.bitwise_not(floodfill_image)
	return floodfill_image




image_path = "images/1_real_2.JPG"
image = cv2.imread(image_path)
resized_image = cv2.resize(image, (300, 300))
hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
hue , saturation , value = cv2.split(hsv_image)
blur_saturation = cv2.blur(saturation , (3,3))
binary_saturation = cv2.threshold(blur_saturation , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
binary_hue = cv2.threshold(hue , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
flooded_saturation = flood(binary_saturation , value = 255)
flooded_hue = flood(binary_hue , value = 255)
combined_image = cv2.bitwise_or(flooded_saturation , flooded_hue)
cv2.imshow('combined_image' , combined_image)
cv2.waitKey(0)
