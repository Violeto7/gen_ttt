import os

def game_won(gameState):
    #loop through gameState and check for winners

    #temporary
    #-------------
    for row in gameState:
        for x in row:
            if x == '-':
                return False
    #-------------
    return True

def take_turn(gameState, agent_symbol):
    #this function will take the current gameState, generate solutions and run our GA
    #after we have determined the best solution, update gameState and move on
    print("Taking turn")
    #temporary
    #----------------------
    for row in gameState:
        for x in row:
            if x == '-':
                x=agent_symbol
                return
    #----------------------
    return

def display_game_state(gameState):
    for x in gameState:
        print(*x, sep=' | ')

def runGame(size):
    print(f"Running game with size {size}")
    gameState = [['-' for x in range(size)] for y in range(size)] # make our nxn grid
    agent_symbol = 'X'
    opponent_symbol = 'O'
    agents_turn = True

    while game_won(gameState) == False:
        if(agents_turn):
            take_turn(gameState, agent_symbol)
        else:
            #temporary
            #----------
            for row in gameState:
                for x in row:
                    if x == '-':
                        x=opponent_symbol
            #----------
            agents_turn = not agents_turn
        
        display_game_state(gameState)

runGame(3)