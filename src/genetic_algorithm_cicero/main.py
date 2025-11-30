import time,os
from utils_cicero import transformar_grid_em_tsplib                                                                                                                                          
def carregar_distancias_brasil58():
    objArq = open("edgesbrasil58.tsp")
    #se você quiser uma lista onde cada objeto será uma string
    #grande representando uma linha do arquivo:
    #listaLinhas = objArq.readlines() #obs: cada linha terah um enter junto com o ultimo elemento

    distancias = {}

    for i in range(1, 58): #linhas 1 a 57 pois a 58 nao terá aresta
        linha = objArq.readline() #le só uma linha do arquivo
        #transformando a linha em lista de strings:
        lista = linha.split() #obs: lista de strings (não int)

        for j in range(i+1, 59): #colunas i+1 a 58
            if len(lista) > 0:
                peso = int(lista.pop(0)) #obs: peso int, poderia ser float em outro problema
            else:
                print(f"Erro! linha {i} do arquivo não possui elementos suficientes")
                exit()
            #gravando a aresta em (i, j) e (j, i):
            distancias[(i,j)] = peso
            distancias[(j,i)] = peso
    objArq.close()
	
    return distancias,58

def carregar_distancias(nome_arquivo):
    caminho = os.path.join(os.path.dirname(__file__), '..','..', 'data', nome_arquivo)
    distancias, qtd_pontos = transformar_grid_em_tsplib(caminho)
    return distancias, qtd_pontos

#funcao que retorna o custo total do caminho:
def custoCaminho(permutacao, dicDistancias):
	#ex: permutacao = [5, 14, 2, 3, 7, ...]
	soma = 0
	for i in range(len(permutacao)-1):
		a = permutacao[i]
		b = permutacao[i+1]
		if (a,b) in dicDistancias:
			soma += dicDistancias[(a,b)]
		else:
			print(f"Erro! ({a},{b}) não existe no dicionario!")
			exit()
	soma += dicDistancias[(permutacao[-1],permutacao[0])]
	return soma
	
def inicializaPopulacao(tamanho, qtdeCidades):
	import random
	#criando uma lista com "tamanho" permutacoes aleatorias de cidades:
	lista = []
	for i in range(tamanho):
		individuo = list(range(1, qtdeCidades+1))
		random.shuffle(individuo)
		lista.append(individuo)
	return lista

def calculaAptidao(populacao, dicDistancias):
	listaAptidao = []
	for elem in populacao:
		listaAptidao.append(custoCaminho(elem, dicDistancias))
	return listaAptidao


def ranquearPopulacao(populacao, dicDistancias):
	"""Retorna uma lista de tuplas (indice, fitness) ordenada da melhor para a pior.

	Fitness aqui é definido como 1 / custo (custos menores => fitness maior).
	"""
	aptidoes = calculaAptidao(populacao, dicDistancias)
	# construímos pares (idx, fitness)
	indice_fitness = [(i, 1.0 / apt if apt != 0 else float('inf')) for i, apt in enumerate(aptidoes)]
	# ordena do melhor (maior fitness) para o pior
	return sorted(indice_fitness, key=lambda x: x[1], reverse=True)


def selecao(pop_ranqueada, tamanho_elite):
	"""Seleciona índices de pais usando elitismo + roleta (fitness proporcional).

	pop_ranqueada deve ser uma lista de (indice, fitness) ordenada (melhor primeiro).
	Retorna uma lista de índices selecionados do mesmo tamanho da população original.
	"""
	indices_selecionados = []

	# garante elitismo: copia os primeiros 'tamanho_elite' indices
	for i in range(tamanho_elite):
		indices_selecionados.append(pop_ranqueada[i][0])

	# soma cumulativa para roleta
	total_fitness = sum([x[1] for x in pop_ranqueada])
	# quando todas as aptidões são zero, faz seleção aleatória uniforme
	if total_fitness == 0:
		from random import choice
		remaining = [p[0] for p in pop_ranqueada[tamanho_elite:]]
		for _ in range(len(pop_ranqueada) - tamanho_elite):
			indices_selecionados.append(choice(remaining))
		return indices_selecionados

	# roleta proporcional
	import random
	aptitudes = [p[1] for p in pop_ranqueada]
	cumulative = []
	s = 0
	for a in aptitudes:
		s += a
		cumulative.append(s)

	for _ in range(len(pop_ranqueada) - tamanho_elite):
		r = random.random() * cumulative[-1]
		for i, c in enumerate(cumulative):
			if r <= c:
				indices_selecionados.append(pop_ranqueada[i][0])
				break

	return indices_selecionados


def cruzamento(pai1, pai2):
	"""Ordered Crossover (OX1) para listas de cidades (inteiros).

	Produz um filho que mantém todas as cidades, sem duplicação.
	"""
	import random
	tamanho = len(pai1)
	filho = [None] * tamanho

	if tamanho <= 2:
		# nada significativo para cruzar em tamanhos muito pequenos
		return pai1.copy()

	inicio, fim = sorted(random.sample(range(tamanho), 2))
	# copia o bloco do pai1
	filho[inicio:fim] = pai1[inicio:fim]

	# percorre pai2 e preenche os espaços vazios mantendo ordem
	pos = fim % tamanho
	for gene in pai2:
		if gene not in filho:
			filho[pos] = gene
			pos = (pos + 1) % tamanho

	return filho


def mutacao(individuo, taxa_mutacao):
	"""Mutação por swap: para cada gene (cidade) com probabilidade taxa_mutacao troca com outra.

	Retorna o indivíduo mutado (lista)."""
	import random
	ind = individuo.copy()
	n = len(ind)
	for i in range(n):
		if random.random() < taxa_mutacao:
			j = random.randint(0, n - 1)
			ind[i], ind[j] = ind[j], ind[i]
	return ind


def proxima_geracao(populacao_atual, pop_ranqueada, tamanho_elite, taxa_mutacao):
	"""Gera a próxima população usando selecao, cruzamento e mutacao.

	pop_ranqueada deve ser lista de (indice, fitness) ordenada do melhor para o pior.
	"""
	import random

	indices_pais = selecao(pop_ranqueada, tamanho_elite)
	pool_de_pais = [populacao_atual[i] for i in indices_pais]

	nova_pop = []

	# copiar elites
	for i in range(tamanho_elite):
		nova_pop.append(pool_de_pais[i].copy())

	# preencher o resto por cruzamentos + mutações
	for _ in range(tamanho_elite, len(pool_de_pais)):
		pai1 = random.choice(pool_de_pais)
		pai2 = random.choice(pool_de_pais)
		filho = cruzamento(pai1, pai2)
		filho = mutacao(filho, taxa_mutacao)
		nova_pop.append(filho)

	# Se por acaso a seleção retornou menos ou mais indivíduos que a população original
	# ajustamos para garantir o mesmo tamanho que população_atual
	if len(nova_pop) < len(populacao_atual):
		# completa com cópias aleatórias de pop_atual
		while len(nova_pop) < len(populacao_atual):
			nova_pop.append(random.choice(populacao_atual).copy())
	elif len(nova_pop) > len(populacao_atual):
		nova_pop = nova_pop[: len(populacao_atual)]

	return nova_pop


# =============================================================================
# 3. LOOP PRINCIPAL (MAIN)
# =============================================================================
if __name__ == "__main__":
    
    dic_distancias,qtd_pontos = carregar_distancias("caso_teste_berlin52_12pts.txt")
    #dic_distancias,qtd_pontos = carregar_distancias_brasil58()
    # --- CONFIGURAÇÕES DO AGENTE ---
    GERACOES = 10000       
    TAM_POPULACAO = 50    
    ELITE = 15             
    TAXA_MUTACAO = 0.02   
    NUM_CIDADES = qtd_pontos
    
    # 1. Carregar Mapa
    
    # 2. Criar População Inicial
    print("Inicializando população...")
    populacao = inicializaPopulacao(TAM_POPULACAO, NUM_CIDADES)
    
    melhor_custo_global = float('inf')
    melhor_rota_global = []
    
    inicio_tempo = time.time()
    
    print(f"\n--- Iniciando Evolução por {GERACOES} gerações ---")
    
    for g in range(GERACOES):
        # A. Ranquear
        # Retorna lista de tuplas [(indice, fitness), ...]
        ranking = ranquearPopulacao(populacao, dic_distancias)
        
        # B. Verificar o Melhor da Geração
        idx_melhor_geracao = ranking[0][0]
        # Recuperamos o custo convertendo o fitness de volta (1/fit) ou recalculando
        custo_melhor_geracao = custoCaminho(populacao[idx_melhor_geracao], dic_distancias)
        
        # C. Atualizar Global Best
        if custo_melhor_geracao < melhor_custo_global:
            melhor_custo_global = custo_melhor_geracao
            melhor_rota_global = populacao[idx_melhor_geracao].copy()
            print(f"Gen {g}: Novo Recorde! Custo = {melhor_custo_global}")
            
        # D. Criar Próxima Geração
        populacao = proxima_geracao(populacao, ranking, ELITE, TAXA_MUTACAO)
        
        # Log periódico
        if g % 100 == 0:
            print(f"Gen {g} | Melhor Atual: {melhor_custo_global}")

    fim_tempo = time.time()
    
    print("\n==================================")
    print("FIM DA EXECUÇÃO")
    print(f"Tempo total: {fim_tempo - inicio_tempo:.2f} segundos")
    print(f"Melhor Custo Encontrado: {melhor_custo_global}")
    print(f"Ótimo Conhecido (Referência): 25395")
    print("==================================")
    
    # Validação Final da Rota
    print("\nRota Final (Primeiros 10 pontos):", melhor_rota_global[:10], "...")
   