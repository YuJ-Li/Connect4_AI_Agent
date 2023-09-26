import numpy as np
import copy
import socket

# This prgram implemented an AI agent that plays the modified version of Connectr 4, game_on() allows user to interact
# with the AI agent; ai_fight() allows 2 AI agents to fight each other; tournement() connects to the mcgill server and
# play against other colleges; PLEASE MAKE SURE THE ATTACHED TXT FILE ARE IN THE SAME DIRECTORY AS THE PROGRAM!!!!!
# To modify parameters for the AI agent, please go to line 224 to modify the method ai_move(),
# it is by default running alphabeta pruning algorithm with a depth of 4, to change the depth please
# modify the third parameter of the alpha_beta_pruning() at line 226; To switch to minimax algorithm, please comment
# line 226 and uncomment line 225, to change the depth for minimax, please change the third parameter of the minimax()
# at line 225

def create_board():
    # create an empty 7x7 game board
    board = []
    for row in range(7):
        board.append([])
        for col in range(7):
            board[row].append(' ')
    return board


def initialize_game(board, filename):
    # initialize the board by reading in txt game board file
    l1 = read_in(filename)
    for row in range(7):
        for col in range(7):
            board[row][col] = l1[row * 7 + col]
            if board[row][col] == '':
                board[row][col] = ' '
    return board


def read_in(filename):
    # reading in txt file
    f = open(filename, 'r')
    l = []
    for line in f:
        temp = line.split(',')
        temp[-1] = temp[-1].strip('\n')
        l += temp
    return l


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
    if x + 1 <= 6:
        if board[x + 1][y] == opp:
            count += 1
    if y + 1 <= 6:
        if board[x][y + 1] == opp:
            count += 1
    if y - 1 >= 0:
        if board[x][y - 1] == opp:
            count += 1
    if x - 1 >= 0 and y - 1 >= 0:
        if board[x - 1][y - 1] == opp:
            count += 1
    if x - 1 >= 0 and y + 1 <= 6:
        if board[x - 1][y + 1] == opp:
            count += 1
    if x + 1 <= 6 and y - 1 >= 0:
        if board[x + 1][y - 1] == opp:
            count += 1
    if x + 1 <= 6 and y + 1 <= 6:
        if board[x + 1][y + 1] == opp:
            count += 1

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
    # check if a move causes any chess to move out of board
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
    # move the chess
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
    # best_move, gamestate, state_visited, _ = minimax(board, user_color, 6, True, 1)
    best_move, gamestate, state_visited, _ = alpha_beta_pruning(board, user_color, 4, True, -np.inf, np.inf, 1)
    best_move = str(int(best_move[0]) + 1) + str(int(best_move[1]) + 1) + best_move[2:]
    print("move: ", best_move)
    print("game state: ", gamestate)
    return best_move


def possible_moves(board, x, y, color):
    # generate all possible moves of the specify chess
    cmd = ''
    cmdlist = []
    for i in reversed(range(1, 4)):
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
    # generate all possible moves of a color
    all_possible_moves = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == color:
                all_possible_moves += possible_moves(board, j, i, color)
    return all_possible_moves


def minimax(board, user_color, depth, maximizing_player, state_visited):
    # minimax algorithm for the agent
    score = detect_game_state(board, user_color)
    if depth == 0 or score == 1000 or score == -1000:
        return None, score, state_visited, depth

    if maximizing_player:
        valid_moves = generate_all_possible_moves(board, user_color)
        if not valid_moves:
            return None, -1000, state_visited, depth
        v = -np.inf
        best_move = valid_moves[0]
        best_d = 0
        for cmd in valid_moves:
            temp_board = copy.deepcopy(board)
            cmd_list = list(cmd)
            move(temp_board, cmd_list)
            _, new_score, state_visited, d = minimax(temp_board, user_color, depth - 1, False, state_visited + 1)

            if new_score == v:
                # win the fast possible or lose the slowest possible
                if new_score > -1000 and d > best_d:
                    best_move = cmd
                    best_d = d
                elif new_score <= -1000 and d < best_d:
                    best_move = cmd
                    best_d = d
            if new_score > v:
                v = new_score
                best_move = cmd
                best_d = d
        return best_move, v, state_visited, best_d
    else:
        opp_color = ''
        if user_color == 'X':
            opp_color = 'O'
        else:
            opp_color = 'X'
        valid_moves = generate_all_possible_moves(board, opp_color)
        if not valid_moves:
            return None, 1000, state_visited, depth
        v = np.inf
        best_move = valid_moves[0]
        best_d = 0
        for cmd in valid_moves:
            temp_board = copy.deepcopy(board)
            cmd_list = list(cmd)
            move(temp_board, cmd_list)
            _, new_score, state_visited, d = minimax(temp_board, user_color, depth - 1, True, state_visited + 1)
            if new_score == v:
                # win the fast possible or lose the slowest possible
                if new_score < 1000 and d > best_d:
                    best_move = cmd
                    best_d = d
                elif new_score >= 1000 and d < best_d:
                    best_move = cmd
                    best_d = d

            if new_score < v:
                v = new_score
                best_move = cmd
                best_d = d
        return best_move, v, state_visited, best_d


def alpha_beta_pruning(board, user_color, depth, maximizing_player, alpha, beta, state_visited):
    # alpha beta pruning algorithm for the agent
    score = detect_game_state(board, user_color)
    if depth == 0 or score == 1000 or score == -1000:
        return None, score, state_visited, depth

    if maximizing_player:
        valid_moves = generate_all_possible_moves(board, user_color)
        if not valid_moves:
            return None, -1000, state_visited, depth
        v = -np.inf
        best_move = valid_moves[0]
        best_d = 0
        for cmd in valid_moves:
            temp_board = copy.deepcopy(board)
            cmd_list = list(cmd)
            move(temp_board, cmd_list)
            _, new_score, state_visited, d = alpha_beta_pruning(temp_board, user_color, depth - 1, False, alpha, beta,
                                                                state_visited + 1)
            if new_score == v:
                # win the fast possible or lose the slowest possible
                if new_score > -1000 and d > best_d:
                    best_move = cmd
                    best_d = d
                elif new_score <= -1000 and d < best_d:
                    best_move = cmd
                    best_d = d
            if new_score > v:
                v = new_score
                best_move = cmd
                best_d = d
            if v >= beta:
                break
            alpha = max(alpha, v)
        return best_move, v, state_visited, best_d
    else:
        opp_color = ''
        if user_color == 'X':
            opp_color = 'O'
        else:
            opp_color = 'X'
        valid_moves = generate_all_possible_moves(board, opp_color)
        if not valid_moves:
            return None, 1000, state_visited, depth
        v = np.inf
        best_move = valid_moves[0]
        best_d = 0
        for cmd in valid_moves:
            temp_board = copy.deepcopy(board)
            cmd_list = list(cmd)
            move(temp_board, cmd_list)
            _, new_score, state_visited, d = alpha_beta_pruning(temp_board, user_color, depth - 1, True, alpha, beta,
                                                                state_visited + 1)
            if new_score == v:
                # win the fast possible or lose the slowest possible
                if new_score < 1000 and d > best_d:
                    best_move = cmd
                    best_d = d
                elif new_score >= 1000 and d < best_d:
                    best_move = cmd
                    best_d = d

            if new_score < v:
                v = new_score
                best_move = cmd
                best_d = d
            if v <= alpha:
                break
            beta = min(beta, v)
        return best_move, v, state_visited, best_d


def detect_game_state(game, player_color):
    # validate the game state and return the score according to the player color entered
    if player_color == 'X':
        opp_color = 'O'
    else:
        opp_color = 'X'
    # detect if one of the player win's the game, return 1000 for player win, -1000 for opp win
    winner = ''
    s = 0
    for i in range(6):
        for j in range(6):
            if game[i][j] != ' ' and i + 1 < 7 and j + 1 < 7 and game[i][j] == game[i][j + 1]:
                if game[i + 1][j] == game[i][j] and game[i + 1][j + 1] == game[i][j]:
                    winner = game[i][j]
    if winner == player_color:
        return 1000
    elif winner == opp_color:
        return -1000
    else:
        for i in range(7):
            for j in range(7):
                if game[i][j] != ' ':
                    s += score_of_chess(game, i, j, player_color)
    return s


def score_of_chess(game, x, y, mycolor):
    # calculate the score of each chess, make sure don't put ' ' in
    curr = game[x][y]
    oppcolor = 'X' if curr == 'O' else 'O'
    score = 0
    if y + 1 < 7 and curr == game[x][y+1]: # check right
        score += 0
        if x - 1 > -1 and (game[x - 1][y] == curr or game[x-1][y+1] == curr): # L shape
            score += 10
            if game[x-1][y] == curr and game[x-1][y+1] == oppcolor: # L shape blocked
                score -= 10
            elif game[x-1][y+1] == curr and game[x-1][y] == oppcolor: # L shape blocked
                score -= 10
            else:
                if game[x-1][y] == curr and game[x-1][y+1] != oppcolor:
                    # about to win
                    if y + 2 < 7 and game[x-1][y+2] == curr:
                        score += 20
                    elif y + 3 < 7 and game[x-1][y+2] != oppcolor and game[x-1][y+3] == curr:
                        score += 20
                    elif y + 4 < 7 and game[x-1][y+2] != oppcolor and game[x-1][y+3] != oppcolor and game[x-1][y+4] == curr:
                        score += 20
                if game[x-1][y+1] == curr and game[x-1][y] != oppcolor:
                    # about to win
                    if y - 1 > -1 and game[x-1][y-1] == curr:
                        score += 20
                    elif y - 2 > -1 and game[x-1][y-1] != oppcolor and game[x-1][y-2] == curr:
                        score += 20
                    elif y - 3 > -1 and game[x-1][y-1] != oppcolor and game[x-1][y-2] != oppcolor and game[x-1][y-3] == curr:
                        score += 20
        elif x + 1 < 7 and (game[x + 1][y] == curr or game[x + 1][y + 1]) == curr: # L shape
            score += 10
            if game[x+1][y] == curr and game[x+1][y+1] == oppcolor: # L shape blocked
                score -= 10
            elif game[x+1][y+1] == curr and game[x+1][y] == oppcolor: # Lshape blocked
                score -= 10
            else:
                if game[x+1][y] == curr and game[x+1][y+1] != oppcolor:
                    # about to win
                    if y + 2 < 7 and game[x+1][y+2] == curr:
                        score += 20
                    elif y + 3 < 7 and game[x+1][y+2] != oppcolor and game[x+1][y+3] == curr:
                        score += 20
                    elif y + 4 < 7 and game[x+1][y+2] != oppcolor and game[x+1][y+3] != oppcolor and game[x+1][y+4] == curr:
                        score += 20
                if game[x+1][y+1] == curr and game[x+1][y] != oppcolor:
                    # about to win
                    if y - 1 > -1 and game[x+1][y-1] == curr:
                        score += 20
                    elif y - 2 > -1 and game[x+1][y-1] != oppcolor and game[x+1][y-2] == curr:
                        score += 20
                    elif y - 3 > -1 and game[x+1][y-1] != oppcolor and game[x+1][y-2] != oppcolor and game[x+1][y-3] == curr:
                        score += 20
    elif x + 1 < 7 and curr == game[x+1][y]: # check bottom
        score += 0
    if curr == mycolor:
        return score
    else:
        return -score

def display_board(board):
    # display the game board
    for row in board:
        temp = '|'
        for e in row:
            e += '|'
            temp += e
        print(temp)



def game_on():
    # human against AI
    game = initialize_game(create_board(), './state1.txt')
    user_color = ''
    ai_color = ''
    turn = 1 # to determine whose turn
    while True: # setup color
        user_color = input("Please choose your color by entering 'O'(white) or 'X'(black): ").upper()
        if user_color == 'X':
            ai_color = 'O'
            turn = -1
            break
        elif user_color == 'O':
            ai_color = 'X'
            break
    display_board(game)
    while detect_game_state(game, ai_color) != 1000 or detect_game_state(game, ai_color) != -1000:
        if turn == 1:
            val = input("It is your turn, please enter your command: ")
            val = str(int(val[0]) - 1) + str(int(val[1]) - 1) + val[2:]
            user_cmd_list = check_valid_move(game, user_color, val)
            if not isinstance(user_cmd_list, list):
                print("This move is not valid, please re-enter your command")
                display_board(game)
                continue
            else:
                move(game, user_cmd_list)
                check_1 = detect_game_state(game, ai_color)
                display_board(game)
                # if a winner found, break
                if check_1 == 1000:
                    print("The winner is ", user_color)
                    break
                elif check_1 == -1000:
                    print("The winner is ", ai_color)
                    break
                turn = -turn
                # CHANGE USER COLOR AFTER TEST
        if turn == -1:
            val = ai_move(game, ai_color)
            val = str(int(val[0]) - 1) + str(int(val[1]) - 1) + val[2:]
            move(game, val)
            check_2 = detect_game_state(game,ai_color)
            display_board(game)
            # if a winner found, break
            if check_2 == 1000:
                print("The winner is ", ai_color)
                break
            elif check_2 == -1000:
                print("The winner is ", user_color)
                break
            turn = -turn
    return 0

def ai_fight():
    # AI against AI
    game = initialize_game(create_board(), './state2.txt')
    ai_color_1 = 'O'
    ai_color_2 = 'X'
    turn = 1 # to determine whose turn
    print("Original state")
    display_board(game)
    while detect_game_state(game, ai_color_1) != 1000 or detect_game_state(game, ai_color_1) != -1000:
        if turn == 1:
            print(ai_color_1, " move")
            val = ai_move(game, ai_color_1)
            val_move = str(int(val[0]) - 1) + str(int(val[1]) - 1) + val[2:]
            move(game, val_move)
            check_1 = detect_game_state(game, ai_color_1)
            display_board(game)
            if check_1 == 1000:
                print("The winner is ", ai_color_1)
                break
            elif check_1 == -1000:
                print("The winner is ", ai_color_2)
                break
            turn = -turn
        else:
            print(ai_color_2, " move")
            val = ai_move(game, ai_color_2)
            val = str(int(val[0]) - 1) + str(int(val[1]) - 1) + val[2:]
            move(game, val)
            check_2 = detect_game_state(game, ai_color_1)
            display_board(game)
            if check_2 == 1000:
                print("The winner is ", ai_color_1)
                break
            elif check_2 == -1000:
                print("The winner is ", ai_color_2)
                break
            turn = -turn
    return 0

def tournement():
    # connect to the server and play against colleagues
    cmd = ''
    game = initialize_game(create_board(), './match.txt')
    # connect to the server
    HOST = "156trlinux-1.ece.mcgill.ca"
    PORT = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST,PORT)
    sock.connect(server_address)
    print("Connected to server")
    # send game id and determine color
    gameID = input("Enter the game ID: \n")
    if 'white' in gameID:
        ai_color = 'O'
        opp_color = 'X'
        turn = 1
    else:
        ai_color = 'X'
        opp_color = 'O'
        turn = -1
    gameID += '\n'
    gameID = gameID.encode('utf-8')

    try:
        # send data
        sock.sendall(gameID)
        # receive data
        amount_received = 0
        amount_expected = len(gameID)

        while amount_received < amount_expected:
            received = sock.recv(128)
            amount_received += len(received)
        print("Original state\n")
        display_board(game)
        # game loop
        while detect_game_state(game, ai_color) != 1000 or detect_game_state(game, ai_color) != -1000:
            # !!!!!! detect game over !!!!!
            if turn == 1:
                val = ai_move(game, ai_color)
                val_move = str(int(val[0]) - 1) + str(int(val[1]) - 1) + val[2:]
                move(game, val_move)
                cmd = val
                val += '\n'
                print(val)
                val = val.encode('utf-8')
                sock.sendall(val)
                send_echo = ''
                amount_received = 0
                amount_expected = 4
                while amount_received < amount_expected:
                    send_echo = sock.recv(64)
                    amount_received += len(send_echo)
                send_echo = send_echo.decode('utf-8')
                print("Send echo ",send_echo)
                check_1 = detect_game_state(game, ai_color)
                display_board(game)
                if check_1 == 1000:
                    print("The winner is ", ai_color)
                    break
                elif check_1 == -1000:
                    print("The winner is ", opp_color)
                    break
                turn = -turn
            else:
                rec_msg = 0
                # receive msg
                while True:
                    print("receiving\n")
                    rec_msg = sock.recv(4)
                    rec_msg = rec_msg.decode('utf-8')
                    if rec_msg != 0 and rec_msg != cmd:
                        break
                rec_msg = rec_msg.strip()
                print("received: ", rec_msg)
                if 'Time' in rec_msg or rec_msg == '':
                    print("You win, Game Over\n")
                    break
                rec_move = str(int(rec_msg[0]) - 1) + str(int(rec_msg[1]) - 1) + rec_msg[2:]
                user_cmd_list = check_valid_move(game, opp_color, rec_move)
                if not isinstance(user_cmd_list, list):
                    print("Not a valid move, Game over\n")
                    break
                else:
                    move(game, user_cmd_list)
                    check_2 = detect_game_state(game, opp_color)
                    display_board(game)
                    # if a winner found, break
                    if check_2 == 1000:
                        print("The winner is ", opp_color)
                        break
                    elif check_2 == -1000:
                        print("The winner is ", ai_color)
                        break
                    turn = -turn

    finally:
        sock.close()
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # game_on()
    # ai_fight()
    tournement()
