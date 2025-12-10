# cvai-nokia-snake-gesture-control

# CVAI Project - Nokia Snake Gesture Control 

This project implements a classic Nokia Snake game controlled via swipe gestures using a webcam.  
Gestures are detected in real time with OpenCV, while the game itself is rendered using pygame.

The project combines:
- Computer Vision (gesture tracking)
- Real-time input processing
- A retro-style Snake game :)

---

## Features

- Classic Snake gameplay (Nokia-inspired visuals)
- Real-time gesture detection using webcam
- Swipe gestures:
  - **LEFT**
  - **RIGHT**
  - **UP**
  - **DOWN**
- Color-based tracking (green glove or object)
- Speed boost indicator
- Particle effects when eating fruit
- Gesture detection runs in a separate thread

---

## How Gesture Control Works

1. The webcam captures video frames.
2. Frames are converted to the HSV color space.
3. A green color mask is applied to detect a green object.
4. The centroid of the detected area is tracked across frames.
5. Movement direction over time is interpreted as a swipe gesture.
6. Detected gestures control the snake’s movement.
