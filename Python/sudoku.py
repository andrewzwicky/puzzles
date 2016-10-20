from pprint import pprint as print
from operator import add
from collections import Counter

easy_puzzle='''000800004
940670020
000250810
604090251
000000000
219060407
086045000
050087096
700006000'''    

med_puzzle='''560000008
400608020
000020036
000005071
050807060
180300000
820040000
040109002
300000047'''    

def sudoku_solver(text_puzzle):
    puzzle = text_to_num(text_puzzle)
    options_grid = [[calculate_options(puzzle,row,col) for col in range(9)] for row in range(9)]

unsolved_squares = []
for row in range(9):
    for col in range(9):
        if options_grid[row][col] != set():
            unsolved_squares.append((row,col))

    print(len(unsolved_squares))
    
    while len(unsolved_squares) > 0:
        for row,col in unsolved_squares[::]:
            if len(options_grid[row][col]) == 1:
                number = options_grid[row][col].pop()
                puzzle[row][col] = number
                
                puzzle, options_grid, unsolved_squares = set_square(puzzle, options_grid, unsolved_squares, row, col, number)

        check_rows, check_cols = [list(set(i)) for i in zip(*unsolved_squares[::])]

        for row in check_rows:
            for number, count in reduce(add, map(Counter,get_row(options_grid,row))):
                if count == 1:
                    for item, col in enumerate(get_row(options_grid,row)):
                        if number in item:
                            puzzle, options_grid, unsolved_squares = set_square(puzzle, options_grid, unsolved_squares, row, col, number)

        for col in check_cols:
            for number, count in reduce(add, map(Counter,get_col(options_grid,col))):
                if count == 1:
                    for item, row in enumerate(get_col(options_grid,col)):
                        if number in item:
                            puzzle, options_grid, unsolved_squares = set_square(puzzle, options_grid, unsolved_squares, row, col, number)
        
        
    print(len(unsolved_squares))
    print(puzzle)

def set_square(puzzle, options_grid, unsolved_squares, row, col, number)
    puzzle[row][col] = number
    options_grid = set_row(options_grid, row, [i-{number} for i in get_row(options_grid, row)])
    options_grid = set_col(options_grid, col, [i-{number} for i in get_col(options_grid, col)])
    options_grid = set_cell(options_grid,row, col , [i-{number} for i in get_cell(options_grid, row, col)])
    unsolved_squares.remove((row,col))

    return puzzle, options_grid, unsolved_squares

def text_to_num(text_puzzle):
    rows = [[int(i) for i in row] for row in text_puzzle.split('\n')]
    return rows

def calculate_options(num_puzzle,row,col):
    if num_puzzle[row][col] == 0:
        all_nums = set(range(1,10))
        
        row_out = set(get_row(num_puzzle,row))
        col_out = set(get_col(num_puzzle,col))
        cell_out = set(get_cell(num_puzzle,row,col))

        options = all_nums - row_out - col_out - cell_out - {0}
    else:
        options = set()

    return options

def get_row(num_puzzle,row):
    return num_puzzle[row]

def get_col(num_puzzle, col):
    return list(list(zip(*num_puzzle))[col])

def get_cell(num_puzzle,row,col):
    cell_row = row//3
    cell_col = col//3

    cell = []
    for i in range(3*cell_row,3*cell_row+3):
        for j in range(3*cell_col,3*cell_col+3):
            cell.append(num_puzzle[i][j])

    return cell  

def set_row(num_puzzle, row, new_row):
    num_puzzle[row] = new_row

    return num_puzzle

def set_col(num_puzzle, col, new_col):
    num_puzzle = [list(i) for i in zip(*num_puzzle)]

    num_puzzle[col] = new_col

    return [list(i) for i in zip(*num_puzzle)]

def set_cell(num_puzzle, row, col, new_cell):
    cell_row = row//3
    cell_col = col//3

    new_cell_iter = iter(new_cell)

    for i in range(3*cell_row,3*cell_row+3):
        for j in range(3*cell_col,3*cell_col+3):
            num_puzzle[i][j] = next(new_cell_iter)
    
    return num_puzzle

if __name__=='__main__':
    sudoku_solver(easy_puzzle)
