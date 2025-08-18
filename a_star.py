import heapq

class Node:
    """
    Representa um nó no grid de busca. Cada nó armazena sua posição,
    o nó pai (para reconstruir o caminho), e os custos g, h, e f.
    """
    def __init__(self, position, parent=None):
        self.position = position  # A coordenada (linha, coluna) do nó no grid.
        self.parent = parent      # O nó que precedeu este no caminho.

        # g: Custo real do caminho desde o nó inicial até este nó.
        self.g = 0
        # h: Custo heurístico estimado deste nó até o nó final.
        self.h = 0
        # f: Custo total (g + h). É o valor usado para priorizar os nós na busca.
        self.f = 0

    def __eq__(self, other):
        # Dois nós são considerados iguais se suas posições forem as mesmas.
        return self.position == other.position

    def __lt__(self, other):
        # Define a ordem dos nós na fila de prioridade (min-heap).
        # Nós com menor custo 'f' têm maior prioridade.
        return self.f < other.f

    def __hash__(self):
        # Permite que o nó seja adicionado a um conjunto (set), usando sua posição como identificador único.
        return hash(self.position)

def manhattan_distance(pos1, pos2):
    """
    Calcula a distância de Manhattan entre dois pontos.
    É uma heurística comum e admissível para grids onde o movimento é restrito
    a quatro direções (cima, baixo, esquerda, direita). A distância de Manhattan
    nunca superestima o custo real, garantindo a otimalidade do A*.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def a_star_search(map_grid, terrain_costs, start_pos, end_pos):
    """
    Implementação do algoritmo A* para encontrar o caminho de menor custo em um grid.
    Utiliza uma fila de prioridade (min-heap) para a 'lista aberta' e um conjunto (set)
    para a 'lista fechada', garantindo eficiência.
    """
    # Cria os nós inicial e final.
    start_node = Node(start_pos)
    end_node = Node(end_pos)

    # A 'lista aberta' armazena os nós a serem visitados.
    # open_list_heap é uma fila de prioridade para obter rapidamente o nó com menor 'f'.
    open_list_heap = []
    # open_list_dict permite verificar em O(1) se um nó já está na lista aberta e acessar seus dados.
    open_list_dict = {}

    # A 'lista fechada' armazena as posições dos nós que já foram completamente explorados.
    closed_set = set()

    # Inicia a busca adicionando o nó inicial à lista aberta.
    heapq.heappush(open_list_heap, start_node)
    open_list_dict[start_node.position] = start_node

    # O loop principal do A* continua enquanto houver nós para explorar na lista aberta.
    while open_list_heap:
        # Retira o nó com o menor custo 'f' da fila de prioridade.
        current_node = heapq.heappop(open_list_heap)
        
        # Otimização: se um nó foi adicionado à heap múltiplas vezes com custos diferentes,
        # este 'del' garante que estamos processando a versão com o menor custo 'f' que chegou primeiro.
        if current_node.position not in open_list_dict:
            continue
        del open_list_dict[current_node.position]

        # Se o nó atual é o destino, o caminho foi encontrado.
        if current_node.position == end_node.position:
            path = []
            cost = current_node.g
            temp = current_node
            # Reconstrói o caminho a partir do nó final, seguindo os pais.
            while temp is not None:
                path.append(temp.position)
                temp = temp.parent
            return path[::-1], cost # Retorna o caminho invertido (do início ao fim) e o custo total.

        # Adiciona a posição do nó atual à lista fechada para não reprocessá-lo.
        closed_set.add(current_node.position)

        # Explora os vizinhos do nó atual (movimentos em 4 direções).
        (row, col) = current_node.position
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Direita, Esquerda, Baixo, Cima
            next_pos = (row + move[0], col + move[1])

            # Verifica se o vizinho está dentro dos limites do mapa.
            if not (0 <= next_pos[0] < len(map_grid) and 0 <= next_pos[1] < len(map_grid[0])):
                continue
            
            # Verifica se o terreno do vizinho é intransponível.
            terrain_type = map_grid[next_pos[0]][next_pos[1]]
            if terrain_costs.get(terrain_type, float('inf')) == float('inf'):
                continue

            # Se o vizinho já está na lista fechada, ignora-o.
            if next_pos in closed_set:
                continue

            # Calcula os custos para o nó vizinho.
            move_cost = terrain_costs[terrain_type]
            g_cost = current_node.g + move_cost
            h_cost = manhattan_distance(next_pos, end_node.position)
            f_cost = g_cost + h_cost

            # Se o vizinho já está na lista aberta com um custo 'f' menor ou igual, não faz nada.
            # Isso evita caminhos piores para nós já descobertos.
            if next_pos in open_list_dict and open_list_dict[next_pos].f <= f_cost:
                continue

            # Cria o nó vizinho e define seus custos e pai.
            neighbor = Node(next_pos, current_node)
            neighbor.g = g_cost
            neighbor.h = h_cost
            neighbor.f = f_cost
            
            # Adiciona o vizinho à lista aberta para exploração futura.
            heapq.heappush(open_list_heap, neighbor)
            open_list_dict[neighbor.position] = neighbor

    return None, 0  # Retorna None se nenhum caminho for encontrado.