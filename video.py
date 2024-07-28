import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow('result')


while True:
    ret, frame = cap.read()
    xsize, ysize, _ = frame.shape
    frameCopy = frame.copy()


    # Window name in which image is displayed
    window_name = 'Image'

    # Using cv2.flip() method
    # Use Flip code 0 to flip vertically
    frameCopy = cv2.flip(frame, 1)

    #for xp in range(xsize):
    #    for yp in range(ysize):
    #        frame[xp, yp] = [frameCopy.item(xp,-yp,0), frameCopy.item(xp,-yp,1), frameCopy.item(xp,-yp,2)]

    #for xp in range(xsize):
    #    for yp in range(ysize):
    #        if frameCopy.item(xp,yp,2) > frameCopy.item(xp,yp,0) and frameCopy.item(xp,yp,2) > frameCopy.item(xp,yp,1):
    #            frameCopy[xp, yp] = [0,0,0]
    hsv = cv2.cvtColor(frameCopy, cv2.COLOR_BGR2HSV)
    hmap = hsv
    smap = hsv
    vmap = hsv
    xsize, ysize, _ = frame.shape
    for xp in range(xsize):
        for yp in range(ysize):
            hmap[xp, yp] = [hsv.item(xp, yp, 0), 0, 0]
            smap[xp, yp] = [0, hsv.item(xp, yp, 1), 0]
            vmap[xp, yp] = [0, 0, hsv.item(xp, yp, 2)]


    cv2.imshow('result', hsv)



    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()