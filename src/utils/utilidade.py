import os

def ler_matriz_de_arquivo(nome_arquivo):
    caminho = os.path.join(os.path.dirname(__file__), '..','..', 'data', nome_arquivo)
    matriz = []
    with open(caminho, 'r') as f:
        primeira_linha = f.readline()
        M = int(primeira_linha[0])
        N = int(primeira_linha[1])
        
        for _ in range(M):
            linha_arquivo = f.readline()
            aux = []
            for caracter in linha_arquivo:
                if caracter == "\n":
                    continue
                aux.append(caracter)
            matriz.append(aux)

    return M, N, matriz

def encontrar_coordenadas(matriz):
    """Varre a matriz e retorna um dicionário com as coordenadas de cada ponto."""
    coordenadas = {}
    for r, linha in enumerate(matriz):
        for c, ponto in enumerate(linha):
            if ponto != '0':
                coordenadas[ponto] = (r, c) 
    return coordenadas

def calcular_distancia_manhattan(coord1, coord2):
    """Calcula a distância entre dois pontos (movimento de drone)."""
    r1, c1 = coord1
    r2, c2 = coord2
    return abs(r1 - r2) + abs(c1 - c2)