# Board class
#
# ATTRIBUTES:
# 
# matrix
# playerToPlay
# lastMove
# colorPlayer1
# colorPlayer2
# empty
#
# METODS:
#
# is_full(self)
# who_is_playing(self)
# get_last_occupied_row_in_column(self, column)
# print(self)
# is_winning(self, last_move_column)
# actions_available(self)
# move
# reset
import numpy as np
import copy

class Board:
    def __init__(self, matrix, colorPlayer1 = 1, colorPlayer2 = -1, empty = 0, playerToPlay = None, lastMove = None):
        self.matrix = matrix
        self.colorPlayer1 = colorPlayer1
        self.colorPlayer2 = colorPlayer2
        self.empty = empty
        self.playerToPlay = self.who_is_playing()
        self.lastMove = None

    def is_full(self):
        # check whether the board is full
        import numpy as np
        if np.count_nonzero(self.matrix[0] == self.empty) == 0:
            return True
        else:
            return False

    def who_is_playing(self):
        # This method returns 1 if Player 1 has to move, and 2 if Player 2 has to move
        # however it shouldn't be need
        pl1_count = 0
        pl2_count = 0
        import numpy as np
        for row in range(np.shape(self.matrix)[0]):
            for column in range(np.shape(self.matrix)[1]):
                if self.matrix[row, column] == self.colorPlayer1:
                    pl1_count = pl1_count + 1
                if self.matrix[row, column] == self.colorPlayer2:
                    pl2_count = pl2_count + 1
        return pl1_count-pl2_count+1

    def get_last_occupied_row_in_column(self, column):
        # return last occupied row in a given column
        # !!Warning: it returns len(board) if the column is empty !!
        # !!Warning len(board) is out of bound!!
        row = len(self.matrix)
        while row > 0 and self.matrix[row - 1][column] != self.empty:
            row = row - 1
        return row

    def print(self):
        # print the board
        print(self.matrix)

    def is_winning(self):
        if self.lastMove is None:
            # if there is no last move, then the board is empty!
            return False
        else:
            # note this method expect that lastMove is a legal value 
            lastMoveRow = self.get_last_occupied_row_in_column(self.lastMove)
            cellValue = self.matrix[lastMoveRow][self.lastMove]
            # first we check if below the last move there are three gettoni of the same color
            # (we do it only if we are above the third row)
            if lastMoveRow < len(self.matrix) - 3:
                if self.matrix[lastMoveRow + 1][self.lastMove] == cellValue:
                    # if the sum of the following three values is tree then they are all of the same color
                    tmpSum = sum(self.matrix[lastMoveRow + 1:lastMoveRow + 4, self.lastMove])
                    if abs(tmpSum) == 3:
                        return True
            # second we check the positive diagonal
            counter = 0
            currentRow = lastMoveRow
            currentColumn = self.lastMove

            def next_cell_on_the_diagonal(matrix, currentRow, currentColumn, direction):
            # This is an auxiliary function that is used only in this method
                if direction == 1:
                    # check we are in the boundaries
                    if currentRow == 0 or currentColumn == len(matrix[0]) - 1:
                        # we return a value that in not in the matrix because we are outside the boundary
                        return 1.5, None, None
                    else:
                        return matrix[currentRow - 1][currentColumn + 1], currentRow - 1, currentColumn + 1
                elif direction == -1:
                    if currentRow == 0 or currentColumn == 0:
                        # we return a value that in not in the matrix because we are outside the boundary
                        return 1.5, None, None
                    else:
                        return matrix[currentRow - 1][currentColumn - 1], currentRow - 1, currentColumn - 1

            def prev_cell_on_the_diagonal(matrix, currentRow, currentColumn, direction):
                if direction == 1:
                    # check we are in the boundaries
                    if currentRow == len(matrix) - 1 or currentColumn == 0:
                         # we return a value that in not in the matrix because we are outside the boundary
                        return 1.5, None, None
                    else:
                        return matrix[currentRow + 1][currentColumn - 1], currentRow + 1, currentColumn - 1
                elif direction == -1:
                    if currentRow == len(matrix) - 1 or currentColumn == len(matrix[0]) - 1:
                        # we return a value that in not in the matrix because we are outside the boundary
                        return 1.5, None, None
                    else:
                        return matrix[currentRow + 1][currentColumn + 1], currentRow + 1, currentColumn + 1
                
            # checking the following items on the diagonal
            while next_cell_on_the_diagonal(self.matrix, currentRow, currentColumn, direction=1)[0] == cellValue:
                counter = counter + 1
                waste, currentRow, currentColumn = next_cell_on_the_diagonal(self.matrix, currentRow, currentColumn, direction=1)
            # checking the preceding items on the diagonal
            currentRow = lastMoveRow
            currentColumn = self.lastMove
            while prev_cell_on_the_diagonal(self.matrix, currentRow, currentColumn, direction=1)[0] == cellValue:
                counter = counter + 1
                waste, currentRow, currentColumn = prev_cell_on_the_diagonal(self.matrix, currentRow, currentColumn, direction=1)
            if counter >= 3:
                return True
            # third we check the negative diagonal
            counter = 0
            currentRow = lastMoveRow
            currentColumn = self.lastMove
            # checking the following items on the diagonal
            while next_cell_on_the_diagonal(self.matrix, currentRow, currentColumn, direction=-1)[0] == cellValue:
                counter = counter + 1
                waste, currentRow, currentColumn = next_cell_on_the_diagonal(self.matrix, currentRow, currentColumn, direction=-1)
            # checking the preceding items on the diagonal
            currentRow = lastMoveRow
            currentColumn = self.lastMove
            while prev_cell_on_the_diagonal(self.matrix, currentRow, currentColumn, direction=-1)[0] == cellValue:
                counter = counter + 1
                waste, currentRow, currentColumn = prev_cell_on_the_diagonal(self.matrix, currentRow, currentColumn, direction=-1)
            if counter >= 3:
                return True
            # fourth we check on the same row
            counter = 0
            currentColumn = self.lastMove - 1
            # check on the left
            while currentColumn >= 0:
                if self.matrix[lastMoveRow][currentColumn] == cellValue:
                    currentColumn = currentColumn - 1
                    counter = counter + 1
                else:
                    break
            # check on the right
            currentColumn = self.lastMove + 1
            while currentColumn < len(self.matrix[0]):
                if self.matrix[lastMoveRow][currentColumn] == cellValue:
                    currentColumn = currentColumn + 1
                    counter = counter + 1
                else:
                    break
            if counter >= 3:
                return True
            return False

    def actions_available(self):
        # returns the available actions
        actions_available = []
        for column in range(len(self.matrix[0])):
            row = self.get_last_occupied_row_in_column(column)
            if row > 0:
                actions_available.append(column)
        return actions_available

    def move(self, column):
        # This metod takes as argument only a column and makes that move.
        if (self.is_full() == False) and (column in self.actions_available()):
            row = self.get_last_occupied_row_in_column(column)
            if self.playerToPlay == 1:
                self.matrix[row -1, column] = self.colorPlayer1
            else:
                self.matrix[row -1, column] = self.colorPlayer2
            # update the lastMove attribute
            self.lastMove = column
            # update the playerToPlay attribute
            self.playerToPlay = 3 - self.playerToPlay
       

    def reset(self, agent, environment):
        # this little function resets the board. The arguments agent and
        # environment are assumed to be instances of the class AI.
        # If agent is player 1 it returns an empty
        (nRows, nColumns) = self.matrix.shape
        self.matrix = np.zeros([nRows, nColumns]).astype(int)
        for row in range(nRows):
            for column in range(nColumns):
                self.matrix[row, column] = self.empty
        self.playerToPlay = 1
        self.lastMove = None
        # if the agent is the second player, then we let the 
        # environment play one move
        if agent.whichPlayer == 2:
           environment.action(self)

# FUNCTIONS

def empty_board(nRows, nColumns):
    matrix = np.zeros([nRows, nColumns]).astype(int)
    return Board(matrix)



