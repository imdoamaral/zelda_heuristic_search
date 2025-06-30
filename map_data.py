import csv

def parse_map_data(file_path):
    """
    Lê um arquivo de mapa CSV e extrai o grid e os pontos de interesse.
    """
    grid = []
    locations = {}
    
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            grid_row = []
            for c, cell in enumerate(row):
                cell_content = cell.strip()
                terrain_type = LEGEND.get(cell_content, 6)
                grid_row.append(terrain_type)
                
                if cell_content in ['L', 'MS', 'E', 'P', 'MA', 'LW']:
                    key = cell_content
                    if key not in locations:
                        locations[key] = []
                    locations[key].append((r, c))

            grid.append(grid_row)
            
    return grid, locations

# --- Legenda de Terrenos e Custos ---
LEGEND = {
    'G': 0, 'S': 1, 'F': 2, 'M': 3, 'A': 4,
    '': 5, 'X': 6,
    'L': 0, 'MS': 0, 'MA': 0, 'LW': 2,
    'E': 5, 'P': 5
}

TERRAIN_COSTS = {
    0: 10, 1: 20, 2: 100, 3: 150, 4: 180,
    5: 10,
    6: float('inf')
}

# --- Carregando Mapas e Localizações ---
HYRULE_MAP_PATH = '/home/israel/zelda_heuristic_search/maps/hyrule_map.csv'
DUNGEON_1_MAP_PATH = '/home/israel/zelda_heuristic_search/maps/dungeon1_map.csv'
DUNGEON_2_MAP_PATH = '/home/israel/zelda_heuristic_search/maps/dungeon2_map.csv'
DUNGEON_3_MAP_PATH = '/home/israel/zelda_heuristic_search/maps/dungeon3_map.csv'

HYRULE_MAP, hyrule_locations = parse_map_data(HYRULE_MAP_PATH)
DUNGEON_1_MAP, dungeon_1_locations = parse_map_data(DUNGEON_1_MAP_PATH)
DUNGEON_2_MAP, dungeon_2_locations = parse_map_data(DUNGEON_2_MAP_PATH)
DUNGEON_3_MAP, dungeon_3_locations = parse_map_data(DUNGEON_3_MAP_PATH)

DUNGEON_MAPS = {
    "dungeon1": DUNGEON_1_MAP,
    "dungeon2": DUNGEON_2_MAP,
    "dungeon3": DUNGEON_3_MAP,
}

# --- Pontos de Interesse (Coordenadas [linha, coluna]) ---
START_POS = hyrule_locations.get('L', [(-1, -1)])[0]
LOST_WOODS_POS = hyrule_locations.get('LW', [(-1,-1)])[0]

# DUNGEON_ENTRANCES: Localizações em Hyrule onde Link entra em uma masmorra (marcado como 'MA' em hyrule_map.csv).
# Estes são os pontos no mapa do mundo.
dungeon_entrances_coords = sorted(hyrule_locations.get('MA', []))
DUNGEON_ENTRANCES = {f"dungeon{i+1}": pos for i, pos in enumerate(dungeon_entrances_coords)}

# DUNGEON_PORTALS: Localizações *dentro* de cada masmorra onde Link aparece ao entrar
# e de onde ele sai de volta para Hyrule (marcado como 'E' nos mapas das masmorras).
DUNGEON_PORTALS = {
    "dungeon1": dungeon_1_locations.get('E', [(-1,-1)])[0],
    "dungeon2": dungeon_2_locations.get('E', [(-1,-1)])[0],
    "dungeon3": dungeon_3_locations.get('E', [(-1,-1)])[0],
}

PENDANT_LOCATIONS = {
    "dungeon1": dungeon_1_locations.get('P', [(-1,-1)])[0],
    "dungeon2": dungeon_2_locations.get('P', [(-1,-1)])[0],
    "dungeon3": dungeon_3_locations.get('P', [(-1,-1)])[0],
}
