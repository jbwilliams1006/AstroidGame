# import pygame 
# import random
# import json
# from NPC import NPC
# from Ship import Ship
# import math
# import time
# import uuid
# import json
# import os
# from GameState import gameState
# import base64
# from comms2 import CommsSender, CommsListener


# BACKGROUND_IMAGE_FILE = "images/space.PNG"
# pygame.mixer.init()

# explodesound = pygame.mixer.Sound('Chunky Explosion.mp3')


# class Vector2Encoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, pygame.math.Vector2):
#             return {"x": obj.x, "y": obj.y}
#         return super().default(obj)

# # Game class
# class Game:
#     def __init__(self, game_duration, screen_width, screen_height):
#         self.game_duration = game_duration
#         self.screen_width = screen_width
#         self.screen_height = screen_height
#         self.start_time = pygame.time.get_ticks()  # Set the start time to the current time
#         self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
#         pygame.display.set_caption("Ship Battle Royale")
#         self.game_state = gameState()
#         # self.player_id = str(uuid.uuid4())
#         # self.player_ship = Ship(0, 0, 0,self.player_id)
#         self.destroyed_ships = []
#         self.last_fire_time = 0
        
#         # Load the background image and scale it to the window size
#         self.background_image = pygame.image.load(BACKGROUND_IMAGE_FILE).convert()
#         self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        


#         creds = {
#         "exchange": "2dgame",
#         "port": "5672",
#         "host": "terrywgriffin.com",
#         "user": "jbwilliams1006",
#         "password": "jbwilliams1006" + "2023!!!",
#         }
#         # # create instances of a comms listener and sender
#         # # to handle message passing.
#         # self.commsListener = CommsListener(**creds)
#         # self.commsSender = CommsSender(**creds)

#         self.player_id = creds["user"]
#         self.player_ship = Ship(0, 0, 0,self.player_id)
#         # Add a ship to the game state
#         self.game_state.ships[self.player_id] = self.player_ship

#         # Create NPCs
#         for i in range(50):
#             npc_id = str(uuid.uuid4())
#             npc_ship = NPC(random.randint(0, self.screen_width), random.randint(0, self.screen_height), random.randint(0, 360),npc_id)
#             self.game_state.add_ship(npc_id, npc_ship)

#         print(self.game_state.ships)


#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.is_running = False

#         keys = pygame.key.get_pressed()

#         # Assuming the first ship in the game_state.ships dictionary is the player's ship
#         player_ship = list(self.game_state.ships.values())[0]

#         if keys[pygame.K_w]:
#             player_ship.move(0, -1)
#         if keys[pygame.K_s]:
#             player_ship.move(0, 1)
#         if keys[pygame.K_a]:
#             player_ship.rotate_right()
#         if keys[pygame.K_d]:
#             player_ship.rotate_left()

#         # Check if enough time has passed since last fire
#         current_time = pygame.time.get_ticks()
#         time_since_last_fire = current_time - self.last_fire_time

#         if keys[pygame.K_SPACE] and time_since_last_fire >= 500:
        
#             # Fire a projectile and set the last fire time to current time
#             self.game_state.projectiles.append(player_ship.fire_projectile())
#             self.last_fire_time = current_time
#             # Create a message containing the firing ship ID and the projectile data
#             # message = {
#             #     "type": "projectile_fired",
#             #     "ship_id": player_ship.id,
#             #     "Projectile":self.game_state.projectiles[-1].to_dict() #Last projectile fired
#             # }

#             # Send the message to the RabbitMQ exchange with the routing key "game.projectile"
#             #self.commsSender.send("game.projectile", json.dumps(message,cls= Vector2Encoder))
                    



#     def update(self):
#         #  # Listen for messages from the RabbitMQ exchange on a separate thread
#         # self.commsListener.threadedListen()
#         # # Process any new messages in the _messageQueue attribute of the listener instance
#         # for message in self.commsListener._messageQueue.get("guest", []):
#         #     # Parse the message JSON data
#         #     message

#         # Update ships
#         for ship in self.game_state.ships.values():
#             # Update ship position based on its velocity
#             dx = ship.velocity.x
#             dy = ship.velocity.y
#             ship.move(dx, dy)
        
#         # Update projectiles
#         projectiles_copy = self.game_state.projectiles.copy()

#         # Update projectiles
#         for projectile in projectiles_copy:
#             # Update projectile position based on its velocity
#             projectile.update()

#             # Check for collisions with ships
#             for ship in self.game_state.ships.values():
#                 if projectile.check_collision(ship):
#                     print(ship, "was Hit")
#                     ship.take_damage(10)
#                    # Remove the projectile
#                     try:
#                         self.game_state.projectiles.remove(projectile)
#                     except ValueError:
#                         pass
#                     print("Projectile Removed")
#                     if ship.health <=0:
#                             # # Add ship to destroyed ships list
#                             # self.destroyed_ships.append(ship)
#                         self.game_state.ships[projectile.id].kills += 1
#                         print(self.game_state.ships[projectile.id], f"earned a kill and now has {self.game_state.ships[projectile.id].kills} kills!")
#                         # Start explosion animation
#                         # Load explosion images
#                         explosion_images = []
#                         for i in range(1,7):
#                             filename = os.path.join('Explosions/', f'Explosion{i}.png')
#                             image = pygame.image.load(filename).convert()
#                             image = pygame.transform.scale(image, Ship.SHIP_SIZE)
#                             explosion_images.append(image)

#                         # Set up explosion animation
#                         explosion_animation = pygame.sprite.Group()
#                         for i in range(0,6):
#                             explosion_sprite = pygame.sprite.Sprite()
#                             explosion_sprite.image = explosion_images[i]
#                             explosion_sprite.rect = explosion_sprite.image.get_rect()
#                             explosion_animation.add(explosion_sprite)


#                         explosion_animation_pos = ship.position.x, ship.position.y
#                         explodesound.play()
#                         for i in range(0,6):
#                             explosion_sprite = explosion_animation.sprites()[i]
#                             explosion_sprite.rect.center = explosion_animation_pos
#                             self.screen.blit(explosion_sprite.image, explosion_sprite.rect)
#                             pygame.display.flip()
                        
#                         # Respawn ship at a random location
#                         ship.position.x = random.randint(0, self.screen_width)
#                         ship.position.y = random.randint(0, self.screen_height)
#                         ship.health = 100

#             # Remove projectiles that are out of bounds
#             if projectile.is_out_of_bounds(self.screen_width, self.screen_height):
#                 try:
#                     self.game_state.projectiles.remove(projectile)
#                 except ValueError:
#                     pass
        
#         # # Remove destroyed ships from game state
#         # for ship in self.destroyed_ships:
#         #     self.game_state.remove_ship(ship.id)
#         #     print("Player:",ship.id, " Removed")
#         # self.destroyed_ships = []

#         # Handle NPC behavior (e.g., random movement and shooting)
#         # Update NPC ships
#         for npc_ship in self.game_state.get_npc_ships():
#             npc_ship.update(self.game_state)

#         # # Send state of game to exchange
#         # state = {
#         #     "ships": {player: {"position": ship.position, "angle": ship.rotation, "kill_count": ship.kills} for player, ship in self.game_state.ships.items()},
#         #     "projectiles": [{"position": projectile.position, "velocity": projectile.speed} for projectile in self.game_state.projectiles],
#         #     "npcs": [{"position": npc.position, "angle": npc.rotation} for npc in self.game_state.get_npc_ships()],
#         # }
#         # message = json.dumps(state, cls=Vector2Encoder)
#         # self.commsSender.threadedSend("game_state", message)

#     def render(self):
#         # Draw the background image on the screen
#         self.screen.blit(self.background_image, (0, 0))
        
#         font = pygame.font.Font("PressStart2P.ttf",20)


#         # Render the timer
#         time_remaining = max(0, self.game_duration - (pygame.time.get_ticks() - self.start_time) // 1000)
#         text = f"Time: {time_remaining} s"
#         text_surface = font.render(text, True, (255, 215, 0))
#         text_rect = text_surface.get_rect(topright=(self.screen_width - 10, 20))
#         self.screen.blit(text_surface, text_rect)


#         # Render the top player's name and kill count
#         top_player = max(self.game_state.ships.values(), key=lambda ship: ship.kills)
#         text = f"Top Player: {top_player.id} - {top_player.kills} kills"
#         text_surface = font.render(text, True, (255, 0, 0))
#         text_rect = text_surface.get_rect(center=(self.screen_width/ 2, 20))
#         self.screen.blit(text_surface, text_rect)

#         # Render player ship
#         player_ship = list(self.game_state.ships.values())[0]
#         rotated_image = pygame.transform.rotate(player_ship.image, player_ship.rotation)
#         # Render the ship ID as text
#         id_text = font.render(player_ship.id[:4], True, (0, 255, 0))
#         # Get the position to blit the text
#         id_text_pos = (player_ship.position.x, player_ship.position.y - 20)
#         rect = rotated_image.get_rect(center=(player_ship.position.x, player_ship.position.y))
#         self.screen.blit(rotated_image, rect)
#         # Blit the text onto the ship's surface
#         self.screen.blit(id_text, id_text_pos)     

        
#         # Draw the health bar
#         health_bar = player_ship.get_health_bar()
#         health_bar_rect = health_bar.get_rect(center=(player_ship.position.x, player_ship.position.y + 30))  # Adjust position as needed
#         self.screen.blit(health_bar, health_bar_rect)


#         # Kill count
#         if player_ship == top_player:
#             kills_text = font.render(str(player_ship.kills), True, (255, 215, 0))
#         else:
#             kills_text = font.render(str(player_ship.kills), True, (255, 255, 255))

#         kills_rect = kills_text.get_rect(center=(player_ship.position.x, player_ship.position.y - rotated_image.get_height() / 2 - 10))
#         self.screen.blit(kills_text, kills_rect)


#         # Render NPC ships
#         for npc_ship in self.game_state.get_npc_ships():
#                 rotated_image = pygame.transform.rotate(npc_ship.image, npc_ship.rotation)
#                 rect = rotated_image.get_rect(center=(npc_ship.position.x, npc_ship.position.y))
#                 # Render the ship ID as text
#                 id_text = font.render(npc_ship.id[:4], True, (255, 255, 255))
#                 # Get the position to blit the text
#                 id_text_pos = (npc_ship.position.x, npc_ship.position.y - 20)
#                 self.screen.blit(rotated_image, rect)
#                 # Blit the text onto the ship's surface
#                 self.screen.blit(id_text, id_text_pos)     

#                 # Draw the health bar
#                 NPChealth_bar = npc_ship.get_health_bar()
#                 NPChealth_bar_rect = NPChealth_bar.get_rect(center=(npc_ship.position.x, npc_ship.position.y + 30))  # Adjust position as needed
#                 self.screen.blit(NPChealth_bar, NPChealth_bar_rect)

#                 # Kill count for NPCs
#                 if npc_ship == top_player:
#                     NPCkills_text = font.render(str(npc_ship.kills), True, (255, 215, 0))
#                 else:
#                     NPCkills_text = font.render(str(npc_ship.kills), True, (255, 255, 255))
#                 NPCkills_rect = kills_text.get_rect(center=(npc_ship.position.x, npc_ship.position.y - rotated_image.get_height() / 2 - 10))
#                 self.screen.blit(NPCkills_text, NPCkills_rect)
            
#         # Draw the projectiles
#         for projectile in self.game_state.projectiles:
#             pygame.draw.circle(self.screen, (255, 255, 255), (int(projectile.position.x), int(projectile.position.y)), 5)


#         # Update the display
#         pygame.display.flip()

#         return top_player

    

#     def display_winner(self, winner):
#         # Clear the screen
#         self.screen.fill((0, 0, 0))

#         # Render the winner text
#         font = pygame.font.Font("PressStart2P.ttf", 20)
#         text = f"{winner.id} is the winner with {winner.kills} kills!"
#         text_surface = font.render(text, True, (255, 215, 0))
#         text_rect = text_surface.get_rect(center=(1400 / 2, 900 / 2))
#         self.screen.blit(text_surface, text_rect)
#         # Update the display
#         pygame.display.flip()


#     def run(self):
#         clock = pygame.time.Clock()

#         start_time = time.time()

#         while time.time() - start_time < self.game_duration:
#             self.handle_events()
#             self.update()
#             Winner = self.render()
            
#             # # Send state updates to other players via RabbitMQ 
#             # game_state = {
#             #     'ships': {},
#             #     'projectiles': [],
#             #     'game_duration': self.game_duration,
#             # }

#             # for ship_id, ship in self.game_state.ships.items():

#             #     image_bytes = pygame.image.tostring(ship.image, 'RGBA')
#             #     image_base64 = base64.b64encode(image_bytes).decode('utf-8')
#             #     game_state['ships'][ship_id] = {
#             #         'x': ship.position.x,
#             #         'y': ship.position.y,
#             #         'angle': ship.rotation,
#             #         'velocity': ship.velocity,
#             #         'kill_count': ship.kills,
#             #         # 'image_path':  image_base64,
#             #     }

#             # for projectile in self.game_state.projectiles:
#             #     game_state['projectiles'].append({
#             #         'x': projectile.x,
#             #         'y': projectile.y,
#             #         'direction': projectile.direction,
#             #         'velocity': projectile.speed,
#             #     })

#             # message = json.dumps(game_state , cls=Vector2Encoder)
#             # self.commsSender.threadedSend('game_state', message)

#             pygame.display.flip()
#             #60 frames per second
#             clock.tick(60)
#         return Winner