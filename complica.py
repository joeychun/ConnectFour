import random
import time

class Board:
    """Class used to make up a custom Complica Board, filled with Xs and Os """

    def __init__(self,columns,rows):
        """
        Initializes variables. Columns and Rows are initialized by input.
        List is initialized as an m x n 2-D list with every element " "

        Attributes:
        ______________

        Columns: amount of columns in the custom board
        Rows: amount of rows in the custom board
        List: 2-D array list that contains the spaces of Xs and Os
        """
        self.columns = columns
        self.rows = rows

        # Generate empty 2D list
        self.list = []
        for m in range(self.rows):
            self.list.append([])
            for n in range(self.columns):
                self.list[m].append(" ")

    def print_board(self):
        """
        Prints the board based on the 2-D array list board.list dividing the spaces with +-+-+, | | | |.
        """
        for m in range(self.rows):
            print("+-"*self.columns + "+")
            for n in range(self.columns):
                print(("|" + self.list[m][n]),end='')
            print("|")
        print("+-"*self.columns + "+")

    def copy(self):
        """
        Returns a board that is a copy of itself. Used in ConsideringComputer
        """
        new_board = Board(self.columns,self.rows)

        # Copy list by copying each element (to prevent new_board alter self)
        for m in range(self.rows):
            for n in range(self.columns):
                new_board.list[m][n] = self.list[m][n]

        return new_board



class Player:
    def __init__(self,symbol):
        self.symbol = symbol

    def play(self,board,column):
        puttable = False

        for x in range(board.rows)[::-1]:
            if board.list[x][column] == " ":
                board.list[x][column] = self.symbol
                puttable = True
                break

        if not puttable:
            rnge = range(board.rows)[:0:-1]
            for x in rnge:
                board.list[x][column] = board.list[x-1][column]

            board.list[0][column] = self.symbol



class Human(Player):
    """Subclass of Player. User can manipulate the playing by giving input oneself """

    def __init__(self,symbol):
        """
        Initializes the variable symbol in the super class Player.

        Attributes
        ______________

        Symbol: a character that the Player uses in doing a move in the board.
        """
        super().__init__(symbol)

    def play(self,board):
        print("From 1 to " + str(board.columns) + ", " + self.symbol + ",")
        while True:
            choice = input("What column do you choose to put your piece in? ")
            try:
                choice = int(choice) - 1
            except ValueError:
                print("\n"*100)
                board.print_board()
                print("Please put in a proper integer, " + self.symbol + ".")
                continue

            if choice >= m or choice <= -1:
                print("\n"*100)
                board.print_board()
                print("Please put an integer from 1 to " + str(board.columns) + ", " + self.symbol + ".")
            else:
                break
        super().play(board,choice)

        return None


class Computer(Player):
    """Subclass of Player. Computer makes decision due to the strategy."""

    def __init__(self,symbol,delay,show=True):
        """
        Initializes the variable symbol in the super class Player.

        Attributes
        ______________

        Symbol: a character that the Computer uses in doing a move in the board.
        Delay: The amount of seconds the time will stop so the User can watch the computer's move
        """
        super().__init__(symbol)
        self.delay = delay
        self.show = show

    def play(self,board,column,show,ff=False):
        if not ff:
            super().play(board,column)

        if show:
            print("Waiting for Computer " + self.symbol + " to make his/her move... ")
            time.sleep(self.delay)
            if ff:
                print("Computer " + self.symbol + " forfeits!")
                return True

        return False


class RandomComputer(Computer):
    """Subclass of Computer.
    Strategy: Chooses any random column, and decides to make a move there. """

    def __init__(self,symbol,delay,show=True):
        super().__init__(symbol,delay,show)

    def play(self,board):
        column = random.randint(0, board.columns - 1)
        super().play(board,column,self.show)

class ConsideringComputer(Computer):
    """Subclass of Computer.
    Strategy:
        1) Checks if there are places in which she can put and win
        2) If (1) situation does not exist, Checks if there are places in which when put leading to the opponent's victory
        3) Besides (2) places, FFs. """

    def __init__(self,symbol,delay,opp_symbol,show=True):
        super().__init__(symbol=symbol,delay=delay,show=show)
        #self.opp_player = opp_player
        self.opp_symbol = opp_symbol

    def play(self,board):
        sim_board = board.copy()
        self.show = False
        winning_move = False
        choices = list(range(board.columns))
        for check in range(board.columns):
            sim_board = board.copy()
            super().play(sim_board,check,False)
            won, connected_tmp = winning_player(sim_board,self.symbol)
            if won:
                super().play(board,check,True)
                winning_move = True
                break

            for opp_check in range(board.columns):
                sim_sim_board = sim_board.copy()
                opp_player = Player(self.opp_symbol)
                opp_player.play(sim_sim_board,opp_check)
                lost, connected_tmp = winning_player(sim_sim_board,self.opp_symbol)
                if lost:
                    # This move does not work
                    choices.remove(check)
                    break

        if not winning_move:
            if choices != []:
                super().play(board,random.choice(choices),True)
            else:
                tmp = super().play(board,0,True,ff=True)
                return tmp






################## CUSTOMIZATION OF GAME ####################

# BOARD (m x n)
m = 7
n = 6

# IN A ROW (normal = 4)
w_cond = 4

####################### OBJECT MAKING #######################

# BOARD OBJECT
board = Board(m,n)
#  PLAYER OBJECT
player1 = Human("X")
#player2 = RandomComputer("O",0)
player2 = ConsideringComputer("O",1.5,"X")
#player2 = Human("O")

####################### FUNCTIONS TO USE ####################


# PLAYER DOING A MOVE
def play(player):
    print("\n"*100) # Clearing up previous board
    board.print_board()
    return player.play(board)

# CHECKING IF ONE WON
def winning_player(board,symbol):
    """
    Boolean Function checking if a particular symbol won
    Ninrow    --> returns True
    Nincolumn --> returns True
    Ndiagonal --> returns True
    else      --> returns False
    """

    # Checking 4 in row
    connected = []

    for row in range(board.rows):
        for col in range(board.columns - w_cond + 1):
            connected = []
            for it in range(w_cond):
                if board.list[row][col+it] == symbol:
                    connected.append([row,col+it])
                else:
                    break
            if len(connected) == w_cond:
                return True, connected

    # Checking 4 in column
    connected = []

    for col in range(board.columns):
        for row in range(board.rows - w_cond + 1):
            connected = []
            for it in range(w_cond):
                if board.list[row+it][col] == symbol:
                    connected.append([row+it,col])
                else:
                    break
            if len(connected) == w_cond:
                return True, connected


    # Checking 4 in diagonal (case 1)
    # X
    #   X
    #     X
    #       X
    connected = []

    # Different way of thinking --> [x,y] is the standard, the other will follow

    for x in range(board.rows - w_cond + 1):
        for y in range(board.columns - w_cond + 1):
            connected = []
            for it in range(w_cond):
                if board.list[x+it][y+it] == symbol:
                    connected.append([x+it,y+it])
                else:
                    break
            if len(connected) == w_cond:
                return True, connected

    # Checking 4 in diagonal (case 2)
    #       X
    #     X
    #   X
    # X
    connected = []


    for x in range(board.rows - w_cond + 1):
        for y in range(w_cond - 1, board.columns):
            connected = []
            for it in range(w_cond):
                if board.list[x+it][y-it] == symbol:
                    connected.append([x+it,y-it])
                else:
                    break
            if len(connected) == w_cond:
                return True, connected


    return False, []


def winning(board,player1,player2):
    won, connected1 = winning_player(board, player1.symbol)
    winner = []
    if won:
        winner.append(player1)

    won, connected2 = winning_player(board, player2.symbol)
    if won:
        winner.append(player2)

    return winner, connected1, connected2

# HIGHLITE THE ONES THAT ARE IN ROW
def highlite(board, list, color):
    for x in list:
        board.list[x[0]][x[1]] = color + '\033[1m' + board.list[x[0]][x[1]] + '\033[0m'


####################### MAIN GAME ###########################

# LOOPING TURNS
while True:
    forfeit1 = play(player1)
    if forfeit1:
        break

    winner, connected1, connected2 = winning(board,player1,player2)
    if winner == [player1,player2]:
        highlite(board,connected1,'\033[92m')
        highlite(board,connected2,'\033[94m')
        print("\n"*100)
        print("It is a tie! Well played, both players!")
        board.print_board()
        break
    elif winner == [player1]:
        print(connected1)
        highlite(board,connected1,'\033[92m')
        print("\n"*100)
        print("It is " + player1.symbol + "'s victory!")
        board.print_board()
        break
    elif winner == [player2]:
        highlite(board,connected2,'\033[94m')
        print("\n"*100)
        print("It is " + player2.symbol + "'s victory!")
        board.print_board()
        break

    forfeit2 = play(player2)
    if forfeit2:
        break

    winner, connected1, connected2 = winning(board,player1,player2)
    if winner == [player1,player2]:
        highlite(board,connected1,'\033[92m')
        highlite(board,connected2,'\033[94m')
        print("\n"*100)
        print("It is a tie! Well played, both players!")
        board.print_board()
        break
    elif winner == [player1]:
        highlite(board,connected1,'\033[92m')
        print("\n"*100)
        print("It is " + player1.symbol + "'s victory!")
        board.print_board()
        break
    elif winner == [player2]:
        highlite(board,connected2,'\033[94m')
        print("\n"*100)
        print("It is " + player2.symbol + "'s victory!")
        board.print_board()
        break
