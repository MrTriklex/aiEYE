import keyboard
import pyautogui
import time
import numpy as np
import cv2
from time import sleep , perf_counter
import keyboard_emu as kbe
from threading import Thread
import imutils


contlist = list()
contorsize = list()
timer1 = 0
t1 = 0
tf = 0
megamoveflag = 0
megamoveflag2 = 0
firstflag1 = 0

cv2.namedWindow('find')









def func(idx, status: callable = None):
    while True:
        position = status()
        #print(position)
        if position < 300 or position > 200:
            if position > 211:
                kbe.key_press(kbe.SC_RIGHT)

            if position < 211:
                kbe.key_press(kbe.SC_LEFT)



def func2(idx, status2: callable = None):
    while True:
        position = status2()
        #print(position)
        if position < 300 or position > 200:
            if position > 211:
                kbe.key_press(kbe.SC_UP)

            if position < 211:
                kbe.key_press(kbe.SC_DOWN)


kayyyw = 'start'
global_status = 211
global_status2 = 211

rangesnik = {
    'min_h1': {'current': 33, 'max': 180},    'max_h1': {'current': 66, 'max': 180},
    'min_sv': {'current': 26, 'max': 255},    'max_sv': {'current': 198, 'max': 255},
    'counters': {'current':0, 'max': 5000}
}


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



def my_status():
    global global_status
    return global_status

def my_status2():
    global global_status2
    return global_status2


th = Thread(target=func, args=(0, my_status))
th.start()




while True:
    pix = pyautogui.screenshot(region=(int(left), int(top), window_resolution[0], window_resolution[1]))
    numpix = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2BGR)

    numpix = numpix[250:, 120:520, :]
    #numpix = cv2.blur(numpix, (20, 20))

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
                max_size = id
            contorsize.append(w * h)


            # И выводим его:
            cv2.rectangle(numpix, (x, y), (x + w, y + h), (0, 255, 0), 1)

            contlist.append((x + w // 2, y + h // 2))


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
        large = (abs(max_x - 200)*abs(max_x - 200) + abs(max_y - 115)*abs(max_y - 115))**0.5
        if large > max_large:
            max_id = id
            max_large = large
    max_large = 0
    poss_x = 0
    poss_y = 0
    poss_x1 = 0
    poss_y1 = 0

    for id in range(len(contours)):
        if 0 == 0:
            poss_x1, poss_y1 = contlist[id]
            if max_id == id:
                cv2.line(numpix, (200, 230), contlist[id], (0, 255, 0), 2)
                poss_x,poss_y = contlist[id]

            else:
                cv2.line(numpix, (200, 230), contlist[id], (0, 0, 255), 2)


    if t1 + 0.1 < perf_counter():
        t1 = perf_counter()
        tf = 1
    else:
        tf = 0
    tf = 1



    xm, ym = pyautogui.position()
    xw, yw , _ , _ = nfs_window_location
    if xm > xw and xm < xw + 640 and ym > yw and ym < yw + 480 and megamoveflag == 0:
        if 200 < poss_x and tf == 1 and poss_x != 0:
            sleep(0.01)
            global_status += 10
            if global_status > 300:
                global_status = 211
            elif global_status < 200:
                global_status = 211
            #keyboard.press("d")
            kayyyw= 'd'
            image = cv2.putText(numpix, 'd' + str(poss_x), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            #time.sleep(0.2)
            

        elif 200 > poss_x and tf == 1and poss_x != 0:
            sleep(0.01)
            global_status -= 10
            if global_status > 300:
                global_status = 211
            elif global_status < 200:
                global_status = 211
            #keyboard.press("a")
            kayyyw = 'a'
            image = cv2.putText(numpix, 'a'+ str(poss_x), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            #time.sleep(0.2)
        if (len(contlist) == 0and megamoveflag == 0):
            image = cv2.putText(numpix, 'f', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                                cv2.LINE_AA)
            if  kayyyw == 'd':
                image = cv2.putText(numpix, 'fd', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                                    cv2.LINE_AA)
                #global_status2 -= 10
                #if global_status2 > 300:
                #    global_status2 = 211
                #elif global_status2 < 200:
                #    global_status2 = 211
                global_status += 10
                if global_status > 300:
                    global_status = 211
                elif global_status < 200:
                    global_status = 211
                sleep(0.05)
            elif kayyyw == 'a':
                image = cv2.putText(numpix, 'fa', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                                    cv2.LINE_AA)
                #global_status2 -= 10
                #if global_status2 > 300:
                #    global_status2 = 211
                #elif global_status2 < 200:
                #    global_status2 = 211
                global_status -= 10
                if global_status > 300:
                    global_status = 211
                elif global_status < 200:
                    global_status = 211
                sleep(0.05)



        #start_x = 200
        #start_y = 230
        #x , y = contlist[max_id]
        #if 0 == 0:
        #    M = cv2.moments(contours[max_id])
#
            # Центр тяжести это первый момент (сумма радиус-векторов), отнесенный к нулевому (площади-массе)
      #      if 0 != M['m00']:
     #           cx = int(M['m10'] / M['m00'])
    #            cy = int(M['m01'] / M['m00'])
    #            cv2.circle(numpix, (cx, cy), 5, 255, 2)
    #            cv2.line(numpix, (start_y, start_x), (cx, cy), (255,), 2)
     #           tangen = start_x - cx
    #            normal = start_y - cy
    #            poss_x = cx
    #            poss_y = cx

    #            if normal != 0:
    #                angle = np.degrees(np.arctan(tangen / normal))
     #           else:
    #                angle = None

            #cv2.line(numpix, (start_y, start_x), (start_y, y + h // 2), (255,), 2)
    if megamoveflag == 1:
        image = cv2.putText(numpix, 'w' , (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)


    contlist = []
    contorsize =[]
    cv2.line(numpix, (0, 250), (640,250), (0, 255, 0), 1)


    cv2.imshow('result', numpix)
    cv2.imshow('find', mask)
    #timer1 += 1

    #if timer1 > 10:
    if megamoveflag == 0:
        keyboard.press("w")
        sleep(0.01)
        #timer1 = 0


    if keyboard.is_pressed('t'):
        if megamoveflag == 0 and megamoveflag2 == 1:
            megamoveflag = 1
            megamoveflag2 = 0
        elif megamoveflag == 1 and megamoveflag2 == 1:
            megamoveflag = 0
            megamoveflag2 = 0
            sleep(5)
    else:
        megamoveflag2 = 1
    if firstflag1 == 0:
        sleep(3)
        firstflag1 = 1


    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()