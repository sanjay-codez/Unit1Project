# enemy.py
from ursina import *
import abc
from math import atan2, degrees
import time

# Abstract Base Class for Enemy
class Enemy(abc.ABC):
    """
        Abstract base class representing an enemy in the game.

        This class defines the common attributes and methods for all enemy types,
        including health management and attack behavior. It serves as a blueprint
        for creating specific enemy subclasses.

        Attributes:
            position (Vec3): The position of the enemy in the game world.
            health (int): The current health of the enemy.
            max_health (int): The maximum health of the enemy.

        Methods:
            attack(): Abstract method to define the attack behavior of the enemy.
            update_health_bar(): Abstract method to update the visual representation
                                 of the enemy's health.
            decrement_health(amount): Abstract method to reduce the enemy's health
                                      by a specified amount.
            is_alive(enemy_instance): Class method to check if the enemy is still alive.
            siphon_health(enemy_instance, amount): Class method to restore health to the enemy
                                                    when they siphon from the player.
    """
    def __init__(self, position):
        self.position = position
        self.health = 100
        self.max_health = 100

    @abc.abstractmethod
    def attack(self):
        pass

    @abc.abstractmethod
    def update_health_bar(self):
        pass

    @abc.abstractmethod
    def decrement_health(self, amount):
        pass

    @classmethod
    def is_alive(cls, enemy_instance):
        """Check if the enemy is still alive based on their health."""
        return enemy_instance.health > 0

    @classmethod
    def siphon_health(cls, enemy_instance, amount):
        """Restore health to the enemy when they siphon from the player."""
        enemy_instance.health += amount
        if enemy_instance.health > enemy_instance.max_health:
            enemy_instance.health = enemy_instance.max_health
        enemy_instance.update_health_bar()


# Different Enemy Types
class StandardEnemy(Enemy):
    """
        Represents a standard enemy type in the game.

        This class defines the behavior and attributes of a standard enemy, including its
        movement towards the player, health management, and attack logic. It inherits from
        the abstract Enemy class.

        Attributes:
            entity (Entity): The visual representation of the enemy in the game world.
            player_entity (Entity): Reference to the player entity for attack and movement logic.
            all_enemies (list): Reference to the list of all enemy instances in the game.
            health_bar (Entity): The visual representation of the enemy's health.
            last_attack_time (float): The last time the enemy attacked the player.

        Methods:
            update_health_bar(): Updates the health bar size and color based on the enemy's current health.
            attack(player): Checks the distance to the player and inflicts damage if within range.
            decrement_health(amount): Reduces the enemy's health by a specified amount and handles death logic.
            duplicate(position, player_entity, all_enemies): Class method to create a duplicate of the enemy.
    """
    def __init__(self, position, player_entity, all_enemies):
        super().__init__(position)
        self.entity = Entity(
            model='assets/man.fbx',
            scale=(.005, .005, .005),
            position=position,
            color=color.smoke,
            name="StandardEnemy",
            double_sided=True,
            collider='box'
        )
        self.player_entity = player_entity
        self.all_enemies = all_enemies  # Save the reference to the enemies list
        self.entity.add_script(CustomSmoothFollow(target=player_entity, offset=(0, 2, 0), speed=.5, all_enemies=all_enemies))
        self.last_attack_time = 0

        # Create the health bar entity
        self.health_bar = Entity(
            model='cube',  # Using 'quad' model to make it more visible
            color=color.green,
            scale=(3, 0.5, 0.1),  # Larger size to make it more visible
            position=self.entity.position + Vec3(0, 3, 0),  # Place it above the enemy initially
            always_on_top=True  # Always render on top for better visibility
        )
        self.entity.parent_enemy = self

    def update_health_bar(self):
        # Update the health bar size based on the current health
        health_ratio = max(self.health / self.max_health, 0)  # Ensure health ratio is not below 0
        self.health_bar.scale_x = health_ratio * 3  # Scale X-axis based on health (max length of 3)

        # Change color based on health (Green -> Yellow -> Red)
        if health_ratio > 0.5:
            self.health_bar.color = color.green
        elif 0.2 < health_ratio <= 0.5:
            self.health_bar.color = color.yellow
        else:
            self.health_bar.color = color.red

        # Update the position to always hover above the enemy
        self.health_bar.position = self.entity.position + Vec3(0, 3, 0)  # Keep it above the entity


        # Ensure the health bar always faces the camera (billboarding effect)
        direction = (self.player_entity.position - self.health_bar.world_position).normalized()
        self.health_bar.rotation = Vec3(0, degrees(atan2(direction.x, direction.z)), 0)

    def attack(self, player):
        distance_to_player = (self.player_entity.position - self.entity.position).length()
        current_time = time.time()
        if distance_to_player < 3 and current_time - self.last_attack_time >= 1:
            player.decrement_health(random.randint(3, 5))
            Audio('assets/hit_sound.mp3', autoplay=True)  # Add hit sound playback here
            self.last_attack_time = current_time

    def decrement_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.update_health_bar()  # Update the health bar to reflect new health

        # Add logic to destroy the enemy entity and remove from the enemies list
        if self.health <= 0:


            destroy(self.entity)
            destroy(self.health_bar)

            # Remove from the enemies list
            if self in self.all_enemies:
                self.all_enemies.remove(self)


    @classmethod
    def duplicate(cls, position, player_entity, all_enemies):
        return cls(position=position, player_entity=player_entity, all_enemies=all_enemies)




class FancyEnemy(Enemy):
    """
        Represents a fancy enemy type in the game.

        This class defines the behavior and attributes of a fancy enemy, including its
        movement towards the player, health management, and attack logic. It inherits from
        the abstract Enemy class.

        Attributes:
            entity (Entity): The visual representation of the enemy in the game world.
            player_entity (Entity): Reference to the player entity for attack and movement logic.
            all_enemies (list): Reference to the list of all enemy instances in the game.
            health_bar (Entity): The visual representation of the enemy's health.
            last_attack_time (float): The last time the enemy attacked the player.

        Methods:
            update_health_bar(): Updates the health bar size and color based on the enemy's current health.
            attack(player): Checks the distance to the player and inflicts damage if within range,
                            and siphons health from the player.
            decrement_health(amount): Reduces the enemy's health by a specified amount and handles death logic.
            duplicate(position, player_entity, all_enemies): Class method to create a duplicate of the enemy.
    """
    def __init__(self, position, player_entity, all_enemies):
        super().__init__(position)
        self.entity = Entity(
            model='assets/man.fbx',
            scale=(.005, .005, .005),
            position=position,
            color=color.gold,
            name="Fancyenemy",
            double_sided=True,
            collider='box'
        )
        self.player_entity = player_entity
        self.all_enemies = all_enemies  # Save the reference to the enemies list
        self.entity.add_script(CustomSmoothFollow(target=player_entity, offset=(0, 2, 0), speed=.5, all_enemies=all_enemies))
        self.last_attack_time = 0

        # Create the health bar entity
        self.health_bar = Entity(
            model='cube',  # Using 'quad' model to make it more visible
            color=color.green,
            scale=(3, 0.5, 0.1),  # Larger size to make it more visible
            position=self.entity.position + Vec3(0, 3, 0),  # Place it above the enemy initially
            always_on_top=True  # Always render on top for better visibility
        )
        self.entity.parent_enemy = self

    def update_health_bar(self):
        # Update the health bar size based on the current health
        health_ratio = max(self.health / self.max_health, 0)  # Ensure health ratio is not below 0
        self.health_bar.scale_x = health_ratio * 3  # Scale X-axis based on health (max length of 3)

        # Change color based on health (Green -> Yellow -> Red)
        if health_ratio > 0.5:
            self.health_bar.color = color.green
        elif 0.2 < health_ratio <= 0.5:
            self.health_bar.color = color.yellow
        else:
            self.health_bar.color = color.red

        # Update the position to always hover above the enemy
        self.health_bar.position = self.entity.position + Vec3(0, 3, 0)  # Keep it above the entity

        # Ensure the health bar always faces the camera (billboarding effect)
        direction = (self.player_entity.position - self.health_bar.world_position).normalized()
        self.health_bar.rotation = Vec3(0, degrees(atan2(direction.x, direction.z)), 0)

    def attack(self, player):
        distance_to_player = (self.player_entity.position - self.entity.position).length()
        current_time = time.time()
        if distance_to_player < 3 and current_time - self.last_attack_time >= 1:
            damage = random.randint(3, 5)
            player.decrement_health(damage)
            Audio('assets/hit_sound.mp3', autoplay=True)
            self.last_attack_time = current_time

            # Use the siphon_health class method
            Enemy.siphon_health(self, damage)

    def decrement_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.update_health_bar()  # Update the health bar to reflect new health

        # Add logic to destroy the enemy entity and remove from the enemies list
        if self.health <= 0:
            destroy(self.entity)
            destroy(self.health_bar)

            # Remove from the enemies list
            if self in self.all_enemies:
                self.all_enemies.remove(self)

    @classmethod
    def duplicate(cls, position, player_entity, all_enemies):
        return cls(position=position, player_entity=player_entity, all_enemies=all_enemies)

class CameraMan(abc.ABC):
    """
        Abstract base class representing a CameraMan enemy in the game.

        This class defines the common attributes and methods for all CameraMan types,
        including health management and attack behavior. It serves as a blueprint
        for creating specific CameraMan subclasses.

        Attributes:
            position (Vec3): The position of the CameraMan in the game world.
            health (int): The current health of the CameraMan.
            max_health (int): The maximum health of the CameraMan.

        Methods:
            attack(): Abstract method to define the attack behavior of the CameraMan.
            update_health_bar(): Abstract method to update the visual representation
                                 of the CameraMan's health.
            decrement_health(amount): Abstract method to reduce the CameraMan's health
                                      by a specified amount.
            duplicate(position, player_entity, all_enemies): Abstract class method to create
                                                              a duplicate of the CameraMan.
            is_alive(enemy_instance): Class method to check if the CameraMan is still alive.
            siphon_health(enemy_instance, amount): Class method to restore health to the CameraMan
                                                    when they siphon from the player.
    """
    def __init__(self, position):
        self.position = position
        self.health = 100
        self.max_health = 100

    @abc.abstractmethod
    def attack(self):
        pass

    @abc.abstractmethod
    def update_health_bar(self):
        pass

    @abc.abstractmethod
    def decrement_health(self, amount):
        pass

    @classmethod
    def duplicate(cls, position, player_entity, all_enemies):
        pass

    @classmethod
    def is_alive(cls, enemy_instance):
        """Check if the enemy is still alive based on their health."""
        return enemy_instance.health > 0

    @classmethod
    def siphon_health(cls, enemy_instance, amount):
        """Restore health to the enemy when they siphon from the player."""
        enemy_instance.health += amount
        if enemy_instance.health > enemy_instance.max_health:
            enemy_instance.health = enemy_instance.max_health
        enemy_instance.update_health_bar()


class StandardCameraMan(CameraMan):
    """
        Represents a standard CameraMan enemy type in the game.

        This class defines the behavior and attributes of a standard CameraMan,
        including its movement towards the player, health management, and attack logic.
        It inherits from the CameraMan abstract class.

        Attributes:
            entity (Entity): The visual representation of the CameraMan in the game world.
            player_entity (Entity): Reference to the player entity for attack and movement logic.
            all_enemies (list): Reference to the list of all enemy instances in the game.
            health_bar (Entity): The visual representation of the CameraMan's health.
            last_attack_time (float): The last time the CameraMan attacked the player.

        Methods:
            update_health_bar(): Updates the health bar size and color based on the CameraMan's current health.
            attack(player): Checks the distance to the player and inflicts damage if within range.
            decrement_health(amount): Reduces the CameraMan's health by a specified amount and handles death logic.
            duplicate(position, player_entity, all_enemies): Class method to create a duplicate of the CameraMan.
    """
    def __init__(self, position, player_entity, all_enemies):
        super().__init__(position)
        self.entity = Entity(
            model='assets/CameraMan.glb',
            scale=(2, 2, 2),
            position=position,
            color=color.smoke,
            name="StandardCameraMan",
            double_sided=True,
            collider='box'
        )
        self.player_entity = player_entity
        self.all_enemies = all_enemies  # Save the reference to the enemies list
        self.entity.add_script(CustomSmoothFollow(target=player_entity, offset=(0, 2, 0), speed=.5, all_enemies=all_enemies))
        self.last_attack_time = 0

        # Create the health bar entity
        self.health_bar = Entity(
            model='cube',  # Using 'quad' model to make it more visible
            color=color.green,
            scale=(3, 0.5, 0.1),  # Larger size to make it more visible
            position=self.entity.position + Vec3(0, 3, 0),  # Place it above the enemy initially
            always_on_top=True  # Always render on top for better visibility
        )
        self.entity.parent_enemy = self

    def update_health_bar(self):
        # Update the health bar size based on the current health
        health_ratio = max(self.health / self.max_health, 0)  # Ensure health ratio is not below 0
        self.health_bar.scale_x = health_ratio * 3  # Scale X-axis based on health (max length of 3)

        # Change color based on health (Green -> Yellow -> Red)
        if health_ratio > 0.5:
            self.health_bar.color = color.green
        elif 0.2 < health_ratio <= 0.5:
            self.health_bar.color = color.yellow
        else:
            self.health_bar.color = color.red

        # Update the position to always hover above the enemy
        self.health_bar.position = self.entity.position + Vec3(0, 3, 0)  # Keep it above the entity


        # Ensure the health bar always faces the camera (billboarding effect)
        direction = (self.player_entity.position - self.health_bar.world_position).normalized()
        self.health_bar.rotation = Vec3(0, degrees(atan2(direction.x, direction.z)), 0)

    def attack(self, player):
        distance_to_player = (self.player_entity.position - self.entity.position).length()
        current_time = time.time()
        if distance_to_player < 3 and current_time - self.last_attack_time >= 1:
            player.decrement_health(random.randint(3, 5))
            Audio('assets/hit_sound.mp3', autoplay=True)  # Add hit sound playback here
            self.last_attack_time = current_time

    def decrement_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.update_health_bar()  # Update the health bar to reflect new health

        # Add logic to destroy the enemy entity and remove from the enemies list
        if self.health <= 0:
            destroy(self.entity)
            destroy(self.health_bar)

            # Remove from the enemies list
            if self in self.all_enemies:
                self.all_enemies.remove(self)

    @classmethod
    def duplicate(cls, position, player_entity, all_enemies):
        return cls(position=position, player_entity=player_entity, all_enemies=all_enemies)

class FancyCameraMan(CameraMan):
    """
        Represents a fancy CameraMan enemy type in the game.

        This class defines the behavior and attributes of a fancy CameraMan,
        including its movement towards the player, health management, and attack logic.
        It inherits from the CameraMan abstract class.

        Attributes:
            entity (Entity): The visual representation of the CameraMan in the game world.
            player_entity (Entity): Reference to the player entity for attack and movement logic.
            all_enemies (list): Reference to the list of all enemy instances in the game.
            health_bar (Entity): The visual representation of the CameraMan's health.
            last_attack_time (float): The last time the CameraMan attacked the player.

        Methods:
            update_health_bar(): Updates the health bar size and color based on the CameraMan's current health.
            attack(player): Checks the distance to the player and inflicts damage if within range,
                            while siphoning health from the player.
            decrement_health(amount): Reduces the CameraMan's health by a specified amount and handles death logic.
            duplicate(position, player_entity, all_enemies): Class method to create a duplicate of the CameraMan.
    """
    def __init__(self, position, player_entity, all_enemies):
        super().__init__(position)
        self.entity = Entity(
            model='assets/CameraMan.glb',
            scale=(2, 2, 2),
            position=position,
            color=color.gold,
            name="FancyCameraMan",
            double_sided=True,
            collider='box'
        )
        self.player_entity = player_entity
        self.all_enemies = all_enemies  # Save the reference to the enemies list
        self.entity.add_script(CustomSmoothFollow(target=player_entity, offset=(0, 2, 0), speed=.5, all_enemies=all_enemies))
        self.last_attack_time = 0

        # Create the health bar entity
        self.health_bar = Entity(
            model='cube',  # Using 'quad' model to make it more visible
            color=color.green,
            scale=(3, 0.5, 0.1),  # Larger size to make it more visible
            position=self.entity.position + Vec3(0, 3, 0),  # Place it above the enemy initially
            always_on_top=True  # Always render on top for better visibility
        )
        self.entity.parent_enemy = self

    def update_health_bar(self):
        # Update the health bar size based on the current health
        health_ratio = max(self.health / self.max_health, 0)  # Ensure health ratio is not below 0
        self.health_bar.scale_x = health_ratio * 3  # Scale X-axis based on health (max length of 3)

        # Change color based on health (Green -> Yellow -> Red)
        if health_ratio > 0.5:
            self.health_bar.color = color.green
        elif 0.2 < health_ratio <= 0.5:
            self.health_bar.color = color.yellow
        else:
            self.health_bar.color = color.red

        # Update the position to always hover above the enemy
        self.health_bar.position = self.entity.position + Vec3(0, 3, 0)  # Keep it above the entity


        # Ensure the health bar always faces the camera (billboarding effect)
        direction = (self.player_entity.position - self.health_bar.world_position).normalized()
        self.health_bar.rotation = Vec3(0, degrees(atan2(direction.x, direction.z)), 0)

    def attack(self, player):
        distance_to_player = (self.player_entity.position - self.entity.position).length()
        current_time = time.time()
        if distance_to_player < 3 and current_time - self.last_attack_time >= 1:
            damage = random.randint(3, 5)
            player.decrement_health(damage)
            Audio('assets/hit_sound.mp3', autoplay=True)
            self.last_attack_time = current_time

            # Use the siphon_health class method
            Enemy.siphon_health(self, damage)

    def decrement_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.update_health_bar()  # Update the health bar to reflect new health

        # Add logic to destroy the enemy entity and remove from the enemies list
        if self.health <= 0:
            destroy(self.entity)
            destroy(self.health_bar)

            # Remove from the enemies list
            if self in self.all_enemies:
                self.all_enemies.remove(self)

    @classmethod
    def duplicate(cls, position, player_entity, all_enemies):
        return cls(position=position, player_entity=player_entity, all_enemies=all_enemies)

# Custom SmoothFollow Script
class CustomSmoothFollow(SmoothFollow):
    """
        A custom class for smooth following behavior for enemies.

        This class extends the SmoothFollow functionality to allow enemies to smoothly follow the player,
        while also maintaining a minimum distance from both the player and other enemies.

        Attributes:
            min_distance (float): Minimum distance to maintain from the player.
            all_enemies (list): Reference to the list of all enemy instances in the game.
            min_enemy_distance (float): Minimum distance to maintain from other enemies.

        Methods:
            calculate_distance(position1, position2): Calculates the distance between two positions.
            calculate_desired_rotation_y(target_position, entity_position): Calculates the desired rotation
                                                                            around the Y-axis to face the target.
            lerp_rotation(current_rotation, desired_rotation, factor): Linearly interpolates between the current
                                                                       and desired rotations.
            ensure_ground_rotation(entity): Ensures that the entity maintains a horizontal rotation.
            calculate_direction_away(position1, position2): Calculates the normalized direction away from one position to another.
            update(): Updates the enemy's position and rotation to smoothly follow the player and avoid overlapping with other enemies.
    """
    def __init__(self, target, offset=(0, 0, 0), speed=1, all_enemies=[]):
        super().__init__(target=target, offset=offset, speed=speed)
        self.min_distance = 2  # Minimum distance to maintain from the player
        self.all_enemies = all_enemies
        self.min_enemy_distance = 2.5  # Minimum distance to maintain from other enemies

    @staticmethod
    def calculate_distance(position1, position2):
        return (position1 - position2).length()

    @staticmethod
    def calculate_desired_rotation_y(target_position, entity_position):
        target_direction = (target_position - entity_position).normalized()
        return atan2(target_direction.x, target_direction.z)

    @staticmethod
    def lerp_rotation(current_rotation, desired_rotation, factor):
        return lerp(current_rotation, degrees(desired_rotation), factor)

    @staticmethod
    def ensure_ground_rotation(entity):
        entity.rotation_x = 0
        entity.rotation_z = 0

    @staticmethod
    def calculate_direction_away(position1, position2):
        return (position1 - position2).normalized()

    def update(self):
        # Calculate the distance to the player using the static method
        distance_to_player = CustomSmoothFollow.calculate_distance(self.target.position, self.entity.position)
        if distance_to_player > self.min_distance:
            super().update()  # Call the original update to follow the player

        # Smoothly rotate the enemy to face the player on the Y-axis only
        desired_rotation_y = CustomSmoothFollow.calculate_desired_rotation_y(self.target.position, self.entity.position)
        current_rotation_y = self.entity.rotation_y
        self.entity.rotation_y = CustomSmoothFollow.lerp_rotation(current_rotation_y, desired_rotation_y, time.dt * 2)

        # Ensure the enemy doesn't rotate around the X or Z axis (feet on the ground)
        CustomSmoothFollow.ensure_ground_rotation(self.entity)

        # make sure they don't overlap
        for other in self.all_enemies:
            if other.entity == self.entity:
                continue
            # Calculate the distance to other enemies using the static method
            distance_to_other = CustomSmoothFollow.calculate_distance(other.entity.position, self.entity.position)
            if distance_to_other < self.min_enemy_distance:
                # move away from the other enemy
                direction_away = CustomSmoothFollow.calculate_direction_away(self.entity.position, other.entity.position)
                self.entity.position += direction_away * time.dt * self.speed