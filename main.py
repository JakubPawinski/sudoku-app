import pygame, requests, json, sys, time, platform, math
from pygame.locals import *
from pprint import pprint
import pandas as pd
from datetime import date

# Pygame init
pygame.init()

#Test grid
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

# ============== Global variables ==============
play_again = False
last_game_score = 0
last_game_possible = True
end_message = ''
current_platform = 'ios'
cords = [0, 0]
board_type = None
value = 0

# ============== Staic variables ==============
SCREEN_SIZE = (500, 600)
GRID_GAP = SCREEN_SIZE[0]/9

#This dictionary contains paths to the images in the project, depending on the current operating system
PATHS = {
    'windows':{
        'ui_main_menu': 'img\\MainMenuTemplate.png',
        'ui_main_menu_disabledLastGame': 'img\\MainMenuTemplateLastGameDisabled.png',
        'ui_loading_screen': 'img\\LoadingScreen.png',
        'game_ui_white': 'img\\GameUIWhite.png',
        'game_ui_dark': 'img\\GameUIDark.png',
        'end_screen': 'img\\EndScreen.png',
        'boards': 'boards.json',
        'health': {3: 'img\\heart_100.png', 2: 'img\\heart_66.png', 1: 'img\\heart_33.png'},
        'pencil': {True: 'img\\pencil_clicked.png', False: 'img\\pencil_unclicked.png'},
        'resultsDataBase' : 'results.csv'
    },
    'ios':{
        'ui_main_menu': 'Projekt_Sudoku/img/MainMenuTemplate.png',
        'ui_main_menu_disabledLastGame': 'Projekt_Sudoku/img/MainMenuTemplateLastGameDisabled.png',
        'ui_loading_screen': 'Projekt_Sudoku/img/LoadingScreen.png',
        'game_ui_white': 'Projekt_Sudoku/img/GameUIWhite.png',
        'game_ui_dark': 'Projekt_Sudoku/img/GameUIDark.png',
        'end_screen': 'Projekt_Sudoku/img/EndScreen.png',
        'boards': 'Projekt_Sudoku/boards.json',
        'health': {3: 'Projekt_Sudoku/img/heart_100.png', 2: 'Projekt_Sudoku/img/heart_66.png', 1: 'Projekt_Sudoku/img/heart_33.png'},
        'pencil': {True: 'Projekt_Sudoku/img/pencil_clicked.png', False: 'Projekt_Sudoku/img/pencil_unclicked.png'},
        'resultsDataBase' : 'Projekt_Sudoku/results.csv'
    }
}


# ======= Fonts =======
FONT_GRID = pygame.font.SysFont(None, 40)
FONT_END_MESSAGE = pygame.font.SysFont(None, 60)
FONT_TIMER = pygame.font.SysFont(None, 80)
FONT_NOTES = pygame.font.SysFont(None, 16)
FONT_LAST_GAME_SCORE = pygame.font.SysFont(None, 40)
FONT_BEST_SCORES = pygame.font.SysFont(None, 26)

# ======= Colors =======
COLOR_BLACK = (0, 0, 0)

COLORS_END_MESSAGE = {
    'victory': (60, 201, 67),
    'defeat': (175, 19, 19)
}

COLORS_DIFFICULTY = {
    'Easy': (41, 226, 111),
    'Medium': (226, 167, 41),
    'Hard': (212, 83, 29)
}

# ======= Themes =======
current_theme = 'white' #This variable contains the current theme, at the beginning it is set to white
colour_themes = { 
    'white': {
        'background_colour': (250, 250, 250),
        'highlited_colour': (177, 219, 238),
        'highlited_colour_background': (230, 230, 230),
        'highlited_number_colour': (118, 171, 246),
        'number': (0, 0, 0),
        'ui': PATHS[current_platform]['game_ui_white']
    },
    'dark': {
        'background_colour': (40, 41, 47),
        'highlited_colour': (86, 166, 206),
        'highlited_colour_background': (53, 55, 63),
        'highlited_number_colour': (86, 166, 206),
        'number': (106, 109, 124),
        'ui': PATHS[current_platform]['game_ui_dark']
    }
}


# ============== Pygame screen init ==============
screen = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("Sudoku")

# ======= Test functions =======
def debug_mouse_position():
    debug_pos = pygame.mouse.get_pos()
    print(debug_pos)


# ======= Init functions =======
def set_current_platform():
    #This function sets current platform
    global current_platform

    if platform.system() == 'Darwin':
        current_platform = 'ios'
    if platform.system() == 'Windows':
        current_platform = 'windows'
    #Refresh colour_themes dictionary
    colour_themes['white']['ui'] = PATHS[current_platform]['game_ui_white']
    colour_themes['dark']['ui'] = PATHS[current_platform]['game_ui_dark']

# ============== Game functions ==============

def save_score(board, time, health):
    #Function saves the result of the game (Date, difficulty level, lives remaining, time, score) to a csv file

    #Read csv file
    CsvFile = pd.read_csv(PATHS[current_platform]['resultsDataBase'])

    #Sets the new row
    new_row = {'Date': date.today(), 'DifficultyLevel': board['difficulty'], 'LivesRemaining': health, 'Time': time, 'Score': count_score(board['difficulty'], time, health)}

    #Add the new row to data
    CsvFile.loc[len(CsvFile)] = new_row

    #Save data to the file
    CsvFile.to_csv(PATHS[current_platform]['resultsDataBase'], index=False)

def get_sudoku_grid(searched_board):
    # The function gets the sudoku board from api or from file
    
    #If the player chooses the last game
    if searched_board == "last":

        #Read the board from file
        with open(PATHS[current_platform]['boards'], 'r') as json_file:
            json_data = json.load(json_file)
        data = json_data
        return data['last']
    
    get_asked_difficulty = False

    while not get_asked_difficulty:

        api_url = 'https://sudoku-api.vercel.app/api/dosuku'
        response = requests.get(api_url) #Response from api

        if response.status_code == 200:
            #If api works
            data = response.json()

            if data['newboard']['grids'][0]['difficulty'] == searched_board:
                get_asked_difficulty = True
                data = {'value': data['newboard']['grids'][0]['value'], 'solution': data['newboard']['grids'][0]['solution'], 'difficulty': data['newboard']['grids'][0]['difficulty']}
                return data #Returns value, solution, difficulty
            time.sleep(0.1)

        else:
            #Read the board from file if api doesn't work
            
            get_asked_difficulty = True

            with open(PATHS[current_platform]['boards'], 'r') as json_file:
                json_data = json.load(json_file)
            data = json_data
            data = {'value': data[searched_board]['newboard']['grids'][0]['value'], 'solution': data[searched_board]['newboard']['grids'][0]['solution'], 'difficulty': data[searched_board]['newboard']['grids'][0]['difficulty']}
            
            return data #Returns value, solution, difficulty

def save_game(board, time, health):
    #This function saves the board, time and health in a file

    #Read the file
    with open(PATHS[current_platform]['boards'], 'r') as json_file:
        json_data = json.load(json_file)
    
    json_data["last"] = board
    json_data["last"].update({"time": time})
    json_data["last"].update({"health": health})

    #Save file
    with open(PATHS[current_platform]['boards'], 'w') as json_file:
        json.dump(json_data, json_file)
    print("Saved")    

def valid(board, value, cords):
    #This function checks if it is possible to place player's number into the board
    if board['value'][int(cords[0])][int(cords[1])] == 0 and board['solution'][int(cords[0])][int(cords[1])] == value:
        return True
    else:
        return False

def change_notes(value, cords):
    #This function insert the player's notes into the note variable or remeves them from the notes
    
    #import global variable
    global notes

    #Add number to notes
    if not value in notes[int(cords[0])][int(cords[1])]:
        notes[int(cords[0])][int(cords[1])].append(value)
        notes[int(cords[0])][int(cords[1])].sort()
    #Remove number from notes
    else:
        notes[int(cords[0])][int(cords[1])].remove(value)

def get_highlighted_box_cords(cords):
    #This function returns the top-left cordinates of the 3x3 box, selected by the player
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
    #If selected cords are out of the board returns the original cords
    else:
        return cords

def get_cords(pos):
    #This function returns the cordinates of the tile, selected by the player
    cords = [0, 0]
    cords[0] = pos[0] // GRID_GAP #Row index
    cords[1] = pos[1] // GRID_GAP #Column index
    
    #Returns calculated cordinates
    return cords

def if_win(board):
    #This funtion checks if it is the end of the game
    if board['value'] == board['solution']:
        return True

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

# ======= Draw functions =======
        
def draw_highlighted_cells():
    #This function draws hilighted cells

    #Check if it is possible to highlight the cells
    if cords[0] <= 8 and cords[1] <= 8:
        box_cords = get_highlighted_box_cords(cords)
        #hilighted box
        pygame.draw.rect(screen, colour_themes[current_theme]['highlited_colour_background'], (box_cords[0] * GRID_GAP, box_cords[1] * GRID_GAP, GRID_GAP * 3, GRID_GAP * 3))
        #vertical line
        pygame.draw.rect(screen, colour_themes[current_theme]['highlited_colour_background'], (cords[0] * GRID_GAP, 0, GRID_GAP, 9 * GRID_GAP))
        #horizontal line
        pygame.draw.rect(screen, colour_themes[current_theme]['highlited_colour_background'], (0, cords[1] * GRID_GAP, GRID_GAP * 9, GRID_GAP))
        #hilighted cell
        pygame.draw.rect(screen, colour_themes[current_theme]['highlited_colour'], (cords[0] * GRID_GAP, cords[1] * GRID_GAP, GRID_GAP, GRID_GAP))

def draw_grid(board):
    #This function draws the sudoku board

    #Draw numbers
    for i in range(9):
        for j in range(9):

            #Draw normal numbers
            if board[i][j] != 0 and board[i][j] != board[int(cords[0])][int(cords[1])] and cords[1] <= 8:
                text1 = FONT_GRID.render(str(board[i][j]), 1, colour_themes[current_theme]['number'])
                screen.blit(text1, (i * GRID_GAP + 20, j * GRID_GAP + 15))
                
            #Hilight the same numbers as the selected number
            if board[i][j] == board[int(cords[0])][int(cords[1])] and board[i][j] != 0 and cords[1] <= 8:
                text1 = FONT_GRID.render(str(board[i][j]), 1, colour_themes[current_theme]['highlited_number_colour'])
                screen.blit(text1, (i * GRID_GAP + 20, j * GRID_GAP + 15))

                ##Draw the selected number normally on the highlighted background
                if i == cords[0] and cords[1] == j:
                    text1 = FONT_GRID.render(str(board[i][j]), 1, colour_themes[current_theme]['number'])
                    screen.blit(text1, (i * GRID_GAP + 20, j * GRID_GAP + 15))
    
    #Draw board lines 
    for i in range(10):
        if i % 3 == 0 : #Every third line thicker
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, colour_themes[current_theme]['number'], (0, i * GRID_GAP), (500, i * GRID_GAP), thick)
        pygame.draw.line(screen, colour_themes[current_theme]['number'], (i * GRID_GAP, 0), (i * GRID_GAP, 500), thick)  

def draw_notes(board):
    #This function draws the player's notes

    for i in range(9):
        for j in range(9):
            if notes[i][j] == [0]:
                continue
            else:
                #Reset gaps
                horizontal_gap = 0
                vertical_gap = 0

                #Draw number in one tile
                for number in notes[i][j]:                    
                    if number != 0:
                        if board[int(cords[0])][int(cords[1])] == number:
                            text1 = FONT_NOTES.render(str(number), 1, colour_themes[current_theme]['highlited_number_colour'])
                        else:
                            text1 = FONT_NOTES.render(str(number), 1, colour_themes[current_theme]['number'])
                        screen.blit(text1, ( (i * GRID_GAP) + ( horizontal_gap * GRID_GAP/3) + 5, (j* GRID_GAP) + ( vertical_gap * GRID_GAP/3 ) + 4))
                        horizontal_gap += 1

                        if horizontal_gap == 3:
                            horizontal_gap = 0
                            vertical_gap += 1

def draw_health(health):
    #This function draws the player's health
    img = pygame.image.load(PATHS[current_platform]['health'][health]) #Change the image depends on player's health
    screen.blit(img,(220, 520)) #Display health

def draw_pencil_button(is_clicked):
    #This function draws the pencil button

    #Import button images
    clicked = pygame.image.load(PATHS[current_platform]['pencil'][is_clicked])
    unclicked = pygame.image.load(PATHS[current_platform]['pencil'][is_clicked])

    #Change the image if the pencil is activate
    if is_clicked == True:
        screen.blit(clicked, (125, 525))
    if is_clicked == False:
        screen.blit(unclicked, (125, 525))

def draw_time(start_ticks, recent_time=0):
    #Function calculates and display the time since the game started
    
    #Calculate time in seconds
    time = (pygame.time.get_ticks() - start_ticks) / 1000
    time = math.floor(time) #Round down the time
    
    #Add last game time if the game continues
    time += recent_time

    #Calculate minutes and seconds from the total time
    seconds = time % 60 
    minutes = time // 60

    #Format the seconds and minutes to have leading zeros if less than 10
    if seconds <= 9:
        seconds = '0' + str(seconds)
    if minutes <= 9:
        minutes = '0' + str(minutes)

    #Render time text
    text = FONT_TIMER.render((str(minutes) + ' : ' + str(seconds)), 1, colour_themes[current_theme]['number'])
    
    #Display current time on the screen
    screen.blit(text, (310, 522))
    
    #Return total time
    return (time)

#============== End screen functions ==============

def set_end_message_cords(end_message):
    #Function sets the cordinates for rendering the end message score based on game result
    if end_message == 'victory':
        return (160, 100)
    if end_message == 'defeat':
        return (168, 100)

def get_score_by_difficulty(difficulty):
    #Function reads the results from the CSV database and returns the best score of the given difficulty

    #Read the csv file and sort it by Difficulty level and score in the descending order
    CsvFile = pd.read_csv(PATHS[current_platform]['resultsDataBase']).sort_values(by=['DifficultyLevel', 'Score'], ascending=[False, False])
    
    #Check if there are any results for the specified difficulty
    if CsvFile[CsvFile['DifficultyLevel'] == difficulty].empty:
        return '000' #If there are no results, return 000
    

    #Returns the best score specified by the difficulty level
    if difficulty == "Easy":
        easy_row = CsvFile.loc[CsvFile['DifficultyLevel'] == 'Easy'].iloc[0]
        return easy_row['Score']
    if difficulty == "Medium":
        medium_row = CsvFile.loc[CsvFile['DifficultyLevel'] == 'Medium'].iloc[0]
        return medium_row['Score']
    if difficulty == "Hard":
        hard_row = CsvFile.loc[CsvFile['DifficultyLevel'] == 'Hard'].iloc[0]
        return hard_row['Score']

# ======= Draw functions =======

def draw_last_game_score():
    #Function renders and displays the score from the last game

    score_text = FONT_LAST_GAME_SCORE.render(str(last_game_score) + ' points', 1, COLORS_END_MESSAGE[end_message])
    screen.blit(score_text, (180, 150))

def draw_best_scores():
    #Function draws the best scores for each difficulty level
    
    #Translation variable to control the vertical position of the text
    translation = 0

    for difficulty in ['Easy', 'Medium', 'Hard']:
        best_score_text = FONT_BEST_SCORES.render(str(get_score_by_difficulty(str(difficulty))), 1, COLORS_DIFFICULTY[difficulty])
        screen.blit(best_score_text, (230, 292 + 65 * translation))
        translation += 1

# ============================ Main menu function ===================================

def main_menu():
    #This function is responsible for the menu in game. It draws a menu window and allows player to choose the difficulty level or continue with the last game
    
    #Import global variables
    global board_type
    global current_platform
    global last_game_possible


    #Enable the last game button if the last game can be played.
    if last_game_possible == True:
        menu = pygame.image.load(PATHS[current_platform]['ui_main_menu'])
    elif last_game_possible == False:
        print("lastGamedisabled")
        menu = pygame.image.load(PATHS[current_platform]['ui_main_menu_disabledLastGame'])

    #Set loading screen
    loading = pygame.image.load(PATHS[current_platform]['ui_loading_screen'])


    run = True
    while run:
        #Display menu UI
        screen.blit(menu,(0, 0))

        for event in pygame.event.get():

            #Quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            #Clicked mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #Gets the mouse position
                pos = pygame.mouse.get_pos()

                #If the mouse covers the last game button
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 145 and pos[1] < 215 and last_game_possible == True:
                    board_type = "last"
                    screen.blit(loading,(0, 0))
                    run = False

                #If the mouse covers the easy button
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 300 and pos[1] < 365:
                    board_type = "Easy"
                    screen.blit(loading,(0, 0))
                    run = False

                #If the mouse covers the medium button
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 385 and pos[1] < 450:
                    board_type = "Medium"
                    screen.blit(loading,(0, 0))
                    run = False

                #If the mouse covers the hard button
                if pos[0] > 115 and pos[0] < 380 and pos[1] > 475 and pos[1] < 540:
                    board_type = "Hard"
                    screen.blit(loading,(0, 0))
                    run = False

        #Update pygame window
        pygame.display.update()

# ============================ Game function ===================================
        
def game():
    #The main game function responsible for the game.
    
    #Import global variables
    global cords, board_type, current_theme, current_platform, PATHS, end_message, notes, last_game_possible, value
  
    #Variables
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
    
    #Set the sudoku board

    # if board_type == "last":
    #     board = test_grid
    # else:
    board = get_sudoku_grid(board_type) 
    pprint(board) #print board
    
    #Set health
    if board_type == "last":
        health = board['health']
    else:
        health = 3

    #Starts counting time
    start_ticks = pygame.time.get_ticks()
    
    run = True
    while run:

        #Reset value variable
        value = 0

        #Draw the game window

        screen.fill(colour_themes[current_theme]['background_colour']) #Fill background
        ui = pygame.image.load(colour_themes[current_theme]['ui']) #loads Game UI
        draw_highlighted_cells() #Marks vertical, horizontal tiles and square
        draw_grid(board['value']) #Draw sudoku grid
        draw_notes(board['value']) #Draw notes

        screen.blit(ui, (0, 500)) #draw Game UI
        draw_health(health) # Draw health
        draw_pencil_button(is_pencil_clicked) #Draw pencil button


        for event in pygame.event.get():

            #Quit the game
            if event.type == pygame.QUIT:
                run = False
                save_game(board, current_time, health)
                
                pygame.quit()
                sys.exit()

            #Mouse button clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #Get mouse position
                pos = pygame.mouse.get_pos()
                
                #Update the highlighted tile if the player clicks on the board.
                if pos[1] <= 500:
                    cords = get_cords(pos)
                
                #Change themes
                if pos[0] >= 25 and pos[0] <= 100 and pos[1] >= 515 and pos[1] <= 585:
                    if current_theme == 'dark':
                        current_theme = 'white'
                        continue
                    if current_theme == 'white':
                        current_theme = 'dark'
                        continue

                #Pencil
                if pos[0] >= 125 and pos[0] <= 175 and pos[1] >= 525 and pos[1] <=575:
                    print('pencil')
                    if is_pencil_clicked == True:
                        is_pencil_clicked = False
                    elif is_pencil_clicked == False:
                        is_pencil_clicked = True

            #Sets the value to the value entered by the player    
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
        
        #Chcecks player move
        if board['value'][int(cords[0])][int(cords[1])] == 0:
            
            #If pencil doesn't active
            if is_pencil_clicked == False and value != 0:  
                if valid(board, value, cords) == True: #If possible, fill the tile
                    board['value'][int(cords[0])][int(cords[1])] = value
                    notes[int(cords[0])][int(cords[1])] = [0] #Reset
                else:
                    health -= 1
            
            #If pencil active
            if is_pencil_clicked == True:
                change_notes(value, cords)
        
        #Ends the game if defeat
        if health == 0:
            last_game_possible = False
            end_message = "defeat" #Set end message text
            run = False

        #Ends game if victory
        if if_win(board) == True:
            last_game_possible = False
            end_message = "victory" #Set end message text
            save_score(board, current_time, health) #Save the result of the game
            run = False
            
        #Set the frame rate limit to 60 frames per second
        clock.tick(60)


        if 'time' in board:
            #If player opens the game again, the last time is added to the current time
            current_time = draw_time(start_ticks, board['time'])  #Saved the current time and display it
        else:
            #Display time from zero
            current_time = draw_time(start_ticks) 
        
        #Update the game window
        pygame.display.update()

# ============================ End menu function ============================
        
def end_menu():
    #Function responsible for the end screen
    
    #Import global variables
    global end_message, play_again

    #Load the end screen image
    end_screen = pygame.image.load(PATHS[current_platform]['end_screen'])

    #Render the end message text
    end_text = FONT_END_MESSAGE.render(end_message.upper(), 1, COLORS_END_MESSAGE[end_message])


    run = True
    while run:

        #Display the end screen image and end message text
        screen.blit(end_screen,(0, 0))
        screen.blit(end_text, set_end_message_cords(end_message))
        
        #If it is victory draw the last game score
        if end_message == 'victory':
            draw_last_game_score()

        #Draw best scores on the screen
        draw_best_scores()

        for event in pygame.event.get():

            #Quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #Set mouse position
                pos = pygame.mouse.get_pos()

                #Check if player wants to play again
                if pos[0] > 115 and pos[0] < 385 and pos[1] > 455 and pos[1] < 525:
                    run = False
                    play_again = True
                    main()
        
        #Update pygame window
        pygame.display.update()


# ============================ Main function ============================
        
def main():
    #Main project function

    #Import global variables
    global play_again

    set_current_platform()
    print(current_platform)


    run = True
    while run:
        play_again = False
        main_menu()
        game()
        end_menu()
        if play_again == True:
            continue
        if play_again == False:
            break

if __name__ == "__main__":
    main()

