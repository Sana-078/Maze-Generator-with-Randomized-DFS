import pygame
import math
import random
from collections import deque
import time

WIDTH=25
TOTAL_WIDTH=650
ROW=TOTAL_WIDTH//(WIDTH+1)
COL=TOTAL_WIDTH//(WIDTH+1)

'''If you wanna play around with the cell size, always remember it is something wholly divisible by
the total width, for eg: I can give my cell a size of 13, which would give 50x50 grid but i want it be a 
little bigger so i gave 26, which leaves me with a 25x25 grid. you can always playaround with this value,
but keep in mind to give the WIDTH variable above the value of the size of the cell you want -1.
My width here is 26, but i gave 25 because in the grid_make function, the 1 is already added as spacing. '''

pygame.init()
surface=pygame.display.set_mode((650, 650))
pygame.display.set_caption('Maze Runner')
done = False

#colors
BLACK = (0, 0, 0)
WHITE=(255,255,255)
#start and end self
red=(222, 49, 99)
purple=(106, 15, 142)
#other selfs
light_blue=(49, 172, 222)
light_orange=(255, 154, 118)
dark_blue=(51, 54, 255 )
light_green=(17, 122, 101 )

#other variables
y0=0
x1=20
y1=20
x0=0
y=0
n=20


#Spot class 
class Spot:
    def __init__(self, x, y, col, row, width):
        self.x=x
        self.y=y
        self.col=col
        self.row=row
        self.color = WHITE
        self.visited=False
        self.walls=[True,True,True,True]
        self.visit=False
        self.line_color=WHITE
        
        
    def draw(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, WIDTH, WIDTH))
        
    def draw_lines(self):

        if self.walls[0]:
            pygame.draw.line(surface, BLACK, (self.x, self.y), (self.x+ WIDTH ,self.y), 1)#top
        if self.walls[1]:
            pygame.draw.line(surface, BLACK, (self.x, self.y), (self.x, self.y+ WIDTH ), 1)#left
        if self.walls[2]:
            pygame.draw.line(surface, BLACK, (self.x, self.y+ WIDTH), (self.x+ WIDTH ,self.y+WIDTH), 1)#bottom
        if self.walls[3]:
            pygame.draw.line(surface, BLACK, (self.x+ WIDTH ,self.y), (self.x+ WIDTH , self.y+WIDTH), 1)#right

        #if self.visited==True:
        #    self.visited_cell()
    def fill_color(self):
        '''this is done for filling the gap between the rectangle which is white (background color, line 160)
        with whatever color it is acquiring, else each cell will have white borders around them which looks messy.'''
        if not self.walls[0]:
            pygame.draw.line(surface, self.line_color, (self.x, self.y), (self.x+ WIDTH ,self.y), 1)#top
        if not self.walls[1]:
            pygame.draw.line(surface, self.line_color, (self.x, self.y), (self.x, self.y+ WIDTH ), 1)#left
        if not self.walls[2]:
            pygame.draw.line(surface, self.line_color, (self.x, self.y+ WIDTH), (self.x+ WIDTH ,self.y+WIDTH), 1)#bottom
        if not self.walls[3]:
            pygame.draw.line(surface, self.line_color, (self.x+ WIDTH ,self.y), (self.x+ WIDTH , self.y+WIDTH), 1)#right
        
    def make_start(self):
        self.color=red

    def make_end(self):
        self.color=purple

    def path(self):
        self.color=light_green
        
    def visited_cell(self):
        self.color=dark_blue

    def make_way(self):
        self.color=light_orange

    def edge_color(self):
        self.color=light_blue

    def reset(self):
        self.color=WHITE

    def check_neighbours(self, grid):
        neighbours=[]
        rowNum=[-1, 0, 1, 0]
        colNum=[0 ,-1 , 0 ,1]

        for i in range(4):
            row=self.row+ rowNum[i]
            col=self.col+ colNum[i]

            if(isValid(row, col) and grid[row][col].visited!=True):
                neighbours.append(grid[row][col])

        if (len(neighbours)>0):
            rand=random.randint(0, len(neighbours)-1)
            
            return neighbours[rand]
        else:
            return False
               

def isValid(row, col):    
    return (row>=0) and (row<=ROW-1) and (col>=0) and (col<=ROW-1)


def grid_make(width):
    w=width+1
    row= math.trunc(TOTAL_WIDTH/w)
    grid=[]
    y0=0
    n=width
    for j in range(1 ,row+1):
        gap=width
        x0=0
        grid.append([])
        for i in range(1, row+1):
            spot=Spot(x0, y0,math.trunc(x0/w),math.trunc(y0/w), width)
            x0=gap+i
            gap=gap+width
            grid[j-1].append(spot)
        y0=n+j
        n=n+width
    return grid

def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw()
            spot.fill_color()
            spot.draw_lines()
            
            
                
    pygame.display.flip()
    

def removeWalls(node1, node2):
    '''Heres how this function works:
    1: It takes the parameters given, current node is the node1 and neighbour node is node2
    2: lets assume current node is grid[0][0] and neighbour node is grid[1][0]
    3: col_diff is the difference between the columns, and row_diff is the difference between the rows
       this is done to know which side of the current cell is this particular neighbour cell situated, 
       and there are total six cases:
       (note: Remember that in pygame the 0,0 coordinate is at the top left and 
       everything to the right and down increases)
       if row_diff =  1: then the neighbour cell is up
       if row_diff = -1: then the neighbour cell is down
       if row_diff =  0: then the neighbour cell is in the same row, different column
       if col_diff =  1: then the neighbour cell is left
       if col_diff = -1: then the neighbour cell is right
       if col_diff =  0: then the neighbour cell is in the same column, different row
    4: After getting the direction it starts to remove the wall accordingly
       (the walls are in the order: 0-top, 1-left, 2-down, 3-right)
       for eg: if the neighbour cell is above say we get -1 for row_diff:
           then the walls to remove are the top of the current cell and bottom of neighbour cell    
     '''
    
    col_diff=node1.col-node2.col
    row_diff=node1.row-node2.row
    
    if row_diff == -1:
        node1.walls[2]=False
        node2.walls[0]=False
    if row_diff == 1:
        node1.walls[0]=False
        node2.walls[2]=False
    if col_diff == -1:
        node1.walls[3]=False
        node2.walls[1]=False
    if col_diff == 1:
        node1.walls[1]=False
        node2.walls[3]=False
    

    
def dfs_maze_build(grid, draw):
    
    unvisited=[[True for i in range(len(grid[0]))] for j in range(len(grid))]
    current_cell=grid[0][0]
    #visited[current_cell.row][current_cell.col]=True
    current_cell.visited=True
    unvisited[current_cell.row][current_cell.col]=False

    stack=[]
    while any (unvisited):
        
    #    current_cell.draw()
    #    current_cell.visited_cell()
        neighbour=current_cell.check_neighbours(grid)
        
        if neighbour:
            #print("order3" , neighbour.row , neighbour.col)
            neighbour.edge_color()
            neighbour.visited=True
            unvisited[neighbour.row][neighbour.col]=False
            stack.append(current_cell)
            
            removeWalls(current_cell, neighbour)
            
            current_cell=neighbour

            #time.sleep(0.05)
            draw()
            neighbour.reset()

        elif stack:
            current_cell=stack.pop()

        else:
            grid[0][0].make_start()
            grid[ROW-1][ROW-1].make_end()
            return True
            break


    
def move(grid, current, direction):
    start= grid[0][0]

    if direction=="up":
        if isValid(current.row-1, current.col):
            cell=grid[current.row-1][current.col]
            if current.walls[0]==False:
                if current!=start:
                    current.line_color=light_orange
                    current.make_way()
                cell.edge_color()
                return cell
            else:
                return False
        return False
    if direction=="left":
        if isValid(current.row, current.col-1):
            cell=grid[current.row][current.col-1]
            if current.walls[1]==False:
                if current!=start:
                    current.line_color=light_orange
                    current.make_way()
                cell.edge_color()
                return cell
            else:
                return False
        return False
    if direction=="down":
        if isValid(current.row+1, current.col):
            cell=grid[current.row+1][current.col]
            if current.walls[2]==False:
                if current!=start:
                    current.line_color=light_orange
                    current.make_way()
                cell.edge_color()
                return cell
            else:
                return False
        return False
    if direction=="right":
        if isValid(current.row, current.col+1):
            cell=grid[current.row][current.col+1]
            if current.walls[3]==False:
                if current!=start:
                    current.line_color=light_orange
                    current.make_way()
                cell.edge_color()
                return cell
            else:
                return False
        return False

    pass
def color_walls(node):
    node.line_color=light_green
    node.path()


def construct_path(curr_self, from_list, start):
    r=curr_self
    for i in range(len(from_list)-1):
        t=from_list[r]
        if t==start:
            break
        else:
            color_walls(t)
            r=t
            
def dfs_solve(grid, draw):
    stack=[]
    start=grid[0][0]
    end=grid[ROW-1][ROW-1]

    visited=[[False for i in range(len(grid[0]))] for j in range(len(grid))]

    parent={}

    rowNum=[-1, 0, 1, 0]
    colNum=[0 ,-1 , 0 ,1]

    stack.append(start)
    l=len(stack)
    print(l, stack)
    visited[start.row][start.col]=True

    while l>0:
        node=stack.pop()

        if node==end:
            construct_path(node, parent, start)
            break
        
        if node!=start:
            node.line_color=light_blue
            node.edge_color()
                
        for i in range(4):
            row=node.row+ rowNum[i]
            col=node.col+ colNum[i]
            #print(self.walls[i])
            if node.walls[i]==False:
                if (isValid(row, col) and visited[row][col]!=True ):
                    cell=grid[row][col]
                    parent[cell]=node
                    stack.append(cell)
                    visited[row][col]=True
                    
                time.sleep(0.003)
                draw()
    return False

def bfs_solve(grid, draw):
    queue=deque()

    start=grid[0][0]
    end=grid[ROW-1][ROW-1]


    visited=[[False for i in range(len(grid[0]))] for j in range(len(grid))]

    parent={}

    rowNum=[-1,  0,  1, 0]
    colNum=[ 0 ,-1 , 0 ,1]

    queue.append(start)
    visited[start.row][start.col]=True

    while len(queue)>0:
        
        node=queue.popleft()

        if node==end:
            construct_path(node, parent, start)
            break
        
        if node!=start:
            node.line_color=light_blue
            node.edge_color()
                
        for i in range(4):
            row=node.row+ rowNum[i]
            col=node.col+ colNum[i]
            #print(self.walls[i])
            if node.walls[i]==False:
                if (isValid(row, col) and visited[row][col]!=True ):
                    cell=grid[row][col]
                    parent[cell]=node
                    queue.append(cell)
                    visited[row][col]=True
                    
                time.sleep(0.003)
                draw()
    return False
    

def reset(grid, draw):
    for row in grid:
        for col in row:
            if  col.color==light_blue or col.color==light_orange or col.color==light_green:
                col.line_color=WHITE
                col.color=WHITE
                
    draw()



def main():
    run = True

    global WIDTH
    global ROW
    global color
    

    grid=grid_make(WIDTH)
    print(len(grid[0]))
    current=grid[0][0]

    maze_finish=False

    while run:
        draw(surface,grid)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    maze_finish=dfs_maze_build(grid, lambda: draw(surface, grid))

            if event.type == pygame.KEYDOWN:

                if event.key==pygame.K_UP and maze_finish:                
                    direction="up"
                    curr=move(grid,  current, direction)
                    if curr!=False:
                        current=curr
                if event.key==pygame.K_LEFT and maze_finish:
                    direction="left"
                    curr=move(grid, current, direction)
                    if curr!=False:
                        current=curr
                if event.key==pygame.K_DOWN and maze_finish:
                    direction="down"
                    curr=move(grid,  current, direction)
                    if curr!=False:
                        current=curr
                if event.key==pygame.K_RIGHT and maze_finish:
                    direction="right"
                    curr=move(grid, current, direction)
                    if curr!=False:
                        current=curr
                    

                if event.key==pygame.K_LCTRL and maze_finish:
                    dfs_solve(grid,  lambda: draw(surface, grid) )

                if event.key==pygame.K_RCTRL and maze_finish:
                    bfs_solve(grid,  lambda: draw(surface, grid) )

                if event.key==pygame.K_c and maze_finish:
                    reset(grid, lambda: draw(surface, grid) )

                # hard and easy version 
                if event.key==pygame.K_h:
                    WIDTH=12
                    ROW=50
                    grid=grid_make(WIDTH)
                    current=grid[0][0]

                if event.key==pygame.K_e:
                    WIDTH=25
                    ROW=25
                    grid=grid_make(WIDTH)
                    current=grid[0][0]
                    
            
    pygame.quit()


if __name__=="__main__":
    main()
