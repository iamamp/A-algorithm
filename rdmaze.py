import math
#Parent updating
#when at goal, print path and break
#Constraints
class Die:
    def __init__(self,top,bottom,right,left,north,south):
        self.top,self.bottom,self.right,self.left,self.north,self.south=top,bottom,right,left,north,south
    def __eq__(self, other):
        if self.top==other.top and self.bottom==other.bottom and self.right==other.right and self.left==other.left and self.north==other.north and \
                        self.south == other.south:
            return True
        else:
            return False
class Node:
    def __init__(self,x,y,parent_x,parent_y,die,distFromStart,directionMoved):
        self.x,self.y,self.parent_x,self.parent_y,self.die,self.distFromStart,self.directionMoved\
            = x,y,parent_x,parent_y,die,distFromStart,directionMoved
    def __eq__(self, other):
        if self.x==other.x and self.y==other.y and self.die.__eq__(other.die):
            return True
        else:
            return False
    def printNode(self):
        print(self.x,self.y,self.parent_x,self.parent_y,self.die)
class Maze:
    def __init__(self,name):
        self.name=name
        self.words=[]
        self.cut=0
        self.dieTop = 1
    def createMaze(self):
        with open(self.name, "r") as f:
            data = f.read()
        for lines in data:
            self.words.append(lines.split())
        for i in self.words:
            if i == []:
                self.cut += 1
        # print(cut)
        k = 0
        self.words = [x for x in self.words if x != []]
        print(self.words)
        # Inserting values into matrix
        self.maze = [[0 for x in range(int((len(self.words)) / (self.cut + 1)))] for y in range(self.cut + 1)]
        for i in range(self.cut + 1):
            for j in range(int((len(self.words)) / (self.cut + 1))):
                if self.words[k] != []:
                    # To remove list of list
                    self.maze[i][j] = self.words[k].pop()
                    if self.maze[i][j] == 'G':
                        self.goal_x = i
                        self.goal_y = j
                    if self.maze[i][j] == 'S':
                        self.start_x=i
                        self.start_y=j
                else:
                    j = j - 1
                k += 1
        self.createEuclidean()
        self.createManhattan()
    def createEuclidean(self):
        self.euclidean = [[0 for x in range(int((len(self.words)) / (self.cut + 1)))] for y in range(self.cut + 1)]
        for i in range(self.cut + 1):
            for j in range(int((len(self.words)) / (self.cut + 1))):
                self.euclidean[i][j]=math.sqrt((self.goal_x - i)**2+(self.goal_y - j)**2)
    def createManhattan(self):
        self.manhattan=[[0 for x in range(int((len(self.words)) / (self.cut + 1)))] for y in range(self.cut + 1)]
        for i in range(self.cut + 1):
            for j in range(int((len(self.words)) / (self.cut + 1))):
                self.manhattan[i][j]=abs(self.goal_x-i)+abs(self.goal_y-j)
    def findPath(self):
        found=False
        self.nodes=[]
        self.visited=[]
        self.parentsOfEveryNode=[[[] for x in range(int((len(self.words)) / (self.cut + 1)))] for y in range(self.cut + 1)]
        self.nodes.append(Node(self.start_x,self.start_y,-1,-1,Die(1,6,3,4,2,5),0,"None"))
        while(len(self.nodes)>0):
            currentNode = self.findMin()
            self.nodes.remove(currentNode)
            self.visited.append(currentNode)
            breadth = (int((len(self.words)) / (self.cut + 1)))
            if currentNode.x==self.goal_x and currentNode.y==self.goal_y and currentNode.die.top==1:
                print("Goal Reached")
#                self.fillVisited()
                self.printPath()
                # for node in self.visited:
                #     print(node.x,node.y)
                found=True
                break
            if (0<=currentNode.x+1<=self.cut) and self.maze[currentNode.x+1][currentNode.y]!='*'\
                    and\
                    self.checkIfVisited(Node(currentNode.x+1,currentNode.y,currentNode.x,currentNode.y,
                                             trackDice(currentNode.die,"south"),currentNode.distFromStart,"south"))\
                    and trackDice(currentNode.die,"south").top!=6:
                self.nodes.append(Node(currentNode.x+1,currentNode.y,currentNode.x,currentNode.y,trackDice(currentNode.die,"south"),currentNode.distFromStart+1,"south"))
                self.parentsOfEveryNode[currentNode.x+1][currentNode.y]=(currentNode.x,currentNode.y)
            if (0 <= currentNode.x - 1 <= self.cut) and self.maze[currentNode.x - 1][currentNode.y] != '*' \
                    and \
                    self.checkIfVisited(Node(currentNode.x - 1, currentNode.y, currentNode.x, currentNode.y,
                                             trackDice(currentNode.die, "north"), currentNode.distFromStart,"north")) \
                    and trackDice(currentNode.die, "north").top != 6:
                self.nodes.append(Node(currentNode.x-1,currentNode.y,currentNode.x,currentNode.y,trackDice(currentNode.die,"north"),currentNode.distFromStart+1,"north"))
                self.parentsOfEveryNode[currentNode.x - 1][currentNode.y]=(currentNode.x, currentNode.y)

            if (0 <= currentNode.y+1 < breadth) and self.maze[currentNode.x][currentNode.y+1] != '*' \
                    and \
                    self.checkIfVisited(Node(currentNode.x, currentNode.y+1, currentNode.x, currentNode.y,
                                             trackDice(currentNode.die, "right"), currentNode.distFromStart,"right")) \
                    and trackDice(currentNode.die, "right").top != 6:
                self.nodes.append(Node(currentNode.x,currentNode.y+1,currentNode.x,currentNode.y,trackDice(currentNode.die,"right"),currentNode.distFromStart+1,"right"))
                self.parentsOfEveryNode[currentNode.x][currentNode.y+1]=(currentNode.x, currentNode.y)
            if (0 <= currentNode.y-1 < breadth) and self.maze[currentNode.x][currentNode.y-1] != '*' \
                    and \
                    self.checkIfVisited(Node(currentNode.x, currentNode.y-1, currentNode.x, currentNode.y,
                                             trackDice(currentNode.die, "left"), currentNode.distFromStart,"left")) \
                    and trackDice(currentNode.die, "left").top != 6:
                self.nodes.append(Node(currentNode.x,currentNode.y-1,currentNode.x,currentNode.y,trackDice(currentNode.die,"left"),currentNode.distFromStart+1,"left"))
                self.parentsOfEveryNode[currentNode.x][currentNode.y-1]=(currentNode.x, currentNode.y)
        if not found:
            print("Path not found")
    def checkIfVisited(self,other):
        for node in self.visited:
            if(node.__eq__(other)):
                return False
        return True

    def findMin(self):
        minimum=math.inf
        minNode=None
        for node in self.nodes:
            if(self.dist(node)<minimum):
                minimum=self.dist(node)
                minNode=node
        print("x:",minNode.x)
        print("y:", minNode.y)
        print("Parent x:",minNode.parent_x)
        print("Parent y:", minNode.parent_y)
        print("dieTop:", minNode.die.top)
        print("dieBottom:", minNode.die.bottom)
        print("dieRight:", minNode.die.right)
        print("dieLeft:", minNode.die.left)
        print("dieNorth:", minNode.die.north)
        print("dieSouth:", minNode.die.south)
        print("Movement",minNode.directionMoved)
        print("\n")
        return minNode


    def printPath(self):
        c=0
        cc = len(self.nodes)
        currentNode=None
        #setgoal
        for node in self.visited:
            if node.x==self.goal_x and node.y==self.goal_y and node.die.top==1:
                currentNode=node
                break

        while not(currentNode.parent_x==-1 and currentNode.parent_y==-1 and currentNode.die.top == 1):
            for node in self.visited:
                if node.x==currentNode.parent_x and node.y==currentNode.parent_y and trackDice(node.die,currentNode.directionMoved).__eq__(currentNode.die):
                    print(node.x,node.y)
                    currentNode=node
                    break
            c+=1
        print('count of nodes visited : ',c)
        print('count of nodes generated : ', cc)

    def dist(self,node):
        #uncomment to choose heuristic of your choice
        return node.distFromStart + ((self.manhattan[node.x][node.y] + self.euclidean[node.x][node.y])/2)
        #return node.distFromStart + self.manhattan[node.x][node.y]
        #return node.distFromStart + self.euclidean[node.x][node.y]

def trackDice(dieTop,direction):
    if direction=='right':
        return Die(dieTop.left,dieTop.right,dieTop.top,dieTop.bottom,dieTop.north,dieTop.south)
    if direction=='left':
        return Die(dieTop.right,dieTop.left,dieTop.bottom,dieTop.top,dieTop.north,dieTop.south)
    if direction=='north':
        return Die(dieTop.south,dieTop.north,dieTop.right,dieTop.left,dieTop.top,dieTop.bottom)
    if direction=='south':
        return Die(dieTop.north,dieTop.south,dieTop.right,dieTop.left,dieTop.bottom,dieTop.top)
def main():
    #name=input("Enter puzzle name \n")
    maze = Maze("p2.txt")
    maze.createMaze()
    #print(maze.maze)
    maze.findPath()
if __name__ == '__main__':
    main()

'''
euclidean | manhattan | mean of euclidean + manhattan
(nodes visited,nodes discovered) 
p1 6,7 | 6,7 | 6,7
p2 path not found
p3 12,13 | 12,13 | 12,13
p4 21,23 | 21,25 | 21,25
p5 444, 26 | 1153,26 | 489,26
'''