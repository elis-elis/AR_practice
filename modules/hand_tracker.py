"""
This class handles hand tracking using MediaPipe.
✅ Detects hands from the webcam feed.
✅ Extracts finger positions.
✅ Draws landmarks on the hand.
"""

import cv2
import mediapipe as mp


class HandTracker:
    """
    A class to track hands using MediaPipe.

    Attributes:
        hands (mp.solutions.hands.Hands): MediaPipe hand detection model.
        mp_draw (mp.solutions.drawing_utils): Utility for drawing hand landmarks.
    """
    def __init__(self, detection_conf=0.8, tracking_conf=0.8):
        """
        Initializes the hand tracking model.

        Args:
            detection_conf (float): Confidence threshold for detecting hands.
            tracking_conf (float): Confidence threshold for tracking hands.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=detection_conf,
                                        min_tracking_confidence=tracking_conf)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        """
        Detects hands in a given frame.

        Args:
            frame (numpy.ndarray): The input frame from the webcam.

        Returns:
            results (mediapipe.python.solution_base.SolutionOutputs): Hand landmarks detected.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        return self.hands.process(rgb_frame)  # Process frame to detect hands


    def get_finger_positions(self, hand_landmarks, frame_shape):
            """
            Extracts the index and middle finger positions and returns them as a dictionary.
            """
            h, w, _ = frame_shape
            fingers = {}

            if hand_landmarks:
                fingers["index"] = (
                    int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].x * w),
                    int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y * h)
                )

                fingers["middle"] = (
                    int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP].x * w),
                    int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP].y * h)
                )

            return fingers

    def draw_landmarks(self, frame, hand_landmarks):
        """
        Draws hand landmarks on the frame.

        Args:
            frame (numpy.ndarray): The frame where landmarks should be drawn.
            hand_landmarks (mediapipe.python.solutions.hands.HandLandmarks): Detected landmarks.
        """
        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
