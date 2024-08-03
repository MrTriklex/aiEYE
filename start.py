import time

import cv2
import os

img = cv2.imread("./road-signs/footpath.jpg")
img2 = cv2.imread("./road-signs/left-turn.jpg")
#list = os.listdir("./road-signs")

if img is None:
    print('no')
    os._exit(1)


#cv2.imshow('img2',img2)
print(img.shape)
print(img.size)
print(img.dtype)
xsize , ysize , _ = img.shape
#x = xsize // 2
#y = ysize // 2
#bgr
#print(img.item(x,y,0))
#print(img.item(x,y,1))
#print(img.item(x,y,2))
#img.itemset((20, 20 , 0) ,0)
#img.itemset((20, 20 , 1) ,0)
#img.itemset((20, 20 , 2) ,0)
#img[x:x +10, y:y +10] = [0, 0, 255]
#x1 = int(input())
#x2 = int(input())
#y1 = int(input())
#y2 = int(input())
#img[x1:x2, y1:y2] = [0, 0, 255]
#for xp in range(xsize):
#    for yp in range(ysize):
#        summ = img.item(xp,yp,0) + img.item(xp,yp,1) + img.item(xp,yp,2)
#        if summ < 382:
#            img[xp, yp] = [0, 0, 0]
#        else:
#            img[xp, yp] = [summ / 3, summ / 3, summ / 3]
for xp in range(xsize):
    for yp in range(ysize):
        img[xp, yp] = [img.item(-xp,yp,0), img.item(-xp,yp,1), img.item(-xp,yp,2)]
bsumm = 0
gsumm = 0
rsumm = 0
blurstrong = 10
blurpixn = 0
#for xp in range(1, xsize-1):  # тут оно работает
#    for yp in range(1, ysize-1):
#        for xb in range (xp - blurstrong , xp+blurstrong):
#            for yb in range(yp - blurstrong, yp + blurstrong):
#                if xb > xp and xb < xsize and yb > yp and yb < ysize:
#                    blurpixn += 1
#                    bsumm += img.item(xb, yb,0)
#                    gsumm += img.item(xb, yb,1)
#                    rsumm += img.item(xb, yb, 1)
#        for xb in range (xp - blurstrong , xp+blurstrong):
#            for yb in range(yp - blurstrong, yp + blurstrong):
#                if xb > xp and xb < xsize and yb > yp and yb < ysize:
#                    img[xb, yb] = [bsumm / blurpixn, gsumm / blurpixn, rsumm / blurpixn]
        #blurpixn = 0
        #bsumm = 0
      #  gsumm = 0
      #  rsumm = 0
        #img[xp, yp+1] = [img.item(xp,yp,0), img.item(xp,yp,1), img.item(xp,yp,2)]
        #img[xp, yp] = [img.item(xp+1,yp,0), img.item(xp+1,yp,1), img.item(xp+1,yp,2)]
        #bsumm = img.item(xp,yp,0) + img.item(xp+1,yp,0) + img.item(xp-1,yp,0) + img.item(xp,yp+1,0) + img.item(xp,yp-1,0)
        #gsumm = img.item(xp, yp, 1) + img.item(xp + 1, yp, 1) + img.item(xp - 1, yp, 1) + img.item(xp, yp + 1,1)+ img.item(xp, yp - 1,1)
        #rsumm = img.item(xp, yp, 2) + img.item(xp + 1, yp, 2) + img.item(xp - 1, yp, 2) + img.item(xp, yp + 1,2)+ img.item(xp, yp - 1,2)
        #img[xp, yp] = [bsumm/5, gsumm/5, rsumm/5]
        #img[xp+1, yp] = [bsumm / 5, gsumm / 5, rsumm / 5]
        #img[xp-1, yp] = [bsumm / 5, gsumm / 5, rsumm / 5]
        #img[xp, yp+1] = [bsumm / 5, gsumm / 5, rsumm / 5]
        #img[xp, yp-1] = [bsumm / 5, gsumm / 5, rsumm / 5]


cv2.imshow('img', img)
while True:
    key = cv2.waitKey(1)
    if key == 32:
        cv2.destroyAllWindows()
        #cv2.imshow('img', list[1])

    if key == 27:
        break
cv2.destroyAllWindows()
