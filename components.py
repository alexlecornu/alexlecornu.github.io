'''This is the the components file which contains some of the key functions'''


#This is the function that initialises the board and
# creates the inital setup of the board.
# It adds the starting white and black tiles

def initialise_board(size=8):
    '''initialised the board'''
    num = 0
    board = []
    # these set the inital valus for the board and the num which is used in the while loop
    while num < size:
        sub_list = ["None "] * size
        # creates the list full of the value "None "
        if num == 3:
            sub_list[3] = "Light"
            sub_list[4] = "Dark "
        # this changes the values to light and dark in the 4th row down
        if num == 4:
            sub_list[3] = "Dark "
            sub_list[4] = "Light"
        # this changes the values to light and dark in the 5th row
        board.append(sub_list)
        num+=1
    return board

def print_board(board):
    '''This iterates through the board list and prints each sublist on a new line'''
    # initial heading for the board
    print("  |   0   |   1    |   2    |   3    |   4    |   5    |   6    |   7    |")
    # iterates through the board line by line printing the sublist on a new line
    for i,sub_list in enumerate(board):
        print(i,sub_list)

def legal_move(colour, coordinate, board):
    '''This function checks if a move is valid by moving in each direaction 
    and checking for a colour the same as the player'''
    # initialises the x and y coordinates and saves tham as x_start and y_start.
    # also creates the tiles to flip array
    x = coordinate[0]
    y = coordinate[1]
    x_start,y_start = x,y
    tiles_to_flip = []

    # checks that the tile to flip already holds the value none and returns false if it doesnt
    if board[y][x] != "None ":
        return False, tiles_to_flip
    # creates the other colour
    if colour == "Dark ":
        other_c = "Light"
    else:
        other_c = "Dark "
        # creates all the possible directions that the tiles can be flipped in.
    for xd, yd in [[0, 1], [1, 1], [1, 0], [1, -1],[0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        # sets x and y as the starting values
        x = x_start
        y = y_start
        # adds the difference to change the tile
        x += xd
        y += yd
        while is_on_board(x,y) and board[y][x] == other_c:
            # this loop repeated adds values to x and y to make the board
            # check in that directing while the tiles equal the other colour
            x += xd
            y += yd
            if is_on_board(x,y) and board[y][x] == colour:
                # if it reaches the player colour it uses this loop and a legal move has been made
                while True:
                    # this loop backtracks and adds all
                    # the tiles it has passed to the tilestoflip array.
                    #  it ends when x and y are back to the start
                    x -= xd
                    y -= yd
                    tiles_to_flip.append([x,y])
                    if x== x_start and y== y_start:
                        break
                    # checks to make sure tiles to flip is not empty
    if len(tiles_to_flip) == 0:
        return False, tiles_to_flip
    else:
        return True, tiles_to_flip

# checks to make sure the coordinate entered is on the board
def is_on_board(x, y,size = 8):
    '''Checks if the coordinate is on the board'''
    return x >= 0 and x < size and y >= 0 and y < size
