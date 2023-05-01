
import pygame
import random
from game2 import Game2
from Messenger import Messenger
import sys


pygame.mixer.init()
background_music = pygame.mixer.Sound("endrit_tone.mp3")
winner_sound = pygame.mixer.Sound("winneris.ogg")

#multiplayer needs: exchange(like a holder of the game), user, password = username + 2023!!!!!, port = 5672, host = terrywgriffin.com
if len(sys.argv) > 1:
    
    try:
        creds = {
        "exchange": sys.argv[1],
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": sys.argv[2],
        "password": sys.argv[2] + "2023!!!",
        }
    except:
        print('\n\nIncorrect arguments for multiplayer!!!')
        print('\n\nShould look like: `python main.py exchange username`')
        sys.exit()
else:
    print('\n\nIncorrect arguments for multiplayer!!!')
    print('\n\nShould look like: `python main.py exchange username`')
    sys.exit()

comm_creds = Messenger(creds)
    
def main():

    screen_width, screen_height = 1400, 900  # Adjust as needed
    # Create a Game instance with adjustable game duration
    game_duration = 45  # seconds
    game = Game2(game_duration,screen_width,screen_height,creds["user"], player = comm_creds)

    background_music.play(-1)
    # Run the game loop
    Winner = game.run()
    background_music.stop()

    winner_sound.play()
    game.display_winner(Winner)
    print(f"Winner is {Winner.id} with {Winner.kills} Kills!")
     # Wait for 8 seconds
    pygame.time.wait(8000)


if __name__ == "__main__":
    main()   