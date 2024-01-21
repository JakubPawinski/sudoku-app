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
from static import *
from drawing_funtions import *
# Pygame init
pygame.init()


# Main variables
current_theme = 'white'



# Colours







#global variables



# Screen init
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
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
    colour_themes['white']['ui'] = PATHS[current_platform]['game_ui_white']
    colour_themes['dark']['ui'] = PATHS[current_platform]['game_ui_dark']

def get_cords(pos):
    #This function gets cords of highlighted cell
    temp = [0, 0]
    temp[0] = pos[0] // GRID_GAP
    temp[1] = pos[1] // GRID_GAP
    print(temp)
    return temp





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
        with open(PATHS[current_platform]['boards'], 'r') as json_file:
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
            with open(PATHS[current_platform]['boards'], 'r') as json_file:
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

def save_game(board, time, health):
    print("Saved")
    with open(PATHS[current_platform]['boards'], 'r') as json_file:
        json_data = json.load(json_file)
    
    json_data["last"] = board
    json_data["last"].update({"time": time})
    json_data["last"].update({"health": health})

    with open(PATHS[current_platform]['boards'], 'w') as json_file:
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
    CsvFile = pd.read_csv(PATHS[current_platform]['resultsDataBase'])
    new_row = {'Date': date.today(), 'DifficultyLevel': board['difficulty'], 'LivesRemaining': health, 'Time': time, 'Score': count_score(board['difficulty'], time, health)}
    CsvFile.loc[len(CsvFile)] = new_row
    CsvFile.to_csv(PATHS[current_platform]['resultsDataBase'], index=False)
    print("Score saved", new_row)

def add_notes(value, cords):
    global notes
    if not value in notes[int(cords[0])][int(cords[1])]:
        notes[int(cords[0])][int(cords[1])].append(value)
        notes[int(cords[0])][int(cords[1])].sort()

def main_menu():
    #Main menu funtion
    global board_type
    global current_platform
    global last_game_possible
    print("Main menu")
    if last_game_possible == True:
        menu = pygame.image.load(PATHS[current_platform]['ui_main_menu'])
    elif last_game_possible == False:
        print("lastGamedisabled")
        menu = pygame.image.load(PATHS[current_platform]['ui_main_menu_disabledLastGame'])
        # menu = pygame.image.load(paths[current_platform]['ui_main_menu'])

    loading = pygame.image.load(PATHS[current_platform]['ui_loading_screen'])
    run = True
    while run:
        SCREEN.blit(menu,(0, 0))
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
                    SCREEN.blit(loading,(0, 0))
                    run = False
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 300 and pos[1] < 365:
                    board_type = "Easy"
                    print(board_type)
                    SCREEN.blit(loading,(0, 0))
                    run = False
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 385 and pos[1] < 450:
                    board_type = "Medium"
                    print(board_type)
                    SCREEN.blit(loading,(0, 0))
                    run = False
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 475 and pos[1] < 540:
                    board_type = "Hard"
                    print(board_type)
                    SCREEN.blit(loading,(0, 0))
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
    global PATHS
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
        SCREEN.fill(colour_themes[current_theme]['background_colour'])
        ui = pygame.image.load(colour_themes[current_theme]['ui']) #loads Game UI
        
        
        draw_highlighted_cells(SCREEN, cords, current_theme)

        draw_grid(SCREEN, board['value'], current_theme)
        draw_notes(SCREEN, current_theme, board['value'], notes, cords)

        

        SCREEN.blit(ui, (0, 500)) #draw Game UI
        draw_health(SCREEN, health)
        draw_pencil_button(SCREEN, is_pencil_clicked)


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
            current_time = draw_time(SCREEN, current_theme, start_ticks, board['time'])  #Saved the current time and display it
        else:
            current_time = draw_time(SCREEN, current_theme, start_ticks) 
        pygame.display.update()

def end():
    global end_message
    global play_again
    print("End screen")
    end_screen = pygame.image.load(PATHS[current_platform]['end_screen'])

    end_text = FONT_END_MESSAGE.render(end_message.upper(), 1, END_MESSAGE_COLORS[end_message])


    run = True
    while run:
        SCREEN.blit(end_screen,(0, 0))
        SCREEN.blit(end_text, check_score(end_message))
        if end_message == 'victory':
            draw_last_game_score(SCREEN)

        draw_best_scores(SCREEN)

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
