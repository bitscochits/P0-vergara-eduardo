"""Benchmark que compara mimatmul con la operacion optimizada A @ B de NumPy.

Mide el tiempo por repeticion para matrices cuadradas de distintos tamanos,
guarda los resultados en data/benchmark_results.csv y genera figures/benchmark.png.
"""

import csv
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mimatmul import mimatmul

HERE = Path(__file__).resolve().parent.parent
DATA_DIR = HERE / "data"
FIGURES_DIR = HERE / "figures"

SIZES = [10, 25, 50, 75, 100, 125, 150, 200, 400]
REPETICIONES = 3
TIPO_DATO = np.float64


def medir_tiempo(funcion, *args):
    """Mide el tiempo de una llamada con time.perf_counter."""
    inicio = time.perf_counter()
    funcion(*args)
    return time.perf_counter() - inicio


def ejecutar_benchmark():
    rng = np.random.default_rng(2026)
    filas = []
    for n in SIZES:
        A = rng.random((n, n)).astype(TIPO_DATO)
        B = rng.random((n, n)).astype(TIPO_DATO)

        mimatmul(A, B)
        A @ B

        for rep in range(1, REPETICIONES + 1):
            filas.append({
                "size": n,
                "metodo": "mimatmul",
                "repeticion": rep,
                "tiempo_s": medir_tiempo(mimatmul, A, B),
            })
            filas.append({
                "size": n,
                "metodo": "numpy",
                "repeticion": rep,
                "tiempo_s": medir_tiempo(lambda: A @ B),
            })
        print(f"tamano {n}x{n} listo")
    return filas


def guardar_csv(filas):
    DATA_DIR.mkdir(exist_ok=True)
    ruta = DATA_DIR / "benchmark_results.csv"
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["size", "metodo", "repeticion", "tiempo_s"])
        writer.writeheader()
        writer.writerows(filas)
    print(f"Resultados guardados en {ruta}")


def generar_grafico(filas):
    FIGURES_DIR.mkdir(exist_ok=True)
    datos = {}
    for fila in filas:
        clave = (fila["size"], fila["metodo"])
        datos.setdefault(clave, []).append(fila["tiempo_s"])

    fig, ax = plt.subplots(figsize=(8, 5))
    for metodo, color, marcador in [("mimatmul", "tab:red", "o"), ("numpy", "tab:blue", "s")]:
        tamanos = sorted({fila["size"] for fila in filas if fila["metodo"] == metodo})
        medias = [np.mean(datos[(n, metodo)]) for n in tamanos]
        ax.plot(tamanos, medias, color=color, marker=marcador, label=metodo)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Tamano de la matriz (n x n)")
    ax.set_ylabel("Tiempo de ejecucion (s)")
    ax.set_title("Benchmark: mimatmul vs A @ B de NumPy")
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    ax.legend()

    ruta = FIGURES_DIR / "benchmark.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    print(f"Grafico guardado en {ruta}")


def main():
    filas = ejecutar_benchmark()
    guardar_csv(filas)
    generar_grafico(filas)


if __name__ == "__main__":
    main()
