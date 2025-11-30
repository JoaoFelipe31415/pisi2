
def calcular_distancia_manhattan(coord1, coord2):
    """Calcula a distância de Manhattan entre duas coordenadas."""
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def transformar_grid_em_tsplib(path_arquivo):
    coordenadas = {}
    
    with open(path_arquivo, 'r') as objArq:
        # Lê dimensões
        linha, coluna = map(int, objArq.readline().split())

        id_ponto = 1 # Contador para criar IDs únicos (1, 2, 3...) para os pontos de entrega
        
        for i in range(linha):
            linha_arquivo = objArq.readline()
            lista_valores = linha_arquivo.split()
            
            for j in range(coluna):
                
                if lista_valores[j] != '0':
                    coordenadas[id_ponto] = (i, j) # Salva (linha, coluna)
                    id_ponto += 1
    
    # Agora calculamos as distâncias APENAS entre os pontos que encontramos
    distancias = {}
    ids_encontrados = list(coordenadas.keys()) # Ex: [1, 2, 3, 4]
    
    for i in range(len(ids_encontrados)):
        for j in range(i + 1, len(ids_encontrados)):
            id1 = ids_encontrados[i]
            id2 = ids_encontrados[j]
            
            dist = calcular_distancia_manhattan(coordenadas[id1], coordenadas[id2])
            
            distancias[(id1, id2)] = dist
            distancias[(id2, id1)] = dist
            
    return distancias, id_ponto - 1  

