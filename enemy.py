# enemy.py
from ursina import *
import abc
from math import atan2, degrees
import time

# Abstract Base Class for Enemy
class Enemy(abc.ABC):
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

    # @classmethod
    # def duplicate(cls, position, player_entity, all_enemies):
    #     pass

# Different Enemy Types
class StandardEnemy(Enemy):
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

            # self.all_enemies.append(
            #     StandardEnemy.duplicate(position=self.entity.position, player_entity=self.player_entity,
            #                              all_enemies=self.all_enemies))
            destroy(self.entity)
            destroy(self.health_bar)

            # Remove from the enemies list
            if self in self.all_enemies:
                self.all_enemies.remove(self)


    @classmethod
    def duplicate(cls, position, player_entity, all_enemies):
        return cls(position=position, player_entity=player_entity, all_enemies=all_enemies)




class FancyEnemy(Enemy):
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

class CameraMan(abc.ABC):
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


class StandardCameraMan(CameraMan):
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

# Custom SmoothFollow Script
class CustomSmoothFollow(SmoothFollow):
    def __init__(self, target, offset=(0, 0, 0), speed=1, all_enemies=[]):
        super().__init__(target=target, offset=offset, speed=speed)
        self.min_distance = 5  # Minimum distance to maintain from the player
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