# main.py
from ursina import *
from player import Player
from toilets import *
import keyboard

app = Ursina()

# Global variables
player = None
toilets = []
# flush_pressed = False



# Start Menu Elements
def start_game():
    #background_music = Audio('assets/background_music.mp3', loop=True, autoplay=True, volume=0.2)

    global player, toilets
    start_button.disable()
    other_button.disable()
    title_text.disable()

    # create a flat platform
    platform = Entity(model='assets/arena',  texture=None, texture_scale=(50, 50),  position=(0, 7.5, 0))

    platform = Entity(model='plane', scale=(10000, 1, 10000), texture='white_cube', texture_scale=(50, 50), collider='box')
    # Add some visual variety with colors or texture
    platform.color = color.gray

    # Create a player
    player = Player()
    player.start_time = time.time()

    # list of toilet objects
    toilets = []

    # Pass the toilets list itself to each toilet's constructor
    toilets.append(StandardToilet(position=(10, 0.5, 10), player_entity=player.controller, all_toilets=toilets))
    toilets.append(FancyToilet(position=(-2, 0.5, -2), player_entity=player.controller, all_toilets=toilets))

    # Add Cameramen
    toilets.append(StandardCameraMan(position=(15, 0.5, 15), player_entity=player.controller, all_toilets=toilets))
    toilets.append(FancyCameraMan(position=(-10, 0.5, -10), player_entity=player.controller, all_toilets=toilets))

    # Set up lighting and sky
    Sky()
    light = DirectionalLight(shadows=True)
    light.look_at(Vec3(1, -1, -1))

    # Ambient light to fill in the darker areas
    #ambient_light = AmbientLight(color=color.rgb(1, 1, 1), intensity=0.01)

    # Adding a point light for softer, focused illumination
    point_light = PointLight(position=(0, 10, 0), color=color.rgb(1, 1, 1), intensity=0.01)



# Set up the game loop
def update():
    if player:
        player.update()

    for toilet in toilets:
        if hasattr(toilet, "flush"):
            toilet.flush(player)
        elif hasattr(toilet, "attack"):
            toilet.attack(player)
        toilet.update_health_bar()  # Update health text every frame

app.update = update

# Start Menu UI Elements
title_text = Text(text='Skibidi Showdown', scale=5, origin=(0, 0), y=0.3, color=color.white)

# Start Button
start_button = Button(text='Start Game', color=color.azure, scale=(0.25, 0.1), y=-0.1)
start_button.on_click = start_game  # Attach the function to the button click

# Other Button
other_button = Button(text='Other', color=color.orange, scale=(0.25, 0.1), y=-0.3)

# Run the app
app.run()