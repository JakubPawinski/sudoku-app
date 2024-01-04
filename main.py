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

highlited_colour = (177, 219, 238)
highlited_colour_background = (230, 230, 230)
highlited_number_colour = (86, 166, 206)

#fonts
font_grid = pygame.font.SysFont(None, 40)

#global variables
grid_gap = screen_size[0]/9
cords = [0, 0]


# Screen init
screen = pygame.display.set_mode((screen_size))
pygame.display.set_caption("Sudoku")

#test funtion
def debug_mouse_position():
    debug_pos = pygame.mouse.get_pos()
    print(debug_pos)

def get_cords(pos):
    #This function gets cords of highlighted cell
    temp = [0, 0]
    temp[0] = pos[0] // grid_gap
    temp[1] = pos[1] // grid_gap
    print(temp)
    return temp

def get_highlighted_box_cords(cords):
    #This function gets the box cords from highlited cell
    if cords[0] >= 0 and cords[0] <= 2:
        if cords[1] >= 0 and cords[1] <= 2:
            return [0, 0]
        elif cords[1] >= 3 and cords[1] <= 5:
            return [0, 3]
        elif cords[1] >= 6 and cords[1] <= 8:
            return [0, 6]
    elif cords[0] >= 3 and cords[0] <= 5:
        if cords[1] >= 0 and cords[1] <= 2:
            return [3, 0]
        elif cords[1] >= 3 and cords[1] <= 5:
            return [3, 3]
        elif cords[1] >= 6 and cords[1] <= 8:
            return[3, 6]
    elif cords[0] >= 6 and cords[0] <= 8:
        if cords[1] >= 0 and cords[1] <= 2:
            return [6, 0]
        elif cords[1] >= 3 and cords[1] <= 5:
            return[6, 3]
        elif cords[1] >= 6 and cords[1] <= 8:
            return[6, 6]
    else:
        return cords

def draw_highlighted_cells():
    #This function draw highlited cells

    #Check if it is possible to highlight the cells
    if cords[0] <= 8 and cords[1] <= 8:
        box_cords = get_highlighted_box_cords(cords)
        #highlited box
        pygame.draw.rect(screen, highlited_colour_background, (box_cords[0] * grid_gap, box_cords[1] * grid_gap, grid_gap * 3, grid_gap * 3))
        #vertical line
        pygame.draw.rect(screen, highlited_colour_background, (cords[0] * grid_gap, 0, grid_gap, 9 * grid_gap))
        #horizontal line
        pygame.draw.rect(screen, highlited_colour_background, (0, cords[1] * grid_gap, grid_gap * 9, grid_gap))
        #Highlited cell
        pygame.draw.rect(screen, highlited_colour, (cords[0] * grid_gap, cords[1] * grid_gap, grid_gap, grid_gap))




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

    # print(test_grid[int(cords[0])][int(cords[1])])
    #This loop draws numbers
    for i in range(9):
        for j in range(9):
            #Draw if highlited number != board number
            if board[i][j] != 0 and board[i][j] != board[int(cords[0])][int(cords[1])]:
                text1 = font_grid.render(str(board[i][j]), 1, black)
                screen.blit(text1, (i * grid_gap + 20, j * grid_gap + 15))
            #Draw if highlited number == board number
            if board[i][j] == board[int(cords[0])][int(cords[1])] and board[i][j] != 0:
                text1 = font_grid.render(str(board[i][j]), 1, highlited_number_colour)
                screen.blit(text1, (i * grid_gap + 20, j * grid_gap + 15))
                if i == cords[0] and cords[1] == j:
                    text1 = font_grid.render(str(board[i][j]), 1, black)
                    screen.blit(text1, (i * grid_gap + 20, j * grid_gap + 15))
    #This loop draws sudoku lines  
    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, black, (0, i * grid_gap), (500, i * grid_gap), thick)
        pygame.draw.line(screen, black, (i * grid_gap, 0), (i * grid_gap, 500), thick)  

def main_menu():
    print("Main menu")
    menu = pygame.image.load(r".\img\MainMenuTemplate.png")
    run = True
    while run:
        screen.blit(menu,(0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

        pygame.display.update()

def game():
    print("Game")
    global cords

    run = True

    board = get_sudoku_grid("Medium")
    pprint(board)

    while run:
        #This section draws the highlighted cells in the correct order in order to draw highlight behind the sudoku grid
        screen.fill(background_colour)
        draw_highlighted_cells()
        draw_grid(test_grid)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cords = get_cords(pos)


        #test funtion
        # debug_mouse_position()
        
        pygame.display.update()


def main():
    # The main project funtion
    main_menu()
    game()

if __name__ == "__main__":
    main()

pygame.quit()