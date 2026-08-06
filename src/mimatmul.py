"""Multiplicacion de matrices con ciclos explicitos de Python.

Implementa mimatmul(A, B), equivalente a A @ B pero sin usar operaciones
optimizadas de NumPy (A @ B, np.matmul, np.dot, np.einsum).
"""

import numpy as np


def mimatmul(A, B):
    """Multiplica las matrices A y B usando tres ciclos anidados de Python.

    El resultado es un arreglo de numpy equivalente a A @ B.
    Lanza ValueError si las dimensiones son incompatibles.
    """
    rows_a, cols_a = len(A), len(A[0])
    rows_b, cols_b = len(B), len(B[0])

    if cols_a != rows_b:
        raise ValueError(
            f"Dimensiones incompatibles: A es {rows_a}x{cols_a} y B es {rows_b}x{cols_b}. "
            "El numero de columnas de A debe coincidir con el numero de filas de B."
        )

    C = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            total = 0.0
            for k in range(cols_a):
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return np.array(C)
