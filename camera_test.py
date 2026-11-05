"""Show a mirrored webcam preview; press Q or Escape to exit."""

import cv2

from vision.camera import Camera


def main() -> None:
    camera = Camera()
    try:
        while True:
            frame = camera.read()
            cv2.imshow("Gesture Bird - Camera Test", frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                break
    finally:
        camera.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()