"""
ESTRATÉGIA GERAL DO PROGRAMA:

O problema de encontrar a rota ótima para Link é resolvido em duas etapas principais:

1.  **Cálculo de Distâncias (Pathfinding):**
    Primeiro, usamos o algoritmo A* para pré-calcular o caminho e o custo de todas
    os trechos da viagem. Isso inclui ir do início a cada masmorra, de uma masmorra
    a outra, e da última masmorra ao final. Também calculamos o custo interno de
    cada masmorra. Isso é feito na função `calculate_all_costs()`.

2.  **Otimização da Rota (Problema do Caixeiro Viajante - TSP):**
    Com todos os custos já conhecidos, testamos todas as ordens (permutações)
    possíveis para visitar as 3 masmorras. Como são poucas masmorras (3! = 6 rotas),
    podemos simplesmente calcular o custo total de cada uma e escolher a mais barata.
    Isso é feito na função `find_optimal_tour()`.

A visualização final apenas junta os caminhos individuais da rota ótima encontrada.
"""

import itertools
import time
import os
from map_data import (
    HYRULE_MAP, DUNGEON_MAPS, TERRAIN_COSTS,
    START_POS, LOST_WOODS_POS, DUNGEON_ENTRANCES, DUNGEON_PORTALS, PENDANT_LOCATIONS
)
from a_star import a_star_search

def calculate_all_costs():
    """
    Pré-calcula e armazena os custos de todos os segmentos de viagem necessários.
    Isso inclui viagens entre todos os pontos de interesse em Hyrule (início, masmorras, fim)
    e os caminhos internos de cada masmorra (do portal de entrada ao pingente).
    Essa abordagem evita recalcular os mesmos caminhos repetidamente.
    """
    # Define todos os pontos importantes no mapa de Hyrule.
    points_of_interest = {"start": START_POS, **DUNGEON_ENTRANCES, "end": LOST_WOODS_POS}
    costs = {} # Dicionário para armazenar os custos (ex: {('start', 'dungeon1'): 1500})
    paths = {} # Dicionário para armazenar os caminhos (ex: {('start', 'dungeon1'): [(0,0), (0,1), ...]}) 

    # Calcula o custo do caminho entre cada par de pontos de interesse em Hyrule.
    poi_names = list(points_of_interest.keys())
    for i in range(len(poi_names)):
        for j in range(i + 1, len(poi_names)):
            p1_name, p2_name = poi_names[i], poi_names[j]
            p1_pos, p2_pos = points_of_interest[p1_name], points_of_interest[p2_name]
            
            # Usa o A* para encontrar o caminho e o custo.
            path, cost = a_star_search(HYRULE_MAP, TERRAIN_COSTS, p1_pos, p2_pos)
            if path:
                costs[(p1_name, p2_name)] = cost
                costs[(p2_name, p1_name)] = cost # O custo é simétrico.
                paths[(p1_name, p2_name)] = path
                paths[(p2_name, p1_name)] = path[::-1] # O caminho de volta é o inverso.
            else:
                costs[(p1_name, p2_name)] = float('inf')
                costs[(p2_name, p1_name)] = float('inf')

    # Calcula o custo do caminho interno para cada masmorra.
    for name in DUNGEON_ENTRANCES:
        dungeon_map = DUNGEON_MAPS[name]
        portal_pos = DUNGEON_PORTALS[name]   # Ponto de entrada/saída dentro da masmorra.
        pendant_pos = PENDANT_LOCATIONS[name] # Local do pingente.
        path, cost = a_star_search(dungeon_map, TERRAIN_COSTS, portal_pos, pendant_pos)
        if path:
            # O custo para "completar" uma masmorra é o custo para ir do portal ao pingente.
            costs[name] = cost 
            paths[name] = path
        else:
            costs[name] = float('inf')

    return costs, paths

def find_optimal_tour(costs):
    """
    Resolve o Problema do Caixeiro Viajante (TSP) para encontrar a ordem ótima de visitação das masmorras.
    Testa todas as permutações possíveis de masmorras para encontrar a que resulta no menor custo total de viagem.
    """
    dungeons = list(DUNGEON_ENTRANCES.keys())
    all_tours = list(itertools.permutations(dungeons)) # Gera todas as ordens possíveis.
    best_tour, min_total_cost = None, float('inf')

    # Itera sobre cada rota (permutação) possível.
    for tour in all_tours:
        # Custo do início até a primeira masmorra da rota.
        current_cost = costs.get(("start", tour[0]), float('inf'))
        
        # Soma os custos de completar a masmorra e viajar para a próxima.
        for i in range(len(tour) - 1):
            current_cost += costs.get(tour[i], float('inf')) # Custo interno da masmorra atual.
            current_cost += costs.get((tour[i], tour[i+1]), float('inf')) # Custo de viagem para a próxima.
        
        # Adiciona o custo de completar a última masmorra.
        current_cost += costs.get(tour[-1], float('inf'))
        # Adiciona o custo da última masmorra até o destino final (Lost Woods).
        current_cost += costs.get((tour[-1], "end"), float('inf'))

        # Se a rota atual for a mais barata encontrada até agora, atualiza a melhor rota.
        if current_cost < min_total_cost:
            min_total_cost = current_cost
            best_tour = tour

    return best_tour, min_total_cost

def visualize_console_journey(full_path, total_cost):
    """
    Exibe uma animação da jornada de Link no console, mostrando o caminho percorrido
    e o personagem se movendo pelo mapa de Hyrule.
    """
    # Códigos de Cores ANSI para estilizar a saída no terminal.
    class Colors:
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        RED = '\033[91m'
        GREY = '\033[90m'
        WHITE = '\033[97m'
        RESET = '\033[0m'

    # Mapeia os tipos de terreno para caracteres de exibição.
    TERRAIN_CHARS = {
        0: ' ',  # Grama
        1: '.',  # Areia
        2: 'F',  # Floresta
        3: 'M',  # Montanha
        4: '~',  # Água
        5: ' ',  # Chão da Masmorra (não usado em Hyrule)
        6: '#',  # Parede (não usado em Hyrule)
    }

    path_set = set()
    current_path_cost = 0

    # Itera por cada passo do caminho completo para criar a animação.
    for i, pos in enumerate(full_path):
        os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela do console.

        path_set.add(pos) # Adiciona a posição atual ao conjunto de posições já visitadas.

        # Calcula o custo acumulado até o ponto atual.
        if i > 0:
            prev_pos = full_path[i-1]
            terrain_type = HYRULE_MAP[prev_pos[0]][prev_pos[1]]
            current_path_cost += TERRAIN_COSTS.get(terrain_type, 0)

        print("Jornada de Link em Hyrule (Console)")
        print("-" * 60)

        # Desenha o mapa linha por linha.
        for r_idx, row in enumerate(HYRULE_MAP):
            row_str = ""
            for c_idx, terrain in enumerate(row):
                char = TERRAIN_CHARS.get(terrain, ' ')
                
                if (r_idx, c_idx) == pos:
                    row_str += f'{Colors.RED}L{Colors.RESET}' # Posição atual de Link.
                elif (r_idx, c_idx) in path_set:
                    row_str += f'{Colors.YELLOW}·{Colors.RESET}' # Caminho já percorrido.
                else:
                    row_str += char # Terreno normal.
            print(row_str)

        print("-" * 60)
        print(f"Passo: {i+1}/{len(full_path)} | Posição: {pos} | Custo Acumulado: {int(current_path_cost)}")
        print(f"Custo Total da Rota Ótima: {int(total_cost)}")
        time.sleep(0.05) # Pausa para criar o efeito de animação.

    print("\nJornada no console concluída!")

def main():
    """
    Função principal que orquestra a execução do programa.
    """
    print("Calculando todos os custos de viagem...")
    all_costs, all_paths = calculate_all_costs()

    print("\nEncontrando a rota ótima...")
    optimal_tour, total_cost = find_optimal_tour(all_costs)

    if not optimal_tour or total_cost == float('inf'):
        print("\nNão foi possível determinar uma rota ótima.")
        return

    print(f"\nA melhor rota encontrada é: start -> {' -> '.join(optimal_tour)} -> Lost Woods")
    print(f"Custo total estimado da jornada: {int(total_cost)}")

    # Monta o caminho completo da jornada ótima para a visualização no console.
    full_path_console = []
    # 1. Caminho do início até a primeira masmorra.
    full_path_console.extend(all_paths[("start", optimal_tour[0])])
    # 2. Caminho entre as masmorras.
    for i in range(len(optimal_tour) - 1):
        # Adiciona o caminho da masmorra i para a masmorra i+1, exceto o primeiro ponto para evitar duplicatas.
        full_path_console.extend(all_paths[(optimal_tour[i], optimal_tour[i+1])][1:])
    # 3. Caminho da última masmorra até o final.
    full_path_console.extend(all_paths[(optimal_tour[-1], "end")][1:])

    # Inicia a visualização da jornada.
    visualize_console_journey(full_path_console, total_cost)

    

if __name__ == "__main__":
    # Garante que o código dentro deste bloco só será executado quando o script for rodado diretamente.
    main()
