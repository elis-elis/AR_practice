import cv2
from modules.hand_tracker import HandTracker
from modules.drawing import DrawingCanvas
from modules.drawing import handle_erase_if_close
from modules.color_manager import ColorManager


DRAW_THRESHOLD = 40
ERASER_SIZE = 30
HAND_COLORS = {"Left": (0, 255, 0), "Right": (255, 182, 193)}
DRAW_THICKNESS = 5

# Initialize modules
cap = cv2.VideoCapture(2)  # Open webcam
tracker = HandTracker()  # Hand tracking module
canvas = None  # Drawing canvas (initialized later)
prev_positions = {"Left": None, "Right": None}  # Store previous hand position
color_manager = ColorManager()
current_color = color_manager.current_color()

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
            tracker.draw_landmarks(frame, hand_landmarks)

            index_finger = fingers.get("index")
            middle_finger = fingers.get("middle")

            if index_finger and middle_finger:  # Ensure both fingers are detected
                erased = handle_erase_if_close(canvas, index_finger, middle_finger, DRAW_THRESHOLD, ERASER_SIZE)
                
                if erased:
                    mode = "erasing"
                    prev_positions[hand_type] = None  # stop drawing while erasing
                else:
                    mode = "drawing"
                    prev = prev_positions[hand_type]
                    if prev:
                        canvas.draw_line(prev, index_finger, current_color, DRAW_THICKNESS)
                    prev_positions[hand_type] = index_finger

        # show mode on screen
        height = frame.shape[0]
        if mode == "erasing":
            cv2.putText(frame, "erasing when index + middle fingers are together", (20, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        elif mode == "drawing":
            cv2.putText(frame, "drawing", (20, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    
    frame = canvas.merge_with_frame(frame)

    cv2.rectangle(frame, (10, 10), (60, 60), current_color, -1)
    cv2.putText(frame, "color", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    
    cv2.imshow("AugmentedReality Drawing App", frame)


    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        if canvas is not None:
            canvas.clear()  # Clear the screen
    elif key == ord('n'):  # 'n' for next color
        current_color = color_manager.next_color()
    elif key == ord('q'):
        break  # Exit the loop

cap.release()
cv2.destroyAllWindows()
