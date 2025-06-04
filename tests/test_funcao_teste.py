from src.funcao_teste import soma

def test_soma():
    """Teste da função soma."""
    assert soma(2, 3) == 5
    assert soma(-1, 1) == 0
    assert soma(0, 0) == 0
    assert soma(-5, -5) == -10
    assert soma(100, 200) == 300