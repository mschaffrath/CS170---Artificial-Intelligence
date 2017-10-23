#
#  CS170 - Artifical Intelligence
#
#  Author: Mathew Schaffrath
#

import copy
import operator

class Node(object):
  def __init__(self,state):
    self.state = state
  gn = 0
  hn = 0
  def SetGn(self, cost):
    self.gn = cost
  def SetHn(self, cost):
    self.hn = cost

goalState = [['1','2','3'],
             ['4','5','6'],
             ['7','8','b']]

expandCount = 0
queueSize = 0
goalDepth = 0

def PrintFormattedState(state):
  for i in range(len(state)):
      print(state[i])

def MakeNode(initState):
  return Node(initState) 

def RemoveFront(nodes):
  temp = nodes[0]
  nodes.pop(0)
  return temp

def GoalTest(node):
  return node.state == goalState

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
 
def Expand(node, ops):
  newNodes = []
  upNode = copy.deepcopy(node)
  downNode = copy.deepcopy(node)
  leftNode = copy.deepcopy(node)
  rightNode = copy.deepcopy(node)

  for i in range(len(node.state)):
    try:
      y = node.state[i].index("b")
    except:
      continue
    x = i
  coord = (x,y)

  if (x == 1 or x == 0):
    newNodes.append(ops.MoveBlankDown(downNode, coord))
  if (x == 1 or x == 2):
    newNodes.append(ops.MoveBlankUp(upNode, coord))
  if (y == 1 or y == 0):
    newNodes.append(ops.MoveBlankRight(rightNode, coord))
  if (y == 1 or y == 2):
    newNodes.append(ops.MoveBlankLeft(leftNode, coord))

#  newNodes = PruneStates(newNodes)
  return newNodes

def PruneStates(nodes):
  end = len(nodes)
  for i in range(end):
    for j in range(i+1, end):
      if nodes[i].state == nodes[j].state:
        print("STATE PRUNED:--------------------------------------")
        PrintFormattedState(nodes[j].state)
        del nodes[j]
        end -= 1
  return nodes

def CountAndSetMTH(node):
  mthCount = 0
  for i in range(len(node.state)):
    for j in range(len(node.state[i])):
      if goalState[i][j] != "b" and (node.state[i][j] != goalState[i][j]):
        mthCount += 1
  node.SetGn(mthCount)
  return True

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

def CountAndSetMDH(node):
  mdhCount = 0
  for i in range(len(node.state)):
    for j in range(len(node.state[i])):
      if node.state[i][j] != "b" and (node.state[i][j] != goalState[i][j]):
        mdhCount += ReturnDifference(node.state[i][j], (i,j))
  node.SetHn(mdhCount)
  return True

def CalcMTH(nodes):
  for i in range(len(nodes)):
    CountAndSetMTH(nodes[i])
  return True

def CalcMDH(nodes):
  for i in range(len(nodes)):
    CountAndSetMDH(nodes[i])
  return True

def UCS(nodes, listOfNewNodes):
  for i in range(len(listOfNewNodes)):
    nodes.append(listOfNewNodes[i])
  return nodes

def MTH(nodes, listOfNewNodes):
  CalcMTH(listOfNewNodes)
  #print("UNSORTED:")
  #for i in range(len(listOfNewNodes)):
  #  PrintFormattedState(listOfNewNodes[i].state)
  #print("SORTED:")
  #for i in range(len(listOfNewNodes)):
  #  PrintFormattedState(listOfNewNodes[i].state)

  for i in range(len(listOfNewNodes)):
    nodes.append(listOfNewNodes[i])
  nodes = sorted(nodes, key=operator.attrgetter('gn'))
  return nodes

def MDH(nodes, listOfNewNodes):
  CalcMDH(listOfNewNodes)
  for i in range(len(listOfNewNodes)):
    nodes.append(listOfNewNodes[i])
  nodes = sorted(nodes, key = operator.attrgetter('hn'))
  return nodes

prevQMax = 0
def GeneralSearch(initState, QueueingFunction):
  global expandCount
  global queueSize
  global goalDepth
  initState = initState.state
  nodes = []
  nodes.append(MakeNode(initState))
  prevQmax = len(nodes)

  while(True):
    global prevQMax
    queueSize = max(prevQMax, len(nodes))
    prevQmax = queueSize

    if not nodes:
      print ("failure")
      return False
    
    node = RemoveFront(nodes)

    if GoalTest(node):
      print ("Success")
      return True

    expandCount += 1
#    print("Expanding State: ")
#    PrintFormattedState(node.state)
    nodes = QueueingFunction(nodes, Expand(node, Operators()))
#    print("Expanded to: ")
#    for i in range(len(nodes)): 
#      PrintFormattedState(nodes[i].state)
#      print("gn: ", nodes[i].gn, " ", "hn: ", nodes[i].hn)
#      print("sumCost: ", nodes[i].gn + nodes[i].hn)
#      print("\n")

defaultInitState = [['8','7','1'],
                    ['6','b','2'],
                    ['5','4','3']]

print ("\n\n\n****PROGRAM START****")

print ("Welcome to Mathew Schaffrath 8-puzzle solver.")
print ("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle.")
selectPuzzle = input("")

if selectPuzzle == "2":
  userInitState = []
  print ("Enter your puzzle, use a \"b\" to represent the blank")
  row1 = input("Enter the first row, use space or tabes between numbers   ")
  userInitState.append(row1.split())
  row2 = input("Enter the first row, use space or tabes between numbers   ")
  userInitState.append(row2.split())
  row3 = input("Enter the first row, use space or tabes between numbers   ")
  userInitState.append(row3.split())
  print("\n")
  problem = MakeNode(userInitState)
elif selectPuzzle == "1":
  problem = MakeNode(defaultInitState)

print("Enter your choice of algorithm")
print("\t", "1.  Uniform Cost Search")
print("\t", "2.  A* with the Misplaced Tile heuristic")
print("\t", "3.  A* with the Manhattan distance heuristic")
selectAlg = input("         ")

print("\nInitial State: ")
PrintFormattedState(problem.state)
if selectAlg == "1":
  GeneralSearch(problem, UCS)
if selectAlg == "2":
  GeneralSearch(problem, MTH)
if selectAlg == "3":
  GeneralSearch(problem, MDH)

print("Nodes expanded: ", expandCount)
print("Max # of nodes in queue at any one time: ", queueSize)

print ("*****PROGRAM END*****\n\n\n")





