"""Monitorea el uso de CPU, RAM y GPU durante una corrida representativa de
mimatmul y de A @ B de NumPy. Genera data/recursos.csv y figures/recursos.png.
"""

import csv
import shutil
import subprocess
import threading
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import psutil

from mimatmul import mimatmul

HERE = Path(__file__).resolve().parent.parent
DATA_DIR = HERE / "data"
FIGURES_DIR = HERE / "figures"

INTERVALO = 0.5
DURACION_MIMATMUL = 8.0
DURACION_NUMPY = 10.0


def nvidia_gpu():
    """Devuelve (uso_gpu, memoria_gpu) de nvidia-smi, o None si no esta disponible."""
    rutas = [shutil.which("nvidia-smi"), r"C:\Windows\System32\nvidia-smi.exe"]
    ruta = next((r for r in rutas if r and Path(r).exists()), None)
    if ruta is None:
        return None
    try:
        salida = subprocess.run(
            [ruta, "--query-gpu=utilization.gpu,memory.used", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
        uso, memoria = [parte.strip() for parte in salida.split(",")]
        return int(uso.replace("%", "")), int(memoria.replace("MiB", ""))
    except (ValueError, subprocess.SubprocessError):
        return None


def correr_fase(descripcion, carga, segundos):
    """Corre `carga` en un hilo y muestrea CPU, RAM y GPU hasta que pase `segundos`."""
    hilo = threading.Thread(target=carga, daemon=True)
    hilo.start()
    inicio = time.time()
    filas = []
    while time.time() - inicio < segundos:
        por_nucleo = psutil.cpu_percent(interval=INTERVALO, percpu=True)
        gpu = nvidia_gpu()
        filas.append({
            "tiempo_s": round(time.time() - inicio, 2),
            "fase": descripcion,
            "cpu_promedio": round(sum(por_nucleo) / len(por_nucleo), 1),
            "cpu_por_nucleo": [round(p) for p in por_nucleo],
            "ram_libre_mb": round(psutil.virtual_memory().available / 2**20),
            "gpu_utilizacion": gpu[0] if gpu else None,
            "gpu_memoria_mb": gpu[1] if gpu else None,
        })
    hilo.join()
    return filas


def guardar_csv(filas):
    DATA_DIR.mkdir(exist_ok=True)
    ruta = DATA_DIR / "recursos.csv"
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "tiempo_s", "fase", "cpu_promedio", "cpu_por_nucleo",
            "ram_libre_mb", "gpu_utilizacion", "gpu_memoria_mb",
        ])
        writer.writeheader()
        writer.writerows(filas)
    print(f"Datos de recursos guardados en {ruta}")


def generar_grafico(filas):
    FIGURES_DIR.mkdir(exist_ok=True)
    tiempos = [f["tiempo_s"] for f in filas]
    cpu = [f["cpu_promedio"] for f in filas]
    ram = [f["ram_libre_mb"] for f in filas]
    gpu = [f["gpu_utilizacion"] for f in filas]

    t_cambio = next(f["tiempo_s"] for f in filas if f["fase"] == "numpy")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

    ax1.axvspan(tiempos[0], t_cambio, color="tab:red", alpha=0.12, label="mimatmul")
    ax1.axvspan(t_cambio, tiempos[-1], color="tab:blue", alpha=0.12, label="numpy")
    ax1.plot(tiempos, cpu, color="black", marker="o", markersize=3, label="CPU promedio (%)")
    ax1.set_ylabel("CPU promedio (%)")
    ax1.set_ylim(0, 100)
    ax1.legend(loc="upper left")

    ax2.axvspan(tiempos[0], t_cambio, color="tab:red", alpha=0.12)
    ax2.axvspan(t_cambio, tiempos[-1], color="tab:blue", alpha=0.12)
    ax2.plot(tiempos, ram, color="tab:green", marker="o", markersize=3, label="RAM libre (MB)")
    ax2.set_ylabel("RAM libre (MB)")
    ax2.set_xlabel("Tiempo (s)")
    ax2.legend(loc="upper left")

    if any(v is not None for v in gpu):
        ax3 = ax2.twinx()
        ax3.plot(tiempos, gpu, color="tab:orange", marker="s", markersize=3, label="GPU (%)")
        ax3.set_ylabel("GPU (%)")
        ax3.set_ylim(0, 100)
        ax3.legend(loc="upper right")

    fig.suptitle("Recursos durante la corrida: mimatmul y numpy A @ B")
    ruta = FIGURES_DIR / "recursos.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    print(f"Grafico de recursos guardado en {ruta}")


def main():
    rng = np.random.default_rng(0)
    A = rng.random((150, 150))
    B = rng.random((150, 150))
    A2 = rng.random((3000, 3000))
    B2 = rng.random((3000, 3000))

    psutil.cpu_percent(interval=0.3)

    filas = []
    filas += correr_fase("mimatmul", lambda: [mimatmul(A, B) for _ in range(10)], DURACION_MIMATMUL)
    filas += correr_fase("numpy", lambda: [A2 @ B2 for _ in range(40)], DURACION_NUMPY)

    guardar_csv(filas)
    generar_grafico(filas)


if __name__ == "__main__":
    main()
