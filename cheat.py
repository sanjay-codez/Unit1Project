import pickle
import os
import customtkinter as ctk
from tkinter import messagebox
from customexception import GameException


# Load saved data from pickle
def load_game_state(filename="pickle_data/savefile.pkl"):
    try:
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                try:
                    game_state = pickle.load(f)
                except pickle.PickleError as e:
                    raise GameException("Failed to deserialize game state.") from e
            return game_state
        else:
            raise FileNotFoundError(f"Save file '{filename}' not found.")
    except FileNotFoundError as e:
        # Chain the FileNotFoundError to a GameException
        raise GameException("Unable to load game state due to missing file.") from e
    except Exception as e:
        # Chain any other exceptions to GameException
        raise GameException("An unknown error occurred while loading the game state.") from e


# Save data to pickle file
def save_game_state(game_state, filename="pickle_data/savefile.pkl"):
    try:
        with open(filename, "wb") as f:
            try:
                pickle.dump(game_state, f)
            except pickle.PickleError as e:
                raise GameException("Failed to serialize game state.") from e
        messagebox.showinfo("Success", "Game state saved successfully!")
    except Exception as e:
        # Chain any exceptions that occur while saving
        raise GameException("An error occurred while saving the game state.") from e


# GUI to modify save data
class SaveEditorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Game Save Data Editor")
        self.geometry("500x400")
        self.resizable(False, False)

        # Load saved data
        self.game_state = load_game_state()
        if not self.game_state:
            self.quit()

        # GUI Elements
        self.setup_gui()

    def setup_gui(self):
        # Player Health Slider
        self.health_label = ctk.CTkLabel(self, text="Player Health:", font=("Arial", 16))
        self.health_label.pack(pady=(20, 5))

        self.health_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100)
        self.health_slider.set(self.game_state["player_health"])
        self.health_slider.pack(pady=(5, 20))

        # Level Selector Dropdown
        self.level_label = ctk.CTkLabel(self, text="Select Level:", font=("Arial", 16))
        self.level_label.pack(pady=(10, 5))

        self.level_options = ["Level 1", "Level 2", "Level 3"]
        self.level_var = ctk.StringVar(value=f"Level {self.game_state['current_level_index'] + 1}")
        self.level_dropdown = ctk.CTkOptionMenu(self, values=self.level_options, variable=self.level_var)
        self.level_dropdown.pack(pady=(5, 20))

        # Save Button
        self.save_button = ctk.CTkButton(self, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=(30, 10))

    def save_changes(self):
        # Update player health
        new_health = self.health_slider.get()
        self.game_state["player_health"] = new_health

        # Update level
        selected_level = self.level_var.get()
        new_level_index = self.level_options.index(selected_level)

        if new_level_index != self.game_state["current_level_index"]:
            # Update level index
            self.game_state["current_level_index"] = new_level_index

            # Reset toilets based on selected level
            if new_level_index == 0:  # Level 1
                self.game_state["enemies"] = [
                    ("StandardEnemy", (10, 0.5, 2), 100),
                    ("FancyEnemy", (-2, 0.5, 2), 100),
                    ("StandardCameraMan", (15, 0.5, 2), 100),
                    ("FancyCameraMan", (-10, 0.5, 2), 100)
                ]
            elif new_level_index == 1:  # Level 2
                self.game_state["enemies"] = [
                    ("StandardEnemy", (10, 0.5, 2), 100),
                    ("FancyEnemy", (-2, 0.5, 2), 100),
                    ("StandardCameraMan", (15, 0.5, 2), 100),
                    ("FancyCameraMan", (-10, 0.5, 2), 100),
                    ("StandardEnemy", (15, 0.5, 2), 100),
                    ("FancyEnemy", (-7, 0.5, 2), 100)
                ]
            elif new_level_index == 2:  # Level 3
                self.game_state["enemies"] = [
                    ("StandardEnemy", (10, 0.5, 2), 100),
                    ("FancyEnemy", (-2, 0.5, 2), 100),
                    ("StandardCameraMan", (15, 0.5, 2), 100),
                    ("FancyCameraMan", (-10, 0.5, 2), 100),
                    ("StandardEnemy", (15, 0.5, 2), 100),
                    ("FancyEnemy", (-7, 0.5, 2), 100),
                    ("StandardEnemy", (20, 0.5, 2), 100)
                ]

        # Save updated game state
        save_game_state(self.game_state)


# Run the SaveEditorGUI
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = SaveEditorGUI()
    app.mainloop()