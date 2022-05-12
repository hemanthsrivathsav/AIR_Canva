from tkinter import Frame
import cvzone.HandTrackingModule
from cvzone.HandTrackingModule import HandDetector
import cv2
from collections import deque
from matplotlib.pyplot import draw
import numpy as np


length=0 


def rescale_frame(frame, scale):    # works for image, video, live video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

cap = cv2.VideoCapture(0)
cap.set(3, 1440)



detector = HandDetector(detectionCon=0.85, maxHands=2)


# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
whitepoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0
white_index = 0

#The kernel to be used for dilation purpose 
kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255),(255,255,255)]
colorIndex = 0



# Here is code for Canvas setup
paintWindow = np.zeros((660,860,3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

cv2.putText(paintWindow, "ERASE", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)



xp,yp=0,0



while True:
    # Get image frame
    success, img = cap.read()
    
    img= rescale_frame(img, scale=.8)


    img=cv2.flip(img,1)
    


    # Adding the colour buttons to the live frame for colour access
    img = cv2.rectangle(img, (40,1), (140,65), (122,122,122), -1)
    img = cv2.rectangle(img, (160,1), (255,65), colors[0], -1)
    img = cv2.rectangle(img, (275,1), (370,65), colors[1], -1)
    img = cv2.rectangle(img, (390,1), (485,65), colors[2], -1)
    img = cv2.rectangle(img, (505,1), (600,65), colors[3], -1)
    cv2.putText(img, "ERASE", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.56, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.56, (0, 0,0), 1, cv2.LINE_AA)
    cv2.putText(img, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.56, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.56, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.56, (0, 0, 0), 1, cv2.LINE_AA)
    
    # Find the hand and its landmarks
    lmListL=[]
    lmListR=[]
    infols=[]

    #img = detector.findHands(img)  # with draw
    hands,img = detector.findHands(img ,draw=1)  # without draw
    
    if len(hands)!= 0 :
        hand1 = hands[0]
            
        lmListL= hand1["lmList"]
        for i in range(len(lmListL[8])):
            x1=lmListL[8][0]
            y1=lmListL[8][1]
            #print(x1,y1)
        for i in range(len(lmListL[12])):
            x2=lmListL[12][0]
            y2=lmListL[12][1]
            #print(x2,y2)
        ll=len(lmListL)-1
        print(hands)
        fingers2L = detector.fingersUp(hand1)
        print(fingers2L)
        lengthL, info, _ = detector.findDistance(lmListL[4], lmListL[8],img|False)
        
        #cv2.line(img,lmListL[4],lmListL[8],(0,200,0),4)
        #if (xp==0 and yp == 0):
           # xp,yp=x1,y1 
        if (lengthL ) <= 35:
            cv2.circle(img, (lmListL[4]), 15, (0, 0, 0), -1)
            if (xp==0 and yp == 0):
                xp,yp=x1,y1 
            cv2.line(paintWindow,(xp,yp),(x1,y1),colors[colorIndex],10)
            xp,yp=x1,y1
        else:
            xp,yp=0,0  
        #if (fingers2L[0] and fingers2L[1]):
            

        #selection mode
        if (fingers2L[1] and fingers2L[2]):
            xp,yp=0,0 
            cv2.rectangle(img,(x1,y1+15),(x2,y2-10),colors[colorIndex],-1)

            if y1 <= 65:
                if 40 <= x1 <= 140: # Clear Button
                    bpoints = [deque(maxlen=512)]
                    gpoints = [deque(maxlen=512)]
                    rpoints = [deque(maxlen=512)]
                    ypoints = [deque(maxlen=512)]
                    whitepoints = [deque(maxlen=512)]

                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0
                    white_index = 0 

                    img[67:,:,:] = 255
                    colorIndex = 4 # white
                elif 160 <= x1 <= 255:
                        colorIndex = 0 # Blue
                elif 275 <= x1 <= 370:
                        colorIndex = 1 # Green
                elif 390 <= x1<= 485:
                        colorIndex = 2 # Red
                elif 505 <= x1<= 600:
                        colorIndex = 3 # Yellow
            else :
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(y1)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(y1)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(y1)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(y1)
                elif colorIndex == 4:
                    whitepoints[white_index].appendleft(y1)
        # Append the next deques when nothing is detected to avois messing up
        else:
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1
            whitepoints.append(deque(maxlen=512))
            white_index += 1
            

        
    if len(hands) == 2:
        hand2 = hands[1]
        lmListR= hand2["lmList"]
        fingers2R = detector.fingersUp(hand2)
        lengthR, info, _ = detector.findDistance(lmListR[4], lmListR[8],img|False)
        #cv2.line(img,lmListR[4],lmListR[8],(0,200,0),4)
        if (lengthR)<35:
            cv2.circle(img, (lmListR[4]), 15, (0,0,0),-1)

    # Show all the windows
    #Hori = np.concatenate((paintWindow,img),axis=0)
    #imnn=cv2.resize(img,(960,540))
    #imnp=cv2.resize(paintWindow,(960,540))
    #numpy_vertical = np.vstack((imnn, imnp))
    #resize
    
    ##cv2.imshow('App',numpy_vertical)

    cv2.imshow("Paint",paintWindow)
    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()