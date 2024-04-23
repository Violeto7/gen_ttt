import os
import numpy as np
import pygad

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
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result and result != 0:
            res = 'X' if result == 1 else 'O'
            print(f"{res} won!")
            return True
        result = checkDiagonals(board)
        if result and result != 0:
            res = 'X' if result == 1 else 'O'
            print(f"{res} won!")
            return True
    return False

def fitness_func(ga, solution, solution_idx):
    temp_gs = [solution[0:3],solution[3:6],solution[6:9]]
    if(game_won(temp_gs) == True):
        return 100
    fitness = 0
    
    # Check rows
    for row in temp_gs:
        if row.count(1) == 3:
            fitness += 2
        elif row.count(1) == 2 and row.count(2) == 1:
            fitness += 1
    
        fitness -= row.count(2)
    
        # Check columns
        for col in range(3):
            column = [temp_gs[row][col] for row in range(3)]
            if column.count(1) == 3:
                fitness += 2
            elif column.count(1) == 2 and column.count(2) == 1:
                fitness += 1
        
            fitness -= column.count(2)
        
        # Check diagonals
        if temp_gs[0][0] == temp_gs[1][1] == temp_gs[2][2] == 1 or \
        temp_gs[0][2] == temp_gs[1][1] == temp_gs[2][0] == 1:
            fitness += 2
        elif temp_gs[0][0] == temp_gs[1][1] == temp_gs[2][2] == 2 or \
           temp_gs[0][2] == temp_gs[1][1] == temp_gs[2][0] == 2:
            fitness -= 1
        
        if temp_gs[0][0] == 1 and temp_gs[1][1] == temp_gs[2][2] == 2:
            fitness += 1
        elif temp_gs[0][0] == 2 and temp_gs[1][1] == temp_gs[2][2] == 1:
            fitness -= 1
        
        if temp_gs[0][2] == 1 and temp_gs[1][1] ==temp_gs[2][0] == 2:
            fitness += 1
        elif temp_gs[0][2] == 2 and temp_gs[1][1] == temp_gs[2][0] == 1:
            fitness -= 1
        
        return fitness

def callback_generation(ga_instance):
    solution = ga_instance.best_solution()[0]
    temp_gs = [solution[0:3],solution[3:6],solution[6:9]]
    if game_won(temp_gs) == True:
        return "stop"
        

def display_game_state(gameState):
    for x in gameState:
        # count = 0
        # for y in x:
        #     if y == 0:
        #         print('-')
        #     elif y == 1:
        #         print('X')
        #     elif y == 2:
        #         print('O')
        #     if count < 2:
        #         print(' | ')
        #     count += 1
        print(*x, sep=' | ')

def take_turn(gameState, agent_symbol):
    #this function will take the current gameState, generate solutions and run our GA
    #after we have determined the best solution, update gameState and move on
    Solutions = []
    #generate solutions
    for row in range(0, len(gameState)):
        for x in range(0, len(gameState)):
            if gameState[row][x] == 0:
                #use this as one of our solutions, copy this gameState and add it to our list of solutions
                temp_gs = gameState
                temp_gs[row][x]=agent_symbol
                flattened_list = [item for sublist in temp_gs for item in sublist]
                Solutions.append(flattened_list)

    ga_instance = pygad.GA(num_generations = 2,
                           num_parents_mating = 2,
                           fitness_func=fitness_func,
                           fitness_batch_size=1,
                           initial_population = Solutions,
                           mutation_type=None,
                            )
    solution = ga_instance.best_solution()[0]
    gameState = [solution[0:3],solution[3:6],solution[6:9]]
    return

def runGame(size):
    print(f"Running game with size {size}")
    global gameState 
    gameState = [[0 for x in range(size)] for y in range(size)] # make our nxn grid
    agent_symbol = 1
    opponent_symbol = 2
    agents_turn = True

    while game_won(gameState) == False:
        if(agents_turn):
            take_turn(gameState, agent_symbol)
        else:
            #temporary
            #----------
            taken = False
            for row in range(0, len(gameState)):
                for x in range(0, len(gameState)):
                    if gameState[row][x] == 0:
                        gameState[row][x] =opponent_symbol
                        taken = True
                        break
                if taken: 
                    break
            #----------
        if agents_turn == True:
            agents_turn = False
        else:
            agents_turn = True
        
        display_game_state(gameState)

runGame(3)