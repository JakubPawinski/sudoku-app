import pygame
from pygame.locals import *
import requests
from pprint import pprint
import json 
import sys

# Pygame init
pygame.init()

# Main variables
screen_size = (500, 600)


# Colours
white = (255, 255, 255)
black = (0, 0, 0)
background_colour = (250, 250, 250)

#fonts
font_grid = pygame.font.SysFont(None, 40)

#global variables
grid_gap = screen_size[0]/9

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

#example grid
test_grid =[
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

def draw_grid(board):
    #This function draws the sudoku board

    screen.fill(background_colour)
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                text1 = font_grid.render(str(board[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * grid_gap + 20, j * grid_gap + 15))

    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, black, (0, i * grid_gap), (500, i * grid_gap), thick)
        pygame.draw.line(screen, black, (i * grid_gap, 0), (i * grid_gap, 500), thick)  





def main_menu():
    print("Main menu")

def game():
    run = True

    board = get_sudoku_grid("Medium")
    pprint(board)

    while run:
        draw_grid(test_grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        
        
        pygame.display.update()


def main():
    # The main project funtion
    main_menu()
    game()

if __name__ == "__main__":
    main()

pygame.quit()