import cv2
import numpy as np
import hand_track as htm
import time
import pyautogui

##########################
wCam, hCam = 640, 480
frameR = 100
smoothening = 7
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
##########################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
pyautogui.FAILSAFE = False
wScr, hScr = pyautogui.size()

sensitivity = 15 

while True:
    # Find hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Get fingers up status
    if len(lmList) != 0:
        fingers = detector.fingersUp()

        # Click mouse
        if fingers[0]:  # Check if the index finger is up (left-click)
            pyautogui.click()
            time.sleep(0.1) 

        # Move mouse
        # We will use the index finger's tip (lmList[8]) to control the mouse movement
        if fingers[1]:  # Check if the middle finger is up (move the mouse)
            x, y = lmList[8][1], lmList[8][2]  # Get the coordinates of the index finger's tip
            x = np.interp(x, [frameR, wCam - frameR], [0, wScr])  # Map the x-coordinate to the screen width
            y = np.interp(y, [frameR, hCam - frameR], [0, hScr])  # Map the y-coordinate to the screen height
            clocX = plocX + (x - plocX) / smoothening
            clocY = plocY + (y - plocY) / smoothening
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY


        # Scroll up and down
        if fingers[2]:  # Check if the ring finger is up (scroll)
            pyautogui.scroll(10)
            time.sleep(0.1)   # You can adjust the scroll amount as needed

        # Zoom in/out mode
        if fingers[3] and fingers[4]:  # Check if both pinky and thumb fingers are up (zoom)
            pyautogui.hotkey('ctrl', '+')  # Zoom in
        elif fingers[3]:  # Check if only the pinky finger is up (zoom out)
            pyautogui.hotkey('ctrl', '-')  # Zoom out

        # Take screenshots
        if fingers[0] and fingers[2]:  # Check if both index and ring fingers are up (take a screenshot)
            pyautogui.screenshot("screenshot.png")  # Save the screenshot to a file named "screenshot.png"

    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
