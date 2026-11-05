"""Flappy Bird game state, rendering, and controls."""

import math
from enum import Enum, auto
from pathlib import Path

import pygame

from game.bird import Bird
from game.pipes import PipeField


class State(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

# w: 480, h: 640
class Game:
    WIDTH = 1080
    HEIGHT = 640
    GROUND_HEIGHT = 92
    BIRD_X = 125
    ROOT = Path(__file__).resolve().parent.parent

    def __init__(self) -> None:
        self.ground_y = self.HEIGHT - self.GROUND_HEIGHT
        self.state = State.MENU
        self.score = 0
        self.best_score = 0
        self.bird = Bird(self.BIRD_X, self.HEIGHT * 0.42)
        self.pipes = PipeField(self.WIDTH, self.ground_y)
        self.ground_offset = 0.0
        self.animation_time = 0.0
        self._load_assets()

    def _load_assets(self) -> None:
        sprites = self.ROOT / "assets" / "sprites"
        self.background = pygame.transform.scale(
            pygame.image.load(str(sprites / "background-day.png")).convert(),
            (self.WIDTH, self.ground_y),
        )
        base = pygame.image.load(str(sprites / "base.png")).convert_alpha()
        self.base = pygame.transform.scale(base, (self.WIDTH, self.GROUND_HEIGHT))
        bird_names = (
            "yellowbird-downflap.png",
            "yellowbird-midflap.png",
            "yellowbird-upflap.png",
        )
        self.bird_frames = [
            pygame.transform.scale(
                pygame.image.load(str(sprites / name)).convert_alpha(), (44, 32)
            )
            for name in bird_names
        ]
        pipe = pygame.image.load(str(sprites / "pipe-green.png")).convert_alpha()
        self.pipe_image = pygame.transform.scale(pipe, (self.pipes.width, 420))
        self.top_pipe_image = pygame.transform.flip(self.pipe_image, False, True)
        self.font = pygame.font.Font(None, 38)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 64)

    def flap(self) -> None:
        if self.state in (State.MENU, State.GAME_OVER):
            self.start()
            return
        if self.state == State.PLAYING:
            self.bird.flap()

    def start(self) -> None:
        self.score = 0
        self.bird = Bird(self.BIRD_X, self.HEIGHT * 0.42)
        self.pipes.reset()
        self.state = State.PLAYING
        self.bird.flap()

    def handle_key(self, key: int) -> bool:
        if key == pygame.K_q:
            return False
        if key in (pygame.K_ESCAPE, pygame.K_p):
            if self.state == State.PLAYING:
                self.state = State.PAUSED
            elif self.state == State.PAUSED:
                self.state = State.PLAYING
            return True
        if key in (pygame.K_r, pygame.K_RETURN) and self.state in (
            State.MENU,
            State.GAME_OVER,
        ):
            self.start()
        return True

    def update(self, dt: float) -> None:
        if self.state == State.MENU:
            self.animation_time += dt
            self.bird.y = self.HEIGHT * 0.42 + 8 * math.sin(self.animation_time * 3)
            self.ground_offset = (self.ground_offset + 42 * dt) % self.WIDTH
            return
        if self.state != State.PLAYING:
            return

        self.animation_time += dt
        self.bird.update(dt)
        self.pipes.update(dt)
        self.score += self.pipes.passed(self.bird.x)
        self.ground_offset = (self.ground_offset + 190 * dt) % self.WIDTH

        if (
            self.bird.rect.top < 0
            or self.bird.rect.bottom >= self.ground_y
            or self.pipes.collides(self.bird.rect)
        ):
            self.best_score = max(self.best_score, self.score)
            self.state = State.GAME_OVER

    def draw(self, surface: pygame.Surface, preview=None, status: str = "") -> None:
        surface.blit(self.background, (0, 0))
        for pipe in self.pipes.pipes:
            x = round(pipe.x)
            top_y = pipe.gap_top - self.pipe_image.get_height()
            surface.blit(self.top_pipe_image, (x, top_y))
            surface.blit(self.pipe_image, (x, pipe.gap_bottom))

        if self.state != State.GAME_OVER:
            frame = self.bird_frames[int(self.animation_time * 12) % len(self.bird_frames)]
            angle = max(-25, min(70, -self.bird.velocity * 0.075))
            rotated = pygame.transform.rotate(frame, angle)
            surface.blit(
                rotated,
                rotated.get_rect(center=(round(self.bird.x), round(self.bird.y))),
            )

        for offset in (0, self.WIDTH):
            surface.blit(self.base, (round(offset - self.ground_offset), self.ground_y))

        if self.state == State.MENU:
            self._center_text(surface, "GESTURE BIRD", self.title_font, 185, (255, 255, 255))
            self._center_text(surface, "SPACE / open palm to flap", self.small_font, 244)
            self._center_text(surface, "Press C to enable webcam control", self.small_font, 273)
            self._center_text(surface, "Avoid the pipes!", self.small_font, 302)
        elif self.state == State.PLAYING:
            self._center_text(surface, str(self.score), self.title_font, 64)
        elif self.state == State.PAUSED:
            self._center_text(surface, "PAUSED", self.title_font, 245, (255, 255, 255))
            self._center_text(surface, "P / Esc to resume", self.small_font, 286)
        elif self.state == State.GAME_OVER:
            self._center_text(surface, "GAME OVER", self.title_font, 220, (255, 255, 255))
            self._center_text(surface, f"Score  {self.score}     Best  {self.best_score}", self.font, 276)
            self._center_text(surface, "SPACE / R to play again", self.small_font, 322)

        if status:
            self._text(surface, status[:60], (10, 10), self.small_font, (255, 240, 190))
        if preview is not None:
            rgb = pygame.surfarray.make_surface(preview.swapaxes(0, 1))
            preview_surface = pygame.transform.scale(rgb, (160, 120))
            surface.blit(preview_surface, (self.WIDTH - 170, 10))
            pygame.draw.rect(surface, (255, 255, 255), (self.WIDTH - 170, 10, 160, 120), 2)

    def _center_text(
        self,
        surface: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        y: int,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        image = font.render(text, True, color)
        rect = image.get_rect(center=(self.WIDTH // 2, y))
        shadow = font.render(text, True, (64, 74, 79))
        surface.blit(shadow, rect.move(2, 2))
        surface.blit(image, rect)

    @staticmethod
    def _text(
        surface: pygame.Surface,
        text: str,
        position: tuple[int, int],
        font: pygame.font.Font,
        color: tuple[int, int, int],
    ) -> None:
        surface.blit(font.render(text, True, color), position)