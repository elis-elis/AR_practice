"""
NumPy – for numerical operations (e.g., working with arrays, images, and points).
OpenCV-Contrib-Python – contains additional OpenCV modules that may be useful later.
Matplotlib – useful for debugging and visualization.
"""

import cv2
import mediapipe as mp

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
        break

    # Flip the frame horizontally (like a mirror image)
    frame = cv2.flip(frame, 1)

    # Display the current frame in a window named 'Webcam Feed'
    cv2.imshow('Webcam Feed', frame)

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
