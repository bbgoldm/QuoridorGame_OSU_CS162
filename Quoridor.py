# Author: Brent Goldman
# Date: 7/29/2021
# Description:  Quoridor Board Game Simulation.  Final Project CS-162

"""
DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS"
Determining how to store the board.
    If player calls move_pawn() and move is successful,
        Call update_location() to update the player's location

    If player calls place_fence() and fence placement is succesful,
        Update _board variable with the fence position


Initializing the board
    Create _board variable when new QuoridorGame object is created

Determining how to track which player's turn it is to play right now.
    After player makes a move by either calling move_pawn() or place_fence(),
        call update_turn() to change which player goes next.

Determining how to validate a moving of the pawn.
    Check if _winner variable is None to make sure there has not been a winner
        declared
    Check _turn variable to make sure it is the player's turn
    Check to make sure move is on the board by looking at the x and y coordinates
        of the move.
    Determine the move size and make sure the move size is either 1 or 2.
    Call is_blocked() to determine if there is a fence blocking the path of the
        pawn.
        For diagonal moves, check to make sure:
            The opponent's pawn is next to the player, in the direction the
                player is trying to move.
            There is a fence behind the opponent's pawn.
            There is no fence between the player's pawn and opponent's pawn.
            There is no fence in the diagonal direction blocking the player's
                pawn.
    If any of the above tests fail, return False, else update pawn location and
        return True.

Determining how to validate placing of the fences.
    Check if _winner variable is None to make sure there has not been a winner
        declared
    Check _turn variable to make sure it is the player's turn
    Call get_fence_count() to make sure the player has a fence to play
    Check the coordinates of the fence location to make sure it is on the board.
    Check there is no fence of the same type already at the location of
        placement.
    If any of the above tests fail, return False, else place the fence and
        return True

Determining how to keep track of fences on the board and off the board.
    place_fence() is passed a tuple of integers that represents the position
        on which the fence is to be placed.
    Set x_fence to the first value in the tuple
    Set y_fence to the second value in the tuple
        If x_fence < 0 or y_fence < 0 or x_fence > 8 or y_fence > 8 Then
            the fence is off the board, return False
        Else, the fence is on the board.

Determining how to keep track of the pawn's position on the board.
    There are two variables, _p1 and _p2 that contain tuples for the player
    positions.

    If move_pawn() passes all validation checks, then call update_location()
        which will update either _p1 or _p2 depending on which integer
        representing the player is passed into the method.
"""


class QuoridorGame:
    """Play the game called Quoridor.  Create an object for the game to
    be played."""

    def __init__(self):
        """
        Constructor method that initializes the board with the fences
        (four edges) and pawns (P1 and P2) placed in the correct positions.

        Moves are expressed as (x,y), where x is column, y is row.
        This is important because the board is expressed as (row, column)
        """
        self._winner = None
        self._turn = 1
        self._p1_fences = 10  # Player 1 fences left to play
        self._p2_fences = 10  # Player 2 fences left to play
        self._p1 = (4, 0)  # Player 1 starting position
        self._p2 = (4, 8)  # Player 2 starting position
        # Represents the fence locations for the Quoridor board
        self._board = [['vh', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],
                       ['v', '-', '-', '-', '-', '-', '-', '-', '-'],
                       ['v', '-', '-', '-', '-', '-', '-', '-', '-'],
                       ['v', '-', '-', '-', '-', '-', '-', '-', '-'],
                       ['v', '-', '-', '-', '-', '-', '-', '-', '-'],
                       ['v', '-', '-', '-', '-', '-', '-', '-', '-'],
                       ['v', '-', '-', '-', '-', '-', '-', '-', '-'],
                       ['v', '-', '-', '-', '-', '-', '-', '-', '-'],
                       ['v', '-', '-', '-', '-', '-', '-', '-', '-'],
                       ['vh', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h']]

    def print_board(self):
        """Method to print out the board.  Doesn't take any parameters.
        The board doesn't contain the players, so before printing the
        players are added onto the board.  They are removed after printing."""

        # Store string for current board
        board_str_1 = self._board[self._p1[1]][self._p1[0]]
        board_str_2 = self._board[self._p2[1]][self._p2[0]]

        # Add player 1 onto board
        self._board[self._p1[1]][self._p1[0]] += '1'

        # Add player 2 onto board
        self._board[self._p2[1]][self._p2[0]] += '2'

        print(self._board)

        # Remove player 1 from board
        self._board[self._p1[1]][self._p1[0]] = board_str_1

        # Remove player 2 from board
        self._board[self._p2[1]][self._p2[0]] = board_str_2

    def move_pawn(self, player, coord):
        """
        Method takes following two parameters in order: an integer that
        represents which player (1 or 2) is making the move and a tuple with
        the coordinates of where the pawn is going to be moved to.

        If the move is forbidden by the rule or blocked by the fence,
        return False

        If the move was successful or if the move makes the player win,
        return True

        If the game has been already won, return False
        """
        # Initial checks (for winner and player turn)
        pass_checks = self.initial_checks(player)
        if not pass_checks:
            return False

        # Get opponent's location
        opp_loc = self.get_opp_location(player)

        # Determine coordinates for move
        x, y = self.get_move_coords(coord)

        # Ensure move is on the board
        is_location_ok = self.check_move_location(coord)
        if not is_location_ok:
            return False

        # Determine move vector
        move_x, move_y = self.get_move_vector(player, coord)

        # Determine move size
        move_size = abs(move_x) + abs(move_y)
        print("Move size is", move_size)

        # If moving diagonally, the opponent pawn must be in a vertical
        # direction, not horizontal
        x_curr, y_curr = self.get_curr_location(player)
        if (abs(move_y) == 1 and abs(move_x) == 1) and \
            opp_loc[0] - x_curr != 0:
            print("Opponent is not vertically adjacent, can't move diag.")
            return False

        # If move size > 2 or <1, then not valid size
        if move_size > 2 or move_size < 1:
            print("Move size of", move_size, "not allowed!")
            return False

        # Check for a jump and whether it passes conditions
        jump_ok = self.check_jump(player, coord, x_curr, y_curr, opp_loc)
        if not jump_ok: return False

        # Validate the fence and pawns are in OK positions for a move
        is_blocked = self.is_blocked(x_curr, y_curr, player, coord, opp_loc)
        if is_blocked: return False


        print("Valid move")
        self.update_location(player, x, y)  # update pawn's location
        print("Moved", player, "to:", coord)
        self.update_winner(player, x, y)  # check if player has won
        self.update_turn(player)  # update player's turn
        return True  # return True since move was successful

    def initial_checks(self, player):
        """
        Method that checks whether there is already a winner and if it is the
        correct player's turn.
        :param player: int of 1 or 2 representing the player making the move
        :return: False if the checks fail, else return True
        """
        # Check if already a winner
        if self._winner is not None:
            print("Player", self._winner, "has already won!")
            return False

        # Return False if not player's turn
        if player != self._turn:
            print("It is not your turn.\n")
            return False

        return True

    def get_opp_location(self, player):
        """
        Method to return a tuple representing the opponent's location
        :param player: int of either 1 or 2 representing the player making the move
        :return: (x,y) tuple for where the opponent is located
        """
        if player == 1:
            opp_loc = self.get_location(2)
        else:
            opp_loc = self.get_location(1)
        return opp_loc

    def get_move_coords(self, coord):
        """
        Method to determine the x and y move coordinates.

        :param coord: (x,y) tuple for where the player is trying to move
        :return: x, y are integers for the move coordinates
        """
        x = coord[0]
        y = coord[1]
        return x, y

    def check_move_location(self, coord):
        """
        Method to determine if the move location is on the board or not.

        :param coord: (x,y) tuple for where the player is trying to move
        :return: True if the move is valid, return False if the move is off the board
        """
        # Determine coordinates for move
        x, y = self.get_move_coords(coord)

        if x > 8 or y > 8 or x < 0 or y < 0:
            print("Move is off the board")
            return False
        return True

    def get_curr_location(self, player):
        """
        This method will return the current x and y coordinates
        for where the player is located
        :param player: integer for the player number
        :return: x_curr, y_curr: integers for the x and y coordinates
        """
        # Get player's location
        curr_location = self.get_location(player)
        x_curr = curr_location[0]
        y_curr = curr_location[1]
        return x_curr, y_curr


    def get_move_vector(self, player, coord):
        """
        This method will calculate the vector for where the player
        is trying to move.  The vector is the x and y direction

        :param player: int representing the player number
        :param coord: tuple for the player's move coordinates
        :return:
            move_x: int, x vector for where the player is moving
            move_y: int, y vector for where the player is moving
        """
        # Determine coordinates for move
        x = coord[0]  # x coordinate for move
        y = coord[1]  # y coordinate for move

        # Get player's location
        x_curr, y_curr = self.get_curr_location(player)

        print("Current location is:", (x_curr, y_curr))
        print("Plan to move to:", coord)
        move_vector = [x - x_curr, y - y_curr]
        move_x = move_vector[0]
        move_y = move_vector[1]
        print("Move vector is", move_vector)
        return move_x, move_y

    def check_jump(self, player, coord, x_curr, y_curr, opp_loc):
        """This method will check when a player is trying to jump
        the opponent's pawn whether the jump is in the vertical
        direction, and if there is a pawn to jump over.  This method
        does not check for fences.

        move_size: is an integer that is an absolute value of how many
                   squares the playing is trying to move.
        move_x: is an integer for the x position of the direction the pawn is moving
        move_y: is an integer for the y position of the direction the pawn is moving
        x_curr: is an integer for current x position of the pawn
        y_curr: is an integer for current y position of the pawn
        opp_loc: is a tuple that represents the opponents location in (x,y)

        The method will return False if one of the checks fail,
        otherwise return true.
        """
        # Move Vector
        move_x, move_y = self.get_move_vector(player, coord)

        # Determine move size
        move_size = abs(move_x) + abs(move_y)

        # If trying to jump, it can only be in vertical direction
        if move_size == 2 and move_x != 0 and move_y == 0:
            print("Can't jump horizontally")
            return False

        # If trying to make a jump, there needs to be a pawn in the first space
        if move_size == 2 and (move_y == 0 or move_x == 0):
            if (x_curr + move_x / 2, y_curr + move_y / 2) != opp_loc:
                print("No pawn to jump")
                return False

        return True

    def is_blocked(self, x_curr, y_curr, player, coord, opp_loc):
        """ Method takes following seven parameters in order:
            x_curr: is an integer for current x position of the pawn
            y_curr: is an integer for current y position of the pawn
            x: is an integer for the x position of where the pawn is moving
            y: is an integer for the y position of where the pawn is moving
            move_vector: is a list with the 2 integers, the difference on the
                x axis where the player is trying to move and where they are
                currently located.  And the the second integer is the same as
                x but for the y axis.
            move_size: is an integer that is an absolute value of how many
                squares the playing is trying to move.
            opp_loc: is a tuple that represents the opponents location in (x,y)

        The purpose of the method is to determine if there is a fence or pawn
        in the player's way that would prevent them from moving to the
        destination space.  If there is a fence blocking the path, return
        True, else return False."""

        # Determine coordinates for move
        x, y = self.get_move_coords(coord)

        # Get x, y move vector
        move_x, move_y = self.get_move_vector(player, coord)

        # Get x, y current location
        x_curr, y_curr = self.get_curr_location(player)

        # Figure out which location to check for a blocking fence
        check_x, check_y, check_vec = self.fence_check(move_x, move_y, x_curr,
                                                       y_curr, x, y)

        # Check for fence blocking path
        if check_vec in self._board[check_y][check_x]:
            print("Blocked by fence")
            return True

        # Check for opponent pawn
        if (x, y) == opp_loc:
            print("Blocked by pawn")
            return True

        # If moving diagonally
        if abs(move_y) == 1 and abs(move_x) == 1:
            # Find difference between player's pawn and opp pawn locations
            x_delta = opp_loc[0] - x_curr
            y_delta = opp_loc[1] - y_curr

            # Confirm there is an opponent pawn one space away
            if x_delta * move_x < 0 or y_delta * move_y < 0:
                print("Diag move not allowed, no opp pawn in way")
                return True

            # Check if there is a fence between players
            check_x, check_y, check_vec = self.pawn_fence(x_delta, y_delta, \
                                                          x_curr, y_curr, x, y)
            if check_vec in self._board[check_y][check_x]:
                print("A fence exists between player pawns, can't move diag.")
                return True

            # Check if there is a fence behind the opponent
            check_x, check_y, check_vec = self.opp_fence(x_delta, y_delta, \
                                                         x_curr, y_curr, x, y)
            if check_vec not in self._board[check_y][check_x]:
                print("No fence behind opponent pawn, can't move diag.")
                return True

        # Not blocked
        else:
            print("Not blocked")
            return False


    def fence_check(self, move_x, move_y, x_curr, y_curr, x, y):
        """
        Method takes following six parameters in order:
            move_x: is an integer that shows the difference on the x-axis
                from where the player is and where the player is moving to.
            move_y: is the same as x_delta but for y-axis.
            x_curr: is an integer for current x position of the pawn
            y_curr: is an integer for current y position of the pawn
            x: is an integer for the x position of where the pawn is moving
            y: is an integer for the y position of where the pawn is moving

        The method will calculate the location where a fence needs to be
        checked, including on a diagonal move, and return the following:
            check_x: integer for the x-axis location to check.
            check_y: integer for the y-axis location to check.
            check_vec: string to check either 'h' or 'v'"""

        if move_x < 0 and move_y == 0:
            check_x = x + 1
            check_y = y
            check_vec = 'v'
        elif move_x > 0 and move_y == 0:
            check_x = x
            check_y = y
            check_vec = 'v'
        elif move_x == 0 and move_y > 0:
            check_x = x_curr
            check_y = y
            check_vec = 'h'
        elif move_x == 0 and move_y < 0:
            check_x = x_curr
            check_y = y + 1
            check_vec = 'h'

        # diagonal check
        elif move_x < 0 and move_y != 0:
            check_x = x + 1
            check_y = y
            check_vec = 'v'
        elif move_x > 0 and move_y != 0:
            check_x = x
            check_y = y
            check_vec = 'v'

        return check_x, check_y, check_vec

    def pawn_fence(self, x_delta, y_delta, x_curr, y_curr, x, y):
        """
        Method takes following six parameters in order:
            x_delta: is an integer that shows the difference on the x-axis
                from where the player is and where the opponent is.
            y_delta: is the same as x_delta but for y-axis.
            x_curr: is an integer for current x position of the pawn
            y_curr: is an integer for current y position of the pawn
            x: is an integer for the x position of where the pawn is moving
            y: is an integer for the y position of where the pawn is moving

        For diagonal moves to be legal, there can't be a fence between the
        pawns.  Calculate where to check for a fence that could block the
        player's move.  This method will return:
            check_x: integer for the x-axis location to check.
            check_y: integer for the y-axis location to check.
            check_vec: string to check either 'h' or 'v'"""

        if x_delta == 0:
            check_vec = 'h'
        else:
            check_vec = 'v'

        if x_delta < 0 or y_delta < 0:
            check_x = x_curr
            check_y = y_curr
        elif x_delta > 0:
            check_x = x_curr + 1
            check_y = y_curr
        elif y_delta > 0:
            check_x = x_curr
            check_y = y_curr + 1

        return check_x, check_y, check_vec

    def opp_fence(self, x_delta, y_delta, x_curr, y_curr, x, y):
        """
        Method takes following six parameters in order:
            x_delta: is an integer that shows the difference on the x-axis
                from where the player is and where the opponent is.
            y_delta: is the same as x_delta but for y-axis.
            x_curr: is an integer for current x position of the pawn
            y_curr: is an integer for current y position of the pawn
            x: is an integer for the x position of where the pawn is moving
            y: is an integer for the y position of where the pawn is moving

        For diagonal moves to be legal, there must be a fence behind the
        opponent's pawn.  Calculate where to check for the fence behind the
        opponent's pawn to make sure it exists.  This method will return:
            check_x: integer for the x-axis location to check.
            check_y: integer for the y-axis location to check.
            check_vec: string to check either 'h' or 'v'"""

        if x_delta == 0:
            check_vec = 'h'
        else:
            check_vec = 'v'

        if y_delta == 0:
            check_y = y_curr
        elif y_delta < 0:
            check_y = y
        else:
            check_y = y + 1

        if x_delta == 0:
            check_x = x_curr
        elif x_delta < 0:
            check_x = x
        else:
            check_x = x + 1

        return check_x, check_y, check_vec

    def update_winner(self, player, x, y):
        """
        Method takes following three parameters in order:
            player: an integer for the player, either 1 or 2.
            x: integer location on the x-axis where the player moved
            y: integerlocation on the y-axis where the player moved

        Check if move if a winning move.  If winning move, update winner.
        For a player to win, they must be located on the opponent's base line.
        This method does not return anything.
        """
        if player == 1 and y == 8:
            self._winner = player
        elif player == 2 and y == 0:
            self._winner = player

    def get_location(self, player):
        """ Method that takes a single integer representing the player number as
        a parameter and then returns the player's location as a tuple."""
        if player == 1:
            return self._p1
        else:
            return self._p2

    def update_location(self, player, x, y):
        """
        Method takes following three parameters in order:
            player: an integer for the player, either 1 or 2.
            x: integer location on the x-axis where the player moved
            y: integerlocation on the y-axis where the player moved

        The method will update the player's location as a tuple and does
        not return anything."""

        if player == 1:
            self._p1 = (x, y)
        else:
            self._p2 = (x, y)

    def update_turn(self, player):
        """Method that takes a single integer representing the player number as
        a parameter and then updates the player's turn as an integer.  The
        method does not return anything."""
        if player == 1:
            self._turn = 2
        else:
            self._turn = 1

    def place_fence(self, player, angle, coord):
        """
        Method takes following parameters in order: an integer that represents
        which player (1 or 2) is making the move, a letter indicating whether
        it is vertical (v) or horizontal (h) fence, a tuple of integers that
        represents the position on which the fence is to be placed.

        If player has no fence left, or if the fence is out of the boundaries
        of the board, or if there is already a fence there and the new fence
        will overlap or intersect with the existing fence, return False.

        If the fence can be placed, return True.

        If it breaks the fair-play rule (and if you are doing the extra
        credit part), return exactly the string breaks the fair play rule.

        If the game has been already won, return False
        """

        # Initial checks (for winner and player turn)
        pass_checks = self.initial_checks(player)
        if not pass_checks:
            return False

        # Ensure player has a fence to play
        if self.get_fence_count(player) <= 0:
            print("Player has no more fences to play")
            return False

        # Ensure fence is on the board
        x_fence = coord[0]
        y_fence = coord[1]
        if x_fence < 0 or y_fence < 0 or x_fence > 8 or y_fence > 8:
            print("Fence can't be placed off the board")
            return False

        # Ensure no same fence already in location
        fence_at_location = self._board[y_fence][x_fence]
        if angle in fence_at_location:
            print("Already same fence at location")
            return False

        # Place the fence
        board_value = self._board[y_fence][x_fence]
        if self._board[y_fence][x_fence] == '-':
            self._board[y_fence][x_fence] = angle
        else:
            self._board[y_fence][x_fence] += angle

        # Ensure fence doesn't violate fair play rule
        is_fair = self.find_path(player)

        if not is_fair:
            self._board[y_fence][x_fence] = board_value
            print("Violates fair play")
            return "breaks the fair play rule"

        self.update_fence_count(player)  # update player fence count
        self.update_turn(player)  # update player's turn
        return True

    def get_fence_count(self, player):
        """ Method that takes a single integer representing the player number as
        a parameter and then returns the player's fence count as an integer."""
        if player == 1:
            return self._p1_fences
        else:
            return self._p2_fences

    def update_fence_count(self, player):
        """ Method that takes a single integer representing the player number as
        a parameter and then updates the player's fence count by decrementing
        it by one.  The method does not return anything."""
        if player == 1:
            self._p1_fences -= 1
        else:
            self._p2_fences -= 1

    def is_winner(self, player):
        """
        Method that takes a single integer representing the player number as
        a parameter and returns True if that player has won and False if that
        player has not won.
        """
        if player == self._winner:
            return True
        else:
            return False

    def get_winner(self):
        """ Method takes no parameters and returns the winner as an integer.
        The return will be None if there is no winner."""
        return self._winner

    def find_path(self, player):
        """
        Method will determine if the fence being played prevents
        the opponent player from reaching the baseline.

        Method takes following two parameters in order:
            x_curr: is an integer for current x position of the pawn
            y_curr: is an integer for current y position of the pawn

        Use Breadth-First algorithm to find path to opponent baseline.
        Return True if the fence placement is valid.  Return False
        if the fence placement blocks the opponent.
            """
        # Player is player making move, need to get opponent's information
        player = self.get_opp_player(player)

        # Get player's pawn location
        start = self.get_location(player)

        # Determine where the pawn is trying to get to
        dest_row = self.get_goal(player)

        # Get the board
        board = self._board

        visit = []
        # Need to keep track of visited locations
        # Set all visit locations to False to start
        for row in range(len(board)):
            visit.append([False] * 9)

        # Create a list queue to store spaces as tuples to traverse
        spaces = [start]

        # Directions to try and move
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

        # Continue to loop until there are no more spaces to check
        while len(spaces) > 0:
            space = spaces.pop()  # pop a space so it isn't checked again
            visit[space[0]][space[1]] = 'True'  # mark space as visited

            # Loop through different directions to move: u, d, l, r
            for dir in directions:

                # Get the current location of the pawn
                x_curr = space[0]
                y_curr = space[1]

                # Get the direction player is moving to
                move_x, move_y = self.get_move_coords(dir)

                # Get coordinates of move
                x = space[0] + dir[0]
                y = space[1] + dir[1]

                # Ensure the move is on the board and we have visited the location
                # If not then skip rest of loop
                if x < 0 or x > 8 or y < 0 or y > 8 or visit[x][y] is not False: continue

                # Need to figure out what fence type to check and where to check
                check_x, check_y, check_vec = self.fence_check(move_x, move_y, x_curr, y_curr, x, y)

                # If no fence blocking move then update spaces
                if check_vec not in self._board[check_y][check_x]:
                    spaces.append((x, y))

                    # Check if reached destination
                    if y == dest_row:
                        print("Passed Fairplay: Destination Reached")
                        return True
        return False

    def get_goal(self, player):
        """
        Method returns the row that the player is trying to get to

        :param player: int of 1 or 2 for the player number
        :return: int for the destination row
        """
        if player == 1:
            dest_row = 8
        else:
            dest_row = 0
        return dest_row

    def get_opp_player(self, player):
        """
        Method returns the opponent's player number

        :param player: int of 1 or 2 for the player number
        :return: int for the opponent player number
        """
        if player == 1:
            player = 2
        else:
            player = 1
        return player

def main():
    """Test various moves"""
    pass


if __name__ == '__main__':
    main()