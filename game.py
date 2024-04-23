import os
import numpy as np
import pygad
import random

who_won = '-1'
def checkRows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return 0

def checkDiagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return 0

def game_won(board):
    #transposition to check rows, then columns
    global who_won
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result and result != 0:
            res = 'X' if result == 1 else 'O'
            who_won = res
            return True
        result = checkDiagonals(board)
        if result and result != 0:
            res = 'X' if result == 1 else 'O'
            who_won = res
            return True
    return False

def check_for_draw():
    global gameState
    for row in gameState:
        for x in row:
            if x == 0:
                return False
    return True

def check_empty():
    global gameState
    for row in gameState:
        for x in row:
            if x != 0:
                return False
    return True

def check_for_blocks():
    global gameState
    #check rows
    for i, row in enumerate(gameState):
        y = np.array(row)
        if ((y==2).sum()) == 2:
            for j, x in enumerate(row):
                if x == 0:
                    return i, j
    # Check columns
    for col in range(3):
        column = [gameState[row][col] for row in range(3)]
        y = np.array(column)
        if ((y==2).sum()) == 2:
            for i, x in enumerate(column):
                    if x == 0:
                        return i, col
    if gameState[0][0] == 2 and gameState[1][1] == 2 and gameState[2][2] == 0:
        return 2, 2
    if gameState[0][0] == 2 and gameState[2][2] == 2 and gameState[1][1] == 0:
        return 1, 1
    if gameState[1][1] == 2 and gameState[2][2] == 2 and gameState [0][0] == 0:
        return 0, 0
    if gameState[2][0] == 2 and gameState[1][1] == 2 and gameState[0][2] == 0:
        return 0, 2
    if gameState[1][1] == 2 and gameState[0][2] == 2 and gameState[2][0] == 0:
        return 2, 0
    if gameState[2][0] == 2 and gameState[0][2] == 2 and gameState[1][1] == 0:
        return 1, 1
    
    return -1, -1
    

def fitness_func(ga, solution, solution_idx):
    temp_gs = [solution[0:3],solution[3:6],solution[6:9]]
    if(game_won(temp_gs) == True):######this is fine because if this is true we alwasys win
        return 300
    
    if(check_empty() and temp_gs[1][1] == 1):
        return 50
    
    fitness = 0
    
    x, y = check_for_blocks()
    if (x != -1):
        if (temp_gs[x][y]):
            fitness += 30

    # Check rows
    for row in temp_gs:
        y = np.array(row)
        if ((y==1).sum()) == 2:
            fitness += 1
        if ((y[0] == 1 and y[1] == 1)
            or (y[1] == 1 and y[2] == 1)):
            fitness += 3
    
        fitness -= ((y==2).sum())/2
    
    # Check columns
    for col in range(3):
        column = [temp_gs[row][col] for row in range(3)]
        y = np.array(column)
        if ((y==1).sum()) == 2:
            fitness += 1
        if ((y[0] == 1 and y[1] == 1)
            or (y[1] == 1 and y[2] == 1)):
            fitness += 3
    
        fitness -= ((y==2).sum())/2
    
    #check adjacency of left diagonal
    if temp_gs[0][0] == temp_gs[1][1] == 1 or temp_gs[1][1] == temp_gs[2][2] == 1:
        fitness+= 2
    #check adjacency of right diagonal
    if temp_gs[2][0] == temp_gs[1][1] == 1 or temp_gs[1][1] == temp_gs[0][2] == 1:
        fitness+=2
    return fitness

def callback_generation(ga_instance):
    solution = ga_instance.best_solution()[0]
    temp_gs = [solution[0:3],solution[3:6],solution[6:9]]
    if game_won(temp_gs) == True:
        return "stop"
        

def display_game_state():
    for row in gameState:
        count = 0
        for x in row:
            if x == 0:
                print('-', end='')
            elif x == 1:
                print('X', end='')
            elif x == 2:
                print('O', end='')
                
            if count < 2:
                print(' | ', end='')
            else:
                print('')
            count += 1
    print('---------------')

def take_turn(agent_symbol):
    global gameState
    #this function will take the current gameState, generate solutions and run our GA
    #after we have determined the best solution, update gameState and move on
    Solutions = []

    flattened_list = [item for sublist in gameState for item in sublist]
    for x in range(len(flattened_list)):
        if flattened_list[x] == 0:
            copy = flattened_list.copy()
            copy[x] = 1
            Solutions.append(copy)

    ga_instance = pygad.GA(num_generations = 2,
                           num_parents_mating = 1,
                           fitness_func=fitness_func,
                           fitness_batch_size=1,
                           initial_population = Solutions,
                           mutation_type=None,
                            )
    solution = ga_instance.best_solution()[0]
    gameState = [solution[0:3],solution[3:6],solution[6:9]]
    return

def runGame(size):
    size = 3
    print(f"Running game with size {size}")
    global gameState 
    global who_won
    gameState = [[0 for x in range(size)] for y in range(size)] # make our nxn grid
    agent_symbol = 1
    opponent_symbol = 2
    agents_turn = False
    controlling = True
    while game_won(gameState) == False:
        if(agents_turn):
            take_turn(agent_symbol)
        else:
            taken = False
            while(not taken):
                if(controlling):
                    str = input("Input desired space index (space-separated, 0-index, row col): ")
                    x, y = str.split(' ')
                    if (int(x) < 0 or int(x) > 2 or int(y) < 0 or int(y) > 2):
                        print("Keep the input between 0 and 2 dummy!")
                    elif(gameState[int(x)][int(y)] == 0):
                        gameState[int(x)][int(y)] = opponent_symbol
                        taken = True
                    else:
                        print("Occupied space dummy!")
                else:
                    taken = False
                    while(not taken):
                        x = random.randint(0 , 2)
                        y = random.randint(0 , 2)
                        if(gameState[x][y]==0):
                            gameState[x][y] = opponent_symbol
                            taken = True
        if agents_turn == True:
            agents_turn = False
        else:
            agents_turn = True
        display_game_state()
        if check_for_draw():
            print("The game was a draw!")
            break
        
    if who_won == '-1':
        print("No one won!")
        return
    print(f"{who_won} won!")

runGame(3)