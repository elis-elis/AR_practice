"""
NumPy – for numerical operations (e.g., working with arrays, images, and points).
OpenCV-Contrib-Python – contains additional OpenCV modules that may be useful later.
Matplotlib – useful for debugging and visualization.
"""

import cv2
import mediapipe as mp

# Initialize the MediaPipe Hands module
mp_hands = mp.solutions.hands  # Load the hand-tracking solution from MediaPipe
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Open webcam
# The argument '0' specifies the default camera (usually the built-in webcam).
cap = cv2.VideoCapture(0)

# Start an infinite loop to continuously capture video frames from the webcam
while cap.isOpened:
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

    # If hands are detected in the frame
    if result.multi_hand_landmarks:
        # Iterate through all detected hands
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


            # Calculate the pixel coordinates of the tip of the index finger


    # Display the current frame in a window named 'Hand Tracking'
    cv2.imshow('Hand Tracking', frame)

    # Wait for a key press for 1 millisecond
    # If the 'q' key is pressed, break the loop to stop the video feed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
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
cv2.destroyAllWindows
