"""
HAND TRACKING USING OPENCV
"""

# requirements :-
# pip install opencv-python
# pip install mediapipe

# prerequisite 
import cv2
import mediapipe as mp
import time

# It initialize the cv2.videoCapture object
# that is connected to default camera ( 0 for default)
cap=cv2.VideoCapture(0)

## mediapipe configurations :-
# Giving short name 'mpHands' to a command that will able to understand hands
# easy to reference this command with this name
mpHands = mp.solutions.hands

# This instance (hands) is used to detect and process hand landmarks (21 points).
# Hands() created instance of Hands class,which is part of mp.solutions.hands
# DEFAULT ARGUMENTS :-
# static_image_mode (default is False):
# When set to True, it indicates that the input images are static and 
# not consecutive video frames. This may affect the model's behavior.
#max_num_hands (default is 2):
#Specifies the maximum number of hands to detect. 
#min_detection_confidence (default is 0.5):
# Sets the minimum confidence threshold for hand detection. 
#Hands with confidence below this threshold are not considered.
# min_tracking_confidence (default is 0.5):
# Sets the minimum confidence threshold for hand tracking. 
#Once a hand is detected, tracking is used to follow its movement. 
#Hands with confidence below this threshold may lose tracking.
hands = mpHands.Hands()

# "drawing_utils" A submodule containing utility functions for drawing on images.
# useful for visualizing detected hands landmarks
mpDraw = mp.solutions.drawing_utils

# frame rate variables
current_time=0
previews_time=0

while True:


    # 'success' boolean indicter for whether frame was successfully read or not
    # 'img' is the actual frame data 
    # 'cap.read()' it reads the frame from the connected camera
    success,img = cap.read()

    # Used to convert color space from BGR TO RGB ,mediapipe uses RGB images only
    # cvtColor() used to change color space of an image
    # "img" - original image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # process() method of 'Hands' class , that processes the image to detect hands
    # "imgRGB" that converted image from BGR TO RGB
    results = hands.process(imgRGB)
    # this will display all positions of hands landmarks in an frame(image) 
    #######    print(results.multi_hand_landmarks)

    # IF not none , then this will execute
    # this conditions contains hands landmarks positions
    if results.multi_hand_landmarks:
        # extracting each frame hand landmarks position 
        for handLms in results.multi_hand_landmarks:

            # handLms contains landmarks(21 points) details in it
            # handLms.landmarks contains index and x,y,z axis position of these points
            # note :- each frame contains 21 landmarks
            # id is index and lm is landmarks
            for id,lm in enumerate(handLms.landmark):
                # display each frame 21 landmarks positions and their index
                # print(id,lm)

                # img.shape returns image height,width and channel(RGB or BGR)
                h, w, c = img.shape
                
                # converting fractional values of lm.x,lm.y into pixels
                # lm.x*w = fraction * actual width gives the pixel position or size
                cx, cy = int(lm.x*w), int(lm.y*h)
                # display index, and their x,y axis positions of each frame
                print(id, cx, cy)
                ## NOTE :- we can use id, landmark position to take use of these landmarks
                
                # draw circle on 4th landmark point
                if id == 4:
                    # it will draw circle at 4th index landmark point,
                    # (cx,cy) is the position of that landmark in current frame
                    # 15 is the radius of circle
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)



            # draw_landmarks() will draw landmarks (points) on image
            # "img" : -actual image ( note:- don't use imgRGB)
            # "handLms" :-0 position of landmarks
            # "mp.Hands.HAND_CONNECTIONS" constant specify the connection b/w landmarks
            # used to draw line between these landmarks
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

    # current time on the current frame
    current_time=time.time()
    # calculating fps formula
    frame_per_second=1/(current_time-previews_time)
    previews_time=current_time

    # used to display test on actual image 
    # (10,70) position of text 
    # 3 is the font scale ( smaller to large size)
    # (255,0,255) color of text
    # 3 is the thickness of the text
    cv2.putText(img,str(int(frame_per_second)),(10,70),
                cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
    
    # this function is used to display image.
    # first argument is the name of appeared window
    # second argument is the actual image or frame data that we want to display
    cv2.imshow("Image",img)
    

    # it defines the wait time for capturing frames
    # if 0 :- means capture only one frame , and wait until a key(event) is pressed
    # note :- arguments in "milliseconds"
    # 1:- every 1 millisecond , it will capture an image(frame) from connected camera
    # if 1000, means at every 1000millisecond it will capture camera frame(image)
    cv2.waitKey(1)
