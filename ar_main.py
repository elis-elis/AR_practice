import cv2
from modules.hand_tracker import HandTracker
from modules.drawing import DrawingCanvas
from modules.utils import calculate_distance

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

            index = fingers.get("index")
            middle = fingers.get("middle")

            if index and middle:  # Ensure both fingers are detected
                distance = calculate_distance(index, middle)

                # Erase if index & middle fingers are close together
                if distance < DRAW_THRESHOLD:
                    canvas.erase(index, middle, ERASER_SIZE)
                    prev_positions[hand_type] = None
                else:
                    prev = prev_positions[hand_type]
                    if prev:
                        canvas.draw_line(prev, index, HAND_COLORS[hand_type], DRAW_THICKNESS)
                    prev_positions[hand_type] = index

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
