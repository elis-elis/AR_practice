"""
Handles all drawing operations, including:
✅ Drawing lines with fingers
✅ Erasing with gestures
✅ Merging drawings with the webcam feed
✅ Clearing the canvas
"""

import cv2
import numpy as np
from utils import calculate_distance


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

    # def draw_dual_line(start1, end1, start2, end2, color1, color2):

    # def switch_color(current_color):

    def erase(self, index_finger, middle_finger, size=20):
        """
        Erases part of the canvas by drawing a black line between two fingers.

        Args:
            index_finger (tuple): Position of the index finger (x, y).
            middle_finger (tuple): Position of the middle finger (x, y).
            size (int): Thickness of the eraser.
        """
        cv2.line(self.canvas, index_finger, middle_finger, (0, 0, 0), size)
    
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


def draw_dual_finger_lines(canvas, prev_fingers, current_fingers, color, thickness):
    """
    This function is a helper function, not a method of the DrawingCanvas class. It uses the existing method draw_line() from the canvas to draw two lines:
    one for the left hand's index finger and one for the right hand's index finger, if both are available.

    It checks if each hand has a previous and current finger position, and draws a line between them on the canvas.

    Args:
        canvas (DrawingCanvas): The canvas to draw on.
        prev_fingers (dict): Previous index finger positions. Format: {'Left': (x, y), 'Right': (x, y)}.
        current_fingers (dict): Current index finger positions. Same format.
        color (tuple): BGR color.
        thickness (int): Line thickness.
    """
    for hand in ['Left', 'Right']:
        prev = prev_fingers.get(hand)
        curr = current_fingers.get(hand)
        if prev and curr:
            canvas.draw_line(prev, curr, color, thickness)


def handle_erase_if_close(canvas, index_tip, middle_tip, threshold, size):
    """
    Checks if two fingers are close enough to trigger erase,
    and applies erasing on the canvas if they are.

    Args:
        canvas (DrawingCanvas): Your drawing surface.
        index_tip (tuple): (x, y) of index finger.
        middle_tip (tuple): (x, y) of middle finger.
        threshold (float): Max distance between fingers to trigger erase.
        size (int): Eraser size (radius).
    
    Returns:
        bool: True if erase occurred, else False.
    """
    if index_tip and middle_tip:
        distance = calculate_distance(index_tip, middle_tip)
        if distance < threshold:
            canvas.erase(index_tip, middle_tip, size)
            return True
    
    return False
