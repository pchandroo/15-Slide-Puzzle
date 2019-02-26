import timeit
import resource
from heapq import heappush, heappop, heapify
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

f_state = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
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

def setting(config):
    global b_length, b_breath
    data = config.split(",")
    for element in data:
        i_state.append(int(element))
    b_length = len(i_state)
    b_breath = int(b_length ** 0.5)

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

def ast_mdist(start_state):
    global max_frontier_size, f_node, m_depth
    explored, heap, heap_entry, counter = set(), list(), {}, itertools.count()
    key = h_mdist(start_state)
    root = State(start_state, None, None, 0, 0, key)
    entry = (key, 0, root)
    heappush(heap, entry)
    heap_entry[root.map] = entry
    while heap:
        node = heappop(heap)
        explored.add(node[2].map)
        if node[2].state == f_state:
            f_node = node[2]
            return heap
        adjacent = expand(node[2])
        for neighbor in adjacent:
            neighbor.key = neighbor.cost + h_mdist(neighbor.state)
            entry = (neighbor.key, neighbor.move, neighbor)
            if neighbor.map not in explored:
                heappush(heap, entry)
                explored.add(neighbor.map)
                heap_entry[neighbor.map] = entry
                if neighbor.depth > m_depth:
                    m_depth += 1
            elif neighbor.map in heap_entry and neighbor.key < heap_entry[neighbor.map][2].key:
                hindex = heap.index((heap_entry[neighbor.map][2].key,
                                     heap_entry[neighbor.map][2].move,
                                     heap_entry[neighbor.map][2]))
                heap[int(hindex)] = entry
                heap_entry[neighbor.map] = entry
                heapify(heap)
        if len(heap) > max_frontier_size:
            max_frontier_size = len(heap)

def h_mdist(state):
    return sum(abs(b % b_breath - g % b_breath) + abs(b//b_breath - g//b_breath)
               for b, g in ((state.index(i), f_state.index(i)) for i in range(1, b_length)))

def ast_misplaced(start_state):
    global max_frontier_size, f_node, m_depth
    explored, heap, heap_entry, counter = set(), list(), {}, itertools.count()
    key = h_misplaced(start_state)
    root = State(start_state, None, None, 0, 0, key)
    entry = (key, 0, root)
    heappush(heap, entry)
    heap_entry[root.map] = entry
    while heap:
        node = heappop(heap)
        explored.add(node[2].map)
        if node[2].state == f_state:
            f_node = node[2]
            return heap
        adjacent = expand(node[2])
        for neighbor in adjacent:
            neighbor.key = neighbor.cost + h_misplaced(neighbor.state)
            entry = (neighbor.key, neighbor.move, neighbor)
            if neighbor.map not in explored:
                heappush(heap, entry)
                explored.add(neighbor.map)
                heap_entry[neighbor.map] = entry
                if neighbor.depth > m_depth:
                    m_depth += 1
            elif neighbor.map in heap_entry and neighbor.key < heap_entry[neighbor.map][2].key:
                hindex = heap.index((heap_entry[neighbor.map][2].key,
                                     heap_entry[neighbor.map][2].move,
                                     heap_entry[neighbor.map][2]))
                heap[int(hindex)] = entry
                heap_entry[neighbor.map] = entry
                heapify(heap)
        if len(heap) > max_frontier_size:
            max_frontier_size = len(heap)

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


def main():
    global moves,nodes_expanded
    board = input("Input:")
    #t= Thread(target=job_function, args=())
    #t.start()
    setting(board)
    start = timeit.default_timer()
    ast_mdist(i_state)
    stop = timeit.default_timer()
    moves = trace()
    print("Output using Manhattan Distance as Heruistic")
    print("Moves: " + str(moves))
    print("Number of nodes expanded: " + str(nodes_expanded))
    print("Time Taken " + format(stop-start))
    print("Memory used" + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0))
    moves = list()
    nodes_expanded = 0
    start = timeit.default_timer()
    ast_misplaced(i_state)
    stop = timeit.default_timer()
    moves = trace()
    print("Output using Misplaced Tiles as Heruistic")
    print("Moves: " + str(moves))
    print("Number of nodes expanded: " + str(nodes_expanded))
    print("Time Taken " + format(stop-start))
    print("Memory used" + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0))

if __name__ == '__main__':
    main()