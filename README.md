# Minesweeper CLI Edition

## How to Install and Run:

1. Install Python 
https://www.python.org/downloads/

2. Download all 3 files: cells.py exceptions.py minesweeper.py

![createfolder](https://user-images.githubusercontent.com/62896013/185715138-6feadcf4-8419-40a0-8cdc-c074f2d4429c.png)

3. Open your terminal/console and change the directory to the folder where you placed the 3 files.

4. Type "python minesweeper.py" without quotes. See below for example.

![menu](https://user-images.githubusercontent.com/62896013/185715320-d1853897-1e65-44ff-acff-84e209c4cc70.png)

## Game Rules

Same rules as Minesweeper on a 10x10 grid. 

There are 10 mines hidden in the game board. 

After each text prompt, type the row number, then a space, followed by the column number. Example: 2 6

If you know a cell has a mine, then flagging is useful so that you don't accidentally trigger the mine.

Type 'F' (without quotes) after the row and column to flag a cell.

Type 'U' (without quotes) after the row and column to unflag a cell.

The game ends when you fully reveal all 90 cells (i.e. every cell except the ones containing mines). 

### Cheat commands

Type the following strings instead of a row and column number to activate something cool.

"showall" - prints the fully revealed board

"winpls" - automatically wins the game

"reset" - restarts the process with a new board
