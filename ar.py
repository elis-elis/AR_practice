"""
Classes help in organizing the code by grouping related functionalities together.
Instead of handling everything inside one file (ar_drawing.py), we separate logic into different modules.

Benefits of Using Classes:
Encapsulation: Groups related functions (e.g., hand tracking, drawing) inside separate classes.
Reusability: We can reuse the same classes in other projects or parts of the code.
Readability: Easier to read and maintain compared to a single long script.
"""

import cv2
import numpy as np
from modules.hand_tracker import HandTracker
from modules.drawing import DrawingCanvas
from modules.utils import calculate_distance

# Initialize modules
cap = cv2.VideoCapture(2)  # Open webcam
tracker = HandTracker()  # Hand tracking module
canvas = None  # Drawing canvas (initialized later)
prev_index = prev_middle = None  # Store previous finger positions

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)  # Mirror effect

    # Ensure canvas matches frame size
    if canvas is None or canvas.canvas.shape != frame.shape:
        canvas = DrawingCanvas(frame)

    result = tracker.detect_hands(frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            h, w, _ = frame.shape
            index_finger = (int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h))
            middle_finger = (int(hand_landmarks.landmark[12].x * w), int(hand_landmarks.landmark[12].y * h))

            tracker.draw_landmarks(frame, hand_landmarks)

            # Distance between fingers
            distance = calculate_distance(index_finger, middle_finger)

            # Erase if fingers are close
            if distance < 40:
                canvas.erase(index_finger, 30)
            else:
                # Draw with the finger that is higher
                if index_finger[1] < middle_finger[1]:  # Index finger higher → draw green
                    if prev_index:
                        canvas.draw_line(prev_index, index_finger, (0, 255, 0), 5)
                    prev_index = index_finger
                    prev_middle = None
                elif middle_finger[1] < index_finger[1]:  # Middle finger higher → draw pink
                    if prev_middle:
                        canvas.draw_line(prev_middle, middle_finger, (255, 182, 193), 5)
                    prev_middle = middle_finger
                    prev_index = None

    frame = canvas.merge_with_frame(frame)
    cv2.imshow("AR Drawing", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        canvas.clear()  # Clear the screen
    elif key == ord('q'):
        break  # Exit the loop

cap.release()
cv2.destroyAllWindows()
