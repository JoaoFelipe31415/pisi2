from src.utils.utilidade import calcular_distancia_manhattan, encontrar_coordenadas, ler_matriz_de_arquivo
import time

def resolver_flyfood_vizinho_mais_proximo(coordenadas):
    """
    Recebe as coordenadas dos pontos e encontra uma rota usando a heurística
    do vizinho mais próximo.
    """
    print(f"\nIniciando Heurística do Vizinho Mais Próximo.")
    start_time = time.time()

    depot = 'R'
    # Cria uma lista de pontos que ainda precisam ser visitados
    pontos_a_visitar = list(coordenadas.keys())
    pontos_a_visitar.remove(depot)
    
    rota_final = [depot]
    ponto_atual = depot
    distancia_total = 0
    
    # Loop principal: continua até que todos os pontos de entrega tenham sido visitados
    while pontos_a_visitar:
        vizinho_mais_proximo = None
        menor_distancia_passo = float('inf')
        
        # Encontra o ponto não visitado mais próximo do ponto atual
        for proximo_ponto in pontos_a_visitar:
            distancia = calcular_distancia_manhattan(
                coordenadas[ponto_atual], 
                coordenadas[proximo_ponto]
            )
            
            if distancia < menor_distancia_passo:
                menor_distancia_passo = distancia
                vizinho_mais_proximo = proximo_ponto
        
        # Atualiza a rota, a distância total e o ponto atual
        distancia_total += menor_distancia_passo
        ponto_atual = vizinho_mais_proximo
        rota_final.append(ponto_atual) # type: ignore
        pontos_a_visitar.remove(ponto_atual) # Marca o ponto como visitado
        
    # Adiciona a distância de volta ao depósito ('R')
    distancia_total += calcular_distancia_manhattan(
        coordenadas[rota_final[-1]], 
        coordenadas[depot]
    )
    rota_final.append(depot)
    
    end_time = time.time()
    print(f"Processo (Vizinho Mais Próximo) finalizado em {end_time - start_time:.6f} segundos.")
    
    return rota_final, distancia_total


if __name__ == "__main__":
    
    _, _, matriz = ler_matriz_de_arquivo('input.txt')
    
    if matriz:
        pontos_coordenadas = encontrar_coordenadas(matriz)
        print("\nPontos e suas coordenadas (linha, coluna):")
        print(pontos_coordenadas)

        rota_otima, distancia_otima = resolver_flyfood_vizinho_mais_proximo(pontos_coordenadas)
 
        print("\n--- Resultado Final ---")
        print(f"Melhor Rota Encontrada: {' -> '.join(rota_otima)}") # type: ignore
        print(f"Distância Total (dronômetros): {distancia_otima}")