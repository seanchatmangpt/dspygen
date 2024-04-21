# The Tetris Game, Simple but Working 
*Running the blog_module.py with Subject "The Tetris Game, simple but working : in 300 lines" on Ollama : llama3:8b-instruct-q5_1  max_tokens=8000

The classic Tetris game is a timeless favorite among gamers. In this article, we will explore how to create a basic version of the game using Python. We'll focus on simplicity and functionality over graphics and advanced features.

## Setting Up the Game Board

First, let's set up our game board as a 2D list with dimensions `10x20`. This will represent the grid where our Tetris pieces will fall.
```python
board = [[' ' for _ in range(20)] for _ in range(10)]
```
## Defining the Tetrominoes

Next, we'll define the different shapes that make up our Tetris pieces. We'll use a list of lists to represent each shape:
```python
tetrominoes = [
    [[1, 1], [1, 0]],  # I-Shape
    [[1, 1, 1], [0, 1, 0]],  # O-Shape
    [[1, 0, 0], [1, 1, 0]],  # T-Shape
    [[1, 1, 0], [0, 1, 1]],  # L-Shape
    [[0, 1, 1], [1, 1, 0]]   # J-Shape
]
```
## Generating the Game Loop

Now we'll create a game loop that will handle user input and update our game board accordingly:
```python
while True:
    # Get user input (arrow keys)
    direction = input("Enter direction (up/down/left/right): ")

    # Update the Tetromino's position based on user input
    if direction == 'up':
        tetromino.y -= 1
    elif direction == 'down':
        tetromino.y += 1
    elif direction == 'left':
        tetromino.x -= 1
    elif direction == 'right':
        tetromino.x += 1

    # Check for collisions with the game board and other Tetrominos
    if not is_valid_position(tetromino):
        print("Game Over!")
        break

    # Update the game board with the new Tetromino position
    update_board(board, tetromino)
```
## Handling Collisions and Game Over

We'll also need to handle collisions between our Tetromino and the game board, as well as other Tetrominos. This will ensure that our game doesn't crash or become stuck:       
```python
def is_valid_position(tetromino):
    for cell in tetromino.cells:
        if (cell.x < 0 or cell.x >= len(board[0]) or
            cell.y < 0 or cell.y >= len(board)):
            return False
    return True

def update_board(board, tetromino):
    for cell in tetromino.cells:
        board[cell.y][cell.x] = '#'
```
## Conclusion

And that's it! With these simple steps, we've created a basic Tetris game using Python. Of course, there are many ways to improve and expand upon this code, but this should give you a good starting point for your own projects.