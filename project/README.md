# Castle Jumper

**Author:** Andrei Romashkov  

---

## Description
Castle Jumper is a 2D platformer game built with Python and Pygame. The player navigates a series of falling platforms, jumping from one to another while avoiding falling off the screen. The game features:  

- Player movement: running left/right, jumping with realistic gravity  
- Top-only collision with platforms  
- Scrolling background to create depth  
- Modular sprite classes (`Player`, `Block`) for visuals  
- Platforms with dynamic widths and optional horizontal motion  
- Score tracking based on blocks spawned and width  
- Game over and restart functionality  
- Highscore saving with name input (validated, 1–3 letters)  
- HUD displaying current score and highscores in boxed format  
- Emerald-green color accents matching gold highlights  

---

## Purpose of the Program
The program demonstrates core game development concepts in Python using Pygame:  

- Handling user input and physics  
- Collision detection and sprite handling  
- Event-driven programming and game loop  
- UI elements (score, highscores, restart button)  
- File I/O for saving highscores  
- Modular code organization with separate class files  

It’s designed as both a fun interactive game and a learning project for Python programming and game mechanics.  

---

## Features Implemented

- Player movement: left, right, jump with physics  
- Gravity and top-only collision with platforms  
- Falling platforms with decreasing width over time  
- Horizontal platform motion  
- Scrolling background for parallax effect  
- Player sprites for idle and jumping states  
- Block sprites using three-part (left/middle/right) textures  
- Score system based on platform width and difficulty  
- Display of score in a boxed HUD  
- Game over screen with restart button  
- Highscore system with validated name input  
- HUD shows current highscores during gameplay  
- Modular class structure (`player.py`, `block.py`)  

---

## Todolist / Completed Tasks

- [x] Split `Player` and `Block` classes into separate files  
- [x] Implement player movement (run, jump)  
- [x] Apply gravity and top-only collision  
- [x] Spawn falling platforms with random widths and optional horizontal motion  
- [x] Make platform width shrink over time  
- [x] Add scrolling background  
- [x] Add player sprites (idle/jumping)  
- [x] Implement scoring system  
- [x] Display score and highscore in boxed HUD  
- [x] Game over detection when player falls off-screen  
- [x] Restart button after game over  
- [x] Highscore saving with validated name input  
- [x] Modular class structure (`player.py`, `block.py`)  
- [ ] Optional: sound effects and background music  
- [ ] Optional: polish graphics and animations  
- [ ] Optional: add enemies or further level progression  

---

## Requirements

- Python 3.x  
- [Pygame](https://www.pygame.org/)  

Install dependencies using:

```bash
pip install -r requirements.txt