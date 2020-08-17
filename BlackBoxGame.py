# Author: Sergio Torres
# Date: 8/1/20
# Description: Implementation of the Black Box Game, with any  >= 1 number of atoms, with a Black Box Game class
# game starts with 25 points, gets one point deducted for every entry or exit not previously used,
# and five points deducted for every incorrect atom guess not previously used.

class BlackBoxGame:
    """Class that represent the Black Box Game Board"""

    def __init__(self, *atoms, board=None):
        """Constructor of Class Black Box"""

        if board is None:
            board = []

        for row in range(0, 10):
            board.append([])
            for col in range(0, 10):
                if col == 0 or col == 9 or row == 0 or row == 9:
                    board[row].append("#")  # symbol for borders
                else:
                    board[row].append("X")  # symbol for squares in the board

        for row in range(1, 9):
            for col in range(1, 9):
                for tup in atoms:
                    for atom in tup:
                        if atom[0] == row and atom[1] == col:
                            del board[row][col]
                            board[row].insert(col, "O")  # insert symbol to represent atoms

        self._board = board
        self._atoms = atoms[0]
        self._num_atoms = len(self._atoms)
        self._score = 25
        self._guesses = []
        self._entries_exits = []

    def get_atoms(self):
        """return the atom locations"""

        return self._atoms

    def atoms_left(self):
        """return the number of atoms left"""

        return self._num_atoms

    def set_num_atoms(self):
        """reduce the number of atoms left by one"""

        self._num_atoms -= 1

    def start_shoot_ray(self, row, col):
        """This method is to define the initial direction of the ray,
        return false in case in an invalid entry or return the direction the ray will
        be heading to"""

        if row == col or row + col == 9:  # condition to check for corners
            return False

        elif row != 0 and row != 9 and col != 0 and col != 9:  # condition to check for borders
            return False

        else:
            if row == 0:
                return "DOWN"
            elif row == 9:
                return "UP"
            elif col == 0:
                return "RIGHT"
            elif col == 9:
                return "LEFT"

    def deflection(self, row, col, direction):
        """Method to look for atoms by the side of the ray's path and change its direction
         return the new direction of the ray or return the current direction in case is not applicable"""

        if direction == "DOWN" and self._board[row+1][col+1] == "O":
            return "LEFT"
        elif direction == "DOWN" and self._board[row+1][col-1] == "O":
            return "RIGHT"

        elif direction == "UP" and self._board[row-1][col+1] == "O":
            return "LEFT"
        elif direction == "UP" and self._board[row-1][col-1] == "O":
            return "RIGHT"

        elif direction == "RIGHT" and self._board[row-1][col+1] == "O":
            return "DOWN"
        elif direction == "RIGHT" and self._board[row+1][col+1] == "O":
            return "UP"

        elif direction == "LEFT" and self._board[row+1][col-1] == "O":
            return "UP"
        elif direction == "LEFT" and self._board[row-1][col-1] == "O":
            return "DOWN"

        else:
            return direction

    def reflection(self, row, col, direction):
        """Method to look for reflections cases and return EXIT string to indicate that they main
        method finish to execute"""

        if direction == "DOWN" and self._board[row+1][col+1] == "O" \
                and self._board[row+1][col-1] == "O":
            return "EXIT"

        elif direction == "UP" and self._board[row-1][col+1] == "O" \
                and self._board[row-1][col-1] == "O":
            return "EXIT"

        elif direction == "RIGHT" and self._board[row-1][col+1] == "O" \
                and self._board[row+1][col+1] == "O":
            return "EXIT"

        elif direction == "LEFT" and self._board[row+1][col-1] == "O" \
                and self._board[row-1][col-1] == "O":
            return "EXIT"

        else:
            return direction

    def ray_move(self, row, col, direction, flag=0):
        """method that makes the ray "move" in the board uses methods reflection and deflection
        return as a tuple the exit of the ray or None in case is not applicable"""
        # base cases
        if self._board[row][col] == "O":  # conditional to look for a HIT
            return None
        # conditional to look for an exit, flag variable is to indicate the ray started moving
        if self._board[row][col] == "#" and flag >= 1:
            if flag == 1:  # if flag is 1 that means was not able to move into the board because a reflection
                return self._entries_exits[-1]
            else:
                return (row, col)  # return as tuple exit of the ray

        direction = self.reflection(row, col, direction)
        direction = self.deflection(row, col, direction)

        # recursive cases
        if direction == "DOWN":
            return self.ray_move(row + 1, col, direction, flag+1)
        elif direction == "UP":
            return self.ray_move(row - 1, col, direction, flag+1)
        elif direction == "RIGHT":
            return self.ray_move(row, col + 1, direction, flag+1)
        elif direction == "LEFT":
            return self.ray_move(row, col - 1, direction, flag+1)
        elif direction == "EXIT":
            return self._entries_exits[-1]

    def deduct_score(self, points):
        """method to deduct points"""

        self._score -= points

    def get_score(self):
        """return the player's score"""

        return self._score

    def shoot_ray(self, row, col, direction=None):
        """ main method to shoot the ray , use  helper methods ray_move and start_shoot_ray
        return None if the ray did not exit the board, or as a tuple the exit in the board"""

        if direction is None:
            direction = self.start_shoot_ray(row, col)
            if direction is False:
                return direction
            else:
                if (row, col) not in self._entries_exits:  # look for previous exits and entries
                    self._entries_exits.append((row, col))  # if the entry is not in memo we added
                    self.deduct_score(1)  # we deduct one point for not being in the list

        res = self.ray_move(row, col, direction)

        if res is not None and res not in self._entries_exits:  # if the ray got out and not in the list
            self._entries_exits.append(res)
            self.deduct_score(1)

        return res

    def guess_atom(self, row, col):
        """method to guess the location of an atom, parameter row and column respectively
        if the location was not previously guessed , five points are deducted"""

        if (row, col) in self.get_atoms():
            if (row, col) not in self._guesses:
                self.set_num_atoms()
                self._guesses.append((row, col))
            return True
        else:
            if (row, col) not in self._guesses:
                self.deduct_score(5)
                self._guesses.append((row, col))
            return False


def main():

    bb = BlackBoxGame([(5, 1), (5, 3), (8, 1)])

    bb.guess_atom(5, 6)
    bb.guess_atom(5, 1)
    bb.guess_atom(5, 1)

    score = bb.get_score()
    atoms = bb.atoms_left()

    print(score)
    print(atoms)


if __name__ == "__main__":
    main()
