Gesture Bird 🐦
A gesture-controlled Flappy Bird-style game built with Python, Pygame,
OpenCV, and MediaPipe. The project combines 2D game development with
real-time computer vision: play with the keyboard or use a hand gesture
detected through your webcam to make the bird flap.
Project status: Keyboard gameplay, webcam hand tracking, and core logic
tests are implemented. Gesture controls require a working webcam;
keyboard play does not.

Table of contents
- Overview
- Goals
- Features
- How it works
- Gesture controls
- Technology stack
- Project structure
- Requirements
- Installation
- MediaPipe model setup
- Running the project
- Configuration and controls
- Development roadmap
- Testing and troubleshooting
- Performance and design notes
- Demo and screenshots
- Contributing
- License
- Acknowledgements
Overview
Gesture Bird is a desktop arcade game inspired by Flappy Bird. The bird
is affected by gravity and must pass through gaps between moving pipe
obstacles. The player can flap using a keyboard key or a hand gesture
recognized from a live webcam feed.

The project is also a practical learning exercise in:
- Building a real-time game loop and 2D game mechanics.
- Capturing and processing webcam frames.
- Detecting hand landmarks with MediaPipe.
- Converting landmark positions into stable, useful controls.
- Designing modular Python code and managing resources.
- Testing, documenting, and publishing a reproducible GitHub project.
The first release targets a local desktop application. A browser or
mobile version may be explored later; it is not required for the initial
release.
Goals
The initial milestone is to deliver these five outcomes:
1. A playable Flappy Bird-style game implemented in Pygame.
2. A working OpenCV webcam preview.
3. A MediaPipe hand detector that locates hand landmarks.
4. One reliable gesture that triggers a flap without repeatedly firing
   on every video frame.
5. A clean GitHub repository with setup instructions, screenshots, and
   a short demo video.
Features
Core game
- Bird movement with gravity and a flap impulse.
- Scrolling pipe obstacles with randomly generated gaps.
- Collision detection against pipes and screen boundaries.
- Score tracking when the bird passes an obstacle.
- Menu, playing, and game-over states.
- Restart support.
- Keyboard control so the game remains playable without a webcam.
Computer vision
- Live webcam capture using OpenCV.
- Mirrored preview for a more natural user experience.
- Hand landmark detection using MediaPipe.
- Landmark and connection visualization for debugging.
- Gesture interpretation in a separate controller module.
- Graceful handling of missing hands and unavailable cameras.
Planned polish
- Sound effects and background music (optional).
- Animated sprites and visual effects.
- Best-score persistence.
- Adjustable gesture sensitivity and cooldown.
- Optional webcam/landmark preview overlay.
- Additional gestures or pose-based controls.
Implementation checklist
- [x] Pygame window and game loop
- [x] Bird physics and keyboard flap
- [x] Pipe generation, movement, and collision detection
- [x] Score, menu, pause, game-over, and restart
- [x] OpenCV webcam preview and MediaPipe hand landmarks
- [x] Open-palm gesture control with debounce and re-arming
- [x] Automated tests for core logic
- [ ] README screenshots and demo video
- [ ] Clean install tested on Windows, macOS, and Linux
How it works
The application is split into three main parts:
Webcam
  |
  v
OpenCV camera capture
  |
  v
MediaPipe hand landmark detection
  |
  v
Gesture controller
  |
  | emits a game action, e.g. FLAP
  v
Pygame game loop <----- Keyboard input
  |
  v
Physics, obstacles, collisions, score, rendering
Processing flow
1. OpenCV reads a frame from the webcam.
2. The frame is converted to the color format expected by the MediaPipe
   API.
3. MediaPipe detects the hand and returns landmark coordinates.
4. The gesture controller interprets the landmarks and determines
   whether a gesture has occurred.
5. The controller emits a discrete action such as FLAP.
6. The Pygame game loop applies the flap impulse and updates the game.
7. Pygame renders the updated game state.
Separation of responsibilities: the game should receive actions such
as FLAP, PAUSE, or RESTART; it should not need to know about
webcam frames or MediaPipe landmark objects. This keeps the game
playable with keyboard input and makes the vision system easier to test
independently.
Gesture controls
Hold an open palm toward the camera. The four fingers (index through
pinky) must be extended; the game triggers one flap after three
consecutive detected frames. Close your hand or move it out of view to
re-arm the gesture. A 450 ms cooldown suppresses accidental repeats.
Use **C** in the game to turn webcam control on or off. If no camera is
available, the game remains playable with the keyboard.
Keyboard fallback
  Input                 Action
  Space / Up arrow    Flap, start, or restart
  C                   Enable/disable webcam gesture control
  P / Esc             Pause/resume
  R / Enter           Restart from the menu or game-over screen
  Q / window close    Quit
Technology stack
  Technology                                 Role
  Python 3.11 / 3.12                        Main programming language
Pygame                                     Game window, rendering, input, sound, and timing
OpenCV                                     Webcam capture, frame conversion, preview, and drawing
MediaPipe                                  Hand landmark detection
NumPy                                      Array operations used by image-processing components
Git and GitHub                             Version control and project hosting
pytest                                     Automated testing
Project structure
gesture-bird/
├── assets/
│   ├── sprites/                 # Bird, pipes, backgrounds, and UI
│   └── audio/                   # Bundled sound effects
├── game/
│   ├── __init__.py
│   ├── bird.py                  # Bird state and physics
│   ├── pipes.py                 # Pipe creation, movement, and collision
│   └── game.py                  # Game states, score, and game orchestration
├── vision/
│   ├── __init__.py
│   ├── camera.py                # OpenCV camera lifecycle and frame capture
│   ├── hand_tracker.py          # MediaPipe hand detection and landmarks
│   └── gesture_controller.py    # Landmark interpretation and game actions
├── tests/                       # Unit and integration tests
├── main.py                      # Application entry point
├── camera_test.py               # Standalone webcam preview
├── gesture_test.py              # Standalone hand-tracking test
├── requirements.txt             # Python dependencies
├── .gitignore
├── README.md
└── LICENSE
Module responsibilities
- main.py: initializes the application, coordinates the game and
  vision components, and handles shutdown.
- game/bird.py: stores bird position and velocity and applies gravity
  and flap impulses.
- game/pipes.py: creates and updates pipe pairs, detects collisions,
  and tracks whether an obstacle has been scored.
- game/game.py: manages game states, score, and rendering.
- vision/camera.py: opens the webcam, reads frames, and releases the
  camera safely.
- vision/hand_tracker.py: runs MediaPipe and exposes hand landmark
  results.
- vision/gesture_controller.py: converts landmark data into discrete
  game actions.
- camera_test.py: verifies webcam capture independently of the game.
- gesture_test.py: verifies hand detection and landmark
  visualization independently of the game.
- tests/: contains tests for physics, scoring, collision logic, and
  gesture interpretation.
Requirements
Hardware
- A computer capable of running Python and Pygame.
- A webcam for gesture control (built-in or USB).
- Keyboard for fallback controls.
- Adequate lighting and enough space for the hand to remain visible to
  the camera.
Software
- Python 3.11 or 3.12 recommended for the dependency versions in
  requirements.txt.
- pip.
- Git (optional for running locally, required for
  contributing/publishing).
- Windows, macOS, or Linux. Camera permissions and device selection
  may differ by operating system.
Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/gesture-bird.git
cd gesture-bird
Replace YOUR_USERNAME with the GitHub account that hosts the
repository.
2. Create a virtual environment
Windows PowerShell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
If PowerShell prevents activation, use the environment's Python
executable directly:
.\.venv\Scripts\python.exe -m pip install --upgrade pip
macOS / Linux
python3.11 -m venv .venv
source .venv/bin/activate
3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
4. Verify the installation
python -c "import pygame, cv2, mediapipe, numpy; print('Dependencies imported successfully')"
If this command fails, check that the virtual environment is active and
that you are using a Python version supported by the pinned packages.
MediaPipe model setup
No separate model download is needed. The project uses MediaPipe
0.10.21's built-in Hands solution and bundled model assets.
Running the project
Run commands from the repository root with the virtual environment
activated.
1. Optionally test webcam capture
python camera_test.py
Press Q or Escape to close the preview. If no camera is connected, skip
this step; keyboard gameplay remains available.
2. Optionally test hand tracking
python gesture_test.py
This displays the camera feed with detected hand landmarks.
3. Run the game
python main.py
Press Space to start and flap. Press C to enable webcam gesture control.
Press P or Escape to pause; press Q or close the game window to quit.
Run automated tests with `python -m unittest discover -s tests`.

Configuration and controls
The game runs at up to 60 FPS and uses elapsed-time-based physics. The
default webcam is camera index 0 at 640x480. To select a different
camera, change the defaults in `vision/camera.py`. The gesture
controller's cooldown and frame threshold are defined in
`vision/gesture_controller.py`.
Development roadmap
The project is intended to be built incrementally.
  Milestone               Work                    Expected result
  1. Game foundation     Pygame window, game     Basic playable bird
loop, bird, gravity,
keyboard input          

  2. Complete game       Pipes, collision,       Keyboard-controlled
scoring, states,        Flappy Bird clone
restart                 

  3. Webcam              OpenCV capture,         Reliable webcam test
preview, FPS, cleanup   

  4. Hand tracking       MediaPipe model,        Standalone hand
landmarks,              detector
visualization           

  5. Gesture control     Gesture rules,          Reliable discrete flap
re-arming, cooldown,    action
calibration             

  6. Integration         Connect controller to   Gesture-controlled game
game loop               

  7. Polish              Assets, sound,          Portfolio-ready release
settings, tests,
documentation           
8. Future work         Browser/mobile version  Optional distribution
or packaged desktop     target
build
Testing and troubleshooting
Automated tests
- Run `python -m unittest discover -s tests` from the project root.
- Bird physics changes consistently with elapsed time.
- A flap applies the intended upward impulse.
- Pipes move and are removed after leaving the screen.
- Collision detection works at pipe edges and screen boundaries.
- Score increments once per pipe pair, not once per frame.
- Restart resets the bird, obstacles, and current score.
- No hand detected means no gesture action.
- Holding a gesture does not trigger a flap on every frame.
- A new gesture can be accepted after the neutral/re-arm condition.
- Camera resources are released when the application exits.
Keep game-logic tests independent of the webcam wherever possible.
Gesture logic should be testable using sample landmark coordinates or
mocked detector results.
Common problems
Webcam does not open
- Check operating-system camera permissions.
- Close other applications that may be using the camera.
- Try another camera index, such as 1.
- Check cap.isOpened() and handle failure gracefully.
Hand landmarks are unstable
- Improve lighting and keep the hand inside the camera frame.
- Avoid backgrounds that visually blend with the hand.
- Adjust detection/tracking confidence settings where supported.
- Test at different distances and camera resolutions.
Game stutters when vision is enabled
- Measure camera capture and inference time separately.
- Try a smaller input resolution.
- Avoid unnecessary frame copies and repeated model initialization.
- Consider asynchronous/live-stream inference or a worker that shares
  the latest result with the game loop.
- Keep Pygame event handling and rendering on the main thread.
Gesture triggers repeatedly
- Use edge/transition detection instead of triggering on every
  positive frame.
- Add a cooldown and neutral/re-arm state.
- Smooth noisy landmark measurements over a short time window.
- Make gesture thresholds configurable.
MediaPipe Hands API is unavailable
- Reinstall the pinned packages with
  `python -m pip install -r requirements.txt`. MediaPipe 0.10.21 is
  required for the bundled `mp.solutions.hands` API.
Performance and design notes
- Use elapsed time (dt) for physics and movement so the game is less
  dependent on frame rate.
- Initialize Pygame, the camera, and the MediaPipe task once; do not
  recreate them every frame.
- Keep camera processing and game rendering responsibilities separate.
- Pass simple actions from the gesture controller to the game.
- Handle camera absence gracefully and preserve keyboard controls.
- Release the camera and close windows in finally blocks or
  equivalent cleanup paths.
- Webcam inference is limited to 30 FPS to leave time for game rendering.
- Avoid committing personal webcam footage, private data, virtual
  environments, or unnecessary model files.
Demo and screenshots
Add project media here after recording it.
Gameplay demo
- Demo video: ADD_YOUR_DEMO_VIDEO_LINK
- Animated preview/GIF: assets/demo/gesture-bird-demo.gif (add
  this file if you create one)
Screenshots
  Game window                         Hand landmark detection
  Add a screenshot of gameplay        Add a screenshot showing hand
landmarks
You can embed images stored in the repository using relative paths, for
example:
![Gesture Bird gameplay](assets/images/gameplay.png)
![MediaPipe hand landmarks](assets/images/hand-landmarks.png)
A useful demo should show the menu, gesture-controlled flap, score
progression, game-over state, and restart. Avoid including private or
unrelated webcam footage.
Contributing
Contributions, bug reports, and suggestions are welcome.
1. Fork the repository.
2. Create a feature branch.
3. Make a focused change.
4. Run the relevant tests and manual checks.
5. Commit with a descriptive message.
6. Open a pull request explaining the change.
For bugs, include the operating system, Python version, dependency
versions, steps to reproduce, and a traceback or screenshot where
appropriate. Do not attach private webcam footage.
License
This project is intended to be released under the license in
LICENSE. If you choose MIT, include the standard MIT
license text and your copyright notice in that file. Do not claim a
license until the file has been added.
Acknowledgements
- Pygame --- Python game development
  library.
- OpenCV --- computer vision and
  image-processing library.
- MediaPipe --- hand
  landmark and gesture-recognition solutions.
- The original Flappy Bird concept, which inspired the gameplay style.
  This is an independent learning project and is not affiliated with
  or endorsed by the original game's creators.
Built as a hands-on project to explore Python game development,
computer vision, and gesture-based interaction.