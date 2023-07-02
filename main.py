import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
import time

prev_time = time.time()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()


def drawAll(image, bttnList):
    for bttn in bttnList:
        xAxis, yAxis = bttn.pos
        width, height = bttn.size
        cvzone.cornerRect(image, (bttn.pos[0], bttn.pos[1], bttn.size[0], bttn.size[1]), 20, rt=0)
        cv2.rectangle(image, bttn.pos, (xAxis + width, yAxis + height), (255, 0, 255), cv2.FILLED)
        cv2.putText(image, bttn.text, (xAxis + 20, yAxis + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return image


class Button:
    def __init__(self, pos, text, size=None):
        if size is None:
            size = [85, 85]
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
buttonList.append(Button([720, 350], "Space", [225, 85]))
buttonList.append(Button([965, 350], "Delete", [240, 85]))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    current_time = time.time()
    if current_time - prev_time < 1:
        continue

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                if l < 30:
                    if button.text == "Space":
                        keyboard.press(' ')
                        if finalText and finalText[-1] != ' ':
                            finalText += ' '
                    elif button.text == "Delete":
                        if len(finalText) > 0:
                            keyboard.press('\b')
                            finalText = finalText[:-1]
                    else:
                        keyboard.press(button.text)
                        finalText += button.text

                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    sleep(0.15)

                    prev_time = time.time()

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Virtual Keyboard", img)
    cv2.waitKey(1)
