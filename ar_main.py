import cv2
from modules.hand_tracker import HandTracker
from modules.drawing import DrawingCanvas
from modules.utils import calculate_distance
from modules.drawing import handle_erase_if_close


DRAW_THRESHOLD = 40
ERASER_SIZE = 30
HAND_COLORS = {"Left": (0, 255, 0), "Right": (255, 182, 193)}
DRAW_THICKNESS = 5

# Initialize modules
cap = cv2.VideoCapture(1)  # Open webcam
tracker = HandTracker()  # Hand tracking module
canvas = None  # Drawing canvas (initialized later)
prev_positions = {"Left": None, "Right": None}  # Store previous hand position

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)  # Mirror effect

    # Ensure canvas matches frame size
    if canvas is None or canvas.canvas.shape != frame.shape:
        canvas = DrawingCanvas(frame)

    results = tracker.detect_hands(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks, hand_label in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_type = hand_label.classification[0].label # "Left" or "Right"
            fingers = tracker.get_finger_positions(hand_landmarks, frame.shape)

            index_finger = fingers.get("index")
            middle_finger = fingers.get("middle")

            if index_finger and middle_finger:  # Ensure both fingers are detected
                erased = handle_erase_if_close(canvas, index_finger, middle_finger, DRAW_THRESHOLD, ERASER_SIZE)
                # Erase if index & middle fingers are close together
                if erased:
                    prev_index_fingers = {}
                else:
                    prev = prev_positions[hand_type]
                    if prev:
                        canvas.draw_line(prev, index_finger, HAND_COLORS[hand_type], DRAW_THICKNESS)
                    prev_positions[hand_type] = index_finger

    frame = canvas.merge_with_frame(frame)
    cv2.imshow("AugmentedReality Drawing App", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        if canvas is not None:
            canvas.clear()  # Clear the screen
    elif key == ord('q'):
        break  # Exit the loop

cap.release()
cv2.destroyAllWindows()
