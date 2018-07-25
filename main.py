import random
import re



# configurations
dim_x = 10
dim_y = 10
num_mines = 20

# global variables
board = []
user_board = []

# . is free, * is mine, f is flag, ? is question, X is not revealed yet
re_options = re.compile('^[f?c] [0-9]+ [0-9]+$')


def main():
    # make boards
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
            mines_left_to_distribute = mines_left_to_distribute - 1

    # start the game
    while True:
        # win condition
        if board == user_board:
            print('*** Congratulations! You Win! ***')
            print_board(user_board)
            break

        # regular move
        else:
            print_board(user_board)
            print()

            # print options
            print_user_options()

            user_choice = input('Next move: ')

            if re_options.match(user_choice):
                op, row, col = user_choice.split(' ')
                row = int(row)
                col = int(col)
                if 1 <= row <= dim_x and 1 <= col <= dim_y:
                    # TODO: make them actually affect the board
                    if op == 'c':
                        print('click ' + str(row) + ' ' + str(col))
                    elif op == 'f':
                        print('flag ' + str(row) + ' ' + str(col))
                    elif op == '?':
                        print('question ' + str(row) + ' ' + str(col))
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
            print(char + '\t', end='')
        print()


if __name__ == '__main__':
    main()
