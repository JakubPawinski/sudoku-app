import pandas as pd
import json
from datetime import date
from static import *

def get_score_by_difficulty(difficulty, current_platform):

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
    
def save_game(board, time, health):
    print("Saved")
    with open(PATHS[current_platform]['boards'], 'r') as json_file:
        json_data = json.load(json_file)
    
    json_data["last"] = board
    json_data["last"].update({"time": time})
    json_data["last"].update({"health": health})

    with open(PATHS[current_platform]['boards'], 'w') as json_file:
        json.dump(json_data, json_file)

def save_score(current_platform, board, time, health):
    CsvFile = pd.read_csv(PATHS[current_platform]['resultsDataBase'])
    new_row = {'Date': date.today(), 'DifficultyLevel': board['difficulty'], 'LivesRemaining': health, 'Time': time, 'Score': count_score(board['difficulty'], time, health)}
    CsvFile.loc[len(CsvFile)] = new_row
    CsvFile.to_csv(PATHS[current_platform]['resultsDataBase'], index=False)
    print("Score saved", new_row)




def count_score(difficulty, time, health):
    if difficulty == "Easy":
        difficulty_level = 1
    elif difficulty == "Medium":
        difficulty_level = 2
    elif difficulty == "Hard":
        difficulty_level = 3
    score = int(-1 * (0.3 * difficulty_level / health * time) + 1000)
    if score >= 0:
        return score
    else:
        return 0
