import cv2
from cvzone.HandTrackingModule import HandDetector
import streamlit as st
import serial
import time
import numpy as np
import random

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.8)

# ser = serial.Serial('COM8')
button_text = "Start"
button_x, button_y = 50, 50
button_width, button_height = 100, 40
button_color = (0, 255, 0)

global user_choice
global robot_choice

def on_button_click(event, x, y, flags, param):
    global button_clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
            button_clicked = True

def result(user, robot):
    print("<<<<<<<<<<<<<<<  Result Time  >>>>>>>>>>>>>>>")
    print(f"User => {user_choice} v/s Robot => {robot_choice}")
    if user == robot:
        print("It's a tie!")
    elif (user == "Rock" and robot == 2) or (user == "Paper" and robot == 1) or (user == "Scissor" and robot == 3):
        print("You win!")
    else:
        print("You lose!")

# def start():
#     for i in range(3):
#         print(3 - i)
#         time.sleep(2)
#     print("GO")
#     hand_make_gesture()


def hand_make_gesture():
    ser = serial.Serial('COM8')

    print("<<<<<<<<<<<<<<<  Robot's turn  >>>>>>>>>>>>>>>")
    hand_gesture = np.random.randint(1, 4)
    print("Robot's gesture: ", hand_gesture)
    robot_choice = hand_gesture
    ser.write(str(hand_gesture).encode())
    time.sleep(2)
    ser.close()

    # print("Auto Home")
    # ser.write(b'3')

def human_gesture():
    global button_clicked
    button_clicked = False
    #button_counter = 0
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hands, img = detector.findHands(img)
        print("<<<<<<<<<<<<<<<  User's turn  >>>>>>>>>>>>>>>")
        print("Make a gesture and click the start button!!")

        cv2.rectangle(img, (button_x, button_y), (button_x + button_width, button_y + button_height), button_color, -1)
        cv2.putText(img, button_text, (button_x + 10, button_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        if hands and button_clicked:
            button_clicked = False
            hand = hands[0]
            fingers = detector.fingersUp(hand)

            if fingers == [0, 1, 1, 0, 0]:
                cv2.putText(img, "Scissor", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                user_choice = "Scissor"
                print("User gesture: ", user_choice)
                hand_make_gesture()
                result(user_choice, robot_choice)
                # break

            if fingers == [1, 1, 1, 1, 1]:
                cv2.putText(img, "Paper", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                user_choice = "Paper"
                print("User gesture: ", user_choice)
                hand_make_gesture()
                # break

            if fingers == [0, 0, 0, 0, 0]:
                cv2.putText(img, "Rock", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                user_choice = "Rock"
                print("User gesture: ", user_choice)
                hand_make_gesture()
                # break

        cv2.imshow("Image", img)
        cv2.setMouseCallback("Image", on_button_click)
        button_clicked = False
        # video_feed.image(img, channels="RGB")
        # button_counter += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# ser.close()

human_gesture()

cap.release()
cv2.destroyAllWindows()