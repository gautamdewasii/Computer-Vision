
import cv2
import mediapipe as mp
import time

# class for hand detection
class HandTracking():

    # defining some members at object creation
    def __init__(self, mode=False, maxHands=2, modelComp=1, detectionCon=0.5, trackCon=0.5):
        
        # current objects members
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComp = modelComp

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComp, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    # for detecting hands
    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # if frame contain hands in it, then execute
        if self.results.multi_hand_landmarks:
            # extracting position data of each landmark from multi_hand_landmarks
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # drawing all landmarks and connecting with lines
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)

        return img

    # used to find position of any particular landmark point
    def find_position(self, img, hand_no=0, draw=True):

        # used to store all landmark data along with its index number
        lm_list = []

        if self.results.multi_hand_landmarks:
            my_hands = self.results.multi_hand_landmarks[hand_no]
            for id,lm in enumerate(my_hands.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                # append landmark details into lm_list object
                lm_list.append([id,cx,cy])        
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lm_list
    

def main():

    current_time=0
    previews_time=0

    cap=cv2.VideoCapture(0)
    detector = HandTracking()

    while True:
        success,img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        if len(lm_list) !=0:
            print(lm_list[4])
        current_time=time.time()
        frame_per_second=1/(current_time-previews_time)
        previews_time=current_time
        
        cv2.putText(img,str(int(frame_per_second)),(10,70),
                cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
    
        cv2.imshow("Image",img)
        cv2.waitKey(1)


# starting point
if __name__ == "__main__":
    main()