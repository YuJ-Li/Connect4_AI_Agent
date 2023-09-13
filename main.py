from pandas import DataFrame
import numpy as np
import copy
import time

# time limit for computer to make a move
time_limit = 1


def create_board():
    # create an empty 7x7 game board
    board = []
    for row in range(7):
        board.append([])
        for col in range(7):
            board[row].append(' ')
    return board


def initialize_game(board, num):
    if num == 1:
        board[0][1] = 'X'
        board[0][2] = 'X'
        board[0][4] = 'O'
        board[1][6] = 'X'
        board[2][0] = 'O'
        board[3][0] = 'O'
        board[3][6] = 'O'
        board[4][6] = 'O'
        board[5][0] = 'X'
        board[6][2] = 'O'
        board[6][4] = 'X'
        board[6][5] = 'X'
    elif num == 2:
        board[0][5] = 'O'
        board[0][6] = 'O'
        board[1][4] = 'O'
        board[1][5] = 'X'
        board[1][6] = 'X'
        board[3][5] = 'O'
        board[5][1] = 'X'
        board[5][5] = 'X'
        board[5][6] = 'O'
        board[6][1] = 'X'
        board[6][2] = 'X'
        # board[6][6] = 'O'

    # place all initial chess as shown in the requirements

    return board


def move_n(board, x, y, steps):
    # move up by entering the game board and the x,y coordinate of the chess
    board[x - steps][y] = board[x][y]
    board[x][y] = ' '
    return board


def move_s(board, x, y, steps):
    # move down by entering the game board and the x,y coordinate of the chess
    board[x + steps][y] = board[x][y]
    board[x][y] = ' '
    return board


def move_w(board, x, y, steps):
    # move left by entering the game board and the x,y coordinate of the chess
    board[x][y - steps] = board[x][y]
    board[x][y] = ' '
    return board


def move_e(board, x, y, steps):
    # move right by entering the game board and the x,y coordiante of the chess
    board[x][y + steps] = board[x][y]
    board[x][y] = ' '
    return board


def check_max_move(board, x, y):
    # check how many moves can the selected chess move
    # my chess
    curr = board[x][y]
    # enemy chess
    if curr == 'X':
        opp = 'O'
    elif curr == 'O':
        opp = 'X'
    else:
        return -1
    # enemy chess count within the 8 squares
    count = 0
    # make sure it is not out of bound
    if x - 1 >= 0:
        if board[x - 1][y] == opp:
            count += 1
        if y - 1 >= 0:
            if board[x - 1][y - 1] == opp:
                count += 1
            if board[x][y - 1] == opp:
                count += 1
        if x + 1 <= 6:
            if board[x + 1][y] == opp:
                count += 1
            if board[x + 1][y - 1] == opp:
                count += 1
            if y + 1 <= 6:
                if board[x + 1][y + 1] == opp:
                    count += 1;
                if board[x][y + 1] == opp:
                    count += 1;
                if board[x - 1][y + 1] == opp:
                    count += 1;
    if count == 0:
        return 3
    elif count == 1:
        return 2
    elif count == 2:
        return 1
    else:
        return 0


def check_jump(game, curr_x, curr_y, steps, dir):
    # verify if a move is a jump, return 1 for jump, 0 for normal move
    if dir.upper() == 'N':
        for i in range(1, steps + 1):
            if game[curr_x - i][curr_y] != ' ':
                return 1
    elif dir.upper() == 'S':
        for i in range(1, steps + 1):
            if game[curr_x + i][curr_y] != ' ':
                return 1
    elif dir.upper() == 'E':
        for i in range(1, steps + 1):
            if game[curr_x][curr_y + i] != ' ':
                return 1
    elif dir.upper() == 'W':
        for i in range(1, steps + 1):
            if game[curr_x][curr_y - i] != ' ':
                return 1
    else:
        return 0


def check_out_of_board(game, cmdlist):
    cmd = cmdlist[2].upper()
    y = int(cmdlist[1])
    x = int(cmdlist[0])
    step = int(cmdlist[3])
    if cmd == 'N':
        if y - step < 0:
            return 1
    elif cmd == 'S':
        if y + step > 6:
            return 1
    elif cmd == 'W':
        if x - step < 0:
            return 1
    elif cmd == 'E':
        if x + step > 6:
            return 1
    else:
        return 0


def check_valid_move(board, user_color, val):
    # Check if it is an valid move
    user_color = user_color.upper()
    if user_color == 'O':
        opp_color = 'X'
    else:
        opp_color = 'O'
    if len(val) != 4:
        # print("This command is not valid")
        return -1
    else:
        # split command into a list [y,x,direction,step]
        val_list = list(val.upper())
        val_list[0] = int(val_list[0])
        val_list[1] = int(val_list[1])
        val_list[3] = int(val_list[3])
        max_move = check_max_move(board, val_list[1], val_list[0])
        if max_move == -1:
            # print("Please move a chess instead of blank")
            return -1
        elif board[val_list[1]][val_list[0]] != user_color:
            # print("Move your own chess")
            return -1
        elif val_list[3] > max_move:
            # print("You are not allowed to move " + str(val_list[3]) + " steps, " + "The maximum you can do is " + str(
            #      max_move))
            return -1
        elif val_list[3] < 1:
            # print("You are not allowed to make negative move or move 0 steps")
            return -1
        elif val_list[2] != 'N' and val_list[2] != 'S' and val_list[2] != 'W' and val_list[2] != 'E':
            # print("Direction can only be N(North),S(South),W(West) or E(East)")
            return -1
        elif check_out_of_board(board, val_list):
            # print("You cannot move out from the board")
            return -1
        elif check_jump(board, val_list[1], val_list[0], val_list[3], val_list[2]):
            # print("Jump is not allowed")
            return -1
        else:
            return val_list


def move(game, user_cmd_list):
    if user_cmd_list[2] == "N":
        move_n(game, int(user_cmd_list[1]), int(user_cmd_list[0]), int(user_cmd_list[3]))
    elif user_cmd_list[2] == "S":
        move_s(game, int(user_cmd_list[1]), int(user_cmd_list[0]), int(user_cmd_list[3]))
    elif user_cmd_list[2] == "W":
        move_w(game, int(user_cmd_list[1]), int(user_cmd_list[0]), int(user_cmd_list[3]))
    elif user_cmd_list[2] == "E":
        move_e(game, int(user_cmd_list[1]), int(user_cmd_list[0]), int(user_cmd_list[3]))
    else:
        return 0


def ai_move(board, user_color):
    best_move, _, state_visited = minimax(board, user_color, 2, True, 0)
    # best_move, _, state_visited = alpha_beta_pruning(board, user_color, 2, True, -np.inf, np.inf, 0)
    return best_move


def possible_moves(board, x, y, color):
    cmd = ''
    cmdlist = []
    for i in range(1, 4):
        cmd = str(x) + str(y) + 'N' + str(i)
        if check_valid_move(board, color, cmd) != -1:
            cmdlist.append(cmd)
        cmd = str(x) + str(y) + 'S' + str(i)
        if check_valid_move(board, color, cmd) != -1:
            cmdlist.append(cmd)
        cmd = str(x) + str(y) + 'W' + str(i)
        if check_valid_move(board, color, cmd) != -1:
            cmdlist.append(cmd)
        cmd = str(x) + str(y) + 'E' + str(i)
        if check_valid_move(board, color, cmd) != -1:
            cmdlist.append(cmd)

    return cmdlist


def generate_all_possible_moves(board, color):
    all_possible_moves = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == color:
                all_possible_moves += possible_moves(board, j, i, color)
    return all_possible_moves


def minimax(board, user_color, depth, maximizing_player, state_visited):
    print(state_visited)
    valid_moves = generate_all_possible_moves(board, user_color)
    if depth == 0 or detect_game_state(board) != 0:
        return None, detect_game_state(board), state_visited

    if maximizing_player:
        v = -np.inf
        best_move = valid_moves[0]
        for cmd in valid_moves:
            temp_board = copy.deepcopy(board)
            cmd_list = list(cmd)
            move(temp_board, cmd_list)
            _, new_score, state_visited = minimax(temp_board, user_color, depth - 1, False, state_visited + 1)
            if user_color == 'X':
                new_score = -new_score
            if new_score > v:
                v = new_score
                best_move = cmd
        return best_move, -v, state_visited
    else:
        v = np.inf
        best_move = valid_moves[0]
        for cmd in valid_moves:
            temp_board = copy.deepcopy(board)
            cmd_list = list(cmd)
            move(temp_board, cmd_list)
            _, new_score, state_visited = minimax(temp_board, user_color, depth - 1, True, state_visited + 1)
            if user_color == 'X':
                new_score = -new_score
            if new_score < v:
                v = new_score
                best_move = cmd
        return best_move, -v, state_visited


def alpha_beta_pruning(board, user_color, depth, maximizing_player, alpha, beta, state_visited):
    valid_moves = generate_all_possible_moves(board, user_color)
    if depth == 0 or detect_game_state(board) != 0:
        return None, detect_game_state(board), state_visited

    if maximizing_player:
        v = -np.inf
        best_move = valid_moves[0]
        for cmd in valid_moves:
            temp_board = copy.deepcopy(board)
            cmd_list = list(cmd)
            move(temp_board, cmd_list)
            _, new_score, state_visited = alpha_beta_pruning(temp_board, user_color, depth - 1, False, alpha, beta,
                                                             state_visited + 1)
            if user_color == 'X':
                new_score = -new_score
            print(new_score, cmd)
            if new_score > v:
                v = new_score
                best_move = cmd
            if v >= beta:
                break
            alpha = max(alpha, v)
        return best_move, -v, state_visited
    else:
        v = np.inf
        best_move = valid_moves[0]
        for cmd in valid_moves:
            temp_board = copy.deepcopy(board)
            cmd_list = list(cmd)
            move(temp_board, cmd_list)
            _, new_score, state_visited = alpha_beta_pruning(temp_board, user_color, depth - 1, True, alpha, beta,
                                                             state_visited + 1)
            if user_color == 'X':
                new_score = -new_score
            if new_score < v:
                v = new_score
                best_move = cmd
            if v <= alpha:
                break
            beta = min(beta, v)
        return best_move, -v, state_visited


def detect_game_state(game):
    # detect if one of the player win's the game, return 1 for White win, -1 for Black win and 0 for neutral
    winner = ''
    for i in range(6):
        for j in range(6):
            if game[i][j] != ' ' and i + 1 < 7 and j + 1 < 7 and game[i][j] == game[i][j + 1]:
                if game[i + 1][j] == game[i][j] and game[i + 1][j + 1] == game[i][j]:
                    winner = game[i][j]
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    else:
        return 0


def display_board(board):
    print(DataFrame(board, index=[1, 2, 3, 4, 5, 6, 7], columns=[1, 2, 3, 4, 5, 6, 7]))


def game_on():
    game = initialize_game(create_board(), 1)
    user_color = ''
    ai_color = ''
    turn = 1
    while True:
        user_color = input("Please choose your color by entering 'O'(white) or 'X'(black): ").upper()
        if user_color == 'X':
            ai_color = 'O'
            turn = -1
            break
        elif user_color == 'O':
            ai_color = 'X'
            break
    display_board(game)
    while detect_game_state(game) == 0:
        if turn == 1:
            val = input("It is your turn, please enter your command: ")
            val = str(int(val[0]) - 1) + str(int(val[1]) - 1) + val[2:]
            print(val)
            user_cmd_list = check_valid_move(game, user_color, val)
            if not isinstance(user_cmd_list, list):
                print("This move is not valid, please re-enter your command")
                display_board(game)
                continue
            else:
                move(game, user_cmd_list)
                check_1 = detect_game_state(game)
                display_board(game)
                # if a winner found, break
                if check_1 == 1:
                    print("The winner is O")
                    break
                elif check_1 == -1:
                    print("The winner is X")
                    break
                turn = -turn
                # CHANGE USER COLOR AFTER TEST
        if turn == -1:
            move(game, ai_move(game, ai_color))
            check_2 = detect_game_state(game)
            display_board(game)
            # if a winner found, break
            if check_2 == 1:
                print("The winner is O")
                break
            elif check_2 == -1:
                print("The winner is X")
                break
            turn = -turn
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game_on()
