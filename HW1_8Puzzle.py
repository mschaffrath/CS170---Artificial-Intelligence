#  CS170 - Artifical Intelligence
#
#  Author: Mathew Schaffrath
#

class Node():
  def __init__(self,state):
    self.state = state
    print("in Node class")
    print(state)
    print("end Node class")

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
  def MoveBlankLeft():
    apple = 1
  def MoveBlankRight():
    apple = 1
  def MoveBlankUp():
    apple = 1
  def MoveBlankDown():
    apple = 1

def Expand(node, Operators):
  

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
    
    Expand(node, Operators)

    return False
#    nodes = QueueingFunction(nodes, Expand(node, Operators))


print ("START")

print("GenSearch:")
GeneralSearch(initState)


print ("END")




#print ("Welcome to Mathew Schaffrath 8-puzzle solver.")
#print ("Type "1" to use a default puzzle, or "2" to enter your own puzzle.")

