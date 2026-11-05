"""Pipe obstacle data and deterministic movement."""

import random
from dataclasses import dataclass

import pygame


@dataclass
class PipePair:
    x: float
    gap_y: float
    gap_size: int
    width: int
    scored: bool = False

    @property
    def gap_top(self) -> int:
        return round(self.gap_y - self.gap_size / 2)

    @property
    def gap_bottom(self) -> int:
        return round(self.gap_y + self.gap_size / 2)

    def collides(self, bird: pygame.Rect, ground_y: int) -> bool:
        pipe = pygame.Rect(round(self.x), 0, self.width, ground_y)
        if not pipe.colliderect(bird):
            return False
        return bird.top < self.gap_top or bird.bottom > self.gap_bottom


class PipeField:
    def __init__(
        self,
        screen_width: int,
        ground_y: int,
        gap_size: int = 168,
        spacing: int = 220,
        width: int = 72,
        speed: float = 190.0,
    ) -> None:
        self.screen_width = screen_width
        self.ground_y = ground_y
        self.gap_size = gap_size
        self.spacing = spacing
        self.width = width
        self.speed = speed
        self.pipes: list[PipePair] = []
        self.reset()

    def reset(self) -> None:
        self.pipes = [self._new_pipe(self.screen_width + 90)]

    def _new_pipe(self, x: float) -> PipePair:
        margin = 78 + self.gap_size // 2
        low = min(margin, self.ground_y - 78 - self.gap_size // 2)
        high = max(low, self.ground_y - 78 - self.gap_size // 2)
        return PipePair(
            x=x,
            gap_y=float(random.randint(low, high)),
            gap_size=self.gap_size,
            width=self.width,
        )

    def update(self, dt: float) -> None:
        for pipe in self.pipes:
            pipe.x -= self.speed * dt
        self.pipes = [pipe for pipe in self.pipes if pipe.x + self.width > 0]
        while not self.pipes or max(pipe.x for pipe in self.pipes) < self.screen_width:
            next_x = (
                max((pipe.x for pipe in self.pipes), default=self.screen_width)
                + self.spacing
            )
            self.pipes.append(self._new_pipe(next_x))

    def collides(self, bird: pygame.Rect) -> bool:
        return any(pipe.collides(bird, self.ground_y) for pipe in self.pipes)

    def passed(self, bird_x: float) -> int:
        count = 0
        for pipe in self.pipes:
            if not pipe.scored and pipe.x + pipe.width < bird_x:
                pipe.scored = True
                count += 1
        return count