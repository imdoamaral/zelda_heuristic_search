import csv

def parse_map_data(file_path):
    """
    Lê um arquivo de mapa no formato CSV e o converte em uma estrutura de dados para o jogo.
    A função extrai o grid do mapa, onde cada célula tem um tipo de terreno, e também
    mapeia a localização de pontos de interesse (como Link, entradas de masmorras, etc.).
    """
    grid = []
    locations = {}
    
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            grid_row = []
            for c, cell in enumerate(row):
                cell_content = cell.strip()
                # Converte o caractere do CSV para um ID numérico de terreno usando a legenda.
                # Se o caractere não for encontrado, assume-se que é uma parede (6).
                terrain_type = LEGEND.get(cell_content, 6)
                grid_row.append(terrain_type)
                
                # Se a célula representa um ponto de interesse, armazena suas coordenadas.
                if cell_content in ['L', 'MS', 'E', 'P', 'MA', 'LW']:
                    key = cell_content
                    if key not in locations:
                        locations[key] = []
                    locations[key].append((r, c))

            grid.append(grid_row)
            
    return grid, locations

# --- Legenda de Terrenos e Custos ---
# Mapeia os caracteres do arquivo CSV para um ID numérico de terreno.
LEGEND = {
    'G': 0, 'S': 1, 'F': 2, 'M': 3, 'A': 4,  # Terrenos de Hyrule
    '': 5, 'X': 6,                           # Terrenos de Masmorra (chão e parede)
    'L': 0, 'MS': 0, 'MA': 0, 'LW': 2,        # Pontos de interesse sobrepõem terrenos (ex: Link está na grama)
    'E': 5, 'P': 5                           # Pontos de interesse em masmorras (ex: Entrada está no chão)
}

# Define o custo de movimento para cada tipo de terreno.
# Terrenos com custo 'inf' (infinito) são intransponíveis.
TERRAIN_COSTS = {
    0: 10,  # Grama
    1: 20,  # Areia
    2: 100, # Floresta
    3: 150, # Montanha
    4: 180, # Água
    5: 10,  # Chão da Masmorra
    6: float('inf') # Parede
}

# --- Carregando Mapas e Localizações ---
# Caminhos absolutos para os arquivos de mapa.
HYRULE_MAP_PATH = '/home/israel/zelda_heuristic_search/maps/hyrule_map.csv'
DUNGEON_1_MAP_PATH = '/home/israel/zelda_heuristic_search/maps/dungeon1_map.csv'
DUNGEON_2_MAP_PATH = '/home/israel/zelda_heuristic_search/maps/dungeon2_map.csv'
DUNGEON_3_MAP_PATH = '/home/israel/zelda_heuristic_search/maps/dungeon3_map.csv'

# Carrega os dados de cada mapa usando a função de parsing.
HYRULE_MAP, hyrule_locations = parse_map_data(HYRULE_MAP_PATH)
DUNGEON_1_MAP, dungeon_1_locations = parse_map_data(DUNGEON_1_MAP_PATH)
DUNGEON_2_MAP, dungeon_2_locations = parse_map_data(DUNGEON_2_MAP_PATH)
DUNGEON_3_MAP, dungeon_3_locations = parse_map_data(DUNGEON_3_MAP_PATH)

# Agrupa os mapas das masmorras em um dicionário para fácil acesso.
DUNGEON_MAPS = {
    "dungeon1": DUNGEON_1_MAP,
    "dungeon2": DUNGEON_2_MAP,
    "dungeon3": DUNGE_3_MAP,
}

# --- Pontos de Interesse (Coordenadas [linha, coluna]) ---
# Posição inicial de Link no mapa de Hyrule.
START_POS = hyrule_locations.get('L', [(-1, -1)])[0]
# Posição da entrada para Lost Woods, o objetivo final.
LOST_WOODS_POS = hyrule_locations.get('LW', [(-1,-1)])[0]

# DUNGEON_ENTRANCES: Mapeia o nome de cada masmorra à sua coordenada de entrada no mapa de Hyrule.
# Estas são as localizações marcadas como 'MA' no mapa principal.
dungeon_entrances_coords = sorted(hyrule_locations.get('MA', []))
DUNGEON_ENTRANCES = {f"dungeon{i+1}": pos for i, pos in enumerate(dungeon_entrances_coords)}

# DUNGEON_PORTALS: Mapeia o nome de cada masmorra à sua coordenada de "portal" *dentro* do mapa da masmorra.
# Este é o ponto onde Link aparece ao entrar (marcado como 'E').
DUNGEON_PORTALS = {
    "dungeon1": dungeon_1_locations.get('E', [(-1,-1)])[0],
    "dungeon2": dungeon_2_locations.get('E', [(-1,-1)])[0],
    "dungeon3": dungeon_3_locations.get('E', [(-1,-1)])[0],
}

# PENDANT_LOCATIONS: Mapeia o nome de cada masmorra à localização do seu respectivo pingente (marcado como 'P').
PENDANT_LOCATIONS = {
    "dungeon1": dungeon_1_locations.get('P', [(-1,-1)])[0],
    "dungeon2": dungeon_2_locations.get('P', [(-1,-1)])[0],
    "dungeon3": dungeon_3_locations.get('P', [(-1,-1)])[0],
}


if __name__ == '__main__':
    # Este bloco é executado apenas quando o script é rodado diretamente.
    # Útil para depuração e verificação rápida dos dados carregados.
    print("Hyrule Map Grid:")
    for row in HYRULE_MAP:
        print(row)
    print("\nHyrule Locations:", hyrule_locations)
    print("\nDungeon 1 Map Grid:")
    for row in DUNGEON_1_MAP:
        print(row)
    print("\nDungeon 1 Locations:", dungeon_1_locations)
    print("\nStart Position:", START_POS)
    print("Dungeon Entrances:", DUNGEON_ENTRANCES)
    print("Dungeon Portals:", DUNGEON_PORTALS)
    print("Pendant Locations:", PENDANT_LOCATIONS)
    print("Lost Woods Position:", LOST_WOODS_POS)
