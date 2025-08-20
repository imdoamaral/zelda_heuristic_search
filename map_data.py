import csv
import os

def parse_map_data(file_path):
    """Lê um CSV, converte os caracteres em números (usando a legenda) e guarda as coordenadas dos pontos de interesse"""
    grid = [] # matriz com o novo mapa
    locations = {} # pontos de interesse

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader): # faz um loop sobre cada linha do csv. r = indice e row = valores de cada linha do CSV
            grid_row = []
            for c, cell in enumerate(row):
                cell_content = cell.strip() # converte cada caractere do CSV para um ID numerico de terreno usando a legenda
                terrain_type = LEGEND.get(cell_content, 6) # se o caractere nao for encontrado, assume-se que é uma parede (6)
                grid_row.append(terrain_type)

                # Se a celula representa um ponto de interesse, armazena suas coordenadas
                if cell_content in ['L', 'MS', 'E', 'P', 'MA', 'LW']:
                    key = cell_content
                    if key not in locations:
                        locations[key] = []
                    locations[key].append((r, c))

            grid.append(grid_row)

    return grid, locations

# --- Legenda de Terrenos e Custos ---
# Mapeia os caracteres do arquivos CSV para um ID numerico de terreno
LEGEND = {
    'G':0, 'S':1, 'F':2, 'M':3, 'A':4,  # terrenos de hyrule
    '':5, 'X':6,                        # terrenos de masmorra (chao e parede)
    'L':0, 'MS':0, 'MA':0, 'LW':2,      # pontos de interesse (sobrepoem terrenos)
    'E':5, 'P':5                        # pontos de interesse em masmorras (entrada, portal)
}

# Define o custo de movimento para cada tipo de terreno
# Terrenos com custo 'inf' (infinito) sao instransponiveis
TERRAIN_COSTS = {
    0: 10,  # Grama
    1: 20,  # Areia
    2: 100, # Floresta
    3: 150, # Montanha
    4: 180, # Água
    5: 10,  # Chao da masmorra
    6: float('inf') # Parede
}

# --- Carrega Mapas e Localizaçoes ---
# Obtem o caminho absoluto para o diretorio onde este script (map_Data.py) esta localizado
script_dir = os.path.dirname(os.path.abspath(__file__))

# Junta o caminho do diretorio do script com o nome da subpasta 'maps' e o nome do arquivo do mapa
HYRULE_MAP_PATH = os.path.join(script_dir, 'maps', 'hyrule_map.csv')
DUNGEON_1_MAP_PATH = os.path.join(script_dir, 'maps', 'dungeon1_map.csv')
DUNGEON_2_MAP_PATH = os.path.join(script_dir, 'maps', 'dungeon2_map.csv')
DUNGEON_3_MAP_PATH = os.path.join(script_dir, 'maps', 'dungeon3_map.csv')

# Carrega os dados de cada mapa usando a funçao de parsing (transformar)
HYRULE_MAP, hyrule_locations = parse_map_data(HYRULE_MAP_PATH)
DUNGEON_1_MAP, dungeon_1_locations = parse_map_data(DUNGEON_1_MAP_PATH)
DUNGEON_2_MAP, dungeon_2_locations = parse_map_data(DUNGEON_2_MAP_PATH)
DUNGEON_3_MAP, dungeon_3_locations = parse_map_data(DUNGEON_3_MAP_PATH)

# Agrupa os mapas das masmorras em um dicionario para facil acesso
DUNGEON_MAPS = {
    "dungeon1": DUNGEON_1_MAP,
    "dungeon2": DUNGEON_2_MAP,
    "dungeon3": DUNGEON_3_MAP,
}

# --- Pontos de interesse (Coordenadas [linha, coluna]) ---
# O valor (-1, -1) é usado como valor padrao pra indicar que a coordenada nao foi encontrada no mapa

# Posiçao inicial de Link no mapa de Hyrule
START_POS = hyrule_locations.get('L', [(-1, -1)])[0]

# Posicao da entrada para Lost Woods, o objetivo final
LOST_WOODS_POS = hyrule_locations.get('LW', [(-1, -1)])[0]

# DUNGEON_ENTRANCES: Mapeia o nome de cada masmorra a a sua coordenada de entrada no mapa de hyrule
dungeon_entrances_coords = sorted(hyrule_locations.get('MA', []))
DUNGEON_ENTRANCES = {f"dungeon{i+1}": pos for i, pos in enumerate(dungeon_entrances_coords)}

"""
DUNGEON_ENTRANCES = {
    "dungeon1": (2, 5),
    "dungeon2": (7, 3),
    "dungeon3": (10, 8)
}
"""

# DUNGEON_PORTALS: Mapeia o noem de cada masmorra a a sua coordenada de portal *dentro* do mapa da masmorra
# Este e o ponto onde Link aparece ao entrar (marcado como 'E')
DUNGEON_PORTALS = {
    "dungeon1": dungeon_1_locations.get('E', [(-1,-1)])[0],
    "dungeon2": dungeon_2_locations.get('E', [(-1,-1)])[0],
    "dungeon3": dungeon_3_locations.get('E', [(-1,-1)])[0],
}

# PENDANT_LOCATIONS: Mapeia o nome de cada masmorra a a localizaçao do seu respectivo pingente (marcado como 'P')
PENDANT_LOCATIONS = {
    "dungeon1": dungeon_1_locations.get('P', [(-1,-1)])[0],
    "dungeon2": dungeon_2_locations.get('P', [(-1,-1)])[0],
    "dungeon3": dungeon_3_locations.get('P', [(-1,-1)])[0],
}

if __name__ == '__main__': # verifica se o script esta sendo rodado diretamente
    # se o modulo acima estiver sendo importado de outro script, nao executa esse main.
    print("Hyrule Map Grid: ")
    for row in HYRULE_MAP:
        print(row)
    print("\nHyrule Locations: ", hyrule_locations)
    print("\nDungeon 1 Map Grid: ")
    for row in DUNGEON_1_MAP:
        print(row)
    print("\nDungeon 1 Locations: ", dungeon_1_locations)
    print("\nStart Position: ", START_POS)
    print("Dungeon Entrances: ", DUNGEON_ENTRANCES)
    print("Dungeon Portals:", DUNGEON_PORTALS)
    print("Pendant Locations: ", PENDANT_LOCATIONS)
    print("Lost Woods Position: ", LOST_WOODS_POS)