"""MediaPipe hand landmark detection."""

import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self) -> None:
        if not hasattr(mp, "solutions"):
            raise RuntimeError(
                "This game requires MediaPipe 0.10.21; install dependencies from requirements.txt."
            )
        self._hands_api = mp.solutions.hands
        self._drawing = mp.solutions.drawing_utils
        self._hands = self._hands_api.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.55,
        )

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb)
        landmarks = None
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            self._drawing.draw_landmarks(
                frame, hand, self._hands_api.HAND_CONNECTIONS
            )
            landmarks = [(point.x, point.y) for point in hand.landmark]
        return frame, landmarks

    def close(self) -> None:
        self._hands.close()