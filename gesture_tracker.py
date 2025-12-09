# gesture_tracker.py
import cv2
import numpy as np
from collections import deque

class GestureTracker:
    """
    Basic HSV + contour + centroid tracking for swipe gesture detection.
    Uses motion direction over the last N frames to infer gestures.
    """

    def __init__(self):
        # HSV range for detecting a green glove/object
        self.lower = (35, 60, 60)
        self.upper = (85, 255, 255)

        # Store last positions
        self.history = deque(maxlen=10)

        # Gesture parameters
        self.min_motion = 40         # pixels needed to count as a swipe
        self.direction_cooldown = 0  # frames until next gesture allowed
        self.cooldown_frames = 6

    def process_frame(self, frame):
        """
        Input: BGR frame from webcam
        Output: (detected_gesture, annotated_frame)
        """
        frame = cv2.flip(frame, 1)
        annotated = frame.copy()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)

        # Clean mask
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        gesture = None
        center = None

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            M = cv2.moments(c)
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                if radius > 10:
                    cv2.circle(annotated, (int(x), int(y)), int(radius), (0,255,255), 2)
                    cv2.circle(annotated, center, 5, (0,255,255), -1)

                    self.history.appendleft(center)

        # Detect gesture only if enough points exist
        if len(self.history) >= 5 and self.direction_cooldown == 0:
            dx = self.history[0][0] - self.history[-1][0]
            dy = self.history[0][1] - self.history[-1][1]

            # Horizontal swipe
            if abs(dx) > abs(dy) and abs(dx) > self.min_motion:
                gesture = "RIGHT" if dx > 0 else "LEFT"

            # Vertical swipe
            elif abs(dy) > self.min_motion:
                gesture = "DOWN" if dy > 0 else "UP"

            if gesture is not None:
                self.direction_cooldown = self.cooldown_frames

        # Cooldown update
        if self.direction_cooldown > 0:
            self.direction_cooldown -= 1

        # Draw gesture text
        if gesture:
            cv2.putText(annotated, f"Gesture: {gesture}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        return gesture, annotated
