import pygame

class Projectile:
    def __init__(self, x, y, direction,player_id):
        self.x = x
        self.y = y
        self.direction = direction
        self.position = pygame.Vector2(x, y)
        self.speed = 10
        self.id = player_id

    def update(self):
        self.position.x += self.direction.x * self.speed
        self.position.y += self.direction.y * self.speed
        # print(self.position)

    def is_out_of_bounds(self, screen_width, screen_height):
        return (self.position.x < 0 or self.position.x > screen_width or
                self.position.y < 0 or self.position.y > screen_height)

    def check_collision(self, ship):
        distance_to_ship = self.position.distance_to(ship.position)
        return distance_to_ship < 20  # Adjust 20 to the size of your ship
    
    def to_dict(self):
        return {
            'position': [self.position.x, self.position.y],
            'speed': 10,
            'direction': self.direction,
            'owner': self.id
        }