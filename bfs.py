import timeit 
from collections import deque
import time
import threading
from threading import Thread
import multiprocessing
import sched, time
import sys
import resource

class State:
    def __init__(self, state, parent, move):
        self.state = state
        self.parent = parent
        self.move = move
        if self.state:
            self.map = ''.join(str(e) for e in self.state)
    def __eq__(self, other):
        return self.map == other.map
    def __lt__(self, other):
        return self.map < other.map

goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
goal_node = State
initial_state = list()
board_len = 0
board_side = 0
nodes_expanded = 0
max_search_depth = 0
moves = list()
costs = set()

def trace():
    current_node = goal_node
    while initial_state != current_node.state:
        if current_node.move == 1:
            action = 'U'
        elif current_node.move == 2:
            action = 'D'
        elif current_node.move == 3:
            action = 'L'
        else:
            action = 'R'
        moves.insert(0, action)
        current_node = current_node.parent
    return moves

def setting(config):
    global board_len, board_side
    data = config.split(",")
    for element in data:
        initial_state.append(int(element))
    board_len = len(initial_state)
    board_side = int(board_len ** 0.5)

def job_function():
    time.sleep(1800)
    print ("Solution cannot be found")
    sys.exit;

def bfs(start_state):
    global goal_node, max_search_depth
    explored, queue = set(), deque([State(start_state, None, None)])
    while queue:
        node = queue.popleft()
        explored.add(node.map)
        if node.state == goal_state:
            goal_node = node
            return queue
        neighbors = expand(node)
        for neighbor in neighbors:
            if neighbor.map not in explored:
                queue.append(neighbor)
                explored.add(neighbor.map)

def expand(node):
    global nodes_expanded
    nodes_expanded += 1
    neighbors = list()
    neighbors.append(State(move(node.state, 1), node, 1))
    neighbors.append(State(move(node.state, 2), node, 2))
    neighbors.append(State(move(node.state, 3), node, 3))
    neighbors.append(State(move(node.state, 4), node, 4))
    nodes = [neighbor for neighbor in neighbors if neighbor.state]
    return nodes

def move(state, position):
    new_state = state[:]
    index = new_state.index(0)
    if position == 1:  # Up
        if index not in range(0, board_side):
            temp = new_state[index - board_side]
            new_state[index - board_side] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None
    if position == 2:  # Down
        if index not in range(board_len - board_side, board_len):
            temp = new_state[index + board_side]
            new_state[index + board_side] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None
    if position == 3:  # Left
        if index not in range(0, board_len, board_side):
            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None
    if position == 4:  # Right
        if index not in range(board_side - 1, board_len, board_side):
            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None

def main():
    board = input("Input:")
    #t= Thread(target=job_function, args=())
    #t.start()
    function = bfs
    setting(board)
    start = timeit.default_timer()
    function(initial_state)
    stop = timeit.default_timer()
    moves = trace()
    print("Move:" +str(moves))
    print("Number of nodes expanded:" +str(nodes_expanded))
    print("Time:" +format(stop-start))
    print("Memory usage:" +format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0))   
    sys.exit;
 
if __name__ == '__main__':
    main()