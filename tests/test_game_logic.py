import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from game.bird import Bird
from game.game import Game, State
from game.pipes import PipeField, PipePair
from vision.gesture_controller import GestureController


class BirdTests(unittest.TestCase):
    def test_flap_and_gravity_are_applied_over_time(self):
        bird = Bird(100, 100)
        bird.flap()
        self.assertLess(bird.velocity, 0)
        bird.update(0.1)
        self.assertLess(bird.y, 100)
        self.assertGreater(bird.velocity, bird.flap_velocity)


class PipeTests(unittest.TestCase):
    def test_gap_allows_bird_and_pipe_edges_collide(self):
        pair = PipePair(x=100, gap_y=200, gap_size=100, width=70)
        self.assertFalse(pair.collides(pygame.Rect(110, 180, 20, 20), 500))
        self.assertTrue(pair.collides(pygame.Rect(110, 120, 20, 20), 500))

    def test_pipe_pair_scores_only_once(self):
        field = PipeField(screen_width=480, ground_y=500)
        field.pipes[0].x = 20
        self.assertEqual(field.passed(100), 1)
        self.assertEqual(field.passed(100), 0)


class GestureTests(unittest.TestCase):
    @staticmethod
    def open_palm():
        points = [(0.5, 0.5)] * 21
        for tip, joint in ((8, 6), (12, 10), (16, 14), (20, 18)):
            points[joint] = (0.5, 0.5)
            points[tip] = (0.5, 0.3)
        return points

    def test_open_palm_flaps_once_until_rearmed(self):
        controller = GestureController(cooldown=0.2, required_frames=2)
        hand = self.open_palm()
        self.assertFalse(controller.update(hand, 1.0))
        self.assertTrue(controller.update(hand, 1.1))
        self.assertFalse(controller.update(hand, 2.0))
        self.assertFalse(controller.update(None, 2.1))
        self.assertFalse(controller.update(hand, 2.2))
        self.assertTrue(controller.update(hand, 2.3))


class GameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_game_starts_and_pauses(self):
        game = Game()
        game.flap()
        self.assertEqual(game.state, State.PLAYING)
        surface = pygame.Surface((Game.WIDTH, Game.HEIGHT))
        game.draw(surface)
        game.handle_key(pygame.K_p)
        self.assertEqual(game.state, State.PAUSED)
        game.handle_key(pygame.K_p)
        self.assertEqual(game.state, State.PLAYING)
        game.bird.y = game.ground_y
        game.update(0)
        self.assertEqual(game.state, State.GAME_OVER)
        game.draw(surface)


if __name__ == "__main__":
    unittest.main()
