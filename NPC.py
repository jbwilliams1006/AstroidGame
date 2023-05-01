import pygame 
from Ship import Ship
import math
import random
# NPC class
class NPC(Ship):
    def __init__(self, x, y, rotation, npc_id):
        super().__init__(x, y, rotation, npc_id)
        self.x = x
        self.y = y
        self.position = pygame.Vector2(x, y)
        self.target_ship = None
        self.target_timer = 0
        self.fire_timer = 0
        self.id = npc_id

    def update(self, game_state):
        # Select a target ship if none exists
        if self.target_ship is None:
            eligible_targets = [ship for ship in game_state.ships.values() if ship != self]
            if eligible_targets:
                self.target_ship = random.choice(eligible_targets)

        # Move towards the target ship
        dx = self.target_ship.position.x - self.position.x
        dy = self.target_ship.position.y - self.position.y
        distance_to_target = math.hypot(dx, dy)
        if distance_to_target > 5:
            # move_direction = pygame.Vector2(dx, dy)
            # move_direction.normalize_ip()
            # move_direction *= self.speed
            # self.move(move_direction.x, move_direction.y)
            self.position += pygame.Vector2(dx, dy).normalize() * 2


        # Rotate towards the target ship
        angle_to_target = math.degrees(math.atan2(dy, dx))
        angle_diff = angle_to_target - self.rotation
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        if abs(angle_diff) > 5:
            rotation_direction = 1 if angle_diff > 0 else -1
            self.rotate_right() if rotation_direction > 0 else self.rotate_left()

        # Fire at the target ship
        self.fire_timer += 1
        if self.fire_timer >= 60:
            self.fire_timer = 0
            projectile = self.fire_projectile()
            game_state.projectiles.append(projectile)

        # Select a new target ship after a certain time
        self.target_timer += 1
        if self.target_timer >= 300:
            self.target_timer = 0
            self.target_ship = random.choice(list(game_state.ships.values()))
