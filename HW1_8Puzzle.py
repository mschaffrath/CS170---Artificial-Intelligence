#
#  CS170 - Artifical Intelligence
#  8 - Puzzle Solver
#  Author: Mathew Schaffrath
#

# Importing modules
# copy - used in expansion to duplicate nodes prior to modifying them with operations
# operator - used to sort by attribute in node
import copy
import operator

# Node class to store STATE of puzzle and COSTS
# Includes getter and setter methods to access memebers
# MTH - Missing Tile Heuristic
# MDH - Manhattan Distance Heuristic
class Node(object):
  def __init__(self,state):
    self.state = state
  parent = None
  depth = 0
  gn = 0
  hn = 0
  MTH = 0
  MDH = 0
  def SetParent(self, parent):
    self.parent = parent
  def GetDepth(self):
    return self.depth
  def SetDepth(self, cost):
    self.depth = cost
  def SetGn(self, cost):
    self.gn = cost
  def SetHn(self, cost):
    self.hn = cost
  def SetTotalMDH(self):
    self.MDH = self.depth + self.hn
  def SetTotalMTH(self):
    self.MTH = self.depth + self.gn
  def GetData(self):
    return(self.parent, self.depth, self.gn, self.hn)

# Global variables for counting 
expandCount = 0
queueSize = 0
goalDepth = 0
prevQMax = 0
repeat = 0

# Hardcoded initial and goal states
defaultInitState = [['8','7','1'],
                    ['6','b','2'],
                    ['5','4','3']]
goalState = [['1','2','3'],
             ['4','5','6'],
             ['7','8','b']]

# Set used to check for repeated States
repeatCheck = set()

# Prints a state in human readable format
def PrintFormattedState(state):
  for i in range(len(state)):
      print(state[i])
  print("")

# Helper function to make a node instance
def MakeNode(initState):
  return Node(initState) 

# Converts a state in the form of a 2D List into a tuple so it can be put into a set
def MakeTuple(state):
  newTuple = tuple()
  for i in range(len(state)):
    newTuple = newTuple + ((tuple(state[i])))
  return newTuple

# Stores and removes the frontmost node of the queue
def RemoveFront(nodes):
  temp = nodes[0]
  nodes.pop(0)
  return temp

# Tests if a node's state matches the goal state
def GoalTest(node):
  return node.state == goalState

# All operators housed in this class
# An operator is passed a node and the coordinate of the blank tile
#   The blank tile is swapped with the appropriate adjacent tile and the modified node is returned
class Operators():
  def MoveBlankLeft(self, node, coord):
    x = coord[0]
    y = coord[1]
    tempVal = node.state[x][y-1]
    node.state[x][y] = tempVal
    node.state[x][y-1] = "b" 
    return node
  def MoveBlankRight(self, node, coord):
    x = coord[0]
    y = coord[1]
    tempVal = node.state[x][y+1]
    node.state[x][y] = tempVal
    node.state[x][y+1] = "b" 
    return node
  def MoveBlankUp(self, node, coord):
    x = coord[0]
    y = coord[1]
    tempVal = node.state[x-1][y]
    node.state[x][y] = tempVal
    node.state[x-1][y] = "b" 
    return node
  def MoveBlankDown(self, node, coord):
    x = coord[0]
    y = coord[1]
    tempVal = node.state[x+1][y]
    node.state[x][y] = tempVal
    node.state[x+1][y] = "b" 
    return node

# Expands a node. Takes in a node and operations that can be used on the node
def Expand(node, ops):
  global expandCount
  global repeat
  newNodes = []
  expandCount += 1  

  # Node is made into 4 copies
  upNode = copy.deepcopy(node)
  downNode = copy.deepcopy(node)
  leftNode = copy.deepcopy(node)
  rightNode = copy.deepcopy(node)

  # Locates the coordinate of the blank tile
  for i in range(len(node.state)):
    try:
      y = node.state[i].index("b")
    except:
      continue
    x = i
  coord = (x,y)

  # If-statements for bounds checking
  # For each case, if the blank tile can be moved: The Parent and Depth is set for the newly created Node. Then the set of previously created nodes is checked to see if the new Node is a duplicate. If not a duplicate, the new Node is added to the queue. If it is a duplicate, it is not added and the repeat counter is incremented.
  dim = len(node.state)
  if (x < dim-1):
    downNode.SetParent(node)
    downNode.SetDepth(downNode.GetDepth() + 1)
    downNode = ops.MoveBlankDown(downNode, coord)
    t = MakeTuple(downNode.state)
    if t not in repeatCheck:
      newNodes.append(downNode)
      repeatCheck.add(MakeTuple(downNode.state))
    else:  
      repeat += 1

  if (x > 0):
    upNode.SetParent(node)
    upNode.SetDepth(upNode.GetDepth() + 1)
    upNode = ops.MoveBlankUp(upNode, coord)
    t = MakeTuple(upNode.state)
    if t not in repeatCheck:
      newNodes.append(upNode)
      repeatCheck.add(MakeTuple(upNode.state))
    else:
      repeat += 1

  if (y < dim-1):
    rightNode.SetParent(node)
    rightNode.SetDepth(rightNode.GetDepth() + 1) 
    rightNode = ops.MoveBlankRight(rightNode, coord)
    t = MakeTuple(rightNode.state)
    if t not in repeatCheck:
      newNodes.append(rightNode)
      repeatCheck.add(MakeTuple(rightNode.state))
    else:  
      repeat += 1

  if (y > 0):
    leftNode.SetParent(node)
    leftNode.SetDepth(leftNode.GetDepth() + 1)
    leftNode = ops.MoveBlankLeft(leftNode, coord)
    t = MakeTuple(leftNode.state)
    if t not in repeatCheck:
      newNodes.append(leftNode)
      repeatCheck.add(MakeTuple(leftNode.state))
    else:      
      repeat += 1

  return newNodes

# Used in the Manhattan Distance Heuristic to find the distance a value is from its proper location in the goal state
# Done by taking the absolute value of the difference between the current coordinate of a value and the coordinate of its goal
def ReturnDifference(value, coord):
  if value == '1':
    diff = abs(coord[0] - 0) + abs(coord[1] - 0)
  elif value == '2':
    diff = abs(coord[0] - 0) + abs(coord[1] - 1)
  elif value == '3':
    diff = abs(coord[0] - 0) + abs(coord[1] - 2)
  elif value == '4':
    diff = abs(coord[0] - 1) + abs(coord[1] - 0)
  elif value == '5':
    diff = abs(coord[0] - 1) + abs(coord[1] - 1)
  elif value == '6':
    diff = abs(coord[0] - 1) + abs(coord[1] - 2)
  elif value == '7':
    diff = abs(coord[0] - 2) + abs(coord[1] - 0)
  elif value == '8':
    diff = abs(coord[0] - 2) + abs(coord[1] - 1)
  elif value == 'b':
    diff = abs(coord[0] - 2) + abs(coord[1] - 2)
  return diff

# Helper functions that set the costs in a node for each heuristic
def CountAndSetMTH(node):
  mthCount = 0
  for i in range(len(node.state)):
    for j in range(len(node.state[i])):
      if goalState[i][j] != "b" and (node.state[i][j] != goalState[i][j]):
        mthCount += 1
  node.SetGn(mthCount)
  return True
def CountAndSetMDH(node):
  mdhCount = 0
  for i in range(len(node.state)):
    for j in range(len(node.state[i])):
      if node.state[i][j] != "b" and (node.state[i][j] != goalState[i][j]):
        mdhCount += ReturnDifference(node.state[i][j], (i,j))
  node.SetHn(mdhCount)
  return True

# Helper functions that call CountAndSet on all nodes
def CalcMTH(nodes):
  for i in range(len(nodes)):
    CountAndSetMTH(nodes[i])
  return True
def CalcMDH(nodes):
  for i in range(len(nodes)):
    CountAndSetMDH(nodes[i])
  return True

# Helper function that adds new Nodes to the queue for Uniform Cost Search
def UCS(nodes, listOfNewNodes):
  for i in range(len(listOfNewNodes)):
    nodes.append(listOfNewNodes[i])
  return nodes

# Helper functions that call methods that calculate total cost for each heuristic
def SetMTHTotal(node):
  node.SetTotalMTH()
  return True
def SetMDHTotal(node):
  node.SetTotalMDH()
  return True

# MTH and MDH append new Nodes to the queue and sort it according to the desired attribute
# This insures a proper dequeueing order
def MTH(nodes, listOfNewNodes):
  CalcMTH(listOfNewNodes)
  for i in range(len(listOfNewNodes)):
    nodes.append(listOfNewNodes[i])
  for i in range(len(listOfNewNodes)):
    SetMTHTotal(listOfNewNodes[i])
  nodes = sorted(nodes, key = operator.attrgetter('MTH'))
  return nodes

def MDH(nodes, listOfNewNodes):
  CalcMDH(listOfNewNodes)
  for i in range(len(listOfNewNodes)):
    nodes.append(listOfNewNodes[i])
  for i in range(len(listOfNewNodes)):
    SetMDHTotal(listOfNewNodes[i])
  nodes = sorted(nodes, key = (operator.attrgetter('MDH')))
  return nodes

# Outputs the traceback from the initial state to the goal state
def GetPath(node):
  if not node.parent:
    PrintFormattedState(node.state)
  else: 
    GetPath(node.parent)
    PrintFormattedState(node.state)

# The General Search algorithm that appliess the desired queueing method
def GeneralSearch(initState, QueueingFunction):
  global expandCount
  global queueSize
  global goalDepth
  global repeat
  # The inital state of the problem is set
  initState = initState.state
  nodes = []
  nodes.append(MakeNode(initState))
  prevQmax = len(nodes)

  while(True):
    global prevQMax
    queueSize = max(prevQMax, len(nodes))
    prevQmax = queueSize

    # If there are no more nodes to dequeue there is no solution
    if not nodes:
      print ("failure")
      return False
   
    node = RemoveFront(nodes)

    # Test if the current node is the goal. If so, end and output goal depth and traceback
    if GoalTest(node):
      print ("Success")
      print ("Goal Node Depth: ", node.depth)
      print ("Path: ")
      GetPath(node)
      return True

    print("Expanding Node: ")
    PrintFormattedState(node.state)
    # Populte the queue with the newly expanded nodes in the proper order
    nodes = QueueingFunction(nodes, Expand(node, Operators()))


#### ---------- DRIVER FOR PROGRAM ---------- ####
print ("\n\n\n****  PROGRAM START  ****")

# Initial Prompt
print ("Welcome to Mathew Schaffrath 8-puzzle solver.")
print ("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle.")
selectPuzzle = input("")

# Take input for custom initial state
if selectPuzzle == "2":
  userInitState = []
  print ("Enter your puzzle, use a \"b\" to represent the blank")
  row1 = input("Enter the first row, use space or tabs between numbers    ")
  userInitState.append(row1.split())
  row2 = input("Enter the second row, use space or tabs between numbers   ")
  userInitState.append(row2.split())
  row3 = input("Enter the third row, use space or tabs between numbers    ")
  userInitState.append(row3.split())
  print("\n")
  problem = MakeNode(userInitState)
elif selectPuzzle == "1":
  problem = MakeNode(defaultInitState)

# User selects algorithm
print("Enter your choice of algorithm")
print("\t", "1.  Uniform Cost Search")
print("\t", "2.  A* with the Misplaced Tile heuristic")
print("\t", "3.  A* with the Manhattan distance heuristic")
selectAlg = input("         ")

# Pass General Search proper algorithm
if selectAlg == "1":
  GeneralSearch(problem, UCS)
if selectAlg == "2":
  GeneralSearch(problem, MTH)
if selectAlg == "3":
  GeneralSearch(problem, MDH)

# Output data
print("Nodes expanded: ", expandCount)
print("Max # of nodes in queue at any one time: ", queueSize)

print ("*****  PROGRAM END  *****\n\n\n")





