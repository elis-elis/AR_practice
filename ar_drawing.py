"""
NumPy – for numerical operations (e.g., working with arrays, images, and points).
OpenCV-Contrib-Python – contains additional OpenCV modules that may be useful later.
Matplotlib – useful for debugging and visualization.
"""
"""
this code:
Opens the webcam using OpenCV.
Converts frames from BGR to RGB (because Mediapipe requires RGB).
Uses Mediapipe's Hand Tracking to detect hands in real-time.
Draws hand landmarks and connections on the screen.
Closes the webcam if you press 'q'.
Flipping the video – Makes it behave like a mirror.
Drawing on a separate canvas – Prevents the drawing from being erased when the frame updates.
Using cv2.line() – Connects the previous finger position to the new one, simulating drawing.
Merging the drawing with the webcam feed – Makes it look like AR.
"""

import cv2
import mediapipe as mp
import numpy as np

# Initialize the MediaPipe Hands module
mp_hands = mp.solutions.hands  # Load the hand-tracking solution from MediaPipe
hands = mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)
mp_draw = mp.solutions.drawing_utils

for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Capera index {i} is available")
        cap.release()

# Open webcam (Try different indexes if needed)
# The argument '2' specifies the default camera (the built-in webcam).
cap = cv2.VideoCapture(2)

# Create a blank canvas that matches the frame size
canvas = None

# Previous finger positions
prev_x, prev_y = None, None
prev_mx, prev_my = None, None  # Track middle finger position

# Start an infinite loop to continuously capture video frames from the webcam
while cap.isOpened():
    # Read a single frame from the webcam
    # `success` is a boolean indicating success; `frame` is the captured frame.
    success, frame = cap.read()

    # Check if the frame was successfully captured
    # If not, break the loop and stop the video capture process.
    if not success:
        continue

    # Flip the frame horizontally (like a mirror image)
    frame = cv2.flip(frame, 1)
    # Convert the frame from BGR (OpenCV default) to RGB (MediaPipe requirement)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the RGB frame to detect and track hands
    result = hands.process(rgb_frame)

    # Ensure canvas has the same shape as frame, and created only once and resized if needed.
    if canvas is None or canvas.shape != frame.shape:
        canvas = np.zeros_like(frame)

    # If hands are detected in the frame
    if result.multi_hand_landmarks:
        # Iterate through all detected hands
        for hand_landmarks in result.multi_hand_landmarks:
            # Get index finger tip position (landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            # Get the frame dimensions (height and width)
            h, w, _ = frame.shape

            # Get Index Finger Position
            cx, cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w), \
                     int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)
            # Get Middle Finger Position
            mx, my = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * w), \
                     int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h)

            # Calculate distance between index and middle fingers (for erasing)
            distance = np.sqrt((cx - mx) ** 2 + (cy - my) ** 2)

            # Draw fingertip circles
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)  # Index finger (Green)
            cv2.circle(frame, (mx, my), 10, (255, 182, 193), -1)  # Middle finger (Pink)

            # If the distance is small, erase instead of drawing
            if distance < 40:  # Threshold for eraser mode
                cv2.circle(canvas, (cx, cy), 30, (0, 0, 0), -1)  # Erase with black
                cv2.blur(canvas, (20, 20))
            else:
                if cy < my:  # If index finger is higher, draw with index finger (green)
                    if prev_x is not None and prev_y is not None:
                        cv2.line(canvas, (prev_x, prev_y), (cx, cy), (0, 255, 0), 5)
                    prev_x, prev_y = cx, cy
                    prev_mx, prev_my = None, None  # Reset middle finger tracking
                
                elif my < cy:  # If middle finger is higher, draw with middle finger (pink)
                    if prev_mx is not None and prev_my is not None:
                        cv2.line(canvas, (prev_mx, prev_my), (mx, my), (255, 182, 193), 5)
                    prev_mx, prev_my = mx, my
                    prev_x, prev_y = None, None  # Reset index finger tracking

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Merge canvas with frame
    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Display the current frame in a window named 'AR Drawing'
    cv2.imshow('AR Drawing', frame)

    # Clear screen when 'c' is pressed
    # If the 'q' key is pressed, break the loop to stop the video feed.
    key = cv2.waitKey(1) & 0xFF 
    if key == ord('c'):
        canvas[:] = 0
    elif key == ord('q'):
        break
    """
    When using cv2.waitKey() in OpenCV, the returned key code may include extra bits depending 
    on the platform. To ensure you correctly detect key presses, you can mask the result with 
    0xFF to isolate the lower 8 bits (the actual ASCII value). Without this, your key comparisons 
    might fail on some systems—so always use & 0xFF for consistent behavior!
    """

# Release the webcam resource to make it available for other programs
cap.release()

# Close all OpenCV-created windows
cv2.destroyAllWindows()
