import tsplib95
import numpy as np
import string

def gerar_casos_testes_berlim52(instancia_base, lista_num_pontos, tamanho_grid=50):
    """
    Gera múltiplos arquivos de teste .txt a partir da instância berlin52.
    
    Args:
        instancia_base (tsplib95.models.StandardProblem): O problema tsplib carregado.
        lista_num_pontos (list): Uma lista de inteiros com o número de pontos para cada caso.
        tamanho_grid (int): A dimensão da matriz a ser gerada.
    """
    print(f"Iniciando geração de casos de teste a partir de '{instancia_base.name}'...")
    print("="*50)

    for num_pontos in lista_num_pontos:
        print(f"Gerando caso com {num_pontos} pontos...")
        
        nos_selecionados = list(instancia_base.get_nodes())[:num_pontos]
        coords_originais = np.array([instancia_base.node_coords[n] for n in nos_selecionados])
       
        min_coords = coords_originais.min(axis=0)
        max_coords = coords_originais.max(axis=0)
        range_coords = max_coords - min_coords
        range_coords[range_coords == 0] = 1
        coords_normalizadas = (coords_originais - min_coords) / range_coords * (tamanho_grid - 1)
        coords_grid = np.round(coords_normalizadas).astype(int)

        rotulos = ['R'] + list(string.ascii_uppercase)
        matriz = [['0' for _ in range(tamanho_grid)] for _ in range(tamanho_grid)]
        
        for i, (r, c) in enumerate(coords_grid):
            rotulo = rotulos[i]
            if matriz[r][c] == '0':
                matriz[r][c] = rotulo
            else:
                found_spot = False
                for dr in [-1, 1, 0, 0]:
                    for dc in [0, 0, -1, 1]:
                        if 0 <= r+dr < tamanho_grid and 0 <= c+dc < tamanho_grid and matriz[r+dr][c+dc] == '0':
                            matriz[r+dr][c+dc] = rotulo
                            found_spot = True
                            break
                    if found_spot:
                        break
                if not found_spot:
                     print(f"Aviso: Colisão de coordenadas no grid para o ponto {rotulo}. Ponto não adicionado.")


        nome_arquivo_saida = f"caso_teste_berlin52_{num_pontos}pts.txt"
        
        with open(nome_arquivo_saida, 'w') as f:
            f.write(f"{tamanho_grid} {tamanho_grid}\n")
            for linha in matriz:
                f.write(" ".join(linha) + "\n")

def ler_brasil_58():

    with open("/home/joao/Desktop/repositories/pisi2/tests_cases/edgesbrasil58.tsp", 'r') as objArq:
        # Número de nós conhecido para este arquivo
        n = 58

        # Cria matriz completa (n x n) e preenche com zeros na diagonal
        full = np.zeros((n, n), dtype=int)

        # Cada linha i (1-indexed original) contém distâncias para j = i+1..n
        for i in range(0, n - 1):
            linha = objArq.readline()
            if not linha:
                raise ValueError(f"Arquivo 'edgesbrasil58.tsp' tem menos linhas que o esperado (esperado {n-1}).")
            lista = linha.split()

            # Preenche distâncias para (i, j) com j > i
            for j in range(i + 1, n):
                if len(lista) > 0:
                    peso = int(lista.pop(0))
                else:
                    raise ValueError(f"Erro! linha {i+1} do arquivo não possui elementos suficientes para completar a linha.")
                full[i, j] = peso
                full[j, i] = peso

    # Converte a matriz completa para vetor 1-D contendo apenas os elementos acima da diagonal
    reduced = []
    for i in range(n):
        for j in range(i + 1, n):
            reduced.append(full[i, j])

    return np.array(reduced, dtype=int)

def gerar_nome_pontos(num_pontos):
    """Gera uma lista de nomes de pontos para o caso de teste."""
    rotulos = list(string.ascii_uppercase + string.ascii_lowercase + string.digits + "".join(['!','@','#','$','%','^','&','*','(',')']))
    dicionario_nomes = {}
    for i in range(num_pontos):
        dicionario_nomes[rotulos[i]] = i+1
    if "R" not in dicionario_nomes:
        dicionario_nomes["R"] = 0
    return  list(dicionario_nomes.keys()) ,dicionario_nomes    

def gerar_rota(tamanho_rota, ponto_inicial='R'):
    """Gera uma rota inicial fixa para testes."""
    rota = []
    rota.append(ponto_inicial)
    rotulos = list(string.ascii_uppercase)
    for i in range(tamanho_rota - 1):
        if(rotulos[i] == ponto_inicial):
            continue
        rota.append(rotulos[i])
    return rota

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    try:
        # Carrega a instância base uma única vez
        #problema = tsplib95.load('berlin52.tsp')
        
        # Define quantos pontos cada caso de teste terá
        # O caso com 10 pontos já será perceptivelmente lento para a força bruta
        pontos_para_testar = [6, 7, 8, 9, 10, 11 , 12, 13, 14, 15] 
        
        #gerar_casos_testes_berlim52(problema, pontos_para_testar,20)
        
        #print("\nTodos os casos de teste foram gerados.")

        print(ler_brasil_58())

    except Exception as e:
        print(f"Ocorreu um erro fatal: {e}")
        print("Verifique se a biblioteca 'tsplib95' está instalada (pip install tsplib95)")