import numpy as np
import cv2


def flood(image , value = 0 , single_seed = None):
	#aplica o filtro flood_fill
	height , width = image.shape[:2]
	floodfill_image = image.copy()                                                          #cria uma copia da imagem recebida para que a mesma nao seja alterada, uma vez que a funcao cv2.floodFill() altera a imagem recebida como parametro ao inves de retornar uma nova imagem com o filtro aplicado
	mask = np.zeros((height + 2 , width + 2) , np.uint8)                          #cria a mascara exigida pela funcao cv2.floodFill()                      
	if single_seed == None:                                                                 #coloca sementes nas extremidades da imagem
		seeds = []                                                                          #lista com todas as sementes
		if width == height:      
			for x in xrange(0 , width , 5):                                                #definindo as coordenadas das sementes 
				seeds.append(tuple([0 , x]))
				seeds.append(tuple([height - 5 , x]))
				seeds.append(tuple([x , 0]))
				seeds.append(tuple([x , width - 5]))
		else:
			limit = 0
			if width > height:
				limit = height
			else:
				limit = width
			for x in xrange(0 , limit , 5):
				seeds.append(tuple([0 , x]))
				seeds.append(tuple([width - 5 , x]))
				seeds.append(tuple([x , 0]))
				seeds.append(tuple([x , height - 5]))	
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


def binary_coin(image): 
	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   #converte imagem para padrao de cores HSV
	hue , saturation , value = cv2.split(hsv_image)      #extrai os canais H S e V
	blur_saturation = cv2.blur(saturation , (3,3))       #borra a saturacao
	binary_saturation = cv2.threshold(blur_saturation , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  #aplica a tecnica de OTSU para binarizar a imagem com a saturacao borrada
	binary_hue = cv2.threshold(hue , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]                     #aplica a tecnica de OTSU para binarizar a imagem referente a matiz    
	flooded_saturation = flood(binary_saturation , value = 255)                                            #aplica o filtro floodFill para remover a caixa
	flooded_hue = flood(binary_hue , value = 255)                                                          #aplica o filtro floodFill para remover a caixa
	combined_image = cv2.bitwise_or(flooded_saturation , flooded_hue)                                      #combina as imagens utilizando a logica OR para obter apenas as moedas
	#cv2.imshow('combined_image' , combined_image)
	#cv2.waitKey(0)	
	return combined_image
	


def define_coin(coin_area):
	value = 0
	if coin_area > 113000 and coin_area < 120000:
		value = 100
	elif coin_area > 87000 and coin_area < 89000:
		value = 50
	elif coin_area > 102000 and coin_area < 104000:
		value = 25
	elif coin_area > 63000 and coin_area < 65000:
		value = 10
	elif coin_area > 78500 and coin_area < 80500:
		value = 5
	elif coin_area > 71500 and coin_area < 73500:
		value = 5
	else:
		return False
	return value



image_path = "images/DSC_0180.JPG"
image = cv2.imread(image_path)
#image = cv2.resize(image , (300, 300))
binary_coin = binary_coin(image)
img, contours, hierarchy = cv2.findContours(binary_coin.copy() , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
 	contour_area = cv2.contourArea(contour)
	if contour_area > 60000 and contour_area < 120000:
		(x,y),radius = cv2.minEnclosingCircle(contour)
		center = (int(x),int(y))
		radius = int(radius)
		cv2.circle(image,center,radius,(0,0,255),2)
		coin_value = define_coin(contour_area)
		#print(contour_area)
		if coin_value:
			print(coin_value)
		#cv2.drawContours(img, [contour], -1, 255, 1)



cv2.imshow('binary_coin' , cv2.resize(binary_coin , (518, 291)))
cv2.imshow('image' , cv2.resize(image , (518, 291)))
cv2.waitKey(0)

