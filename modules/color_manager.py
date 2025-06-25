class ColorManager:
    """
    This class manages drawing colors, it cycles through colors.
    """
    def __init__(self):
        """
        self.colors: A list of color values in BGR (used by OpenCV)
        self.index: Starts at 0, meaning first color (Blue) is selected.
        """
        self.colors = [(0, 0, 255), (0, 255, 0), (255, 182, 193)] # Red, Green, Pink
        self.index = 0

    def next_color(self):
        """
        self.index + 1 → move to next color in the list.
        % len(self.colors) → cycles back to 0 if we go past the last color (looping).
        return self.current_color() → return the new color.
        """
        self.index = (self.index + 1) % len(self.colors)
        return self.current_color()
    
    def current_color(self):
        """
        Returns the color that’s currently selected by index.
        """
        return self.colors[self.index]
    