from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# --- Window Settings (macOS Retina-safe) ---
screen_width, screen_height = window.fullscreen_size
window.size = (int(screen_width * 0.95), int(screen_height * 0.95))  # slightly smaller than full screen
window.borderless = False
window.fullscreen = False
window.title = "My Ursina 3D Game"
window.exit_button.visible = False
window.fps_counter.enabled = True

# --- Environment ---
floor = Entity(model='cube', scale=(30,1,30), color=color.green, collider='box', position=(0,-0.5,0))

# Walls (bounded room)
wall1 = Entity(model='cube', scale=(30,3,1), color=color.gray, collider='box', position=(0,1.5,15))
wall2 = Entity(model='cube', scale=(30,3,1), color=color.gray, collider='box', position=(0,1.5,-15))
wall3 = Entity(model='cube', scale=(1,3,30), color=color.gray, collider='box', position=(15,1.5,0))
wall4 = Entity(model='cube', scale=(1,3,30), color=color.gray, collider='box', position=(-15,1.5,0))

# --- Player ---
player = FirstPersonController()
player.y = 1
player.cursor.visible = False  # hide purple crosshair

# --- Collectibles ---
collectibles = []
score = 0

for i in range(10):
    x = random.uniform(-14, 14)
    z = random.uniform(-14, 14)
    c = Entity(model='cube', color=color.yellow, scale=1, position=(x,0.5,z), collider='box')
    collectibles.append(c)

# --- Sky ---
sky = Sky()

# --- Score Text (macOS-safe) ---
def create_score():
    global score_text
    score_text = Text(
        text=f"Score: {score}",
        position=(-0.85, 0.45),  # top-left corner
        scale=2,
        origin=(0,0),
        color=color.white,
        parent=camera.ui
    )

# Delay to ensure camera.ui exists
invoke(create_score, delay=0.01)

# --- Game Logic ---
def update():
    global score
    for c in collectibles:
        if c and distance(player.position, c.position) < 1.5:  # pick up when close
            destroy(c)
            collectibles.remove(c)
            score += 1
            score_text.text = f"Score: {score}"

app.run()
