"""Pruebas automaticas de la funcion mimatmul."""

import numpy as np
import pytest

from mimatmul import mimatmul


def test_caso_pequeno_con_resultado_conocido():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    expected = [[19, 22], [43, 50]]
    assert np.allclose(mimatmul(A, B), expected)


def test_matrices_cuadradas():
    rng = np.random.default_rng(42)
    for n in (1, 3, 8):
        A = rng.random((n, n))
        B = rng.random((n, n))
        assert np.allclose(mimatmul(A, B), A @ B)


def test_matrices_rectangulares():
    rng = np.random.default_rng(7)
    A = rng.random((2, 3))
    B = rng.random((3, 4))
    result = mimatmul(A, B)
    assert result.shape == (2, 4)
    assert np.allclose(result, A @ B)


def test_comparacion_con_numpy():
    rng = np.random.default_rng(123)
    A = rng.random((5, 4))
    B = rng.random((4, 6))
    assert np.allclose(mimatmul(A, B), A @ B)


def test_dimensiones_incompatibles():
    A = np.ones((2, 3))
    B = np.ones((4, 2))
    with pytest.raises(ValueError, match="incompatibles"):
        mimatmul(A, B)
