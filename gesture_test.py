"""Show webcam hand landmarks; press Q or Escape to exit."""

import cv2

from vision.camera import Camera
from vision.hand_tracker import HandTracker


def main() -> None:
    tracker = HandTracker()
    camera = None
    try:
        camera = Camera()
        while True:
            frame, _ = tracker.process(camera.read())
            cv2.imshow("Gesture Bird - Hand Tracking", frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                break
    finally:
        tracker.close()
        if camera is not None:
            camera.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()