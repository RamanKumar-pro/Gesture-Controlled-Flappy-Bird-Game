"""OpenCV camera lifecycle."""

import platform

import cv2


class CameraError(RuntimeError):
    """Raised when a camera cannot be opened or read."""


class Camera:
    def __init__(self, index: int = 0, width: int = 640, height: int = 480) -> None:
        if platform.system() == "Windows":
            self.capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if not self.capture.isOpened():
                self.capture.release()
                self.capture = cv2.VideoCapture(index, cv2.CAP_MSMF)
        else:
            self.capture = cv2.VideoCapture(index)
        if not self.capture.isOpened():
            self.capture.release()
            raise CameraError(
                f"Could not open camera {index}. Check camera permissions or try another index."
            )
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        success, frame = self.capture.read()
        if not success or frame is None:
            raise CameraError("Could not read from the webcam.")
        return cv2.flip(frame, 1)

    def close(self) -> None:
        if self.capture is not None:
            self.capture.release()
            self.capture = None