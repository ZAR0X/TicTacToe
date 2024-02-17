# Tic Tac Toe Game

![Tic Tac Toe Logo](https://raw.githubusercontent.com/MineisZarox/TicTacToe/master/assets/tic.png)

## Overview

This is a simple implementation of a Tic Tac Toe game using Pygame. The game features a graphical user interface (GUI) and is structured using object-oriented programming (OOP) principles.

## Features

- GUI-based Tic Tac Toe game.
- Player vs. AI gameplay.
- Welcome screen with start and exit buttons.
- Victory, defeat, and tie screens.
- Reset option to play again.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame library

### Clone the Repository

```bash
git clone https://github.com/MineisZarox/TicTacToe.git
```

### Navigate to the Directory

```bash
cd TicTacToe
```

### Run the Game

```bash
python tictactoe.py
```

## Gameplay

- Launch the game and navigate through the welcome screen.
- Click the "Start" button to begin the game.
- Make your moves by clicking on the desired empty cell.
- The game alternates between player (X) and AI (O) turns.
- After the game ends, you can choose to reset or exit.

## `oBrain` Function Logic

The `oBrain` function serves as the AI logic for the game. It attempts to make strategic moves by identifying potential winning combinations for the AI (O) based on the current state of the board.

1. It first checks if there are two O's in a winning combination and returns the remaining empty cell to complete the sequence.
2. If no potential winning moves are found for the AI, it checks for potential winning moves for the player (X) and attempts to block them.
3. The function returns `None` if no immediate winning or blocking moves are identified.

## Note

Feel free to explore the code, experiment with the AI logic, and enjoy playing Tic Tac Toe!

Feedback and contributions are welcome.

---

*This game is created by MineisZarox using Pygame. Original repository: [TicTacToe](https://github.com/MineisZarox/TicTacToe)*
```
