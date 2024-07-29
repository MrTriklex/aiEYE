import keyboard
import pyautogui
import time
import numpy as np
import cv2
from time import sleep
import imutils


contlist = list()
contorsize = list()
timer1 = 0




cv2.namedWindow('find')




ranges = {
    'min_h1': {'current': 27, 'max': 180},
    'max_h1': {'current': 70, 'max': 180},
}
ranges2 = {
    'min_h2': {'current': 81, 'max': 255},
    'max_h2': {'current': 255, 'max': 255},
}
ranges3 = {
    'min_h3': {'current': 0, 'max': 255},
    'max_h3': {'current': 71, 'max': 255},
}

def trackbar_handler(name):
    def handler(x):
        global ranges
        ranges[name]['current'] = x

    return handler
def trackbar_handler2(name):
    def handler(x):
        global ranges2
        ranges2[name]['current'] = x

    return handler
def trackbar_handler3(name):
    def handler(x):
        global ranges3
        ranges3[name]['current'] = x

    return handler


for name in ranges:
    cv2.createTrackbar(name,
                       'find',
                       ranges[name]['current'],
                       ranges[name]['max'],
                       trackbar_handler(name)
                       )
for name in ranges2:
    cv2.createTrackbar(name,
                       'find',
                       ranges2[name]['current'],
                       ranges2[name]['max'],
                       trackbar_handler2(name)
                       )

for name in ranges3:
    cv2.createTrackbar(name,
                       'find',
                       ranges3[name]['current'],
                       ranges3[name]['max'],
                       trackbar_handler3(name)
                       )




# Ждем три секунды, успеваем переключиться на окно:
print('waiting for 2 seconds...')
time.sleep(2)

#ВНИМАНИЕ! PyAutoGUI НЕ ЧИТАЕТ В JPG!
title = './nfs-shift-title.png'

nfs_window_location = None
searching_attempt = 1
while searching_attempt <= 5:
    nfs_window_location = pyautogui.locateOnScreen(title)

    if nfs_window_location is not None:
        print('nfs_window_location = ', nfs_window_location)
        break
    else:
        searching_attempt += 1
        time.sleep(1)
        print("attempt %d..." % searching_attempt)

if nfs_window_location is None:
    print('NFS Window not found')
    exit(1)

# Извлекаем из картинки-скриншота только данные окна NFS.
# Наша target-картинка - это заголовочная полоска окна.
# Для получения скриншота, мы берем ее левую точку (0),
# а к верхней (1) прибавляем высоту (3)
left = nfs_window_location[0]
top = nfs_window_location[1]+nfs_window_location[3]

# ВНИМАНИЕ!  У вас, скорее всего, будет другое разрешение, т.к. у меня 4К-монитор!
# Здесь надо выставить те параметры, которые вы задали в игре.
window_resolution = (640, 480)

window = (left, top, left+window_resolution[0], top+window_resolution[1])

cv2.namedWindow('result')

while True:
    pix = pyautogui.screenshot(region=(int(left), int(top), window_resolution[0], window_resolution[1]))
    numpix = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2BGR)

    numpix = numpix[250:, :, :]

    min_ = (ranges['min_h1']['current'], ranges2['min_h2']['current'], ranges3['min_h3']['current'])
    max_ = (ranges['max_h1']['current'], ranges2['max_h2']['current'], ranges3['max_h3']['current'])

    mask = cv2.inRange(numpix, min_, max_)

    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Сами структуры контуров хранятся в начальном элементе возвращаемого значения:
    contours = contours[0]


    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Третий аргумент — это индекс aaтура, который мы хотим вывести. Мы хотим самый большой.
        # Вывести все можно, передав -1 вместо 0:
        cv2.drawContours(mask, contours, 0, (255, 0, 0), 1)
        for id in range(len(contours)):

            # Получаем прямоугольник, обрамляющий наш контур:
            (x, y, w, h) = cv2.boundingRect(contours[id])
            max_size = 0

            if w * h > max_size:
                max_size = w * h
            contorsize.append(w * h)

            if x > 160 and x < 520:

                # И выводим его:
                cv2.rectangle(numpix, (x, y), (x + w, y + h), (0, 255, 0), 1)

                contlist.append((x, y))
            else:
                contlist.append((320, 480))

            #if y > 320:
            #    keyboard.press("d")
            #else:
            #    keyboard.press("a")

            # Аналогично строим минимальную описанную вокруг наибольшего контура окружность:
            (x1, y1), radius = cv2.minEnclosingCircle(contours[id])
            center = (int(x1), int(y1))
            radius = int(radius)
            cv2.circle(mask, center, radius, (0, 255, 0), 1)
    max_large = 0
    max_id = 0

    for id in range(len(contours)):
        max_x, max_y = contlist[id]
        large = (abs(max_x - 320)*abs(max_x - 320) + abs(max_y - 240)*abs(max_y - 240))**0.5
        if large > max_large:
            max_id = id
            max_large = large
    max_large = 0
    poss_x = 0
    poss_y = 0
    for id in range(len(contours)):
        if 0 == 0:
            if contorsize[id] == max_size:
                cv2.line(numpix, (320, 480), contlist[id], (0, 255, 0), 2)
                poss_x,poss_y = contlist[id]

            else:
                cv2.line(numpix, (320, 480), contlist[id], (0, 0, 255), 2)
    if 320 > poss_x:
        keyboard.press("d")
        image = cv2.putText(numpix, 'd', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        time.sleep(1)
    elif 320 < poss_x:
        keyboard.press("a")
        image = cv2.putText(numpix, 'a', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        time.sleep(1)



    #    start_x = 480
  #      start_y = 320
     #   x , y = contlist[id]
    #    if x > 240 and y > 300 and x < 440:
    #        M = cv2.moments(contours[id])

            # Центр тяжести это первый момент (сумма радиус-векторов), отнесенный к нулевому (площади-массе)
      #      if 0 != M['m00']:
         #       cx = int(M['m10'] / M['m00'])
           #     cy = int(M['m01'] / M['m00'])
         #       cv2.circle(numpix, (cx, cy), 5, 255, 2)
       #         cv2.line(numpix, (start_y, start_x), (cx, cy), (255,), 2)
        #        tangen = start_x - cx
       #         normal = start_y - cy

         #       if normal != 0:
       #             angle = np.degrees(np.arctan(tangen / normal))
        #        else:
        #            angle = None
#
            #cv2.line(numpix, (start_y, start_x), (start_y, y + h // 2), (255,), 2)




    contlist = []
    contorsize =[]
    cv2.line(numpix, (0, 250), (640,250), (0, 255, 0), 1)


    cv2.imshow('result', numpix)
    cv2.imshow('find', mask)
    timer1 += 1

    if timer1 > 500:
        #keyboard.press("w")
        timer1 = 0



    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()