import math
from static import *
from data_functions import *

def draw_grid(SCREEN, current_theme, board):
    #This function draws the sudoku board

    # print(test_grid[int(cords[0])][int(cords[1])])
    #This loop draws numbers
    for i in range(9):
        for j in range(9):
            #Draw if highlited number != board number
            if board[i][j] != 0 and board[i][j] != board[int(cords[0])][int(cords[1])] and cords[1] <= 8:
                text1 = FONT_GRID.render(str(board[i][j]), 1, colour_themes[current_theme]['number'])
                SCREEN.blit(text1, (i * GRID_GAP + 20, j * GRID_GAP + 15))
                
            #Draw if highlited number == board number
            if board[i][j] == board[int(cords[0])][int(cords[1])] and board[i][j] != 0 and cords[1] <= 8:
                text1 = FONT_GRID.render(str(board[i][j]), 1, colour_themes[current_theme]['highlited_number_colour'])
                SCREEN.blit(text1, (i * GRID_GAP + 20, j * GRID_GAP + 15))
                if i == cords[0] and cords[1] == j:
                    text1 = FONT_GRID.render(str(board[i][j]), 1, colour_themes[current_theme]['number'])
                    SCREEN.blit(text1, (i * GRID_GAP + 20, j * GRID_GAP + 15))
                    # print(i, j, board[i][j], "cords", cords)
    #This loop draws sudoku lines  
    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(SCREEN, colour_themes[current_theme]['number'], (0, i * GRID_GAP), (500, i * GRID_GAP), thick)
        pygame.draw.line(SCREEN, colour_themes[current_theme]['number'], (i * GRID_GAP, 0), (i * GRID_GAP, 500), thick)  


    
def draw_highlighted_cells(SCREEN, current_theme, cords):
    #This function draws highlited cells

    #Check if it is possible to highlight the cells
    if cords[0] <= 8 and cords[1] <= 8:
        box_cords = get_highlighted_box_cords(cords)
        #highlited box
        pygame.draw.rect(SCREEN, colour_themes[current_theme]['highlited_colour_background'], (box_cords[0] * GRID_GAP, box_cords[1] * GRID_GAP, GRID_GAP * 3, GRID_GAP * 3))
        #vertical line
        pygame.draw.rect(SCREEN, colour_themes[current_theme]['highlited_colour_background'], (cords[0] * GRID_GAP, 0, GRID_GAP, 9 * GRID_GAP))
        #horizontal line
        pygame.draw.rect(SCREEN, colour_themes[current_theme]['highlited_colour_background'], (0, cords[1] * GRID_GAP, GRID_GAP * 9, GRID_GAP))
        #Highlited cell
        pygame.draw.rect(SCREEN, colour_themes[current_theme]['highlited_colour'], (cords[0] * GRID_GAP, cords[1] * GRID_GAP, GRID_GAP, GRID_GAP))

def draw_time(SCREEN, current_theme, start_ticks, recent_time=0):
    time = (pygame.time.get_ticks() - start_ticks) / 1000
    time = math.floor(time)
    time += recent_time
    seconds = time % 60 
    minutes = time // 60
    if seconds <= 9:
        seconds = '0' + str(seconds)
    if minutes <= 9:
        minutes = '0' + str(minutes)

    text = FONT_TIMER.render((str(minutes) + ' : ' + str(seconds)), 1, colour_themes[current_theme]['number'])
    SCREEN.blit(text, (310, 522))
    return (time)

def draw_health(SCREEN, current_platform, health):

    img = pygame.image.load(PATHS[current_platform]['health'][health])
    SCREEN.blit(img,(220, 520))

def draw_pencil_button(SCREEN, current_platform, is_clicked):
    clicked = pygame.image.load(PATHS[current_platform]['pencil'][is_clicked])
    unclicked = pygame.image.load(PATHS[current_platform]['pencil'][is_clicked])
    if is_clicked == True:
        SCREEN.blit(clicked, (125, 525))
    if is_clicked == False:
        SCREEN.blit(unclicked, (125, 525))

def draw_notes(SCREEN, current_theme, board, notes, cords):

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
                            text1 = FONT_NOTES.render(str(number), 1, colour_themes[current_theme]['highlited_number_colour'])
                        else:
                            text1 = FONT_NOTES.render(str(number), 1, colour_themes[current_theme]['number'])
                        SCREEN.blit(text1, ( (i * GRID_GAP) + ( horizontal_gap * GRID_GAP/3) + 5, (j* GRID_GAP) + ( vertical_gap * GRID_GAP/3 ) + 4))
                        horizontal_gap += 1

                        if horizontal_gap == 3:
                            horizontal_gap = 0
                            vertical_gap += 1

def draw_last_game_score(SCREEN, end_message, difficulty, time, health):
    last_game_score = count_score(difficulty, time, health)
    score_text = FONT_LAST_GAME_SCORE.render(str(last_game_score) + ' points', 1, END_MESSAGE_COLORS[end_message])
    SCREEN.blit(score_text, (180, 150))

def draw_best_scores(SCREEN, current_platform):
    translation = 0
    for difficulty in ['Easy', 'Medium', 'Hard']:
        best_score_text = FONT_BEST_SCORES.render(str(get_score_by_difficulty(str(difficulty), current_platform)), 1, DIFFICULTY_FONT_COLORS[difficulty])
        SCREEN.blit(best_score_text, (230, 292 + 65 * translation))
        translation += 1