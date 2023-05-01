import pygame
import math
from Projectile import Projectile
import random
import os 
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

#The path to the ship images folder
SHIP_IMAGES_DIR = "images/"

class Ship:
    SHIP_SIZE = (70, 70)
    def __init__(self, x, y, rotation,player_id):
        self.position = pygame.Vector2(x, y)
        self.rotation = rotation
        self.speed = 5
        self.angular_speed = 5
        self.deaths = 0
        self.velocity = pygame.Vector2(0, 0)
        self.image = self.load_random_image()  # Replace with your ship image
        self.health = 100
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=self.position)  # for collision detection
        self.id = player_id
        self.kills = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.deaths += 1
            # self.health = 100  # Reset health after death

    def get_health_bar(self, width=50, height=10):
        # Calculate the health bar fill percentage
        fill_pct = self.health / 100

        # Create the health bar surface
        health_bar_surf = pygame.Surface((width, height))
        health_bar_surf.fill((255, 0, 0))
        
        # Create the health bar fill surface
        fill_surf = pygame.Surface(((width-2)*fill_pct, height-2))
        fill_surf.fill((0, 255, 0))

        # Draw the health bar fill surface onto the health bar surface
        health_bar_surf.blit(fill_surf, (1, 1))

        return health_bar_surf
    def move(self, dx, dy):
        direction = pygame.Vector2(dx, dy).rotate(-self.rotation)
        self.position += direction * self.speed
        self.position.x = max(0, min(self.position.x, SCREEN_WIDTH))
        self.position.y = max(0, min(self.position.y, SCREEN_HEIGHT))

    def rotate_left(self):
        self.rotation -= self.angular_speed
        if self.rotation < 0:
            self.rotation += 360

    def rotate_right(self):
        self.rotation += self.angular_speed
        if self.rotation >= 360:
            self.rotation -= 360

    def fire_projectile(self):
        direction = pygame.Vector2(-math.sin(math.radians(self.rotation)), -math.cos(math.radians(self.rotation)))
        start_position = self.position + direction * self.image.get_width() / 2  # Set start position at the front of the ship 
        return Projectile(start_position.x, start_position.y, direction, self.id)
    
    def load_random_image(self):
        # Get a list of all ship image filenames in the directory
        ship_images = [filename for filename in os.listdir(SHIP_IMAGES_DIR) if filename.endswith(".png")]
        # Choose a random ship image filename
        image_filename = random.choice(ship_images)

        # Load the image from file and resize it to the desired size
        image = pygame.image.load(os.path.join(SHIP_IMAGES_DIR, image_filename)).convert_alpha()
        image = pygame.transform.scale(image, Ship.SHIP_SIZE)

        # Return the resized image
        return image