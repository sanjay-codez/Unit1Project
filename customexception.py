
class GameException(Exception):
    """Base class for other exceptions"""
    pass

class PlayerNotFoundError(GameException):
    """Raised when the player entity is not initialized properly"""
    pass

class HealthBelowZeroError(GameException):
    """Raised when health goes below zero"""
    def __init__(self, message="Health cannot go below zero", cause=None):
        super().__init__(message)
        self.cause = cause

class AmmoDepletedError(GameException):
    """Raised when player tries to shoot without ammo"""
    def __init__(self, message="No ammo left", cause=None):
        super().__init__(message)
        self.cause = cause

class GameSaveError(GameException):
    """Raised when there is an error saving the game state"""
    pass










