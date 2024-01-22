import pygame

#pygame init
pygame.init()

cords = [0, 0]
board_type = None
value = 0


play_again = False
last_game_score = 0
last_game_possible = True

end_message = ''
current_platform = 'windows'

SCREEN_SIZE = (500, 600)


PATHS = {
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


#colors

END_MESSAGE_COLORS = {
    'victory': (60, 201, 67),
    'defeat': (175, 19, 19)
}

DIFFICULTY_FONT_COLORS = {
    'Easy': (41, 226, 111),
    'Medium': (226, 167, 41),
    'Hard': (212, 83, 29)
}

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

BLACK_COLOR = (0, 0, 0)


GRID_GAP = SCREEN_SIZE[0]/9



#fonts
FONT_GRID = pygame.font.SysFont(None, 40)
FONT_END_MESSAGE = pygame.font.SysFont(None, 60)
FONT_TIMER = pygame.font.SysFont(None, 80)
FONT_NOTES = pygame.font.SysFont(None, 16)
FONT_LAST_GAME_SCORE = pygame.font.SysFont(None, 40)
FONT_BEST_SCORES = pygame.font.SysFont(None, 26)


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