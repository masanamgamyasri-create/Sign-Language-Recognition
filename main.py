import pyttsx3

engine = pyttsx3.init()
last_gesture = ""
import cv2
import mediapipe as mp
from datetime import datetime

camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

while True:

    success, frame = camera.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark

            fingers = []

            # Thumb
            if landmarks[4].x < landmarks[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

            # Index, Middle, Ring, Pinky
            for tip in [8, 12, 16, 20]:

                if landmarks[tip].y < landmarks[tip - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = sum(fingers)

            gesture = ""

            if total_fingers == 0:
                 gesture = "A"

            elif total_fingers == 1:
                gesture = "ONE"

            elif total_fingers == 2:
                gesture = "VICTORY"

            elif total_fingers == 5:
                gesture = "B"

            elif total_fingers == 3:
                gesture = "THREE"

            elif total_fingers == 4:
                gesture = "FOUR"

            thumb = fingers[0]
            index = fingers[1]
            middle = fingers[2]
            ring = fingers[3]
            pinky = fingers[4]

            if thumb == 1 and index == 1 and middle == 0 and ring == 0 and pinky == 0:
                gesture = "L"

            elif thumb == 0 and index == 0 and middle == 0 and ring == 0 and pinky == 1:
                gesture = "I"

            if gesture != "" and gesture != last_gesture:
                engine.say(gesture)
                engine.runAndWait()

                with open("gestures.txt", "w") as file:
                    file.write("Gesture Log\n\n")

                last_gesture = gesture

            cv2.putText(
                frame,
                f"{gesture} ({total_fingers})",
                (20,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )
    cv2.imshow("Finger Counter", frame)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()
