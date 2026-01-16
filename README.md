
# Coin Raining Game (Python / Pygame)

This project is a small 2D arcade-style game developed using Python and Pygame as part of a
programming assignment connected to the University of Helsinki.

The goal of the project was to gain hands-on experience with real-time game loops, event-driven
programming, basic physics, and manual collision handling — without relying on high-level
game engines or abstractions.

## Gameplay Overview
- Coins fall from the top of the screen at increasing difficulty
- The player controls a character to catch falling coins
- Missed coins reduce score / end the game depending on configuration
- The game runs in real-time using a fixed update loop

## Technical Highlights
- Implemented a custom game loop using Pygame
- Manual collision detection using coordinate-based boundary checks
- State-driven logic for player movement and coin spawning
- Increasing difficulty through spawn rate and speed adjustments
- Clean separation between game logic and rendering

Instead of relying solely on built-in rectangle collision helpers, collision detection was
handled through explicit coordinate comparisons, providing a deeper understanding of spatial
logic and edge conditions.

## Assets
All visual assets used in the project were provided as part of a University of Helsinki
programming assignment.

## How to Run
```
python3 main.py
```
## Possible Improvements
- Sound and music integration
- Refined collision abstraction
- Additional gameplay mechanics (power-ups, levels)

## Notes
This project represents an early-stage exploration into interactive programming and game
development fundamentals.
