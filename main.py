import pygame
from pygame.locals import *
import requests
from pprint import pprint
import json 
import sys
import time
import platform
import math
import pandas as pd
from datetime import date
# Pygame init
pygame.init()


# Main variables
screen_size = (500, 600)

play_again = False
last_game_score = 0
last_game_possible = True

end_message = ''
current_platform = 'windows'
paths = {
    'windows':{
        'ui_main_menu': 'img\MainMenuTemplate.png',
        'ui_main_menu_disabledLastGame': 'img\MainMenuTemplateLastGameDisabled.png',
        'ui_loading_screen': 'img\LoadingScreen.png',
        'game_ui_white': 'img\GameUIWhite.png',
        'game_ui_dark': 'img\GameUIDark.png',
        'end_screen': 'img\EndScreen.png',
        'boards': 'boards.json',
        'health': {3: 'img\heart_100.png', 2: 'img\heart_66.png', 1: 'img\heart_33.png'},
        'pencil': {True: 'img\pencil_clicked.png', False: 'img\pencil_unclicked.png'},
        'resultsDataBase' : 'results.csv'
    },
    'ios':{
        'ui_main_menu': 'Projekt_Sudoku/img/MainMenuTemplate.png',
        'ui_main_menu_disabledLastGame': '',
        'ui_loading_screen': 'Projekt_Sudoku/img/LoadingScreen.png',
        'game_ui_white': 'Projekt_Sudoku/img/GameUIWhite.png',
        'game_ui_dark': 'Projekt_Sudoku/img/GameUIDark.png',
        'end_screen': 'Projekt_Sudoku/img/EndScreen.png',
        'boards': 'Projekt_Sudoku/boards.json',
        'health': {3: 'Projekt_Sudoku/img/heart_100.png', 2: 'Projekt_Sudoku/img/heart_66.png', 1: 'Projekt_Sudoku/img/heart_33.png'},
        'pencil': {True: 'Projekt_Sudoku/img/pencil_clicked.png', False: 'Projekt_Sudoku/img/pencil_unclicked.png'},
        'resultsDataBase' : 'xxxxxxxxxxxxxxxxxxxx'
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
end_message_colours = {
    'victory': (60, 201, 67),
    'defeat': (175, 19, 19)
}
difficulty_colors = {
    'Easy': (41, 226, 111),
    'Medium': (226, 167, 41),
    'Hard': (212, 83, 29)
}

black = (0, 0, 0)

#global variables
grid_gap = screen_size[0]/9
cords = [0, 0]
board_type = None
value = 0

notes = [
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]]
]

#fonts
font_grid = pygame.font.SysFont(None, 40)
font_end_message = pygame.font.SysFont(None, 60)
font_timer = pygame.font.SysFont(None, 80)
font_notes = pygame.font.SysFont(None, 16)
font_last_game_score = pygame.font.SysFont(None, 40)
font_best_scores = pygame.font.SysFont(None, 26)

# Screen init
screen = pygame.display.set_mode((screen_size))
pygame.display.set_caption("Sudoku")

#test funtion
def debug_mouse_position():
    debug_pos = pygame.mouse.get_pos()
    print(debug_pos)

def check_score(end_message):
    if end_message == 'victory':
        return (160, 100)
    if end_message == 'defeat':
        return (168, 100)

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

def get_sudoku_grid(searched_board):
    # The function gets the sudoku board from api and returns both the sudoku board and its solution
    if searched_board == "last":
        with open(paths[current_platform]['boards'], 'r') as json_file:
            json_data = json.load(json_file)
        data = json_data
        return data['last']
    
    get_asked_difficulty = False

    while not get_asked_difficulty:
        api_url = 'https://sudoku-api.vercel.app/api/dosuku'
        response = requests.get(api_url)

        if response.status_code == 200:
            pprint(response)
            data = response.json()
            pprint(data)
            if data['newboard']['grids'][0]['difficulty'] == searched_board:
                get_asked_difficulty = True
                print('===============')
                data = {'value': data['newboard']['grids'][0]['value'], 'solution': data['newboard']['grids'][0]['solution'], 'difficulty': data['newboard']['grids'][0]['difficulty']}
                return data
            time.sleep(0.1)
        else:
            get_asked_difficulty = True
            with open(paths[current_platform]['boards'], 'r') as json_file:
                json_data = json.load(json_file)
            data = json_data
            data = {'value': data[searched_board]['newboard']['grids'][0]['value'], 'solution': data[searched_board]['newboard']['grids'][0]['solution'], 'difficulty': data[searched_board]['newboard']['grids'][0]['difficulty']}
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
              [2, 8, 3, 6, 5, 4, 9, 7, 1]],
        'health': 3,
        'difficulty': 'Medium'

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

def save_game(board, time, health):
    print("Saved")
    with open(paths[current_platform]['boards'], 'r') as json_file:
        json_data = json.load(json_file)
    
    json_data["last"] = board
    json_data["last"].update({"time": time})
    json_data["last"].update({"health": health})

    with open(paths[current_platform]['boards'], 'w') as json_file:
        json.dump(json_data, json_file)

def count_score(difficulty, time, health):
    global last_game_score
    if difficulty == "Easy":
        difficulty_level = 1
    elif difficulty == "Medium":
        difficulty_level = 2
    elif difficulty == "Hard":
        difficulty_level = 3
    score = int(-1 * (0.3 * difficulty_level / health * time) + 1000)
    last_game_score = score
    if score >= 0:
        return score
    else:
        return 0

def save_score(board, time, health):
    CsvFile = pd.read_csv(paths[current_platform]['resultsDataBase'])
    new_row = {'Date': date.today(), 'DifficultyLevel': board['difficulty'], 'LivesRemaining': health, 'Time': time, 'Score': count_score(board['difficulty'], time, health)}
    CsvFile.loc[len(CsvFile)] = new_row
    CsvFile.to_csv(paths[current_platform]['resultsDataBase'], index=False)
    print("Score saved", new_row)

def get_score_by_difficulty(difficulty):

    CsvFile = pd.read_csv(paths[current_platform]['resultsDataBase']).sort_values(by=['DifficultyLevel', 'Score'], ascending=[False, False])
    if difficulty == "Easy":
        easy_row = CsvFile.loc[CsvFile['DifficultyLevel'] == 'Easy'].iloc[0]
        return easy_row['Score']
    if difficulty == "Medium":
        medium_row = CsvFile.loc[CsvFile['DifficultyLevel'] == 'Medium'].iloc[0]
        return medium_row['Score']
    if difficulty == "Hard":
        hard_row = CsvFile.loc[CsvFile['DifficultyLevel'] == 'Hard'].iloc[0]
        return hard_row['Score']

def draw_time(start_ticks, recent_time=0):
    time = (pygame.time.get_ticks() - start_ticks) / 1000
    time = math.floor(time)
    time += recent_time
    seconds = time % 60 
    minutes = time // 60
    if seconds <= 9:
        seconds = '0' + str(seconds)
    if minutes <= 9:
        minutes = '0' + str(minutes)

    text = font_timer.render((str(minutes) + ' : ' + str(seconds)), 1, colour_themes[current_theme]['number'])
    screen.blit(text, (310, 522))
    return (time)

def draw_health(health):

    img = pygame.image.load(paths[current_platform]['health'][health])
    screen.blit(img,(220, 520))

def draw_pencil_button(is_clicked):
    clicked = pygame.image.load(paths[current_platform]['pencil'][is_clicked])
    unclicked = pygame.image.load(paths[current_platform]['pencil'][is_clicked])
    if is_clicked == True:
        screen.blit(clicked, (125, 525))
    if is_clicked == False:
        screen.blit(unclicked, (125, 525))

def add_notes(value, cords):
    global notes
    if not value in notes[int(cords[0])][int(cords[1])]:
        notes[int(cords[0])][int(cords[1])].append(value)
        notes[int(cords[0])][int(cords[1])].sort()

def draw_notes(board):
    global notes
    global cords

       #This loop draws numbers
    for i in range(9):
        for j in range(9):
            #Draw if highlited number != board number
            if notes[i][j] == [0]:
                continue
            else:
                horizontal_gap = 0
                vertical_gap = 0
                for number in notes[i][j]:
                    
                    if number != 0:
                        if board[int(cords[0])][int(cords[1])] == number:
                            text1 = font_notes.render(str(number), 1, colour_themes[current_theme]['highlited_number_colour'])
                        else:
                            text1 = font_notes.render(str(number), 1, colour_themes[current_theme]['number'])
                        screen.blit(text1, ( (i * grid_gap) + ( horizontal_gap * (grid_gap)/3) + 5, (j* grid_gap) + ( vertical_gap * (grid_gap)/3 ) + 4))
                        horizontal_gap += 1



                        if horizontal_gap == 3:
                            horizontal_gap = 0
                            vertical_gap += 1
                    

                # #Draw if highlited number == board number
                # if notes[i][j] == notes[int(cords[0])][int(cords[1])] and notes[i][j] != 0 and cords[1] <= 8:
                #     text1 = font_grid.render(str(notes[i][j]), 1, colour_themes[current_theme]['highlited_number_colour'])
                #     screen.blit(text1, (i * grid_gap + 20, j * grid_gap + 15))
                #     if i == cords[0] and cords[1] == j:
                #         text1 = font_grid.render(str(notes[i][j]), 1, colour_themes[current_theme]['number'])
                #         screen.blit(text1, (i * grid_gap + 20, j * grid_gap + 15))
                #         # print(i, j, board[i][j], "cords", cords) 

def draw_last_game_score():

    score_text = font_last_game_score.render(str(last_game_score) + ' points', 1, end_message_colours[end_message])
    screen.blit(score_text, (180, 150))

def draw_best_scores():
    translation = 0
    for difficulty in ['Easy', 'Medium', 'Hard']:
        best_score_text = font_best_scores.render(str(get_score_by_difficulty(str(difficulty))), 1, difficulty_colors[difficulty])
        screen.blit(best_score_text, (230, 292 + 65 * translation))
        translation += 1

def main_menu():
    #Main menu funtion
    global board_type
    global current_platform
    global last_game_possible
    print("Main menu")
    if last_game_possible == True:
        menu = pygame.image.load(paths[current_platform]['ui_main_menu'])
    elif last_game_possible == False:
        print("lastGamedisabled")
        menu = pygame.image.load(paths[current_platform]['ui_main_menu_disabledLastGame'])
        # menu = pygame.image.load(paths[current_platform]['ui_main_menu'])

    loading = pygame.image.load(paths[current_platform]['ui_loading_screen'])
    run = True
    while run:
        screen.blit(menu,(0, 0))
        # debug_mouse_position()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if pos[0] > 115 and pos[0] < 380 and pos[1] > 145 and pos[1] < 215 and last_game_possible == True:
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
    global end_message
    global notes
    global last_game_possible
    

    clock = pygame.time.Clock()
    is_pencil_clicked = False


    notes = [
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]],
    [[0], [0], [0], [0], [0], [0], [0], [0], [0]]
]
    # if board_type == "last":
    #     board = test_grid
    # else:
    board = get_sudoku_grid(board_type)
    pprint(board)
    
    if board_type == "last":
        health = board['health']
    else:
        health = 3

    start_ticks = pygame.time.get_ticks()
    run = True
    while run:
        global value
        value = 0
        #This section draws the highlighted cells in the correct order in order to draw highlight behind the sudoku grid
        screen.fill(colour_themes[current_theme]['background_colour'])
        ui = pygame.image.load(colour_themes[current_theme]['ui']) #loads Game UI
        draw_highlighted_cells()
        draw_grid(board['value'])
        draw_notes(board['value'])

        

        screen.blit(ui, (0, 500)) #draw Game UI
        draw_health(health)
        draw_pencil_button(is_pencil_clicked)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                save_game(board, current_time, health)
                pygame.quit()
                sys.exit()
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
                    if is_pencil_clicked == True:
                        is_pencil_clicked = False
                    elif is_pencil_clicked == False:
                        is_pencil_clicked = True
                    
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
        
        if (value != 0 and board['value'][int(cords[0])][int(cords[1])] == 0):
            if is_pencil_clicked == False:
                print(value)  
                if valid(board, value, cords) == True:
                    board['value'][int(cords[0])][int(cords[1])] = value
                    notes[int(cords[0])][int(cords[1])] = [0] #Reset
                else:
                    health -= 1
            if is_pencil_clicked == True:
                add_notes(value, cords)

        if health == 0:
            print('Koniec')
            last_game_possible = False
            end_message = "defeat"
            run = False

        if if_win(board) == True:
            print("Wygrana")
            last_game_possible = False
            end_message = "victory"
            save_score(board, current_time, health)
            run = False
        # #test funtion
        # debug_mouse_position()
            
        #Time counter
        clock.tick(60)
        if 'time' in board:
            current_time = draw_time(start_ticks, board['time'])  #Saved the current time and display it
        else:
            current_time = draw_time(start_ticks) 
        pygame.display.update()

def end():
    global end_message
    global play_again
    print("End screen")
    end_screen = pygame.image.load(paths[current_platform]['end_screen'])

    end_text = font_end_message.render(end_message.upper(), 1, end_message_colours[end_message])


    run = True
    while run:
        screen.blit(end_screen,(0, 0))
        screen.blit(end_text, check_score(end_message))
        if end_message == 'victory':
            draw_last_game_score()

        draw_best_scores()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] > 115 and pos[0] < 385 and pos[1] > 455 and pos[1] < 525:
                    print("Play again")
                    run = False
                    play_again = True
                    main()
        pygame.display.update()

def main():
    global play_again
    # The main project funtion
    check_platform()
    print(current_platform)

    run = True
    while run:
        play_again = False
        main_menu()
        game()
        end()
        if play_again == True:
            continue
        if play_again == False:
            break

if __name__ == "__main__":
    main()

