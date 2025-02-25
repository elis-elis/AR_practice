"""
Handles all drawing operations, including:
✅ Drawing lines with fingers
✅ Erasing with gestures
✅ Merging drawings with the webcam feed
✅ Clearing the canvas
"""

import cv2
import numpy as np

class DrawingCanvas:
    """
    A class to manage a virtual drawing canvas.

    Attributes:
        canvas (numpy.ndarray): The blank canvas used for drawing.
    """
    def __init__(self, frame_shape):
        """
        Initializes the drawing canvas to match the webcam frame size.

        Args:
            frame_shape (numpy.ndarray): The shape of the webcam frame.
        """
        self.canvas = np.zeros_like(frame_shape)  # Create a blank canvas

    def draw_line(self, start, end, color=(0, 255, 0), thickness=5):
        """
        Draws a line on the canvas.

        Args:
            start (tuple): Starting coordinates (x, y).
            end (tuple): Ending coordinates (x, y).
            color (tuple): Line color (default: green).
            thickness (int): Line thickness.
        """
        cv2.line(self.canvas, start, end, color, thickness)

    def erase(self, position, size=20):
        """
        Erases part of the canvas by drawing a black circle.

        Args:
            position (tuple): Center of the eraser (x, y).
            size (int): Radius of the eraser.
        """
        cv2.circle(self.canvas, position, size, (0, 0, 0), -1)
    
    def merge_with_frame(self, frame):
        """
        Merges the canvas with the webcam frame.

        Args:
            frame (numpy.ndarray): The original webcam frame.

        Returns:
            numpy.ndarray: The combined frame.
        """
        return cv2.addWeighted(frame, 0.5, self.canvas, 0.5, 0)  # Overlay drawing on webcam
    
    def clear(self):
        """
        Clears the canvas by setting all pixels to black.
        """
        self.canvas[:] = 0
