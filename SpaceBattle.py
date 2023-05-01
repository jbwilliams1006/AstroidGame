
# import pygame
# import random
# import math
# import time
# import uuid
# import json
# import pika
# from game2 import Game2
# from localgame import Game
# from comms2 import CommsSender, CommsListener

# pygame.mixer.init()
# background_music = pygame.mixer.Sound("endrit_tone.mp3")
# winner_sound = pygame.mixer.Sound("winneris.ogg")
# def main():
#     # # Initialize Pygame
#     pygame.init()
#     screen_width, screen_height = 1400, 900  # Adjust as needed

#     # Create a Game instance with adjustable game duration
#     game_duration = 30  # seconds
#     game = Game(game_duration,screen_width,screen_height)

#     background_music.play(-1)
#     # Run the game loop
#     Winner = game.run()
#     background_music.stop()

#     winner_sound.play()
#     game.display_winner(Winner)
#     print(f"Winner is {Winner.id} with {Winner.kills} Kills!")
#      # Wait for  seconds
#     pygame.time.wait(8000)

#     # Clean up
#     pygame.quit()

# if __name__ == "__main__":
#     main()   