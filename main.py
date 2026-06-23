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

            thumb_tip = landmarks[4]
            index_tip = landmarks[8]

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

            thumb = fingers[0]
            index = fingers[1]
            middle = fingers[2]
            ring = fingers[3]
            pinky = fingers[4]

            distance = ((thumb_tip.x - index_tip.x) ** 2 +
            (thumb_tip.y - index_tip.y) ** 2) ** 0.5

            gesture = ""

            if distance < 0.05:
                gesture = "OK"

            elif total_fingers == 0:
                gesture = "A"

            elif total_fingers == 5:
                gesture = "B"

            elif thumb == 0 and index == 1 and middle == 0 and ring == 0 and pinky == 0:
                gesture = "D"

            elif thumb == 1 and index == 0 and middle == 0 and ring == 0 and pinky == 1:
                gesture = "Y"

            elif thumb == 0 and index == 1 and middle == 1 and ring == 0 and pinky == 0:
                gesture = "V"

            elif thumb == 1 and index == 1 and middle == 0 and ring == 0 and pinky == 0:
                gesture = "L"

            elif thumb == 0 and index == 0 and middle == 0 and ring == 0 and pinky == 1:
                gesture = "I"

            elif thumb == 1 and index == 1 and middle == 0 and ring == 0 and pinky == 1:
                gesture = "I LOVE YOU"

            elif thumb == 1 and index == 0 and middle == 0 and ring == 0 and pinky == 0:
                gesture = "GOOD"

            if gesture != "" and gesture != last_gesture:
                engine.say(gesture)
                engine.runAndWait()

                with open("gestures.txt", "a") as file:
                    file.write(f"{datetime.now()} - {gesture}\n")

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
