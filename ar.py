"""
Main AR Drawing App
✅ Tracks the index finger to draw.
✅ Uses two fingers (index + middle) close together to erase.
✅ Allows clearing the canvas ('C' key) and quitting ('Q' key).
"""

import cv2
from modules.hand_tracker import HandTracker
from modules.drawing import DrawingCanvas
from modules.utils import calculate_distance

DRAW_THRESHOLD = 40
ERASER_SIZE = 30
DRAW_COLOR = (0, 255, 0)
DRAW_THICKNESS = 5

# Initialize modules
cap = cv2.VideoCapture(1)  # Open webcam
tracker = HandTracker()  # Hand tracking module
canvas = None  # Drawing canvas (initialized later)
prev_index = None  # Store previous index finger position

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
            index_finger, middle_finger = tracker.get_finger_positions(hand_landmarks, frame.shape)

            if index_finger and middle_finger:  # Ensure both fingers are detected
                distance = calculate_distance(index_finger, middle_finger)  # Calculate distance

                # Erase if index & middle fingers are close together
                if distance < DRAW_THRESHOLD:
                    canvas.erase(index_finger, middle_finger, ERASER_SIZE)
                    prev_index = None
                else:
                    # Draw with index finger
                    if prev_index:
                        canvas.draw_line(prev_index, index_finger, DRAW_COLOR, DRAW_THICKNESS)  # Green color
                    prev_index = index_finger

    frame = canvas.merge_with_frame(frame)
    cv2.imshow("AR Drawing", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        if canvas is not None:
            canvas.clear()  # Clear the screen
    elif key == ord('q'):
        break  # Exit the loop

cap.release()
cv2.destroyAllWindows()
