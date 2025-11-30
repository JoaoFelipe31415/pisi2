from src.genetic_algorithm_cicero.main import (
    cruzamento,
    mutacao,
    proxima_geracao,
    ranquearPopulacao,
)


def test_cruzamento_preserva_elementos_varias_execucoes():
    pai1 = [1, 2, 3, 4, 5]
    pai2 = [5, 4, 3, 2, 1]

    for _ in range(50):
        filho = cruzamento(pai1, pai2)
        assert len(filho) == len(pai1)
        assert len(set(filho)) == len(pai1)
        assert set(filho) == set(pai1)


def test_mutacao_preserva_elementos_com_swap_forcado():
    individuo = [1, 2, 3, 4, 5]
    mutated = mutacao(individuo.copy(), taxa_mutacao=1.0)
    assert set(mutated) == set(individuo)
    assert len(mutated) == len(individuo)


def test_proxima_geracao_preserva_populacao_e_elementos():
    populacao = [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 1, 4, 3],
    ]

    # calculamos ranking usando a função fornecida com um dic de distancias fictício
    # para manter a simplicidade, usamos distancias uniformes: custo = soma de valores
    # assim podemos obter ranking consistente
    # cria um dicionário de distâncias que garante custos diferentes por rota
    dic = {}
    # Usamos dist = abs(a-b) como peso entre cidades (simples e determinística)
    for a in range(1, 5):
        for b in range(1, 5):
            dic[(a, b)] = abs(a - b)

    pop_ranqueada = ranquearPopulacao(populacao, dic)
    nova = proxima_geracao(populacao, pop_ranqueada, tamanho_elite=1, taxa_mutacao=0.5)

    assert len(nova) == len(populacao)
    for ind in nova:
        assert set(ind) == set(populacao[0])


if __name__ == "__main__":
    test_cruzamento_preserva_elementos_varias_execucoes()
    test_mutacao_preserva_elementos_com_swap_forcado()
    test_proxima_geracao_preserva_populacao_e_elementos()
    print("All cicero genetic tests passed")
