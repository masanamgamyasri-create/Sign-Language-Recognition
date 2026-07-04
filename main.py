import pyttsx3
import time

word_gestures = ["HELLO", "OK", "GOOD", "I LOVE YOU"]

engine = pyttsx3.init()
last_gesture = ""

sentence = ""
gesture_start_time = 0

current_gesture = ""
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

            if gesture != "":

                # A new gesture appeared
                if gesture != current_gesture:
                    current_gesture = gesture
                    gesture_start_time = time.time()

                else:
                    elapsed = time.time() - gesture_start_time

                    if elapsed >= 2:

                        if sentence == "" or not sentence.endswith(gesture):

                            if gesture in word_gestures:
                                if sentence != "":
                                    sentence += " "
                                sentence += gesture + " "
                            else:
                                sentence += gesture

                            engine.say(gesture)
                            engine.runAndWait()

                            with open("gestures.txt", "a") as file:
                                file.write(f"{datetime.now()} - {gesture}\n")

                        gesture_start_time = time.time()

            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Sentence: " + sentence,
                (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            remaining = max(0, 2 - (time.time() - gesture_start_time))

            elapsed = time.time() - gesture_start_time

            progress = min(elapsed / 2, 1.0)

            cv2.putText(
                frame,
                f"Hold: {remaining:.1f}s",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            # Progress bar position
            bar_x = 20
            bar_y = 120
            bar_width = 250
            bar_height = 20

            # Draw empty bar
            cv2.rectangle(
                frame,
                (bar_x, bar_y),
                (bar_x + bar_width, bar_y + bar_height),
                (255, 255, 255),
                2
            )

            # Draw filled part
            filled_width = int(bar_width * progress)

            cv2.rectangle(
                frame,
                (bar_x, bar_y),
                (bar_x + filled_width, bar_y + bar_height),
                (0, 255, 0),
                -1
            )

    else:
        current_gesture = ""
        gesture_start_time = time.time()

    cv2.imshow("Finger Counter", frame)

    key = cv2.waitKey(1) & 0xFF

    # BACKSPACE → Remove last character
    if key == 8 or key == 127:
        sentence = sentence[:-1]

    # C → Clear sentence
    elif key == ord('c'):
        sentence = ""

    # S → Speak complete sentence
    elif key == ord('s'):
        if sentence != "":
            engine.say(sentence)
            engine.runAndWait()

    # ESC → Exit
    elif key == 27:
        break
