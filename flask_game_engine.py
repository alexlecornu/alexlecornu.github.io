'''This is the code for the program to run with a flask gui'''
import random
from flask import Flask,render_template, request,jsonify,session
import components
import game_engine



app = Flask(__name__)
# sets the app secret key
app.secret_key = "othellogame"


@app.route('/')
def index():
    '''initalises the board and sets the inital colour to dark,
      uses the flask module session to store the colour and colour'''
    board = components.initialise_board()
    colour = "Dark "
    session["board"] = board
    session["colour"] = colour
    return render_template("index.html", game_board = board, colour = colour)




@app.route("/move")
def player_move():
    '''gets the board and colour from the session'''
    colour = session.get("colour")
    board = session.get("board")
    # checks to make sure the board and colour have a value, if not it returns an error
    if board is None or colour is None:
        return jsonify({"status":"fail","message":"session error"})
    # main loop to run the game checks if there are moves
    # for dark and light and switches to the other colour if not,
    # ends the game if both cant move
    loop = True
    while loop:
        cond1 = len(game_engine.valid_moves("Dark ",board))
        cond2 = len(game_engine.valid_moves("Light",board))
        if cond1 ==0  and cond2 == 0:
            endgame = game_end_counter(board)
            loop = False
            return jsonify({'finished':f"Game over, {endgame[0]} ","board":board})

        elif colour == "Dark " and len(game_engine.valid_moves(colour,board)) == 0:
            colour = "Light"
            session["colour"] = colour
            return jsonify({"status":"fail",'message':
                            "No moves available, switching Colour to Light."})
        elif colour == "Light" and len(game_engine.valid_moves(colour,board)) == 0:
            colour = "Dark "
            session["colour"] = colour
            return jsonify({"status":"fail",
                            'message':"No moves available, switching Colour to Dark."})
        if colour == "Dark ":
            x = int(request.args["x"])-1
            y = int(request.args["y"])-1
            coord = (x,y)
            # gets the state and tiles to flip from the legal move function
            state,tiles = components.legal_move(colour,coord,board)
            if state:
                i = 0
                # loop to update the board if tiles are flipped
                while i < len(tiles):
                    board[tiles[i][1]][tiles[i][0]] = colour
                    i+=1
                session["board"] = board
                session["colour"] = "Light"
                ai_result = ai_move(board)
                # returns a message saying success if the move is valid
                return jsonify({"status":"success","board":board,
                                "colour":colour, "ai_board":ai_result["board"],
                                "ai_move":ai_result["move"]})   
            else:
                # returns an error saying illegal move if it is illegel
                return jsonify({"status":"fail",'message':"illegal move."})
        else:
            ai_result = ai_move(board)
            session["board"] = board
            session["colour"] = "Dark "
            return jsonify({"status":"success","board":board,
                                "colour":colour, "ai_board":ai_result["board"],
                                "ai_move":ai_result["move"]}) 


def ai_move(board, colour = "Light"):
    '''this is my ai move function that takes a move as an ai'''
    # it first gets a list of all of the available moves using the valid moves
    #  function from game engine
    available_moves = game_engine.valid_moves(colour,board)
    # then does an if statement to make sure that there are moves it can do
    if len(available_moves) > 0:
        # picks a random index in the array and uses that
        #  as the moveas the index is random it favours the human
        # as no descison making is used to make sure the moves are the best
        index_val = random.randint(0,len(available_moves)-1)
        move = available_moves[index_val]

        # varifies that the move is legal and then changes the tiles
        state,tiles = components.legal_move(colour,move,board)
        if state:
            i = 0
            # loop to update the board if tiles are flipped
            while i < len(tiles):
                board[tiles[i][1]][tiles[i][0]] = colour
                i+=1
            # updates the board
            session["board"] = board
            # sets the colour back to dark
            colour = "Dark "
            # updates the colour
            session["colour"] = colour
            # returns the move and the new board
            return ({"move":move,"board":board})
    else:
        # if the moves available is 0 then it switches the colour back to black
        session["colour"] = "Dark "
        session["board"] = board

        return {"move":None,"board":board}

def game_end_counter(board, size = 8):
    '''This function is used when the game ends to count the number
      of tiles and show who is the winner'''
    #sets the inital conditions
    i = 0
    dark = 0
    light = 0
    # loops through each sublist in the list and counts up the number of black and white tiles
    while i < size:
        j = 0
        while j < size:
            if board[j][i] == "Dark ":
                dark += 1
            elif board[j][i] == "Light":
                light += 1
            j+=1
        i+=1

    # returns an approprate message if light or dark won and if it was a draw
    if light > dark:
        return f"Light has {light} tiles and Dark has {dark} tiles so Light wins!", light, dark
    elif dark > light:
        return f"Light has {light} tiles and Dark has {dark} tiles so Dark wins!",light,dark
    else:
        return f"Light has {light} tiles and Dark has {dark} tiles so its a draw!",light,dark

if __name__ == "__main__":
    app.run()
