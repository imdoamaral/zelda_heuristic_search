import heapq

class Node:
    """
    Representa um ponto (nó) no grid. Funciona como um "passo" no caminho.
    Armazena sua posiçao e os custos necessarios para o calculod e A*.
    """

    def __init__(self, position, parent=None):
        self.position = position    # Coordenada (linha, coluna) no mapa
        self.parent = parent        # O nó anterior no caminho, para reconstruçao

        self.g = 0 # G: custo real do inicio ate este nó. É o custo ja acumulado.
        self.h = 0 # H: custo heuristico (estimado) deste no ate o final. É uma previsao inteligente.
        self.f = 0 # F: custo total (g + h). É a prioridade do nó. O A* sempre explora o nó com menor F.

    # eq = equal
    def __eq__(self, other):
        # Permite comparar 2 nós pelo atributo position
        # Se ocupam o mesmo lugar no mapa, sao considerados iguais.
        return self.position == other.position
    
    # lt = less then
    def __lt__(self, other):
        # Define que nós com menor custo 'f' tem maior prioridade
        return self.f < other.f
    
    # hash = cria um numero para um objeto com base apenas na sua posiçao
    def __hash__(self):
        # Permite adicionar nós a um conjunto (set)
        return hash(self.position)
        
def manhattan_distance(pos1, pos2):
    """
    Calcula a distancia manhattan entre 2 pontos.
    É uma heuristica comum e admissivel para grids onde o movimento é restrito
    a 4 direçoes (cima, baixo, esquerda, direita). A distancia de manhattan
    nunca superestima o custo real, garantindo a otimalidade do A*.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
def a_star_search(map_grid, terrain_costs, start_pos, end_pos):
    """
    Implementaçao do algoritmo A* para encontra o caminho de menor custo em um grid.
    Utiliza uma fila de prioridade (min-heap) para a 'lista aberta' e um conjunto (set)
    para a 'lista fechada', garantindo eficiencia.
    """
    # Cria os nós Inicial e Final
    start_node = Node(start_pos)
    end_node = Node(end_pos)

    # --- Agora, o A* usa 2 listas principais para controlar a busca: ---
    
    # 1. LISTA ABERTA (open_list): Nós que foram descobertos, mas ainda nao visitados.        
    # Usamos uma fila de prioridade (heap) para sempre pegar o nó com menor custo 'f' rapidamente.
    open_list_heap = []

    # Usamos tambem um dicionario pra acessar e verificar a existencia de um nó na lista aberta em tempo O(1).
    open_list_dict = {}

    # 2. LISTA FECHADA (closed_set): Nós que ja foram completamente explorados.
    # Evita que o algoritmo ande em circulos ou reavalie caminhos ja consolidados.
    closed_set = set()

    # O ponto de partida é o primeiro nó a ser explorado
    heapq.heappush(open_list_heap, start_node)
    open_list_dict[start_node.position] = start_node

    # O loop principal de A* continua enquanto houver nós para explorar na lista aberta
    while open_list_heap:
        # Pega o nó mais promissor (menor custo 'f') da lista aberta
        current_node = heapq.heappop(open_list_heap)

        # Remove o nó do dicionario de controle
        if current_node.position not in open_list_dict:
            continue
        del open_list_dict[current_node.position]

        # Chegamos ao destino, a busca terminou com sucesso
        if current_node.position == end_node.position:
            path = []
            cost = current_node.g # O custo final é o 'g' do nó de destino
            temp = current_node
            # Volta pelo caminho usando os 'pais' de cada nó para montar a rota
            while temp is not None:
                path.append(temp.position)
                temp = temp.parent
            return path[::-1], cost # Retorna o caminho invertido (do inicio ao fim) e o custo total
        
        # Adiciona o nó atual à lista fechada, marcando como "ja explorado"
        closed_set.add(current_node.position)

        # Explora os vizinhos do nó atual (movimentos em 4 direções)
        (row, col) = current_node.position
        for move in [(0,1), (0,-1), (1,0), (-1,0)]: # direita, esquerda, baixo, cima
            next_pos = (row + move[0], col + move[1])

            # --- Validaçao do vizinho ---
            # 1. Esta dentro do mapa?
            if not (0 <= next_pos[0] < len(map_grid) and 0 <= next_pos[1] < len(map_grid[0])):
                continue

            # 2. É um obstáculo (terreno intransponivel)?
            terrain_type = map_grid[next_pos[0]][next_pos[1]]
            if terrain_costs.get(terrain_type, float('inf')) == float('inf'):
                continue

            # 3. Ja foi explorado (esta na lista fechada)?
            if next_pos in closed_set:
                continue

            # --- Calcula os custos para o vizinho ---
            move_cost = terrain_costs[terrain_type]
            g_cost = current_node.g + move_cost
            h_cost = manhattan_distance(next_pos, end_node.position)
            f_cost = g_cost + h_cost

            # Se ja conhecemos um caminho melhor para este vizinho, ignoramos este caminho atual
            if next_pos in open_list_dict and open_list_dict[next_pos].f <= f_cost:
                continue

            # Se este é um caminho melhor, criamos/atualizamos o nó vizinho
            neighbor = Node(next_pos, current_node)
            neighbor.g = g_cost
            neighbor.h = h_cost
            neighbor.f = f_cost

            # Adiciona o vizinho à lista aberta para ser explorado no futuro
            heapq.heappush(open_list_heap, neighbor)
            open_list_dict[neighbor.position] = neighbor

    return None, 0 # Se a lista aberta esvaziar, nao ha caminho possivel.