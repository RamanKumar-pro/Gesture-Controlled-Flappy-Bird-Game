"""Bird physics and collision bounds."""

from dataclasses import dataclass

import pygame


@dataclass
class Bird:
    x: float
    y: float
    width: int = 34
    height: int = 24
    velocity: float = 0.0
    gravity: float = 1250.0
    flap_velocity: float = -390.0

    def flap(self) -> None:
        self.velocity = self.flap_velocity

    def update(self, dt: float) -> None:
        self.velocity += self.gravity * dt
        self.y += self.velocity * dt

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.x - self.width / 2),
            round(self.y - self.height / 2),
            self.width,
            self.height,
        )