import cv2
import os
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
import pygame
import time

prev_time = time.time()

print(os.getcwd())

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keyboard = Controller()

pygame.init()
piano_sounds = [pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound1_C2.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound2_D2.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound3_E2.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound4_F2.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound5_G2.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound6_A2.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound7_B2.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound8_C3.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound9_D3.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound10_E3.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound11_F3.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound12_G3.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound13_A3.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound14_B3.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound15_C4.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound16_D4.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound17_E4.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound18_F4.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound19_G4.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound20_A4.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound21_B4.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound22_C5.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound23_D5.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound24_E5.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound25_F5.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound26_G5.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound27_A5.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound28_B5.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound29_C6.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound30_D6.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound31_E6.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound32_F6.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound33_G6.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound34_A6.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound35_B6.wav"),
                pygame.mixer.Sound(r"F:\etf\II godina\IV semestar\DPSprojekat\pianoSamples\PianoSound36_C7.wav")
                ]

key_positions = [(50, 50), (120, 50), (190, 50), (260, 50), (330, 50), (400, 50),
                 (470, 50), (540, 50), (610, 50), (680, 50), (750, 50), (820, 50),
                 (890, 50), (960, 50), (1030, 50), (1100, 50), (1170, 50), (1240, 50),
                 (1310, 50), (1380, 50), (1450, 50), (1520, 50), (1590, 50), (1660, 50),
                 (1730, 50), (1800, 50), (1870, 50), (1940, 50), (2010, 50), (2080, 50),
                 (2150, 50), (2220, 50), (2290, 50), (2360, 50), (2430, 50), (2500, 50)]

white_key_size = (40, 120)
black_key_size = (30, 80)


class Button:
    def __init__(self, position, sound, text, size=None, is_black=False):
        if size is None:
            size = white_key_size if not is_black else black_key_size
        self.pos = position
        self.size = size
        self.sound = sound
        self.text = text
        self.is_black = is_black


buttonList = []
key_texts = ["C2", "D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3", "E3", "F3", "G3", "A3",
             "B3", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5",
             "A5", "B5", "C6", "D6", "E6", "F6", "G6", "A6", "B6", "C7"]

for i, pos in enumerate(key_positions):
    buttonList.append(Button(pos, piano_sounds[i], key_texts[i], is_black=False))


def drawAll(image, bttnList):
    for bttn in bttnList:
        xPosition, yPosition = bttn.pos
        w, h = bttn.size
        cv2.rectangle(image, (xPosition, yPosition), (xPosition + w, yPosition + h), (255, 255, 255), cv2.FILLED)
    return image


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    current_time = time.time()
    if current_time - prev_time < 0.4:
        continue

    if lmList:
        for button in buttonList:
            xPos, yPos = button.pos
            width, height = button.size

            if xPos < lmList[8][0] < xPos + width and yPos < lmList[8][1] < yPos + height:
                cv2.rectangle(img, (xPos - 5, yPos - 5), (xPos + width + 5, yPos + height + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (xPos, yPos + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                cv2.rectangle(img, button.pos, (xPos + width, yPos + height), (0, 0, 0), cv2.FILLED)

                l, _, _ = detector.findDistance(8, 12, img, draw=False)

                if l < 30:
                    if not button.is_black:
                        button.sound.play()
                        time.sleep(0.15)
                        button.sound.stop()
                    prev_time = time.time()

    cv2.imshow("Virtual Piano Keyboard", img)
    cv2.waitKey(1)
