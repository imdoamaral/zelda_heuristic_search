import heapq

class Node:
    """Representa um nó no grid de busca."""
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Custo do início até o nó atual
        self.h = 0  # Custo heurístico do nó atual até o fim
        self.f = 0  # Custo total (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        # heapq é uma min-heap, então ele vai priorizar o menor f
        return self.f < other.f

    def __hash__(self):
        # Permite adicionar nós a um set
        return hash(self.position)

def manhattan_distance(pos1, pos2):
    """Calcula a distância de Manhattan, uma heurística admissível para grids."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def a_star_search(map_grid, terrain_costs, start_pos, end_pos):
    """
    Encontra o caminho de menor custo usando uma implementação otimizada de A*.
    Esta versão usa um set para a lista aberta para buscas O(1).
    """
    start_node = Node(start_pos)
    end_node = Node(end_pos)

    open_list_heap = []
    open_list_dict = {}  # Dicionário para acesso O(1) aos nós na open_list

    closed_set = set()

    heapq.heappush(open_list_heap, start_node)
    open_list_dict[start_node.position] = start_node

    while open_list_heap:
        current_node = heapq.heappop(open_list_heap)
        
        # Se o nó já foi processado com um custo menor, ignore
        if current_node.position not in open_list_dict:
            continue
        
        del open_list_dict[current_node.position]


        if current_node.position == end_node.position:
            path = []
            cost = current_node.g
            temp = current_node
            while temp is not None:
                path.append(temp.position)
                temp = temp.parent
            return path[::-1], cost

        closed_set.add(current_node.position)

        (row, col) = current_node.position
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (row + move[0], col + move[1])

            if not (0 <= next_pos[0] < len(map_grid) and 0 <= next_pos[1] < len(map_grid[0])):
                continue
            
            terrain_type = map_grid[next_pos[0]][next_pos[1]]
            if terrain_costs.get(terrain_type, float('inf')) == float('inf'):
                continue

            if next_pos in closed_set:
                continue

            move_cost = terrain_costs[terrain_type]
            
            g_cost = current_node.g + move_cost
            h_cost = manhattan_distance(next_pos, end_node.position)
            f_cost = g_cost + h_cost

            # Se o vizinho já está na lista aberta com um custo menor, ignore
            if next_pos in open_list_dict and open_list_dict[next_pos].f <= f_cost:
                continue

            neighbor = Node(next_pos, current_node)
            neighbor.g = g_cost
            neighbor.h = h_cost
            neighbor.f = f_cost
            
            heapq.heappush(open_list_heap, neighbor)
            open_list_dict[neighbor.position] = neighbor

    return None, 0  # Caminho não encontrado