import itertools
import time
from tests_cases.build_tests_cases import gerar_casos_berlin52
from src.utils.utilidade import calcular_distancia_manhattan, encontrar_coordenadas, ler_matriz_de_arquivo


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
    
    _, _, matriz = ler_matriz_de_arquivo('input.txt')
    
    if matriz:
        pontos_coordenadas = encontrar_coordenadas(matriz)
        print("\nPontos e suas coordenadas (linha, coluna):")
        print(pontos_coordenadas)

        rota_otima, distancia_otima = resolver_flyfood_forca_bruta(pontos_coordenadas)
 
        print("\n--- Resultado Final ---")
        print(f"Melhor Rota Encontrada: {' -> '.join(rota_otima)}") # type: ignore
        print(f"Distância Total (dronômetros): {distancia_otima}")
