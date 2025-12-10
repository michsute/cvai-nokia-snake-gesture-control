# game_manager.py
import cv2
import pygame
import time
import threading
import os

from gesture_tracker import GestureTracker
from snake_game import SnakeGame

class GameManager:
    """
    Links gesture detection with the SnakeGame.
    Runs gesture tracking in a separate thread.
    """

   def __init__(self):
        # Move the game window to the right side of the screen 
        os.environ['SDL_VIDEO_WINDOW_POS'] = "1000,200"
        pygame.init()
       
        self.game = SnakeGame()
        self.tracker = GestureTracker()

        self.cap = None
        self.running = True

        self.current_gesture = None

    def init_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("ERROR: Cannot open camera")
            return False
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        return True

    def gesture_loop(self):
        """Runs independently: detects gestures while game runs in pygame."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            gesture, annotated = self.tracker.process_frame(frame)
            self.current_gesture = gesture

             # --- WINDOWS USERS: ENABLE PREVIEW HERE ---------------------------
            #
            # On Windows or Linux, you can uncomment the block below to enable 
            # a live OpenCV preview window for gesture tracking.
            #
            # WARNING (macOS users): DO NOT UNCOMMENT. 
            # cv2.imshow WILL CRASH on macOS (Python 3.13 + OpenCV backend).
            #
            """
            cv2.imshow("Gesture Tracking", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break
            """
            # -------------------------------------------------------------------

            if gesture:
                print("Gesture detected:", gesture)

            time.sleep(0.03)


    def run(self):
        if not self.init_camera():
            return

        # Background thread
        gesture_thread = threading.Thread(target=self.gesture_loop, daemon=True)
        gesture_thread.start()

        last_update = time.time()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            # Apply gesture to snake
            if self.current_gesture:
                self.game.change_direction(self.current_gesture)
                self.game.handle_restart(self.current_gesture)

            # Update snake at speed defined inside SnakeGame
            if time.time() - last_update > 1.0 / self.game.get_current_speed():
                self.game.update()
                last_update = time.time()

            self.game.draw()
            self.game.clock.tick(60)

        self.cleanup()

    def cleanup(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.game.quit()

