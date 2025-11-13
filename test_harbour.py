from ursina import *
import random

app = Ursina()

# --- Window Settings ---
screen_width, screen_height = window.fullscreen_size
window.size = (int(screen_width*0.95), int(screen_height*0.95))
window.borderless = False
window.fullscreen = False
window.title = "Harbour.Race"
window.exit_button.visible = False
window.fps_counter.enabled = True

# --- Environment ---
sky = Sky()
quay_length = 50
quay_width = 8

# Floor (quay)
floor = Entity(model='cube', scale=(quay_width,1,quay_length), color=color.gray, collider='box', position=(0,0,quay_length/2))

# Water on sides
water_left = Entity(model='cube', scale=(5,1,quay_length), color=color.azure, position=(-quay_width/2 - 2.5,-0.5,quay_length/2))
water_right = Entity(model='cube', scale=(5,1,quay_length), color=color.azure, position=(quay_width/2 + 2.5,-0.5,quay_length/2))

# --- Player ---
player = Entity(model='cube', color=color.red, scale=(1,2,1), position=(0,1,0))
camera.parent = player
camera.position = Vec3(0,4,-10)
camera.rotation_x = 20

# --- Stars (collectibles) ---
stars = []
for i in range(15):
    x = random.uniform(-quay_width/2 + 1, quay_width/2 - 1)
    z = random.uniform(5, quay_length - 2)
    star = Entity(model='sphere', color=color.yellow, scale=0.5, position=(x,1,z), collider='box')
    stars.append(star)

# --- Obstacles ---
obstacles = []
for i in range(10):
    x = random.uniform(-quay_width/2 + 1, quay_width/2 - 1)
    z = random.uniform(5, quay_length - 2)
    obstacle = Entity(model='cube', color=color.brown, scale=(1,2,1), position=(x,1,z), collider='box')
    obstacles.append(obstacle)

# --- Score UI ---
score = 0
score_text = Text(text=f"Score: {score}", position=(-0.85,0.45), scale=2, origin=(0,0), color=color.white, parent=camera.ui)
win_text = Text(text="You Win!", position=(0,0), scale=3, origin=(0,0), color=color.green, enabled=False, parent=camera.ui)

# --- Game logic ---
player_speed = 5
side_speed = 7

def update():
    global score

    dt = time.dt

    # Automatic forward movement
    player.z += player_speed * dt

    # Left/Right controls
    if held_keys['a'] or held_keys['left arrow']:
        player.x -= side_speed * dt
    if held_keys['d'] or held_keys['right arrow']:
        player.x += side_speed * dt

    # Keep player within quay
    player.x = clamp(player.x, -quay_width/2 + 0.5, quay_width/2 - 0.5)

    # Collect stars
    for star in stars:
        if distance(player.position, star.position) < 1:
            destroy(star)
            stars.remove(star)
            score += 1
            score_text.text = f"Score: {score}"

    # Collide with obstacles
    for obs in obstacles:
        if distance(player.position, obs.position) < 1:
            # Reset player to start
            player.position = Vec3(0,1,0)

    # Check win condition
    if player.z >= quay_length:
        win_text.enabled = True

app.run()
