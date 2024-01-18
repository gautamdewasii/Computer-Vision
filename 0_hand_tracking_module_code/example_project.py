import cv2
import mediapipe as mp
import time
# importing our module for hand detection
import hand_tracking_module as htm



current_time=0
previews_time=0

cap=cv2.VideoCapture(0)

# using 'htm' predefine class, which we created
detector = htm.HandTracking()

while True:
    success,img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img)
    if len(lm_list) !=0:
        print(lm_list[1])
    current_time=time.time()
    frame_per_second=1/(current_time-previews_time)
    previews_time=current_time
        
    cv2.putText(img,str(int(frame_per_second)),(10,70),
            cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)