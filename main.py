"""Launch Gesture Bird."""

import sys

import cv2
import pygame

from game.game import Game
from vision.camera import Camera, CameraError
from vision.gesture_controller import GestureController
from vision.hand_tracker import HandTracker


def run() -> int:
    pygame.init()
    screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
    pygame.display.set_caption("Gesture Bird")
    clock = pygame.time.Clock()
    game = Game()
    camera = None
    tracker = None
    gesture = GestureController()
    camera_error = ""
    preview = None
    vision_elapsed = 0.0
    running = True

    try:
        while running:
            dt = min(clock.tick(60) / 1000.0, 0.05)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    if camera is None:
                        try:
                            camera = Camera()
                            tracker = HandTracker()
                            gesture.reset()
                            camera_error = "Gesture control on"
                        except (CameraError, RuntimeError) as error:
                            camera_error = str(error)
                            if camera is not None:
                                camera.close()
                            camera = None
                            tracker = None
                    else:
                        tracker.close()
                        camera.close()
                        camera = None
                        tracker = None
                        preview = None
                        camera_error = "Gesture control off"
                elif event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_SPACE,
                    pygame.K_UP,
                ):
                    game.flap()
                elif event.type == pygame.KEYDOWN:
                    running = game.handle_key(event.key)

            vision_elapsed += dt
            if camera is not None and tracker is not None and vision_elapsed >= 1 / 30:
                vision_elapsed = 0.0
                try:
                    frame = camera.read()
                    if frame is None:
                        camera_error = "Camera frame unavailable"
                    else:
                        frame, landmarks = tracker.process(frame)
                        preview = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        if gesture.update(landmarks):
                            game.flap()
                except (CameraError, RuntimeError) as error:
                    camera_error = str(error)
                    tracker.close()
                    camera.close()
                    camera = None
                    tracker = None
                    preview = None

            game.update(dt)
            game.draw(screen, preview=preview, status=camera_error)
            pygame.display.flip()
    finally:
        if tracker is not None:
            tracker.close()
        if camera is not None:
            camera.close()
        pygame.quit()

    return 0


if __name__ == "__main__":
    sys.exit(run())
