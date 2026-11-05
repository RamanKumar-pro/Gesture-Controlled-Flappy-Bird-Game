# Gesture Bird

A desktop Flappy Bird-style game built with Python and Pygame. Flap with
the keyboard or enable webcam control to flap with an open-palm gesture.
The game uses OpenCV for camera capture and MediaPipe for hand tracking.

## Features

- Animated bird, scrolling pipes, collision detection, and score tracking.
- Menu, gameplay, pause, and game-over screens.
- Keyboard controls; a webcam is optional.
- Optional mirrored webcam preview with hand landmark visualization.
- Open-palm gesture detection with consecutive-frame confirmation and
  neutral-pose re-arming.

## Requirements

- Python 3.11 or 3.12.
- A webcam for gesture controls (optional).
- Windows, macOS, or Linux.

## Install

Clone the repository and enter its directory:

```shell
git clone https://github.com/RamanKumar-pro/Gesture-Controlled-Flappy-Bird-Game.git
cd Gesture-Controlled-Flappy-Bird-Game
```

Create and activate a virtual environment.

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```shell
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```shell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

MediaPipe 0.10.21 includes the hand-tracking model used by this project;
no separate model download is required.

## Play

Run the game from the repository root:

```shell
python main.py
```

| Input | Action |
| --- | --- |
| `Space` or `Up` | Start, flap, or restart after game over |
| `C` | Turn webcam gesture control on or off |
| `P` or `Esc` | Pause or resume |
| `R` or `Enter` | Start or restart from the menu or game-over screen |
| `Q` or close the window | Quit |

For gesture control, press `C` and hold an open palm in view of the
camera. Extend your index, middle, ring, and little fingers. A flap is
triggered after the open-palm gesture is seen in three consecutive
camera frames. Close your hand or move it out of view to re-arm the
gesture. The controller applies a 450 ms cooldown.

The first webcam is used by default. Camera selection and requested
resolution (640×480) can be changed in `vision/camera.py`. Grant the
terminal or application camera permission if prompted.

Optional camera and hand-tracking previews:

```shell
python camera_test.py
python gesture_test.py
```

Press `Q` or `Esc` to close either preview. Both require a working
webcam.

## Tests

Run the automated tests from the project root:

```shell
python -m pytest
```

The tests cover bird physics, pipe collisions and scoring, game states,
and gesture re-arming. They do not require a webcam.

## Project layout

```text
assets/
  audio/                 Sound effects
  sprites/               Bird, pipe, background, and UI artwork
game/
  bird.py                Bird physics and collision bounds
  game.py                Game state, rendering, and controls
  pipes.py               Pipe generation, movement, and scoring
vision/
  camera.py              Webcam capture and cleanup
  gesture_controller.py  Open-palm gesture detection
  hand_tracker.py        MediaPipe hand landmark detection
tests/
  test_game_logic.py     Automated game and gesture tests
main.py                  Application entry point
camera_test.py           Standalone webcam preview
gesture_test.py          Standalone hand-tracking preview
requirements.txt         Pinned Python dependencies
```

## Troubleshooting

- **Camera does not open:** Check operating-system camera permissions,
  close other camera applications, or try a different camera index in
  `vision/camera.py`.
- **Gesture control is unavailable:** Install the pinned dependencies
  inside the active virtual environment with
  `python -m pip install -r requirements.txt`.
- **Hand detection is unreliable:** Improve lighting, keep your hand
  fully in frame, and present your palm clearly to the camera.
- **No webcam:** Play with `Space` or the `Up` arrow; webcam control is
  optional.

## Assets and licensing

The artwork and sound assets are provided in `assets/`; see
[`assets/LICENSE`](assets/LICENSE) for their license and attribution.
The root `LICENCE` file is empty, so this repository does not currently
specify a license for its source code.

Gesture Bird is an independent learning project inspired by the
Flappy Bird style of gameplay and is not affiliated with or endorsed by
the original game's creators.
