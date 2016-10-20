input='''15 15
###############
#S        #   #
### ### ### # #
#   #   #   # #
# ##### ##### #
#     #   #   #
# ### # ### ###
# #   # #   # #
# # ### # ### #
# # # # # #   #
### # # # # # #
#   #   # # # #
# ####### # # #
#           #E#
###############'''

translate_dict={'#':'#',' ':' ','S':' ','E':' '}

class Maze(object):
    def __init__(self, width, height, grid):
        self.height = height
        self.width  = width
        for num, row in enumerate(grid):
            try:
                self.start =(num,row.index('S'))
            except ValueError:
                pass
            try:
                self.end =(num,row.index('E'))
            except ValueError:
                pass
        self.grid = [[translate_dict[i] for i in row] for row in grid]
            

def parse_maze(input):
    size,*grid = input.split('\n')
    width, height = map(int,size.split(' '))
    return Maze(width, height, grid)

def process_maze(maze, current_path, completed_paths):
    if not current_path:
        current_path.append(maze.start)
    
    possible_moves = {tuple(map(sum,zip(current_path[-1],move))) for move in [(-1,0),(1,0),(0,-1),(0,1)]}
    possible_moves = possible_moves - set(current_path)

    for x,y in possible_moves:
        if maze.end == (x,y):
            return current_path+[(x,y)]
        if maze.grid[y][x] == ' ':
            return process_maze(maze,current_path+[(x,y)],completed_paths)
    

if __name__ == '__main__':
    test = parse_maze(input)
    path = process_maze(test,[],[])
    for x,y in path:
        test.grid[y][x]='*'
