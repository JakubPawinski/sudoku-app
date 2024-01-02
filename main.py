import pygame
from pygame.locals import *
import requests
from pprint import pprint
import json 

# Pygame init
pygame.init()

# Main variables
screen_size = (750, 750)

# Colours
white = (255, 255, 255)
black = (0, 0, 0)
#global variables

# Screen init
screen = pygame.display.set_mode((screen_size))
pygame.display.set_caption("Sudoku")


def get_sudoku_grid(difficulty):
    # The function gets the sudoku board from api and returns both the sudoku board and its solution
    api_url = 'https://sudoku-api.vercel.app/api/dosuku'
    queries = {
        'newboard': 'newboard',
        'limit': 1,
        'grids': f'{{"value": "value", "solution" : "solution", "difficulty": "{difficulty}"}}',
        'results': 'results',
        'message': 'message'                 
      }
    

    response = requests.get(api_url, params=queries)
    data = response.json()
    # Create dictionary with solution and the value of the sudoku board
    data = {'value': data['newboard']['grids'][0]['value'], 'solution': data['newboard']['grids'][0]['solution']}
    return data



def game():
    pprint(get_sudoku_grid("Medium"))


if __name__ == "__main__":
    game()