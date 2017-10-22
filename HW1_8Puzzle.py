#  CS170 - Artifical Intelligence
#
#  Author: Mathew Schaffrath
#

import copy

class Node(object):
  def __init__(self,state):
    self.state = state

initState = [[1,  2,  3 ],
             [4,  5,  6 ],
             [7, "b", 8 ]]
goalState = [[1,  2,  3 ],
             [4,  5,  6 ],
             [7,  8, "b"]]

def MakeNode(initState):
  print("Make Node called")
  return Node(initState) 

def RemoveFront(nodes):
  temp = nodes[0]
  nodes.pop(0)
  return temp

def GoalTest(node):
  return node.state == goalState

class Operators():
  def MoveBlankLeft(self, node, coord):
    print("move left called")
    x = coord[0]
    y = coord[1]
    tempVal = node.state[x][y-1]
    print("tempVal: ", tempVal)
    node.state[x][y] = tempVal
    node.state[x][y-1] = "b" 
    return node
  def MoveBlankRight(self, node, coord):
    print("move right called on: ", node.state)
    x = coord[0]
    y = coord[1]
    tempVal = node.state[x][y+1]
    print("tempVal: ", tempVal)
    node.state[x][y] = tempVal
    node.state[x][y+1] = "b" 
    return node
  def MoveBlankUp(self, node, coord):
    print("move up called on: ", node.state)
    x = coord[0]
    y = coord[1]
    tempVal = node.state[x-1][y]
    print("tempVal: ", tempVal)
    node.state[x][y] = tempVal
    node.state[x-1][y] = "b" 
    return node
  def MoveBlankDown(self, node, coord):
    print("move down called")
    x = coord[0]
    y = coord[1]
    tempVal = node.state[x+1][y]
    print("tempVal: ", tempVal)
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
  print("coord: ", x , " " , y) 
  
  if (x == 1 or x == 0):
    newNodes.append(ops.MoveBlankDown(downNode, coord))
  if (x == 1 or x == 2):
    newNodes.append(ops.MoveBlankUp(upNode, coord))
  if (y == 1 or y == 0):
    newNodes.append(ops.MoveBlankRight(rightNode, coord))
  if (y == 1 or y == 0):
    newNodes.append(ops.MoveBlankLeft(leftNode, coord))

  print ("new nodes: ")
  print (newNodes[0].state[0])
  print (newNodes[0].state[1])
  print (newNodes[0].state[2])
  print (newNodes[1].state[0])
  print (newNodes[1].state[1])
  print (newNodes[1].state[2])
   
  return newNodes

# def QueueingFunction(nodes, listOfNewNodes):


# TESTING *************************
MakeNode(initState)

def GeneralSearch(initState):
  nodes = []
  nodes.append(MakeNode(initState))

  while(True):
    
    if not nodes:
      print ("failure")
      return False
    
    node = RemoveFront(nodes)
    print("node after remove")
    print(node.state)

    if GoalTest(node):
      print ("success")
      return True
    
    ops = Operators()
    Expand(node, ops)

    return False

#    nodes = QueueingFunction(nodes, Expand(node, Operators))


print ("START")

print("GenSearch:")
GeneralSearch(initState)


print ("END")




#print ("Welcome to Mathew Schaffrath 8-puzzle solver.")
#print ("Type "1" to use a default puzzle, or "2" to enter your own puzzle.")

