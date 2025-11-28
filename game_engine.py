'''This is the game engine file that allows the game to run in command line'''

import components




def cli_coords_input():
    '''This function allows the user to enter the coordinates'''
    # sets the loop to be true
    loop = True
    while loop:
        # asks for the coordinate inputs
        x = int(input("Enter the x coordinate: "))
        y = int(input("Enter the y coordinate: "))
        # validates the inputs making sure they are within the allowed range
        if x < 0 or x > 7:
            print("Invalid x")
        elif y < 0 or y > 7:
            print("Invalid y")
        else:
            # if the coordinates are valid the loop is false and the while loop stops
            loop = False
    return (x,y)

def simple_game_loop():
    '''This code runs a loop that allows for exactly 60 moves 
    and flips the tiles if the move is valid'''
    print("Welcome to Othello")

    # sets the inital conditions
    colour = "Dark "
    board = components.initialise_board()
    components.print_board(board)
    move_counter = 60

    # main loop for the game, uses the number of moves as a counter
    # and counts down until no moves remain
    while move_counter > 0:
        # checks if there are moves available for dark, if not it switches to white
        if colour == "Dark " and len(valid_moves(colour,board)) == 0:
            colour = "Light"
            print("No available moves for Dark, switching to light")
        # checks if there are moves available for light, if not switches to dark
        elif colour == "Light" and len(valid_moves(colour,board)) == 0:
            colour = "Dark "
            print("No available moves for Light, switching to Dark ")
        # checks to see if there are moves avaiable for light and dark, ends the game if not
        if len(valid_moves("Dark ",board)) ==0 and len(valid_moves("Light",board)) == 0:
            print("Game Over!")
            game_end_counter(board)
            #shows whose turn it is, prints all the valid moves available
        print(f"It is {colour}'s turn")
        print(f'The valid moves are: {valid_moves(colour,board)}')
        #gets the input for the move coordinates
        coords = cli_coords_input()
        # checks if the move is legal setting the state as true if it is and false if it isnt
        state = components.legal_move(colour,coords,board)[0]
        # if the move is legal it flips the tiles returned in the legal move function
        if state:
            tiles = components.legal_move(colour,coords,board)[1]
            i = 0
            # the while loop is used to iterate through the list that contains the tiles to flip
            while i < len(tiles):
                board[tiles[i][1]][tiles[i][0]] = colour
                i+=1
            # prints the board so the new move can be seen
            components.print_board(board)
            # switches the players turn
            if colour == "Dark ":
                colour = "Light"
            else:
                colour = "Dark "
            # decrements the move counter
            move_counter -= 1
        else:
            print("Invalid move")
    #whe the move counter reaches 0 the game ends and the winner is decided by counting up the tiles
    print("Game Over!")
    game_end_counter(board)

def valid_moves(colour,board,size = 8):
    "This function searches the board and returns all of the possible valid moves"
    i = 0
    available_moves = []
    # iterates through the main list
    while i < size:
        j = 0
        # iterates through each sublist and checks if the move in that position is legal
        while j < size:
            # if the move is legal it is appended to a valid_moves array
            if components.legal_move(colour,(i,j),board)[0]:
                available_moves.append((i,j))
            j+=1
        i+=1
    return available_moves

def game_end_counter(board, size = 8):
    '''This function is used when the game ends to count the number of tiles 
    and show who is the winner'''
    # sets the inital variables to 0
    i = 0
    dark = 0
    light = 0
    # iterates through each sub list in the list and counts up the dark adn light values
    while i < size:
        j = 0
        while j < size:
            if board[j][i] == "Dark ":
                dark += 1
            else:
                light += 1
            j+=1
        i+=1
    # compares the dark andlight values to see which is greater
    if light > dark:
        print(f"Light has {light} tiles and Dark has {dark} tiles, so Light wins!")
    elif dark > light:
        print(f"Light has {light} tiles and Dark has {dark} tiles, so Dark wins!")
    else:
        print(f"Light has {light} tiles and Dark has {dark} tiles, so Light and Dark draw!")


if __name__ == "__main__":
    simple_game_loop()
