import random
import re



# configurations
dim_x = 10
dim_y = 10
num_mines = 5

# global variables
board = []
user_board = []
unrevealed_safe_cells = []
mine_cells = []

# . is free, * is mine, f is flag, ? is question, X is not revealed yet
re_options = re.compile('^[f?c] [0-9]+ [0-9]+$')


def main():
    # make boards
    global board, user_board, unrevealed_safe_cells, mine_cells
    board = [['.' for i in range(dim_x)] for j in range(dim_y)]
    user_board = [['X' for i in range(dim_x)] for j in range(dim_y)]

    # distribute mines randomly
    mines_left_to_distribute = num_mines
    while mines_left_to_distribute > 0:
        # place mine in random spot
        # redo if position already has mine
        pos = (random.randint(0, dim_x-1), random.randint(0, dim_y-1))
        # debug: print(pos)
        if board[pos[0]][pos[1]] == '*':
            continue
        else:
            board[pos[0]][pos[1]] = '*'
            mine_cells.append((pos[0], pos[1]))
            mines_left_to_distribute = mines_left_to_distribute - 1

    # put numbers on board
    # also fill unrevealed safe cells for win condition
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == '.':
                unrevealed_safe_cells.append((row, col))

                adjacent_cells = get_adjacent_cells((row, col))

                for cell in adjacent_cells:
                    if board[cell[0]][cell[1]] == '*':
                        if board[row][col] == '.':
                            board[row][col] = 1
                        elif board[row][col] in [1, 2, 3, 4, 5, 6, 7]:
                            board[row][col] = board[row][col] + 1

    # start the game
    while True:
        # win condition
        if not unrevealed_safe_cells:
            print('*** Congratulations! You Win! ***')
            print_board(board)
            break

        # regular move
        else:
            print_board(user_board)
            print()

            # print options
            print_user_options()

            user_choice = input('Next move: ')

            if re_options.match(user_choice):
                op, input_row, input_col = user_choice.split(' ')
                input_row = int(input_row)
                input_col = int(input_col)
                if 1 <= input_row <= dim_x and 1 <= input_col <= dim_y:
                    row = input_row - 1
                    col = input_col - 1
                    # option: click
                    if op == 'c':
                        print('click ' + str(input_row) + ' ' + str(input_col))
                        if (row, col) in mine_cells:
                            print('*** BOOM ***')
                            print('You clicked a mine! Game Over.')
                            exit(0)
                        elif (row, col) in unrevealed_safe_cells:
                            click((row, col))

                    # option: flag
                    elif op == 'f':
                        # debug: print('flag ' + str(input_row) + ' ' + str(input_col))
                        if user_board[row][col] in ['X', '?']:
                            user_board[row][col] = 'f'
                        elif user_board[row][col] == 'f':
                            user_board[row][col] = 'X'

                    # option: question
                    elif op == '?':
                        # debug: print('question ' + str(input_row) + ' ' + str(input_col))
                        if user_board[row][col] in ['X', 'f']:
                            user_board[row][col] = '?'
                        elif user_board[row][col] == '?':
                            user_board[row][col] = 'X'
                else:
                    print('Invalid row or column')
                    continue

            elif user_choice == 'quit':
                print('Have a nice day!')
                exit(1)

            else:
                print('Invalid input. Must have valid option and row and column separated by spaces')


def print_user_options():
    ops = [
        'f r c: mark a flag on the box in row r, column c',
        'c r c: click the box in row r, column c',
        '? r c: mark a question mark on the box in row r, column c',
        'quit: quit the game',
    ]
    for op in ops:
        print(op)
    print()


def print_board(b):
    # print column numbers
    print('\t', end='')
    for col_num in range(dim_x):
        print(str(col_num + 1) + '\t', end='')
    print()

    # print board with row numbers
    row_num = 1
    for row in b:
        print(str(row_num) + '\t', end='')
        row_num = row_num + 1

        for char in row:
            print(str(char) + '\t', end='')
        print()


def get_adjacent_cells(cell):
    global dim_x, dim_y

    row = cell[0]
    col = cell[1]
    ret = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if 0 <= (row + dx) <= (dim_x - 1) and 0 <= (col + dy) <= (dim_y - 1) \
                    and not (dx == 0 and dy == 0):
                ret.append((row + dx, col + dy))
    return ret


def click(cell):
    global board, user_board, unrevealed_safe_cells

    row = cell[0]
    col = cell[1]
    print(cell)

    # prevent list.remove error and infinite recursion
    was_not_yet_revealed = (user_board[row][col] in ['X', 'f', '?'])

    if was_not_yet_revealed:
        unrevealed_safe_cells.remove(cell)
    user_board[row][col] = board[row][col]

    # continue expanding to reveal numbers
    if board[row][col] == '.' and was_not_yet_revealed:
        adjacent_cells = get_adjacent_cells(cell)
        for cell in adjacent_cells:
            click(cell)




if __name__ == '__main__':
    main()
