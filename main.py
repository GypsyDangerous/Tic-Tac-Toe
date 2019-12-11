import pygame
import numpy as np
pygame.init()
import math
import time
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, r"C:\Users\david\Python")

from misc import Random

SIZE = WIDTH, HEIGHT = 470, 470

def rect(screen, color, x, y, w, h, fill=0):
    pygame.draw.rect(screen, color, (x, y, w, h), fill)

def square(screen, color, x, y, s, fill=0):
    rect(screen, color, x, y, s, s, fill)
    
def ellipse(screen, color, x, y, w, h, fill=0):
    pygame.draw.ellipse(screen, color, (x, y, w, h), fill)

def circle(screen, color, x, y, r, fill=0):
    ellipse(screen, color, x, y, r, r, fill)

def background(screen, color):
    rect(screen, color, 0, 0, WIDTH, HEIGHT)

def check_win(board):
    n = len(board)
    first = board[0][0]
   
    diagonal = first != ""
    for i in range(n):
        if board[i][i] != first:
            diagonal = False
            break
    if diagonal:
        return first
    first = board[0][n-1]
    back_diag = first != ""
    for i in range(1, n+1):
        if board[i-1][n-i] != first:
            back_diag = False
            break
    if back_diag:
        return first

    for i in range(n):
        first = board[i][0]
        sideways = first != ""
        for j in range(n):
            if board[i][j] != first:
                sideways = False
        if sideways:
            return first

    for i in range(n):
        first = board[0][i]
        # print(first)
        sideways = first != ""
        for j in range(n):
            if board[j][i] != first:
                sideways = False
        if sideways:
            return first
    
    open_spots = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                open_spots += 1
    if open_spots == 0:
        return "tie"
    return None

def best_move(board):
    n = len(board)
    best_score = -math.inf
    move = (0, 0)
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                board[i][j] = "x"
                score = minimax(board, 0, False, len(board))
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    board[move[0]][move[1]] = "x"
    return board

scores = {
        "x" : 10,
        "o" : -10,
        "tie": 0
    }

def minimax(board, depth, is_max, n, alpha = -math.inf, beta = math.inf):
    winner = check_win(board)
    if winner:
        # print(depth)
        return scores[winner]
    if is_max:
        best_score = -math.inf
        for i in range(n):
            for j in range(n):
                if board[i][j] == "":
                    board[i][j] = "x"
                    score = minimax(board, depth+1, False, n, alpha, beta)+Random(-5, 5)
                    board[i][j] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta >= alpha:
                        pass
        return best_score
    else:
        best_score = math.inf
        for i in range(n):
            for j in range(n):
                if board[i][j] == "":
                    board[i][j] = "o"
                    score = minimax(board, depth+1, True,n, alpha, beta)+Random(-5, 5)
                    board[i][j] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if alpha >= beta:
                        pass
        return best_score

def reset(n):
    board = [["" for i in range(n)] for j in range(n)]
    loop = True
    return board, loop, None, True

def main():
    padding = 10
    n = 3
    s = (WIDTH-padding*2)//n
    
    board = [["" for i in range(n)] for j in range(n)]

    turn = "x"

    x_image = pygame.image.load(r"ex.png")
    x_image = pygame.transform.scale(x_image, (s, s))
    o_image = pygame.image.load(r"o.png")
    o_image = pygame.transform.scale(o_image, (s, s))

    loop = True
    gameover = False

    frame_count = 0
    human_played = False
    winner = False
    restarted = False
    
    running = True
    board = best_move(board)
    turn = "x" if turn == "o" else "o"
    # print(f"{turn}'s Turn")

    screen = pygame.display.set_mode(SIZE) #Start the screen

    while running:
        prev = frame_count
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
                if event.type == pygame.QUIT: #The user closed the window!
                    running = False #Stop running
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        board, loop, winner, restarted = reset(n)
                        
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    j = int(Mouse_x//s)
                    i = int(Mouse_y//s)
                    if i < n and j < n:
                        if board[i][j] == "":
                            board[i][j] = turn
                            turn = "x" if turn == "o" else "o"
                            # print(f"{turn}'s Turn")
                            human_played = True
                        winner = check_win(board)
                        # print(np.array(board))
                                

        if loop:
            rect(screen, (255, 255, 255), padding, padding, WIDTH-padding*2, HEIGHT-padding*2)
            
            # Logic goes here
            if not winner:
                winner = check_win(board)
            # print(winner)
            if winner:
                if winner == "tie":
                    print(winner.upper()+"!")
                else:
                    print(winner.upper(), "Wins!")
                print("Press 'r' to restart")
                loop = False

            for i in range(n):
                for j in range(n):
                    item = board[i][j]
                    if item == "x":
                        screen.blit(x_image, (j*s+padding, i*s+padding))
                    elif item == "o":
                        screen.blit(o_image, (j*s+padding, i*s+padding))
                    square(screen, (0,0, 0), j*s+padding, i*s+padding, s, 3)


            pygame.display.update()

            if restarted:
                turn = "x"
                board = best_move(board)
                turn = "x" if turn == "o" else "o"
                restarted = False

            if human_played:
                time.sleep(.5)
                board = best_move(board)
                turn = "x" if turn == "o" else "o"
                # print(f"{turn}'s Turn")
                human_played = False
            frame_count += 1
    pygame.quit() #Close the window

if __name__ == "__main__":
    main()