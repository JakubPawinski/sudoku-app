# Sudoku Game

## Project Overview

This project is a fully-featured **Sudoku game** developed using **Pygame**. Sudoku is a classic logic-based number puzzle where players fill a 9x9 grid with digits from 1 to 9, ensuring no repetition in any row, column, or 3x3 subgrid. The game offers a polished user experience with multiple difficulty levels, dynamic themes, and advanced features like score tracking and game state persistence.

The game is designed for single-player use and provides an engaging and intuitive interface for players of all skill levels.

## Key Features

- **Multiple Difficulty Levels**: Choose between Easy, Medium, and Hard for a tailored challenge.
- **Dynamic Themes**: Switch between light and dark themes for a personalized visual experience.
- **Pencil Mode**: Take notes directly on the board to assist with solving puzzles.
- **Score Tracking**: Tracks and displays scores based on performance, including high scores for each difficulty level.
- **Game Persistence**: Save and resume your last game seamlessly.
- **API Integration**: Sudoku boards are dynamically fetched from an external API for variety and replayability.
- **Error Feedback**: Lose health points for incorrect moves, adding a layer of challenge.

## Game Rules:

1.  The standard Sudoku board consists of a 9x9 grid divided into 3x3 blocks. Each block is further divided into 3x3 fields.
2.  The player fills the board with numbers from 1 to 9. Each number can only appear once in each row, column, and 3x3 block.
3.  The game starts with a partially filled grid, where some fields already have numbers.
4.  Each field on the board can only contain one digit. The player's task is to fill the entire board.

## System Requirements

- **Python Version**: Python 3.8 or higher
- **Required Libraries**:
  - [Pygame](https://www.pygame.org/)
  - [Pandas](https://pandas.pydata.org/)
  - [Requests](https://docs.python-requests.org/)

## Installation Guide

Follow these steps to set up and run the Sudoku game:

1. **Ensure Python is Installed**:
   Verify that Python 3.8 or higher is installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Clone the Repository**:
   Clone the project repository to your local machine:

   ```bash
   git clone https://github.com/JakubPawinski/sudoku-app.git
   cd sudoku

   ```

3. **Install Dependencies**:

   ```bash
   pip install pygame pandas requests
   ```

4. **Run the Game**:
   ```bash
   python main.py
   ```

## Controls

### Mouse Interaction:

- **Click on cells** to select them.
- **Use the pencil button** to toggle note-taking mode.

### Keyboard Input:

- **Press numeric keys (1-9)** to input values into selected cells.

### Theme Toggle:

- **Click the theme button** to switch between light and dark modes.

## Scoring System

The scoring system rewards players based on the difficulty level, time taken, and remaining health. Scores are calculated as follows:

- **Easy**: Base score multiplier of 1.
- **Medium**: Base score multiplier of 2.
- **Hard**: Base score multiplier of 3.
- **Health and Time**: Higher health and faster completion result in higher scores.

High scores for each difficulty level are saved and displayed on the end screen.

## Screenshots

![GameScreenshot01](img/MainMenuTemplate.png)

   <br>

![GameScreenshot02](img/GameScreenshot01.png)

   <br>

![GameScreenshot03](img/GameScreenshot02.png)

## Author

- Jakub Pawiński
