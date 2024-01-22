# THIS COMPUTER VISION MODEL WILL ABLE TO MANIPULATE COMPUTER SOUND USING HAND GESTURE


# LIBRARIES 
import cv2  #Connectivity, capturing frames and putting text/objects on frame
import time  # fps
import hand_tracking_module as htm  # user define module for hand, landmarks detection
import math  #hypot() 
import numpy as np  # interp() - 
# **pycaw** module requirements ( for sound controlling) 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# connecting with default camera
cap = cv2.VideoCapture(0)
width_cam = 640 
height_cam = 480
cap.set(3, width_cam)  # defining width of camera window
cap.set(4, height_cam)  # defining height of camera window

# creating object of HandTracking module ( user define module)
# detectionCon :- connecting points will not fluctuate  (0 - 1)
hands = htm.HandTracking(detectionCon=0.8)
#for fps
p_time = 0

# pycaw prerequisite 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()

# for identifying sound range of pycaw module
volume_range = volume.GetVolumeRange() # range from ( -64 to 0 )
min_volume = volume_range[0]  # min_volume value ( where sound is muted) 0%
max_volume = volume_range[1]  # max_volume value , where sound is 100%

# for fluctuate computer sound
vol_value=0
# for rectangle bar
vol_bar = 400 # default 400, means bar will be un filled
# for text percentage
vol_per = 0

# iterating through each frame
while True:

    # reading frame from camera
    success, img = cap.read()

    # used to detect hands from user define module
    img=hands.find_hands(img)
    # used to find landmarks of current points
    # draw=False, means non of these landmarks will be displayed using circle()
    landmarks = hands.find_position(img,draw=False)

    # if hand exist on current frame
    if len(landmarks) != 0:

        # thumb top point or landmark 4
        # Note at [4][0] :- index of that landmark point
        x1, y1 = landmarks[4][1], landmarks[4][2]
        # top of index finger , or landmark 8
        x2, y2 = landmarks[8][1], landmarks[8][2]

        # calculating middle point of the line 
        # between index finger and thumb top point
        cx, cy = (x1+x2) // 2 , (y1+y2) // 2

        # displaying additional pink point on the thumb
        cv2.circle(img,(x1,y1), 10, (255,0,255), cv2.FILLED)
        # for index finger
        cv2.circle(img,(x2,y2), 10, (255,0,255), cv2.FILLED)
        # creating line between landmark 4 and 8
        cv2.line(img,(x1,y1), (x2,y2),(255,0,255), 2 )
        # displaying point on the center of the line or landmark 4,8
        cv2.circle(img, (cx, cy), 10, (255,0,255),cv2.FILLED)

        # calculating the line length ( useful for sound up-down)
        length = math.hypot(x2-x1, y2-y1)

        # Converting actual length of line into another value as per range(min_volume, max_volume)
        # means line length know lies from -64 to 0
        vol_value = np.interp(length, [17, 170], [min_volume, max_volume])
        # check this one
        #print(length, vol_value)
        
        # pycaw method, used to manipulate computer speaker sound
        volume.SetMasterVolumeLevel(vol_value, None)

        # know, for rectangle bar, defining its filled value according to rectangle size(400,150) height(y axis)
        vol_bar = np.interp(length, [18,170], [400,150])
        # for displaying percentage value from 0 to 100
        vol_per = np.interp(length, [18, 170], [0, 100])

        # if landmark 4 and 8 are very near to each other
        if length < 20:
            # for dynamic look, changed our center point color from pink to green
            cv2.circle(img, (cx, cy), 10, (0,255,0),cv2.FILLED)

    # for rectangle bar
    # 50-75 ( x-axis or width)
    # 150-400 (y-axis or height)
    # this rectangle is empty from inside
    cv2.rectangle(img,(50,150), (75,400), (205,24,0), 3)
    # filled rectangle according to vol_bar value
    cv2.rectangle(img,(50,int(vol_bar)), (75,400), (205,24,0), cv2.FILLED)
    # displaying bar percentage at the bottom 
    cv2.putText(img, f"{int(vol_per)}", (50,450),cv2.FONT_HERSHEY_COMPLEX, 0.8, (205,24,0), 2)

    # fps
    c_time = time.time()
    fps = 1/(c_time - p_time)
    p_time = c_time

    # fps displaying
    cv2.putText(img, f"FPS :-  {int(fps)}", (10,40), cv2.FONT_HERSHEY_COMPLEX, 0.8 , (205,24,0), 2)
    cv2.imshow("Image ", img)
    cv2.waitKey(1)