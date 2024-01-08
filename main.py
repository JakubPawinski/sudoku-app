import pygame
from pygame.locals import *
import requests
from pprint import pprint
import json 
import sys
import time
import platform

# Pygame init
pygame.init()

# Main variables
screen_size = (500, 600)

current_platform = 'windows'
paths = {
    'windows':{
        'ui_main_menu': 'img\MainMenuTemplate.png',
        'ui_loading_screen': 'img\LoadingScreen.png',
        'game_ui_white': 'img\GameUIWhite.png',
        'game_ui_dark': 'img\GameUIDark.png'
    },
    'ios':{
        'ui_main_menu': 'Projekt_Sudoku/img/MainMenuTemplate.png',
        'ui_loading_screen': 'Projekt_Sudoku/img/LoadingScreen.png',
        'game_ui_white': 'Projekt_Sudoku/img/GameUIWhite.png',
        'game_ui_dark': 'Projekt_Sudoku/img/GameUIDark.png'
    }
}

# Colours
current_theme = 'white'
colour_themes = {
    'white': {
        'background_colour': (250, 250, 250),
        'highlited_colour': (177, 219, 238),
        'highlited_colour_background': (230, 230, 230),
        'highlited_number_colour': (118, 171, 246),
        'number': (0, 0, 0),
        'ui': paths[current_platform]['game_ui_white']
    },
    'dark': {
        'background_colour': (40, 41, 47),
        'highlited_colour': (86, 166, 206),
        'highlited_colour_background': (53, 55, 63),
        'highlited_number_colour': (86, 166, 206),
        'number': (106, 109, 124),
        'ui': paths[current_platform]['game_ui_dark']
    }
}
#fonts
font_grid = pygame.font.SysFont(None, 40)

#global variables
grid_gap = screen_size[0]/9
cords = [0, 0]
board_type = None
value = 0

# Screen init
screen = pygame.display.set_mode((screen_size))
pygame.display.set_caption("Sudoku")

#test funtion
def debug_mouse_position():
    debug_pos = pygame.mouse.get_pos()
    print(debug_pos)

def check_platform():
    #This function checks the current platform and refreshes dictionaries
    global current_platform
    if platform.system() == 'Darwin':
        current_platform = 'ios'
    if platform.system() == 'Windows':
        current_platform = 'windows'
    #refresh colour_themes dictionary
    colour_themes['white']['ui'] = paths[current_platform]['game_ui_white']
    colour_themes['dark']['ui'] = paths[current_platform]['game_ui_dark']

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
    #This function draws highlited cells

    #Check if it is possible to highlight the cells
    if cords[0] <= 8 and cords[1] <= 8:
        box_cords = get_highlighted_box_cords(cords)
        #highlited box
        pygame.draw.rect(screen, colour_themes[current_theme]['highlited_colour_background'], (box_cords[0] * grid_gap, box_cords[1] * grid_gap, grid_gap * 3, grid_gap * 3))
        #vertical line
        pygame.draw.rect(screen, colour_themes[current_theme]['highlited_colour_background'], (cords[0] * grid_gap, 0, grid_gap, 9 * grid_gap))
        #horizontal line
        pygame.draw.rect(screen, colour_themes[current_theme]['highlited_colour_background'], (0, cords[1] * grid_gap, grid_gap * 9, grid_gap))
        #Highlited cell
        pygame.draw.rect(screen, colour_themes[current_theme]['highlited_colour'], (cords[0] * grid_gap, cords[1] * grid_gap, grid_gap, grid_gap))

def valid(board, value, cords):
    #This function checks if it is possible to place player's number into the board
    if board['value'][int(cords[0])][int(cords[1])] == 0 and board['solution'][int(cords[0])][int(cords[1])] == value:
        return True
    else:
        return False

def if_win(board):
    #This funtion checks if it is the end of the game
    if board['value'] == board['solution']:
        return True

def get_sudoku_grid(difficulty):
    # The function gets the sudoku board from api and returns both the sudoku board and its solution
    print(difficulty)

    get_asked_difficulty = False

    while not get_asked_difficulty:
        api_url = 'https://sudoku-api.vercel.app/api/dosuku'
        response = requests.get(api_url)

        if response.status_code == 200:
            pprint(response)
            data = response.json()
            pprint(data)
            if data['newboard']['grids'][0]['difficulty'] == difficulty:
                get_asked_difficulty = True
                print('===============')
                data = {'value': data['newboard']['grids'][0]['value'], 'solution': data['newboard']['grids'][0]['solution']}
                return data
            time.sleep(0.1)
        else:
            get_asked_difficulty = True
            with open("boards.json", 'r') as json_file:
                json_data = json.load(json_file)
            data = json_data
            data = {'value': data[difficulty]['newboard']['grids'][0]['value'], 'solution': data[difficulty]['newboard']['grids'][0]['solution']}
            pprint(data)
            return data
        
#example grid
test_grid ={
        'value':[[4, 5, 8, 7, 9, 6, 3, 1, 2],
           [7, 6, 9, 1, 2, 3, 5, 8, 4],
           [1, 3, 2, 4, 8, 5, 7, 9, 6],
           [8, 2, 7, 3, 6, 9, 1, 4, 5],
           [3, 9, 1, 5, 4, 2, 8, 6, 7],
           [6, 4, 5, 8, 1, 7, 2, 3, 9],
           [5, 1, 4, 9, 7, 8, 6, 2, 3],
           [9, 7, 6, 2, 3, 1, 4, 5, 8],
           [2, 8, 3, 6, 5, 4, 9, 0, 0]],
        'solution': [[4, 5, 8, 7, 9, 6, 3, 1, 2],
              [7, 6, 9, 1, 2, 3, 5, 8, 4],
              [1, 3, 2, 4, 8, 5, 7, 9, 6],
              [8, 2, 7, 3, 6, 9, 1, 4, 5],
              [3, 9, 1, 5, 4, 2, 8, 6, 7],
              [6, 4, 5, 8, 1, 7, 2, 3, 9],
              [5, 1, 4, 9, 7, 8, 6, 2, 3],
              [9, 7, 6, 2, 3, 1, 4, 5, 8],
              [2, 8, 3, 6, 5, 4, 9, 7, 1]]
}

def draw_grid(board):
    #This function draws the sudoku board

    # print(test_grid[int(cords[0])][int(cords[1])])
    #This loop draws numbers
    for i in range(9):
        for j in range(9):
            #Draw if highlited number != board number
            if board[i][j] != 0 and board[i][j] != board[int(cords[0])][int(cords[1])] and cords[1] <= 8:
                text1 = font_grid.render(str(board[i][j]), 1, colour_themes[current_theme]['number'])
                screen.blit(text1, (i * grid_gap + 20, j * grid_gap + 15))
                
            #Draw if highlited number == board number
            if board[i][j] == board[int(cords[0])][int(cords[1])] and board[i][j] != 0 and cords[1] <= 8:
                text1 = font_grid.render(str(board[i][j]), 1, colour_themes[current_theme]['highlited_number_colour'])
                screen.blit(text1, (i * grid_gap + 20, j * grid_gap + 15))
                if i == cords[0] and cords[1] == j:
                    text1 = font_grid.render(str(board[i][j]), 1, colour_themes[current_theme]['number'])
                    screen.blit(text1, (i * grid_gap + 20, j * grid_gap + 15))
                    # print(i, j, board[i][j], "cords", cords)
    #This loop draws sudoku lines  
    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, colour_themes[current_theme]['number'], (0, i * grid_gap), (500, i * grid_gap), thick)
        pygame.draw.line(screen, colour_themes[current_theme]['number'], (i * grid_gap, 0), (i * grid_gap, 500), thick)  

def main_menu():
    #Main menu funtion
    global board_type
    global current_platform
    print("Main menu")
    menu = pygame.image.load(paths[current_platform]['ui_main_menu'])
    loading = pygame.image.load(paths[current_platform]['ui_loading_screen'])
    run = True
    while run:
        screen.blit(menu,(0, 0))
        # debug_mouse_position()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if pos[0] > 115 and pos[0] < 380 and pos[1] > 145 and pos[1] < 215:
                    board_type = "last"
                    print(board_type)
                    screen.blit(loading,(0, 0))
                    run = False
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 300 and pos[1] < 365:
                    board_type = "Easy"
                    print(board_type)
                    screen.blit(loading,(0, 0))
                    run = False
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 385 and pos[1] < 450:
                    board_type = "Medium"
                    print(board_type)
                    screen.blit(loading,(0, 0))
                    run = False
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 475 and pos[1] < 540:
                    board_type = "Hard"
                    print(board_type)
                    screen.blit(loading,(0, 0))
                    run = False
        pygame.display.update()

def game():
    #game funtion
    print("Game")
    #variables
    global cords
    global board_type
    global current_theme
    global current_platform
    global paths
    health = 3
    
    if board_type == "last":
        print("Last grid")
        board = test_grid
        pprint(board)
    else:
        board = get_sudoku_grid(board_type)
        pprint(board)

    print(colour_themes[current_theme]['ui'])
    print(current_platform)
    run = True
    while run:
        global value

        value = 0
        #This section draws the highlighted cells in the correct order in order to draw highlight behind the sudoku grid
        screen.fill(colour_themes[current_theme]['background_colour'])
        ui = pygame.image.load(colour_themes[current_theme]['ui']) #loads Game UI
        draw_highlighted_cells()
        draw_grid(board['value'])
        screen.blit(ui, (0, 500)) #draw Game UI


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] <= 500:
                    cords = get_cords(pos)
                if pos[0] >= 25 and pos[0] <= 100 and pos[1] >= 515 and pos[1] <= 585:
                    if current_theme == 'dark':
                        current_theme = 'white'
                        continue
                    if current_theme == 'white':
                        current_theme = 'dark'
                        continue
                if pos[0] >= 125 and pos[0] <= 175 and pos[1] >= 525 and pos[1] <=575:
                    print('pencil')
            if event.type == KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    value = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    value = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    value = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    value = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    value = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    value = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    value = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    value = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    value = 9
        
        if value != 0 and board['value'][int(cords[0])][int(cords[1])] == 0:
            print(value)  
            if valid(board, value, cords) == True:
                board['value'][int(cords[0])][int(cords[1])] = value
            else:
                health -= 1
        if health == 0:
            print('Koniec')
            run = False

        if if_win(board) == True:
            print("Wygrana")
            run = False
        # #test funtion
        # debug_mouse_position()
        
        pygame.display.update()


def main():
    # The main project funtion
    check_platform()
    print(current_platform)
    main_menu()
    game()

if __name__ == "__main__":
    main()

pygame.quit()