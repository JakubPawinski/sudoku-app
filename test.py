import requests
from pprint import pprint
import time

def get_sudoku_grid(difficulty):
    # The function gets the sudoku board from api and returns both the sudoku board and its solution
    print(difficulty)

    get_asked_difficulty = False

    while not get_asked_difficulty:
        api_url = 'https://sudoku-api.vercel.app/api/dosuku'
        response = requests.get(api_url)
        pprint(response)
        data = response.json()
        pprint(data)
        if data['newboard']['grids'][0]['difficulty'] == difficulty:
            get_asked_difficulty = True
            print('===============')
            data = {'value': data['newboard']['grids'][0]['value'], 'solution': data['newboard']['grids'][0]['solution']}
            return data
        time.sleep(1)



pprint(get_sudoku_grid("Easy"))