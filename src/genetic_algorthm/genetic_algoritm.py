import random
import numpy as np
import matplotlib.pyplot as plt
import time
import os


def ler_matriz_de_arquivo(nome_arquivo):
    caminho = os.path.join(os.path.dirname(__file__), '..','..', 'data', nome_arquivo)
    matriz = []
    with open(caminho, 'r') as f:
        primeira_linha = f.readline().split()
        M = int(primeira_linha[0])
        N = int(primeira_linha[1])
        
        for _ in range(M):
            linha_arquivo = f.readline().split()
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

def reduzir_matriz_distância(dist_matrix):
    """Armazena apenas os valores acima da diagonal principal da matriz de distâncias."""
    n = dist_matrix.shape[0]
    reduced_matrix = []
    for i in range(n):
        for j in range(i + 1, n):
            reduced_matrix.append(dist_matrix[i, j])
    return np.array(reduced_matrix)

#  FUNÇÕES DE INTERFACE E CÁLCULO PARA O AG 

def construir_matriz_distancias(coordenadas):
    """Usa as funções do usuário para construir a matriz de distâncias para o AG."""
    nomes_pontos = list(coordenadas.keys())
    n = len(nomes_pontos)
    map_idx = {nome: i for i, nome in enumerate(nomes_pontos)}
    dist_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):              
            ponto1_nome = nomes_pontos[i]
            ponto2_nome = nomes_pontos[j]
            
            coord1 = coordenadas[ponto1_nome]
            coord2 = coordenadas[ponto2_nome]
            
            # Utiliza a função de cálculo de distância fornecida
            dist = calcular_distancia_manhattan(coord1, coord2)
            dist_matrix[i, j] = dist_matrix[j, i] = dist
            
    return dist_matrix, nomes_pontos, map_idx

def calcular_custo_rota(rota, dist_matrix, map_idx):
    """Calcula o custo total de uma rota usando a matriz de distâncias reduzida (apenas triângulo superior)."""
    
    custo = 0
    n = len(map_idx)
    
    for i in range(len(rota)):
        idx1 = map_idx[rota[i]]
        idx2 = map_idx[rota[(i + 1) % len(rota)]]
        
        if idx1 == idx2:
            continue
            
        # Garante que idx1 < idx2 para acessar o triângulo superior
        if idx1 > idx2:
            idx1, idx2 = idx2, idx1
            
        # Fórmula para mapear (i, j) para índice do vetor 1D (sendo i < j)
        # k = n*i - i*(i+1)/2 + j - i - 1
        k = int(n * idx1 - (idx1 * (idx1 + 1) // 2) + idx2 - idx1 - 1)
        
        custo += dist_matrix[k]
    return custo

# OPERADORES GENÉTICOS 

def criar_populacao_inicial(nomes_pontos, tamanho_populacao):
    """Cria uma população inicial de rotas aleatórias."""
    populacao = []
    ponto_inicial = 'R' # Ponto de partida fixo para o FlyFood
    ponto_destino = 'R' # Ponto de retorno fixo para o FlyFood
    outros_pontos = [p for p in nomes_pontos if p != ponto_inicial]
    
    for _ in range(tamanho_populacao):
        rota_aleatoria = random.sample(outros_pontos, len(outros_pontos))
        individuo = [ponto_inicial] + rota_aleatoria 
        populacao.append(individuo)
        
    return populacao

def ranquear_rotas(populacao, dist_matrix, map_idx):
    """Calcula a aptidão (fitness) de cada rota e as ordena da melhor para a pior."""
    resultados_aptidao = {}
    for i, individuo in enumerate(populacao):
        resultados_aptidao[i] = 1 / calcular_custo_rota(individuo, dist_matrix, map_idx)
    
    return sorted(resultados_aptidao.items(), key=lambda x: x[1], reverse=True)

def selecao(pop_ranqueada, tamanho_elite):
    """Seleciona os pais para a próxima geração, incluindo elitismo."""
    indices_selecionados = []
    
    for i in range(tamanho_elite):
        indices_selecionados.append(pop_ranqueada[i][0])
    
    aptidao_acumulada = [sum([x[1] for x in pop_ranqueada[:i+1]]) for i in range(len(pop_ranqueada))]
    
    for _ in range(len(pop_ranqueada) - tamanho_elite):
        ponto_aleatorio = random.random() * aptidao_acumulada[-1]
        for i in range(len(pop_ranqueada)):
            if ponto_aleatorio <= aptidao_acumulada[i]:
                indices_selecionados.append(pop_ranqueada[i][0])
                break
                
    return indices_selecionados

def cruzamento(pai1, pai2):
    """Gera um filho a partir de dois pais usando Ordered Crossover (OX1)."""
    # Garante que a posição 0 (ponto de partida) é sempre 'R' e
    # aplica o OX1 apenas nas posições [1..n-1].
    filho = [None] * len(pai1)
    filho[0] = 'R'

    inicio, fim = sorted(random.sample(range(1, len(pai1)), 2))
    segmento_pai1 = pai1[inicio:fim]
    
    filho[inicio:fim] = segmento_pai1
    
    ponteiro_pai2 = 0
    # Preenche apenas posições a partir de 1 (não tocamos no índice 0 que é 'R')
    for i in range(1, len(filho)):
        if filho[i] is None:
            # pula elementos do pai2 que estão no segmento herdado do pai1
            # e pula também o ponto 'R' — não queremos duplicá-lo fora do índice 0
            while ponteiro_pai2 < len(pai2) and (pai2[ponteiro_pai2] in segmento_pai1 or pai2[ponteiro_pai2] == 'R'):
                ponteiro_pai2 += 1
            if ponteiro_pai2 < len(pai2):
                filho[i] = pai2[ponteiro_pai2]
                ponteiro_pai2 += 1
            else:
                # fallback seguro: preenche com um elemento válido encontrado na outra parentela
                for v in pai1[1:]:
                    if v not in filho:
                        filho[i] = v
                        break
            
    return filho

def mutacao(individuo, taxa_mutacao):
    """Aplica uma mutação de troca (swap) em um indivíduo."""
    # Nunca alteramos a posição 0, que é o ponto inicial fixo 'R'.
    for i in range(1, len(individuo)):
        if random.random() < taxa_mutacao:
            j = random.randint(1, len(individuo) - 1)
            individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

def proxima_geracao(populacao_atual, pop_ranqueada, tamanho_elite, taxa_mutacao):
    """Cria a próxima geração aplicando os operadores genéticos."""
    indices_pais = selecao(pop_ranqueada, tamanho_elite)
    pool_de_pais = [populacao_atual[i] for i in indices_pais]
    
    proxima_geracao = []
    
    # Mantém elitismo mas copia explicitamente os indivíduos (para evitar aliasing)
    for i in range(tamanho_elite):
        elite_copy = pool_de_pais[i].copy()
        # força garantia: o primeiro elemento deve ser 'R'
        if len(elite_copy) > 0:
            elite_copy[0] = 'R'
        proxima_geracao.append(elite_copy)
    
    for i in range(tamanho_elite, len(pool_de_pais)):
        pai1 = random.choice(pool_de_pais)
        pai2 = random.choice(pool_de_pais)
        filho = cruzamento(pai1, pai2)
        filho = mutacao(filho, taxa_mutacao)
        # reforça invariantes: a rota sempre deve começar em 'R'
        if len(filho) > 0:
            filho[0] = 'R'
        proxima_geracao.append(filho)
        
    return proxima_geracao

#  FUNÇÃO PRINCIPAL E VISUALIZAÇÃO 

def plotar_rota(coordenadas, rota, titulo="Rota"):
    """Plota a rota encontrada usando Matplotlib."""
    plt.figure(figsize=(8, 6))
    # Invertendo (linha, coluna) para (x, y) para um gráfico padrão
    x_coords = [coordenadas[p][1] for p in rota]
    y_coords = [coordenadas[p][0] for p in rota]
    
    x_coords.append(coordenadas[rota[0]][1])
    y_coords.append(coordenadas[rota[0]][0])
    
    plt.plot(x_coords, y_coords, 'o-')
    
    for ponto_id, coords in coordenadas.items():
        plt.text(coords[1], coords[0], f' {ponto_id}', fontsize=12)
        
    plt.title(titulo)
    plt.xlabel("Coordenada Coluna (X)")
    plt.ylabel("Coordenada Linha (Y)")
    # Inverte o eixo Y para que (0,0) fique no topo, como na matriz
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()

def resolver_flyfood_com_ag(nome_arquivo, geracoes, tam_pop, taxa_elite, taxa_mutacao):
    """Função principal que executa o Algoritmo Genético para o FlyFood."""
    print(f"\nIniciando Algoritmo Genético para '{nome_arquivo}'...")
    start_time = time.time()
    
    # Passo 1: Usar as funções para carregar os dados
    _, _, matriz = ler_matriz_de_arquivo(nome_arquivo)
    coordenadas = encontrar_coordenadas(matriz)

    
    # Passo 2: Construir a matriz de distâncias
    dist_matrix_full, nomes_pontos, map_idx = construir_matriz_distancias(coordenadas)
    dist_matrix = reduzir_matriz_distância(dist_matrix_full)
    
    # Passo 3: Executar o AG
    populacao = criar_populacao_inicial(nomes_pontos, tam_pop)
    
    
    melhor_distancia_inicial = calcular_custo_rota(populacao[0], dist_matrix, map_idx)
    print(f"Distância da melhor rota inicial: {melhor_distancia_inicial:.2f}")
    
    for i in range(geracoes):
        pop_ranqueada = ranquear_rotas(populacao, dist_matrix, map_idx)
        populacao = proxima_geracao(populacao, pop_ranqueada, taxa_elite, taxa_mutacao)
        
        if (i + 1) % 20 == 0:
            melhor_dist_atual = 1 / pop_ranqueada[0][1]
            print(f"Geração {i+1} | Melhor Distância: {melhor_dist_atual:.2f}")
            
    end_time = time.time()
    print(f"Processo finalizado em {end_time - start_time:.4f} segundos.")
    
    melhor_rota_idx = ranquear_rotas(populacao, dist_matrix, map_idx)[0][0]
    melhor_rota = populacao[melhor_rota_idx]
    distancia_final = calcular_custo_rota(melhor_rota, dist_matrix, map_idx)
    
  
    rota_resposta = " -> ".join(melhor_rota[1:])
    print("\n--- Resultado Final ---")
    print(f"Melhor Sequência de Entrega Encontrada: {rota_resposta}")
    print(f"Distância Total (dronômetros): {distancia_final:.2f}")

    plotar_rota(coordenadas, melhor_rota, f"Melhor Rota Encontrada (Distância: {distancia_final:.2f})")

# EXECUÇÃO 
if __name__ == "__main__":

    valor = 12

    # Parâmetros do Algoritmo Genético
    GERACOES = 100
    TAMANHO_POPULACAO = 50
    TAXA_ELITE = 10 
    TAXA_MUTACAO = 0.01 

    # Executa a solução para o problema FlyFood
    resolver_flyfood_com_ag(
        nome_arquivo=f"caso_teste_berlin52_{valor}pts.txt",
        geracoes=GERACOES,
        tam_pop=TAMANHO_POPULACAO,
        taxa_elite=TAXA_ELITE,
        taxa_mutacao=TAXA_MUTACAO
    )