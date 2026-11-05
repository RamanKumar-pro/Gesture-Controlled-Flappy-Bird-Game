"""Convert hand landmarks into one-shot open-palm flap actions."""

import time


class GestureController:
    def __init__(self, cooldown: float = 0.45, required_frames: int = 3) -> None:
        self.cooldown = cooldown
        self.required_frames = required_frames
        self._open_frames = 0
        self._armed = True
        self._last_flap = float("-inf")

    @staticmethod
    def is_open_palm(landmarks) -> bool:
        if landmarks is None or len(landmarks) < 21:
            return False
        return all(
            landmarks[tip][1] < landmarks[joint][1]
            for tip, joint in ((8, 6), (12, 10), (16, 14), (20, 18))
        )

    def update(self, landmarks, now: float | None = None) -> bool:
        current_time = time.monotonic() if now is None else now
        if not self.is_open_palm(landmarks):
            self._open_frames = 0
            self._armed = True
            return False

        self._open_frames += 1
        if (
            self._armed
            and self._open_frames >= self.required_frames
            and current_time - self._last_flap >= self.cooldown
        ):
            self._last_flap = current_time
            self._armed = False
            return True
        return False

    def reset(self) -> None:
        self._open_frames = 0
        self._armed = True
        self._last_flap = float("-inf")