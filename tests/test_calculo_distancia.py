from src.genetic_algorthm.genetic_algoritm import (
    construir_matriz_distancias,
    reduzir_matriz_distância,
    calcular_custo_rota,
)


def test_calculo_de_custo_inclui_retorno_a_R():
    # Montamos um conjunto de coordenadas simples (R, A, B) em linha
    # R-(0,0), A-(0,1), B-(0,2)
    coordenadas = {
        'R': (0, 0),
        'A': (0, 1),
        'B': (0, 2),
    }

    # Construir matriz reduzida usada pelo AG
    dist_full, nomes, map_idx = construir_matriz_distancias(coordenadas)
    dist_reduzida = reduzir_matriz_distância(dist_full)

    # Rota sem repetir R no final — a função deve considerar o retorno (R <- B)
    rota = ['R', 'A', 'B']

    # Distâncias manhattan: R-A=1, A-B=1, B-R=2 => total esperado = 4
    custo = calcular_custo_rota(rota, dist_reduzida, map_idx)
    print("Custo calculado da rota:", custo)
    assert custo == 4


test_calculo_de_custo_inclui_retorno_a_R()