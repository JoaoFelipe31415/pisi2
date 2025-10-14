import itertools
import time
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

def resolver_flyfood_forca_bruta(coordenadas):
    """
    Recebe as coordenadas dos pontos e encontra a melhor rota via força bruta.
    """
    depot = 'R'
    pontos_entrega = [ponto for ponto in coordenadas if ponto != depot]
    
    min_distancia = float('inf')
    melhor_rota = None
    
    num_permutacoes = len(list(itertools.permutations(pontos_entrega)))
    print(f"\nIniciando Força Bruta. Total de rotas a testar: {num_permutacoes}")
    start_time = time.time()

    for permutacao in itertools.permutations(pontos_entrega):
        distancia_atual = 0
        
        rota_atual = [depot] + list(permutacao)
        

        distancia_atual += calcular_distancia_manhattan(
            coordenadas[rota_atual[0]], 
            coordenadas[rota_atual[1]]
        )
        

        for i in range(1, len(rota_atual) - 1):
            distancia_atual += calcular_distancia_manhattan(
                coordenadas[rota_atual[i]], 
                coordenadas[rota_atual[i+1]]
            )
        

        distancia_atual += calcular_distancia_manhattan(
            coordenadas[rota_atual[-1]], 
            coordenadas[depot]
        )
        
        if distancia_atual < min_distancia:
            min_distancia = distancia_atual
            melhor_rota = rota_atual + [depot] 
            
    end_time = time.time()
    print(f"Processo finalizado em {end_time - start_time:.6f} segundos.")
    
    return melhor_rota, min_distancia

if __name__ == "__main__":
  
    _, _, matriz = ler_matriz_de_arquivo('caso_teste_berlin52_6pts.txt')
    
    if matriz:
        pontos_coordenadas = encontrar_coordenadas(matriz)
        print("\nPontos e suas coordenadas (linha, coluna):")
        print(pontos_coordenadas)

        rota_otima, distancia_otima = resolver_flyfood_forca_bruta(pontos_coordenadas)
 
        print("\n--- Resultado Final ---")
        print(f"Melhor Rota Encontrada: {' -> '.join(rota_otima)}") # type: ignore
        print(f"Distância Total (dronômetros): {distancia_otima}")
