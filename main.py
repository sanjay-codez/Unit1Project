# main.py
from ursina import *
from player import Player
from enemy import StandardEnemy, FancyEnemy, StandardCameraMan, FancyCameraMan
from abc import ABC, abstractmethod
import pickle
import os
from customexception import GameException


app = Ursina()


window.fullscreen = True

if not os.path.exists('pickle_data'):
    os.makedirs('pickle_data')

# Global variables
player = None
enemies = []
current_level_index = 0
level_start_button = None
level_title_text = None
congrats_text = None
exit_button = None
level_in_progress = False
sky_entity = None
level_overlay_ui = []
level_start_screen_active = False

def destroy_ui_elements():
    """
        Destroys all UI elements related to the current game level.

        This function checks for the existence of global UI elements such as
        the level start button, level title text, congrats text, and exit button.
        If they exist, they are destroyed and set to None. Additionally, it removes
        all elements from the level overlay UI list.

        Global variables modified:
            level_start_button: The button to start the level.
            level_title_text: The text displaying the level title.
            congrats_text: The text displaying congratulations to the player.
            exit_button: The button to exit the level.

        Returns:
            None
    """
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

# Abstract class for Game Level
class GameLevel(ABC):
    """
        Abstract class representing a game level.

        This class serves as a blueprint for creating specific game levels.
        It manages the initialization of enemies, the player, and the game environment.

        Attributes:
            num_enemies_each_type (int): The number of enemies for each type in the level.

        Methods:
            load(): Initializes the game level by setting up the environment,
                     spawning the player, and spawning enemies.
            setup_environment(): Configures the game environment, including the platform
                                and lighting.
            spawn_enemies(): Abstract method that must be implemented in subclasses
                             to define how enemies are spawned.
            all_enemies_killed(): Checks if all enemies in the level have been defeated.

    """
    def __init__(self, num_enemies_each_type):
        self.num_enemies_each_type = num_enemies_each_type

    def load(self):
        global player, enemies, level_in_progress, sky_entity

        if sky_entity is None:
            self.setup_environment()

        if player is None:
            player = Player()
        enemies = []
        self.spawn_enemies()
        level_in_progress = True

    def setup_environment(self):
        global sky_entity

        platform = Entity(model='assets/arena', texture=None, texture_scale=(50, 50), position=(0, 7.5, 0))
        platform = Entity(model='plane', scale=(10000, 1, 10000), texture='white_cube', texture_scale=(50, 50), collider='box')
        platform.color = color.gray


        sky_entity = Sky()
        light = DirectionalLight(shadows=True)
        light.look_at(Vec3(1, -1, -1))
        point_light = PointLight(position=(0, 10, 0), color=color.rgb(1, 1, 1), intensity=0.01)

    @abstractmethod
    def spawn_enemies(self):
        pass

    def all_enemies_killed(self):
        return len(enemies) == 0

# Derived class for Level 1
class LevelOne(GameLevel):
    """
        Derived class representing Level 1 of the game.

        This class defines the specific implementation of enemies for Level 1,
        inheriting from the abstract GameLevel class. It initializes a set number
        of enemies and defines their spawning behavior.

        Methods:
            __init__(): Initializes LevelOne with a specific number of enemies.
            spawn_enemies(): Creates and spawns enemy instances in the game level.
                              It also checks for enemy health and duplicates them
                              based on a random chance.
    """
    def __init__(self):
        super().__init__(num_enemies_each_type=1)

    def spawn_enemies(self):
        """Spawns enemies in Level 1 and handles their duplication based on random chance."""
        enemy1 = StandardEnemy(position=(10, 0.5, 2), player_entity=player.controller, all_enemies=enemies)
        enemy2 = FancyEnemy(position=(-2, 0.5, 2), player_entity=player.controller, all_enemies=enemies)
        enemy3 = StandardCameraMan(position=(15, 0.5, 2), player_entity=player.controller, all_enemies=enemies)
        enemy4 = FancyCameraMan(position=(-10, 0.5, 2), player_entity=player.controller, all_enemies=enemies)

        enemies.append(enemy1)
        enemies.append(enemy2)
        enemies.append(enemy3)
        enemies.append(enemy4)

        for enemy in [enemy1, enemy2, enemy3, enemy4]:
            # Check if the enemy is alive
            if StandardEnemy.is_alive(enemy):
                print(f"{enemy.entity.name} is alive!")


            if random.random() < 0.20:
                duplicate = enemy.__class__.duplicate(position=enemy.entity.position + Vec3(2, 0, 0),
                                                     player_entity=enemy.player_entity, all_enemies=enemies)
                enemies.append(duplicate)

# Derived class for Level 2
class LevelTwo(GameLevel):
    """
        Derived class representing Level 2 of the game.

        This class defines the specific implementation of enemies for Level 2,
        inheriting from the abstract GameLevel class. It initializes a specific
        number of enemies and defines their spawning behavior with positional offsets.

        Methods:
            __init__(): Initializes LevelTwo with a specific number of enemies.
            spawn_enemies(): Creates and spawns multiple enemy instances in the game level,
                             with positional offsets for each pair of enemies. It also checks
                             for enemy health and duplicates them based on a random chance.
    """
    def __init__(self):
        super().__init__(num_enemies_each_type=2)

    def spawn_enemies(self):
        """Spawns enemies in Level 2 and handles their duplication based on random chance."""
        for i in range(2):

            enemy1 = StandardEnemy(position=(10 + i * 5, 0.5, 2), player_entity=player.controller, all_enemies=enemies)
            enemy2 = FancyEnemy(position=(-2 - i * 5, 0.5, 2), player_entity=player.controller, all_enemies=enemies)
            enemy3 = StandardCameraMan(position=(15 + i * 5, 0.5, 2), player_entity=player.controller,
                                       all_enemies=enemies)
            enemy4 = FancyCameraMan(position=(-10 - i * 5, 0.5, 2), player_entity=player.controller,
                                    all_enemies=enemies)


            enemies.append(enemy1)
            enemies.append(enemy2)
            enemies.append(enemy3)
            enemies.append(enemy4)


            for enemy in [enemy1, enemy2, enemy3, enemy4]:

                if StandardEnemy.is_alive(enemy):
                    print(f"{enemy.entity.name} is alive!")

                if random.random() < 0.50:
                    duplicate = enemy.__class__.duplicate(position=enemy.entity.position + Vec3(2, 0, 0),
                                                          player_entity=enemy.player_entity, all_enemies=enemies)
                    enemies.append(duplicate)

# Derived class for Level 3
class LevelThree(GameLevel):
    """
        Derived class representing Level 3 of the game.

        This class defines the specific implementation of enemies for Level 3,
        inheriting from the abstract GameLevel class. It initializes a specific
        number of enemies and defines their spawning behavior with positional offsets.

        Methods:
            __init__(): Initializes LevelThree with a specific number of enemies.
            spawn_enemies(): Creates and spawns multiple enemy instances in the game level,
                             with positional offsets for each set of enemies. It also checks
                             for enemy health and duplicates them based on a random chance.
    """
    def __init__(self):
        super().__init__(num_enemies_each_type=3)

    def spawn_enemies(self):
        """Spawns enemies in Level 3 and handles their duplication based on random chance."""
        for i in range(3):

            enemy1 = StandardEnemy(position=(10 + i * 5, 0.5, 2), player_entity=player.controller, all_enemies=enemies)
            enemy2 = FancyEnemy(position=(-2 - i * 5, 0.5, 2), player_entity=player.controller, all_enemies=enemies)
            enemy3 = StandardCameraMan(position=(15 + i * 5, 0.5, 2), player_entity=player.controller,
                                       all_enemies=enemies)
            enemy4 = FancyCameraMan(position=(-10 - i * 5, 0.5, 2), player_entity=player.controller,
                                    all_enemies=enemies)


            enemies.append(enemy1)
            enemies.append(enemy2)
            enemies.append(enemy3)
            enemies.append(enemy4)


            for enemy in [enemy1, enemy2, enemy3, enemy4]:


                if StandardEnemy.is_alive(enemy):
                    print(f"{enemy.entity.name} is alive!")

                if random.random() < 0.70:
                    duplicate = enemy.__class__.duplicate(position=enemy.entity.position + Vec3(2, 0, 0),
                                                          player_entity=enemy.player_entity, all_enemies=enemies)
                    enemies.append(duplicate)

# GameLevels list
gamelevels = [LevelOne(), LevelTwo(), LevelThree()]

def load_level(level_index):
    """
        Loads the specified game level and activates the level start screen.

        This function displays the start screen for the specified level and sets
        a global variable to indicate that the level start screen is active.

        Parameters:
            level_index (int): The index of the level to be loaded.

        Global variables modified:
            level_start_screen_active (bool): Indicates whether the level start screen is currently active.

        Returns:
            None
    """
    global level_start_screen_active
    show_level_start_screen(level_index)
    level_start_screen_active = True

def show_level_start_screen(level_index):
    """
        Displays the start screen for the specified level.

        This function clears existing UI elements, creates a title text displaying the
        current level number, and adds a start button that initiates the level when clicked.
        It also unlocks the mouse cursor for player interaction.

        Parameters:
            level_index (int): The index of the level for which the start screen is displayed.

        Global variables modified:
            level_start_button: The button to start the level.
            level_title_text: The text displaying the level number.

        Returns:
            None
    """
    global level_start_button, level_title_text
    destroy_ui_elements()
    level_title_text = Text(text=f'Level {level_index + 1}', scale=5, origin=(0, 0), y=0.3, color=color.white)
    level_start_button = Button(text='Start Level', color=color.azure, scale=(0.25, 0.1), y=-0.1)
    level_start_button.on_click = lambda: start_level(level_index)


    level_overlay_ui.append(level_title_text)
    level_overlay_ui.append(level_start_button)


    mouse.locked = False

def start_level(level_index):
    """
        Initiates the specified game level.

        This function clears the UI elements, loads the specified level, and updates
        the status of the level and start screen. It locks the mouse cursor to prevent
        player interaction with the UI during gameplay.

        Parameters:
            level_index (int): The index of the level to be started.

        Global variables modified:
            level_start_button: Reference to the start button, which will be destroyed.
            level_title_text: Reference to the level title text, which will be destroyed.
            level_in_progress (bool): Indicates whether a level is currently in progress.
            level_start_screen_active (bool): Indicates that the start screen is no longer active.

        Returns:
            None
    """
    global level_start_button, level_title_text, level_in_progress, level_start_screen_active

    destroy_ui_elements()
    gamelevels[level_index].load()
    level_in_progress = True
    level_start_screen_active = False


    mouse.locked = True

def save_game_state(filename="pickle_data/savefile.pkl"):
    """
        Saves the current game state to a file.

        This function captures the player's position, health, the state of all enemies,
        and the current level index, then serializes this data into a specified file
        using the pickle module.

        Parameters:
            filename (str): The path to the file where the game state will be saved.
                            Default is "pickle_data/savefile.pkl".

        Global variables modified:
            player: Reference to the player object to retrieve position and health.
            enemies: List of current enemy instances to capture their states.
            current_level_index (int): Index of the current level.

        Returns:
            None
    """

    global player, enemies, current_level_index
    game_state = {
        "player_position": player.controller.position,
        "player_health": player.get_health(),
        "enemies": [(enemy.__class__.__name__, enemy.entity.position, enemy.health) for enemy in enemies],
        "current_level_index": current_level_index
    }
    with open(filename, "wb") as f:
        pickle.dump(game_state, f)
    print("Game state saved!")

def load_game_state(filename="pickle_data/savefile.pkl"):
    """
        Loads the game state from a specified file.

        This function retrieves the player's position, health, the states of all enemies,
        and the current level index from a saved file. It updates the game state accordingly
        and clears any existing enemies before adding new instances based on the saved data.

        Parameters:
            filename (str): The path to the file from which the game state will be loaded.
                            Default is "pickle_data/savefile.pkl".

        Global variables modified:
            player: Reference to the player object, updating position and health.
            enemies: List of current enemy instances, cleared and repopulated with loaded data.
            current_level_index (int): Index of the current level, updated from the loaded state.

        Raises:
            GameException: If the file is not found or if an error occurs during loading.

        Returns:
            None
    """

    global player, enemies, current_level_index
    try:
        with open(filename, "rb") as f:
            game_state = pickle.load(f)
            player.controller.position = game_state["player_position"]
            player.set_health(game_state["player_health"])

            current_level_index = game_state["current_level_index"]


            for enemy in enemies:
                destroy(enemy.entity)
                if hasattr(enemy, 'health_bar'):
                    destroy(enemy.health_bar)
            enemies.clear()


            for enemy_class_name, position, health in game_state["enemies"]:
                enemy_class = globals()[enemy_class_name]
                new_enemy = enemy_class(position=position, player_entity=player.controller, all_enemies=enemies)
                new_enemy.health = health
                new_enemy.update_health_bar()
                enemies.append(new_enemy)

        print("Game state loaded!")
    except FileNotFoundError as e:
        raise GameException(f"Failed to load game state: File '{filename}' not found.") from e

    except Exception as e:
        raise GameException("An error occurred while loading the game state.") from e

def update():
    """
        Updates the game state during each frame.

        This function is responsible for updating the player's state, handling enemy actions,
        and managing game controls for saving and loading the game state. It also checks if
        all enemies have been defeated in the current level and transitions to the next level if so.

        Global variables modified:
            level_in_progress (bool): Indicates whether the current level is still in progress.
            level_start_screen_active (bool): Indicates if the level start screen is currently displayed.

        Returns:
            None

        Raises:
            GameException: If there is an error during the player's update, such as if the player is
                           not properly initialized or has been destroyed.
    """

    global level_in_progress, level_start_screen_active
    if player and level_in_progress:
        try:
            player.update()
        except AttributeError as e:
            raise GameException("Error during player update: Player not properly initialized or destroyed.") from e

    if not level_start_screen_active:
        if held_keys['p']:
            save_game_state()

        if held_keys['l']:
            load_game_state()

    for enemy in enemies:
        enemy.attack(player)
        enemy.update_health_bar()


    if level_in_progress and current_level_index < len(gamelevels) and gamelevels[current_level_index].all_enemies_killed():
        level_in_progress = False
        go_to_next_level()

def go_to_next_level():
    """
        Advances the game to the next level.

        This function increments the current level index and checks if there are more levels
        available. If there are, it loads the next level; otherwise, it displays a
        congratulations screen for completing all levels.

        Global variables modified:
            current_level_index (int): The index of the current level, which is incremented
                                       to point to the next level.

        Returns:
            None
    """
    global current_level_index
    current_level_index += 1
    if current_level_index < len(gamelevels):
        load_level(current_level_index)
    else:
        show_congratulations_screen()

def show_congratulations_screen():
    """
        Displays the congratulations screen upon winning the game.

        This function creates a congratulatory message and an exit button.
        It adds these UI elements to the screen and unlocks the mouse cursor
        to allow the player to exit the game.

        Global variables modified:
            congrats_text: The text displayed to indicate the player has won.
            exit_button: The button that allows the player to exit the game.

        Returns:
            None
    """
    global congrats_text, exit_button
    congrats_text = Text(text='You Win!', scale=5, origin=(0, 0), y=0.3, color=color.white)
    exit_button = Button(text='Exit', color=color.red, scale=(0.25, 0.1), y=-0.1)
    exit_button.on_click = application.quit


    level_overlay_ui.append(congrats_text)
    level_overlay_ui.append(exit_button)


    mouse.locked = False


def show_start_menu():
    """
        Displays the start menu for the game.

        This function clears any existing UI elements, creates a title text and a start button,
        and sets up the start button's action to load the game level when clicked.
        The start menu UI elements are then added to the overlay.

        Global variables modified:
            title_text: The text displayed as the title of the game.
            start_button: The button that initiates the game when clicked.

        Returns:
            None
    """
    global title_text, start_button
    destroy_ui_elements()  # Clear previous UI elements if any
    title_text = Text(text='Unit 1 Project', scale=5, origin=(0, 0), y=0.3, color=color.white)
    start_button = Button(text='Start Game', color=color.azure, scale=(0.25, 0.1), y=-0.1)
    start_button.on_click = lambda: (destroy(start_button), destroy(title_text), load_level(current_level_index))


    level_overlay_ui.append(title_text)
    level_overlay_ui.append(start_button)


show_start_menu()

# Run the app
app.update = update
app.run()