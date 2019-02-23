import timeit
import resource
from collections import deque
import itertools

class State:
    def __init__(self, state, parent, move, depth, cost, key):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.key = key
        if self.state:
            self.map = ''.join(str(e) for e in self.state)
    def __eq__(self, other):
        return self.map == other.map
    def __lt__(self, other):
        return self.map < other.map

f_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
f_node = State
i_state = list()
b_length = 0
b_breath = 0
nodes_expanded = 0
m_depth = 0
max_frontier_size = 0
moves = list()
costs = set()

def job_function():
    time.sleep(1800)
    print ("Solution cannot be found")
    sys.exit;

def setting(configuration):
    global b_length, b_breath
    data = configuration.split(",")
    for element in data:
        i_state.append(int(element))
    b_length = len(i_state)
    b_breath = int(b_length ** 0.5)

def ida_star(start_state, mode):
    global costs
    if mode == 1:
        threshold = h_mdist(start_state)
    else:
        threshold = h_misplaced(start_state)
    while 1:
        response = search_mod(start_state, threshold, mode)
        if type(response) is list:
            return response
            break
        threshold = response
        costs = set()

def search_mod(start_state, threshold, mode):
    global max_frontier_size, f_node, m_depth, costs
    explored, stack = set(), list([State(start_state, None, None, 0, 0, threshold)])
    while stack:
        node = stack.pop()
        explored.add(node.map)
        if node.state == f_state:
            f_node = node
            return stack
        if node.key > threshold:
            costs.add(node.key)
        if node.depth < threshold:
            adjacent = reversed(expand(node))
            for neighbor in adjacent:
                if neighbor.map not in explored:
                    if mode == 1:
                        neighbor.key = neighbor.cost + h_mdist(neighbor.state)
                    else:
                        neighbor.key = neighbor.cost + h_misplaced(neighbor.state)
                    stack.append(neighbor)
                    explored.add(neighbor.map)
                    if neighbor.depth > m_depth:
                        m_depth += 1
            if len(stack) > max_frontier_size:
                max_frontier_size = len(stack)
    return min(costs)

def h_mdist(state):
    return sum(abs(b % b_breath - g % b_breath) + abs(b//b_breath - g//b_breath)
               for b, g in ((state.index(i), f_state.index(i)) for i in range(1, b_length)))

def h_misplaced(state):
    Misplaced=0
    for i in range(16):
        if state[i]!=f_state[i]:
            Misplaced +=1
    return Misplaced

def expand(node):
    global nodes_expanded
    nodes_expanded += 1
    adjacent = list()
    adjacent.append(State(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    adjacent.append(State(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    adjacent.append(State(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    adjacent.append(State(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))
    nodes = [neighbor for neighbor in adjacent if neighbor.state]
    return nodes

def move(state, position):
    new_state = state[:]
    index = new_state.index(0)
    if position == 1:
        if index not in range(0, b_breath):
            temp = new_state[index - b_breath]
            new_state[index - b_breath] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None
    if position == 2:  
        if index not in range(b_length - b_breath, b_length):
            temp = new_state[index + b_breath]
            new_state[index + b_breath] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None
    if position == 3: 
        if index not in range(0, b_length, b_breath):
            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None
    if position == 4:
        if index not in range(b_breath - 1, b_length, b_breath):
            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp
            return new_state
        else:
            return None

def trace():
    current_node = f_node
    while i_state != current_node.state:
        if current_node.move == 1:
            movement = 'U'
        elif current_node.move == 2:
            movement = 'D'
        elif current_node.move == 3:
            movement = 'L'
        else:
            movement = 'R'
        moves.insert(0, movement)
        current_node = current_node.parent
    return moves

def main():
    global moves,nodes_expanded
    board = input("Input (separated by commas):")
    #t= Thread(target=job_function, args=())
    #t.start()
    setting(board)
    start = timeit.default_timer()
    ida_star(i_state, 1)
    stop = timeit.default_timer()
    moves = trace()
    print("\nOutput using Manhattan Distance as Heruistic")
    print("Moves: " + str(moves))
    print("Number of nodes expanded: " + str(nodes_expanded))
    print("Time Taken " + format(stop-start))
    print("Memory used" + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0))
    moves = list()
    nodes_expanded = 0
    start = timeit.default_timer()
    ida_star(i_state, 2)
    stop = timeit.default_timer()
    moves = trace()
    print("\nOutput using Misplaced Tiles as Heruistic")
    print("Moves: " + str(moves))
    print("Number of nodes expanded: " + str(nodes_expanded))
    print("Time Taken " + format(stop-start))
    print("Memory used" + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0))   

if __name__ == '__main__':
    main()
