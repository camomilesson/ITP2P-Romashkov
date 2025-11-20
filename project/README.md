# Castle Jumper

**Author:** Andrei Romashkov  

---

## Description
Castle Jumper is a 2D platformer game built with Python and Pygame. The player navigates a series of falling platforms, jumping from one to another while avoiding falling off the screen. The game features:  

- Player movement: running left/right, jumping with realistic gravity  
- Top-only collision with platforms  
- Scrolling background to create depth  
- Player and block sprites for visuals  
- Score tracking based on blocks spawned  
- Game over and restart functionality  
- Highscore saving with name input and validation  
- HUD displaying current score and hiscore in boxed format  

---

## Purpose of the Program
The program demonstrates core game development concepts in Python using Pygame:  

- Handling user input and physics  
- Collision detection  
- Sprite handling  
- UI elements (score, hiscore, restart button)  
- File I/O for saving highscores  
- Game loop and event-driven programming  

It’s designed as both a fun interactive game and a learning project for Python programming and game mechanics.  

---

## Features Implemented

- Player movement: left, right, jump with physics  
- Gravity and top-only collision with platforms  
- Falling platforms with decreasing width over time  
- Scrolling background for parallax effect  
- Player sprites for idle and jumping states  
- Score system based on platform width  
- Display of score in a boxed HUD  
- Game over screen with restart button  
- Highscore system with name input and validation  
- HUD shows current hiscore during gameplay  

---

## Todolist / Completed Tasks

- [x] Create README.md  
- [x] Implement player movement (run, jump)  
- [x] Apply gravity and top-only collision  
- [x] Spawn falling platforms with random widths  
- [x] Make platform width shrink over time  
- [x] Add scrolling background  
- [x] Add player sprites (idle/jumping)  
- [x] Implement scoring system  
- [x] Display score and hiscore in boxed HUD  
- [x] Game over detection when player falls off-screen  
- [x] Restart button after game over  
- [x] Highscore saving with name input and validation  
- [ ] Optional: sound effects and background music  
- [ ] Optional: polish graphics and animations  
- [ ] Optional: add enemies or further level progression  

---

## Notes for Running

1. Make sure all asset images (`player_idle.png`, `player_jumping.png`, `block.png`, `background.png`) are in the same directory as the Python script.  
2. Run the game using Python 3.x with Pygame installed:  

```bash
python main.py
