import itertools
import time
import os
from map_data import (
    HYRULE_MAP, DUNGEON_MAPS, TERRAIN_COSTS,
    START_POS, LOST_WOODS_POS, DUNGEON_ENTRANCES, DUNGEON_PORTALS, PENDANT_LOCATIONS
)
from a_star import a_star_search

def calculate_all_costs():
    """Calcula e armazena o custo de todos os segmentos de viagem necessários."""
    # points_of_interest: Inclui o ponto de partida, todas as entradas das masmorras (do mapa de Hyrule),
    # e o destino final (entrada de Lost Woods).
    points_of_interest = {"start": START_POS, **DUNGEON_ENTRANCES, "end": LOST_WOODS_POS}
    costs = {}
    paths = {}

    poi_names = list(points_of_interest.keys())
    for i in range(len(poi_names)):
        for j in range(i + 1, len(poi_names)):
            p1_name, p2_name = poi_names[i], poi_names[j]
            p1_pos, p2_pos = points_of_interest[p1_name], points_of_interest[p2_name]
            path, cost = a_star_search(HYRULE_MAP, TERRAIN_COSTS, p1_pos, p2_pos)
            if path:
                costs[(p1_name, p2_name)] = cost
                costs[(p2_name, p1_name)] = cost
                paths[(p1_name, p2_name)] = path
                paths[(p2_name, p1_name)] = path[::-1]
            else:
                costs[(p1_name, p2_name)] = float('inf')
                costs[(p2_name, p1_name)] = float('inf')

    for name in DUNGEON_ENTRANCES: # Itera por cada masmorra definida por sua entrada em Hyrule
        dungeon_map = DUNGEON_MAPS[name]
        portal_pos = DUNGEON_PORTALS[name] # O ponto de entrada/saída *dentro* da masmorra
        pendant_pos = PENDANT_LOCATIONS[name]
        path, cost = a_star_search(dungeon_map, TERRAIN_COSTS, portal_pos, pendant_pos)
        if path:
            costs[name] = cost
            paths[name] = path
        else:
            costs[name] = float('inf')

    return costs, paths

def find_optimal_tour(costs):
    """Encontra a ordem ótima de visitação das masmorras com o menor custo total."""
    dungeons = list(DUNGEON_ENTRANCES.keys())
    all_tours = list(itertools.permutations(dungeons))
    best_tour, min_total_cost = None, float('inf')

    for tour in all_tours:
        current_cost = costs.get(("start", tour[0]), float('inf'))
        for i in range(len(tour) - 1):
            current_cost += costs.get(tour[i], float('inf'))
            current_cost += costs.get((tour[i], tour[i+1]), float('inf'))
        
        current_cost += costs.get(tour[-1], float('inf'))
        current_cost += costs.get((tour[-1], "end"), float('inf'))

        if current_cost < min_total_cost:
            min_total_cost = current_cost
            best_tour = tour

    return best_tour, min_total_cost

def visualize_console_journey(full_path, total_cost):
    # Códigos de Cores ANSI para o Terminal
    class Colors:
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        RED = '\033[91m'
        GREY = '\033[90m'
        WHITE = '\033[97m'
        RESET = '\033[0m'

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

    for i, pos in enumerate(full_path):
        os.system('cls' if os.name == 'nt' else 'clear') # Limpa o console

        path_set.add(pos)

        # Calcula o custo acumulado
        if i > 0:
            prev_pos = full_path[i-1]
            terrain_type = HYRULE_MAP[prev_pos[0]][prev_pos[1]]
            current_path_cost += TERRAIN_COSTS.get(terrain_type, 0)

        print("Jornada de Link em Hyrule (Console)")
        print("-" * 60)

        for r_idx, row in enumerate(HYRULE_MAP):
            row_str = ""
            for c_idx, terrain in enumerate(row):
                char = TERRAIN_CHARS.get(terrain, ' ')
                
                if (r_idx, c_idx) == pos:
                    row_str += f'{Colors.RED}L{Colors.RESET}' # Link atual
                elif (r_idx, c_idx) in path_set:
                    row_str += f'{Colors.YELLOW}·{Colors.RESET}' # Caminho percorrido
                else:
                    row_str += char
            print(row_str)

        print("-" * 60)
        print(f"Passo: {i+1}/{len(full_path)} | Posição: {pos} | Custo Acumulado: {current_path_cost}")
        print(f"Custo Total da Rota Ótima: {total_cost}")
        time.sleep(0.05) # Pequeno atraso para visualização

    print("\nJornada no console concluída!")

def main():
    print("Calculando todos os custos de viagem...")
    all_costs, all_paths = calculate_all_costs()

    print("\nEncontrando a rota ótima...")
    optimal_tour, total_cost = find_optimal_tour(all_costs)

    if not optimal_tour or total_cost == float('inf'):
        print("\nNão foi possível determinar uma rota ótima.")
        return

    print(f"\nA melhor rota encontrada é: start -> {' -> '.join(optimal_tour)} -> Lost Woods")
    print(f"Custo total estimado da jornada: {total_cost}")

    # Montar o caminho completo para visualização no console
    full_path_console = []
    full_path_console.extend(all_paths[("start", optimal_tour[0])])
    for i in range(len(optimal_tour) - 1):
        full_path_console.extend(all_paths[(optimal_tour[i], optimal_tour[i+1])][1:])
    full_path_console.extend(all_paths[(optimal_tour[-1], "end")][1:])

    visualize_console_journey(full_path_console, total_cost)

    

if __name__ == "__main__":
    main()