# main.py
from ursina import *
from player import Player
from toilets import StandardToilet, FancyToilet, StandardCameraMan, FancyCameraMan
import time
from abc import ABC, abstractmethod

app = Ursina()

# Global variables
player = None
toilets = []
current_level_index = 0
level_start_button = None
level_title_text = None
congrats_text = None
exit_button = None
level_in_progress = False
sky_entity = None
level_overlay_ui = []

def destroy_ui_elements():
    global level_start_button, level_title_text, congrats_text, exit_button
    if level_start_button is not None:
        destroy(level_start_button)
        level_start_button = None
    if level_title_text is not None:
        destroy(level_title_text)
        level_title_text = None
    if congrats_text is not None:
        destroy(congrats_text)
        congrats_text = None
    if exit_button is not None:
        destroy(exit_button)
        exit_button = None
    # Remove level overlay elements
    for ui_element in level_overlay_ui:
        destroy(ui_element)
    level_overlay_ui.clear()

# Abstract Base Class for Levels
class Level(ABC):
    def __init__(self, num_enemies_each_type):
        self.num_enemies_each_type = num_enemies_each_type

    def load(self):
        global player, toilets, level_in_progress, sky_entity
        # Set up platform and environment if not already set up
        if sky_entity is None:
            self.setup_environment()

        # Create the player if not already created
        if player is None:
            player = Player()
        toilets = []
        self.spawn_enemies()
        level_in_progress = True

    def setup_environment(self):
        global sky_entity
        # Create a flat platform
        platform = Entity(model='assets/arena', texture=None, texture_scale=(50, 50), position=(0, 7.5, 0))
        platform = Entity(model='plane', scale=(10000, 1, 10000), texture='white_cube', texture_scale=(50, 50), collider='box')
        platform.color = color.gray

        # Set up lighting and sky
        sky_entity = Sky()  # Only create the sky once, reuse it across levels
        light = DirectionalLight(shadows=True)
        light.look_at(Vec3(1, -1, -1))
        point_light = PointLight(position=(0, 10, 0), color=color.rgb(1, 1, 1), intensity=0.01)

    @abstractmethod
    def spawn_enemies(self):
        pass

    def all_enemies_killed(self):
        return len(toilets) == 0

class Level1(Level):
    def __init__(self):
        super().__init__(num_enemies_each_type=1)

    def spawn_enemies(self):
        toilets.append(StandardToilet(position=(10, 0.5, 2), player_entity=player.controller, all_toilets=toilets))
        toilets.append(FancyToilet(position=(-2, 0.5, 2), player_entity=player.controller, all_toilets=toilets))
        toilets.append(StandardCameraMan(position=(15, 0.5, 2), player_entity=player.controller, all_toilets=toilets))
        toilets.append(FancyCameraMan(position=(-10, 0.5, 2), player_entity=player.controller, all_toilets=toilets))

class Level2(Level):
    def __init__(self):
        super().__init__(num_enemies_each_type=2)

    def spawn_enemies(self):
        for i in range(2):
            toilets.append(StandardToilet(position=(10 + i * 5, 0.5, 2), player_entity=player.controller, all_toilets=toilets))
            toilets.append(FancyToilet(position=(-2 - i * 5, 0.5, 2), player_entity=player.controller, all_toilets=toilets))
            toilets.append(StandardCameraMan(position=(15 + i * 5, 0.5, 2), player_entity=player.controller, all_toilets=toilets))
            toilets.append(FancyCameraMan(position=(-10 - i * 5, 0.5, 2), player_entity=player.controller, all_toilets=toilets))

class Level3(Level):
    def __init__(self):
        super().__init__(num_enemies_each_type=3)

    def spawn_enemies(self):
        for i in range(3):
            toilets.append(StandardToilet(position=(10 + i * 5, 0.5, 2), player_entity=player.controller, all_toilets=toilets))
            toilets.append(FancyToilet(position=(-2 - i * 5, 0.5, 2), player_entity=player.controller, all_toilets=toilets))
            toilets.append(StandardCameraMan(position=(15 + i * 5, 0.5, 2), player_entity=player.controller, all_toilets=toilets))
            toilets.append(FancyCameraMan(position=(-10 - i * 5, 0.5, 2), player_entity=player.controller, all_toilets=toilets))

# Levels list
levels = [Level1(), Level2(), Level3()]

def load_level(level_index):
    show_level_start_screen(level_index)

def show_level_start_screen(level_index):
    global level_start_button, level_title_text
    destroy_ui_elements()  # Clear previous UI elements if any
    level_title_text = Text(text=f'Level {level_index + 1}', scale=5, origin=(0, 0), y=0.3, color=color.white)
    level_start_button = Button(text='Start Level', color=color.azure, scale=(0.25, 0.1), y=-0.1)
    level_start_button.on_click = lambda: start_level(level_index)

    # Store the UI elements for later removal
    level_overlay_ui.append(level_title_text)
    level_overlay_ui.append(level_start_button)

    # Enable mouse cursor to click the start button
    mouse.locked = False

def start_level(level_index):
    global level_start_button, level_title_text, level_in_progress
    # Destroy only the overlay UI elements
    destroy_ui_elements()
    levels[level_index].load()
    level_in_progress = True

    # Lock the mouse cursor when the level starts
    mouse.locked = True

def update():
    global level_in_progress
    if player and level_in_progress:
        try:
            player.update()
        except AttributeError:
            # Ensure player is properly initialized before trying to update
            print("Player not yet initialized or has been destroyed.")

    for toilet in toilets:
        if hasattr(toilet, "flush"):
            toilet.flush(player)
        elif hasattr(toilet, "attack"):
            toilet.attack(player)
        toilet.update_health_bar()  # Update health text every frame

    # Check if current level is complete
    if level_in_progress and current_level_index < len(levels) and levels[current_level_index].all_enemies_killed():
        level_in_progress = False
        go_to_next_level()

def go_to_next_level():
    global current_level_index
    current_level_index += 1
    if current_level_index < len(levels):
        show_level_start_screen(current_level_index)
    else:
        show_congratulations_screen()

def show_congratulations_screen():
    global congrats_text, exit_button
    congrats_text = Text(text='You Win!', scale=5, origin=(0, 0), y=0.3, color=color.white)
    exit_button = Button(text='Exit', color=color.red, scale=(0.25, 0.1), y=-0.1)
    exit_button.on_click = application.quit

    # Store the UI elements for later removal
    level_overlay_ui.append(congrats_text)
    level_overlay_ui.append(exit_button)

    # Enable mouse cursor to click the exit button
    mouse.locked = False

# Start Menu UI Elements
def show_start_menu():
    global title_text, start_button
    destroy_ui_elements()  # Clear previous UI elements if any
    title_text = Text(text='Skibidi Showdown', scale=5, origin=(0, 0), y=0.3, color=color.white)
    start_button = Button(text='Start Game', color=color.azure, scale=(0.25, 0.1), y=-0.1)
    start_button.on_click = lambda: (destroy(start_button), destroy(title_text), load_level(current_level_index))

    # Store the UI elements for later removal
    level_overlay_ui.append(title_text)
    level_overlay_ui.append(start_button)

# Show the start menu initially
show_start_menu()

# Run the app
app.update = update
app.run()
