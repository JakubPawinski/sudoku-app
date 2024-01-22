import pandas as pd
from static import *

def get_score_by_difficulty(difficulty):

    CsvFile = pd.read_csv(PATHS[current_platform]['resultsDataBase']).sort_values(by=['DifficultyLevel', 'Score'], ascending=[False, False])
    if difficulty == "Easy":
        easy_row = CsvFile.loc[CsvFile['DifficultyLevel'] == 'Easy'].iloc[0]
        return easy_row['Score']
    if difficulty == "Medium":
        medium_row = CsvFile.loc[CsvFile['DifficultyLevel'] == 'Medium'].iloc[0]
        return medium_row['Score']
    if difficulty == "Hard":
        hard_row = CsvFile.loc[CsvFile['DifficultyLevel'] == 'Hard'].iloc[0]
        return hard_row['Score']


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