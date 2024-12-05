from vpython import sphere, box, vector, rate, color, text, random, scene
import random

# Define constants
gravity = vector(0, -9.8, 0)
jump_velocity = 15
speed = 7
pipe_spawn_interval = 500  # Frames between new pipe spawns
dt = 0.01

# Ground settings
ground_sections = []
section_width = 10
heights = [0, 1, 2, 1, 1.5, 2.5]  # Varying heights for ground sections
initial_x = 0 #-scene.width / 2  # Start from the left edge of the scene
scene_center_x = scene.center.x

# Set initial scene range for zoom effect
scene.range = 50  # Start zoomed out
target_range = 20  # Target zoom level
zoom_speed = 0.1  # Controls the zooming speed

# Calculate the number of ground sections to fill the initial scene width
num_initial_sections = int(scene.width // section_width) + 2

# Create initial ground sections
for i in range(num_initial_sections):
    ground_sections.append(
        box(pos=vector(initial_x + i * section_width, heights[i % len(heights)] - 1, 0), 
            size=vector(section_width, 2, 5), 
            color=vector(0.6, 0.4, 0.2))
    )

# Create Mario as a ball
mario = sphere(pos=vector(initial_x + 10, ground_sections[0].pos.y + 1.5, 0), radius=1, color=color.red)

# Initialize velocity and state
velocity = vector(0, 0, 0)
is_jumping = False

# List to store pipes
pipes = []

# Track keyboard inputs
keys_pressed = {'left': False, 'right': False, 'up': False}

# Key down event handler
def keydown(evt):
    global is_jumping
    if evt.key == 'left':
        keys_pressed['left'] = True
    elif evt.key == 'right':
        keys_pressed['right'] = True
    elif evt.key == 'up' and not is_jumping:
        keys_pressed['up'] = True
        velocity.y = jump_velocity
        is_jumping = True

# Key up event handler
def keyup(evt):
    if evt.key == 'left':
        keys_pressed['left'] = False
    elif evt.key == 'right':
        keys_pressed['right'] = False
    elif evt.key == 'up':
        keys_pressed['up'] = False

# Function to generate pipes at random positions
def spawn_pipe():
    x_pos = ground_sections[-1].pos.x + random.randint(5, 15)
    pipe_height = random.uniform(5, 10)
    new_pipe = box(pos=vector(x_pos, pipe_height / 2, 0), 
                   size=vector(2, pipe_height, 5), 
                   color=color.green)
    pipes.append(new_pipe)


# Function to generate new ground section
def spawn_ground():
    last_section = ground_sections[-1]
    new_x = last_section.pos.x + section_width
    new_height = random.uniform(0, 3)  # Randomize the height of the next ground
    new_section = box(pos=vector(new_x, new_height - 1, 0), 
                      size=vector(section_width, 2, 5), 
                      color=vector(0.6, 0.4, 0.2))
    ground_sections.append(new_section)

# Function to get the ground level below Mario
def get_ground_level():
    for section in ground_sections:
        if mario.pos.x > section.pos.x - section_width / 2 and mario.pos.x < section.pos.x + section_width / 2:
            return section.pos.y + section.size.y / 2
    return None

# Check collision between Mario and pipes
def check_collision():
    for pipe in pipes:
        if abs(mario.pos.x - pipe.pos.x) < (mario.radius + pipe.size.x / 2):
            if mario.pos.y < (pipe.pos.y + pipe.size.y / 2):
                return True
    return False

# Display "GAME OVER" text
def display_game_over():
    text(text="GAME OVER", align='center', color=color.red, height=3, 
         pos=vector(mario.pos.x + 10, mario.pos.y + 5, 0))

frame_count = 0

# Bind events for keyboard input
scene.bind('keydown', keydown)
scene.bind('keyup', keyup)

# Main loop
while True:
    scene.center = mario.pos
    rate(100)
    frame_count += 1

    # Gradually zoom in at the start
    if scene.range > target_range:
        scene.range -= zoom_speed

    # Spawn pipes periodically
    if frame_count % pipe_spawn_interval == 0:
        spawn_pipe()

    # Handle keyboard input
    if keys_pressed['left']:
        mario.pos.x -= speed * dt
    if keys_pressed['right']:
        mario.pos.x += speed * dt

    # Apply gravity
    velocity += gravity * dt
    mario.pos += velocity * dt

    # Check and correct Mario's position with respect to the ground
    ground_y = get_ground_level()
    if ground_y is not None:
        if mario.pos.y - mario.radius < ground_y:
            mario.pos.y = ground_y + mario.radius
            velocity.y = 0
            is_jumping = False

    # Remove pipes and ground sections that are far left
    pipes = [pipe for pipe in pipes if pipe.pos.x > mario.pos.x - 30]
    ground_sections = [section for section in ground_sections if section.pos.x > mario.pos.x - 50]

    # Move pipes leftward to simulate motion
    for pipe in pipes:
        pipe.pos.x -= speed * dt

    # Check for collision with pipes
    if check_collision():
        display_game_over()
        break

    # Spawn new ground sections if Mario gets close to the edge of the last ground section
    if mario.pos.x > ground_sections[-1].pos.x - section_width:
        spawn_ground()


