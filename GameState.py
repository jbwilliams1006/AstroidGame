import pygame
from NPC import NPC
# GameState class
class gameState:
    def __init__(self):
        self.ships = {}  # a dictionary mapping ship IDs to ship objects
        self.projectiles = []  # a list of projectile objects
        self.scores = {}  # a dictionary mapping player names to their score (number of deaths)
    def add_ship(self, id, ship):
        self.ships[id] = ship

    def remove_ship(self, id):
        del self.ships[id]

    def get_ship(self, id):
        return self.ships.get(id)

    def get_all_ships(self):
        return self.ships.values()

    def get_npc_ships(self):
        return [ship for ship in self.ships.values() if isinstance(ship, NPC)]