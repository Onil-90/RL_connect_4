# Board class
#
# Available methods so far:
#
# is_full(self)
# get_last_occupied_row_in_column(self, column)
# print(self)
# is_winning(self, last_move_column)
# 

class Board:
    def __init__(self, matrix, colorPlayer1 = 1, colorPlayer2 = -1, empty = 0):
        self.matrix = matrix
        self.colorPlayer1 = colorPlayer2
        self.colorPlayer2 = colorPlayer2
        self.empty = empty

    def is_full(self):
        # check whether the board is full
        import numpy as np
        if np.count_nonzero(self.matrix[0] == self.empty) == 0:
            return True
        else:
            return False

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

    def is_winning(self, last_move_column):
        # note this function expect that last_move_column is a legal value 
        last_move_row = self.get_last_occupied_row_in_column(last_move_column)
        cell_value = self.matrix[last_move_row][last_move_column]
        # first we check if below the last move there are three gettoni of the same color
        # (we do it only if we are above the third row)
        if last_move_row < len(self.matrix) - 3:
            if self.matrix[last_move_row + 1][last_move_column] == cell_value:
                # if the sum of the following three values is tree then they are all of the same color
                tmp_sum = sum(self.matrix[last_move_row + 1:last_move_row + 4, last_move_column])
                if abs(tmp_sum) == 3:
                    return True
        # second we check the positive diagonal
        counter = 0
        current_row = last_move_row
        current_column = last_move_column


        def next_cell_on_the_diagonal(matrix, current_row, current_column, direction):
        # This is an auxiliary function that is used only in this method
            if direction == 1:
                # check we are in the boundaries
                if current_row == 0 or current_column == len(matrix[0]) - 1:
                    # we return a value that in not in the matrix because we are outside the boundary
                    return 1.5, None, None
                else:
                    return matrix[current_row - 1][current_column + 1], current_row - 1, current_column + 1
            elif direction == -1:
                if current_row == 0 or current_column == 0:
                    # we return a value that in not in the matrix because we are outside the boundary
                    return 1.5, None, None
                else:
                    return matrix[current_row - 1][current_column - 1], current_row - 1, current_column - 1

        def prev_cell_on_the_diagonal(matrix, current_row, current_column, direction):
            if direction == 1:
               # check we are in the boundaries
                if current_row == len(matrix) - 1 or current_column == 0:
                    # we return a value that in not in the matrix because we are outside the boundary
                    return 1.5, None, None
                else:
                    return matrix[current_row + 1][current_column - 1], current_row + 1, current_column - 1
            elif direction == -1:
                if current_row == len(matrix) - 1 or current_column == len(matrix[0]) - 1:
                    # we return a value that in not in the matrix because we are outside the boundary
                    return 1.5, None, None
                else:
                    return matrix[current_row + 1][current_column + 1], current_row + 1, current_column + 1
                
        # checking the following items on the diagonal
        while next_cell_on_the_diagonal(self.matrix, current_row, current_column, direction=1)[0] == cell_value:
            counter = counter + 1
            waste, current_row, current_column = next_cell_on_the_diagonal(self.matrix, current_row, current_column, direction=1)
        # checking the preceding items on the diagonal
        current_row = last_move_row
        current_column = last_move_column
        while prev_cell_on_the_diagonal(self.matrix, current_row, current_column, direction=1)[0] == cell_value:
            counter = counter + 1
            waste, current_row, current_column = prev_cell_on_the_diagonal(self.matrix, current_row, current_column, direction=1)
        if counter >= 3:
            return True
        # third we check the negative diagonal
        counter = 0
        current_row = last_move_row
        current_column = last_move_column
        # checking the following items on the diagonal
        while next_cell_on_the_diagonal(self.matrix, current_row, current_column, direction=-1)[0] == cell_value:
            counter = counter + 1
            waste, current_row, current_column = next_cell_on_the_diagonal(self.matrix, current_row, current_column, direction=-1)
        # checking the preceding items on the diagonal
        current_row = last_move_row
        current_column = last_move_column
        while prev_cell_on_the_diagonal(self.matrix, current_row, current_column, direction=-1)[0] == cell_value:
            counter = counter + 1
            waste, current_row, current_column = prev_cell_on_the_diagonal(self.matrix, current_row, current_column, direction=-1)
        if counter >= 3:
            return True
        # fourth we check on the same row
        counter = 0
        current_column = last_move_column - 1
        # check on the left
        while current_column >= 0:
            if self.matrix[last_move_row][current_column] == cell_value:
                current_column = current_column - 1
                counter = counter + 1
            else:
                break
        # check on the right
        current_column = last_move_column + 1
        while current_column < len(self.matrix[0]):
            if self.matrix[last_move_row][current_column] == cell_value:
                current_column = current_column + 1
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
