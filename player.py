# player.py
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina import Audio, Text
from ursina import invoke
from weapon import Weapon, Bullet
import time
import customtkinter as ctk
import sys

class Player:
    def __init__(self, position=(0, 2, 0), speed=5, jump_height=2):
        self.__controller = FirstPersonController(position=position)
        self.__controller.speed = speed
        self.__controller.jump_height = jump_height

        self.__start_time = time.time()

        self.__weapon = Weapon(parent=self.__controller.camera_pivot)
        self.__weapon.entity.position = Vec3(0.5, -0.5, 1.5)
        self.__weapon.entity.rotation = Vec3(0, 0, 0)

        self.__bullets = []
        self.__shoot_cooldown = .1
        self.__last_shoot_time = 0
        self.__health = HealthBar(bar_color=color.lime.tint(-.25), curve=.5, max_value=100, value=100)

        self.__ammo = 60
        self.__magazine_capacity = 60
        self.__reloading = False
        self.__reload_time = 2.5

        self.__ammo_counter = Text(text=f'MP5K: {self.__ammo}/{self.__magazine_capacity}', position=(0.70, -0.45), scale=2, origin=(0, 0), color=color.white)

    # Getter for health
    def get_health(self):
        return self.__health.value

    def set_health(self, value):
        self.__health.value = value

    # Decrement health safely
    def decrement_health(self, number):
        self.__health.value -= number
        if self.__health.value <= 0:
            self.__health.value = 0
            print("Player has died.")
            self.game_over_popup()  # Call the game over popup when player dies

    # Display Game Over CustomTkinter Popup
    def game_over_popup(self):
        # Initialize the Tkinter root window
        root = ctk.CTk()
        root.geometry("300x150")
        root.title("Game Over")

        # Create a label for the popup
        label = ctk.CTkLabel(root, text="Game Over!", font=("Arial", 24))
        label.pack(pady=20)

        # Create an exit button
        button = ctk.CTkButton(root, text="Exit Game", command=self.exit_game)
        button.pack(pady=20)

        # Start the Tkinter main loop
        root.mainloop()

    # Exit the game
    def exit_game(self):
        sys.exit()

    # Shooting logic (private)
    def __shoot(self):
        if time.time() - self.__last_shoot_time >= self.__shoot_cooldown and self.__ammo > 0:
            bullet = self.__weapon.shoot()
            if bullet:
                self.__bullets.append(bullet)
                self.__ammo -= 1
            self.__last_shoot_time = time.time()

    # Public method to control shooting
    def shoot(self):
        # Check if the mouse is clicked and if the player is not reloading
        if mouse.left and not self.__reloading and time.time() - self.__start_time > 1:
            self.__shoot()

    # Update method
    def update(self):
        if held_keys['shift']:
            self.__controller.speed = 10
        else:
            self.__controller.speed = 5

        if held_keys['r'] and not self.__reloading:
            self.reload()

        # Only shoot when the left mouse button is pressed
        if mouse.left:
            self.shoot()

        for bullet in self.__bullets:
            bullet.update()
            if not bullet.alive:
                self.__bullets.remove(bullet)

        self.__ammo_counter.text = f'MP5K: {self.__ammo}/{self.__magazine_capacity}'
        if self.__ammo > 20:
            self.__ammo_counter.color = color.white
        elif 1 <= self.__ammo <= 20:
            self.__ammo_counter.color = color.yellow
        else:
            self.__ammo_counter.color = color.red

    # Reload method (private)
    def __reload(self):
        if self.__ammo < self.__magazine_capacity:
            self.__reloading = True
            Audio('assets/reload_sound.mp3', autoplay=True)
            invoke(self.__finish_reload, delay=self.__reload_time)

    def reload(self):
        self.__reload()

    # Finish reload logic (private)
    def __finish_reload(self):
        self.__ammo = self.__magazine_capacity
        self.__reloading = False

    @property
    def controller(self):
        return self.__controller