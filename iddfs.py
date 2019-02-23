#CS 411 - Assignment 5 Solution
#Iterative Deepening Depth First Search on 15 Puzzle
#Sarit Adhikari
#2018 Fall

import random
import math
import time
import psutil
import os

CUTOFF = 0
FAILURE = -1
num_expanded = 0

#This class defines the state of the problem in terms of board configuration
class Board:
	def __init__(self,tiles):
		self.size = int(math.sqrt(len(tiles)))
		self.tiles = tiles
	#This function returns the resulting state from taking particular action from current state
	def execute_action(self,action):
		new_tiles = self.tiles[:]
		empty_index = new_tiles.index('0')
		if action=='l':	
			if empty_index%self.size>0:
				new_tiles[empty_index-1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-1]
		if action=='r':
			if empty_index%self.size<(self.size-1): 	
				new_tiles[empty_index+1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+1]
		if action=='u':
			if empty_index-self.size>=0:
				new_tiles[empty_index-self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-self.size]
		if action=='d':
			if empty_index+self.size < self.size*self.size:
				new_tiles[empty_index+self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+self.size]
		return Board(new_tiles)
		
#This class defines the node on the search tree, consisting of state, parent, previous action and level (0 denotes root level)
class Node:
	def __init__(self,state,parent,action):
		self.state = state
		self.parent = parent
		self.action = action
		if parent is None:
			self.level=0
		else:
			self.level = parent.level+1
	#Returns string representation of the state
	def __repr__(self):
		return str(self.state.tiles)
	
	#Comparing current node with other node. They are equal if states are equal		
	def __eq__(self,other):
		return self.state.tiles == other.state.tiles

#Utility function to randomly generate 15-puzzle		
def generate_puzzle(size):
	numbers = list(range(size*size))
	random.shuffle(numbers)
	return Node(Board(numbers),None,None)
	
#This function returns the list of children obtained after simulating the actions on current node
def get_children(parent_node):
	children = []
	actions = ['l','r','u','d']
	for action in actions:
		child_state = parent_node.state.execute_action(action)
		child_node = Node(child_state,parent_node,action)
		children.append(child_node)
	return children

#This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path	
def find_path(node):
	
	path = []
	
	while(node.parent is not None):
		path.append(node.action)
		node = node.parent
	path.reverse()
	return path


#This function runs depth limited search from given node till the provided depth limit	
def run_dls(node,limit):
	global num_expanded
	
	if goal_test(node.state.tiles) : return node
	elif limit==0 : return CUTOFF
	else:
		cutoff_occured = False
		num_expanded=num_expanded+1
		for child in get_children(node):
			result = run_dls(child,limit-1)
			if isinstance(result,int) and result==CUTOFF : 
				cutoff_occured = True
			elif result != FAILURE : return result
		if cutoff_occured : return CUTOFF
		else: return FAILURE
		
#Main function accepting input from console , runnung iddfs and showing output
def main():
	process = psutil.Process(os.getpid())
	initial_memory = process.memory_info().rss / 1024.0
	global num_expanded
	initial = str(raw_input("initial configuration: "))
	initial_list = initial.split(" ")
	root = Node(Board(initial_list),None,None)
	start_time = time.time()
	for i in range(0,100):
		num_expanded = 0
		print("CURENT MAX DEPTH: "+ str(i))		 
		result = run_dls(root,i)
		if isinstance(result,Node):
			print find_path(result)
			print("Expanded Nodes: " + str(num_expanded))
			break
		elif result==CUTOFF:
			print "solution doesn't exist at this depth"
		else:
			print "solution not found"
	end_time = time.time()		
	final_memory = process.memory_info().rss / 1024.0
	print(str(final_memory-initial_memory)+" KB")
	print(str(end_time-start_time)+" sec")


def goal_test(cur_tiles):
	return cur_tiles == ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']	
	
if __name__=="__main__":main()	