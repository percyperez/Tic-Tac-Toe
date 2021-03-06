import random


# Posible ways to win based on one-dimensional list
# Horizontal
ways_to_win = [
    tuple([i for i in range(i, r)]) for i, r in [(0, 3), (3, 6), (6, 9)]
]

# Vertical
vertical = [(v, v+3, v+6) for v in range(3)]
for v in vertical:
    ways_to_win.append(v)

# Add Diagonal
ways_to_win.append((0, 4, 8))
ways_to_win.append((2, 4, 6))
"""
>>> ways_to_win
[
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]
"""

AI_LETTER = 'X'
HUMAN_LETTER = 'O'

"""
According to http://en.wikipedia.org/wiki/Tic-tac-toe
If human does not take the center, then AI takes the center. If center is taken
then playing the corner gives the opponent the smallest choice of squares
"""
BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)
SIDE_MOVES = [1, 3, 5, 7]
SPECIAL_CASE_MOVES = {
    (0, 5): 2,
    (5, 6): 7,
    (2, 3): 0,
    (3, 8): 1
}


def take_corner(request):
    """
    There are 4 possible corners = [0, 2, 6, 8]
    [
        '0', '1', '2',
        '3', '4', '5',
        '6', '7', '8'
    ]
    """
    corners = [0, 2, 6, 8]
    corner = random.choice(corners)
    move(request, corner)
    return corner


def move(request, position, letter=AI_LETTER):
    """
    Updates the board
    """
    board = request.session['board']
    board[position] = letter
    request.session['board'] = board


def move_ai(board):
    """
    Checks to win or block the openent depending on the board
    """
    # Check first if AI can win the game
    move = find_winner_move(board, AI_LETTER)
    if move is not None:
        return move, True

    # Check for special cases if human has two corners in a diagonal or a side
    # with a corner move on the 4th move
    if len(filter(None, board)) == 3:
        move = check_special_moves(board)
        if move is not None:
            return move, False

    # Check if human can win, if so block that move
    move = find_winner_move(board, HUMAN_LETTER)
    if move is not None:
        return move, False

    # Find the best move (empty position) for AI
    empty_positions = get_empty_positions(board)
    for move in BEST_MOVES:
        if move in empty_positions:
            return move, False


def find_winner_move(board, letter):
    """
    Check for all empty positions on the board if AI or Human can win the game
    Returns the winner move. Otherwise None
    """
    empty_positions = get_empty_positions(board)
    board = board[:]

    for move in empty_positions:
        board[move] = letter
        if winner(board) == letter:
            return move

        # Didn't win
        board[move] = ''

    return None


def get_empty_positions(board):
    """
    Returns current empty positions on the board
    """
    positions = [pos for pos in range(9) if board[pos] == '']
    return positions


def winner(board):
    for row in ways_to_win:
        letters = [board[r] for r in row]
        if all(letter == letters[0] and letter != '' for letter in letters):
            return letters[0]

    return None


def is_tie(request):
    """
    Return True if the board is full. Otherwise False
    """
    return all(request.session['board'])


def check_special_moves(board):
    """
    If special case is present in the board, then return a pre-defined move to
    force a draw. Otherwise return None
    """
    for m1, m2 in [(2, 6), (0, 8)]:
        if board[m1] == board[m2] == HUMAN_LETTER:
            move = random.choice(SIDE_MOVES)
            return move

    for moves, move in SPECIAL_CASE_MOVES.iteritems():
        if board[moves[0]] == board[moves[1]] == HUMAN_LETTER:
            return move

    return None
