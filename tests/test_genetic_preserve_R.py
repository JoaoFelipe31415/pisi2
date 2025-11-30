from src.genetic_algorthm.genetic_algoritm import cruzamento, mutacao, proxima_geracao


def test_cruzamento_preserva_R_varias_execucoes():
    pai1 = ['R', 'A', 'B', 'C', 'D']
    pai2 = ['R', 'D', 'C', 'B', 'A']

    for _ in range(50):
        filho = cruzamento(pai1, pai2)
        # a rota deve começar por R
        assert filho[0] == 'R'
        # R não deve aparecer novamente no resto da rota
        assert 'R' not in filho[1:]
        # todos os pontos devem estar presentes e sem duplicatas
        assert len(filho) == len(set(filho)) == len(pai1)
        assert set(filho) == set(pai1)


def test_mutacao_preserva_R_com_swap_forcado():
    individuo = ['R', 'A', 'B', 'C', 'D']
    # usar taxa 1.0 para forçar muitas trocas
    mutated = mutacao(individuo.copy(), taxa_mutacao=1.0)
    assert mutated[0] == 'R'
    assert 'R' not in mutated[1:]
    assert set(mutated) == set(individuo)


def test_proxima_geracao_preserva_R():
    populacao = [
        ['R', 'A', 'B', 'C'],
        ['R', 'C', 'B', 'A'],
        ['R', 'B', 'A', 'C'],
    ]
    # pop_ranqueada: (index, fit)
    # apenas uma pessoa de elite
    pop_ranqueada = [(0, 1.0), (1, 0.5), (2, 0.2)]

    nova = proxima_geracao(populacao, pop_ranqueada, tamanho_elite=1, taxa_mutacao=0.5)
    assert len(nova) == len(populacao)

    for ind in nova:
        assert ind[0] == 'R'
        assert 'R' not in ind[1:]
        assert set(ind) == set(populacao[0])


if __name__ == "__main__":
    # Run tests manually so they can be executed without pytest
    test_cruzamento_preserva_R_varias_execucoes()
    test_mutacao_preserva_R_com_swap_forcado()
    test_proxima_geracao_preserva_R()
    print("All genetic-preserve-R tests passed")
