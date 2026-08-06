"""Recolecta informacion basica del computador y la guarda en data/system_info.json.

Usa Python estandar y PowerShell (CIM) para verificar los datos con herramientas
del sistema operativo. Si un dato no puede obtenerse, se registra como "no disponible".
"""

import json
import os
import platform
import shutil
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
DATA_DIR = HERE / "data"


def run_powershell(command):
    """Ejecuta un comando de PowerShell y devuelve su salida limpia (o None si falla)."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return None


def get_system_info():
    info = {}

    os_caption = run_powershell("(Get-CimInstance Win32_OperatingSystem).Caption")
    info["sistema_operativo"] = os_caption or f"{platform.system()} {platform.release()}"
    info["arquitectura"] = platform.machine()
    info["version_python"] = platform.python_version()
    info["version_numpy"] = np.__version__

    info["modelo_procesador"] = run_powershell(
        "(Get-CimInstance Win32_Processor).Name"
    ) or "no disponible"

    info["nucleos_fisicos"] = run_powershell(
        "(Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfCores -Sum).Sum"
    ) or "no disponible"

    info["procesadores_logicos"] = run_powershell(
        "(Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum"
    ) or "no disponible"

    total_ram_bytes = run_powershell(
        "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory"
    )
    available_ram_kb = run_powershell(
        "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory"
    )

    def to_gib(bytes_value):
        return round(int(bytes_value) / (1024**3), 2)

    if total_ram_bytes:
        info["ram_total_gb"] = to_gib(total_ram_bytes)
    else:
        info["ram_total_gb"] = "no disponible"

    if available_ram_kb:
        info["ram_disponible_gb"] = to_gib(int(available_ram_kb) * 1024)
    else:
        info["ram_disponible_gb"] = "no disponible"

    gpu_names = run_powershell(
        "(Get-CimInstance Win32_VideoController).Name"
    )
    if gpu_names:
        info["modelo_gpu"] = "; ".join(
            line.strip() for line in gpu_names.splitlines() if line.strip()
        )
    else:
        info["modelo_gpu"] = "no disponible"

    root = os.path.splitdrive(str(HERE))[0] + os.sep
    try:
        usage = shutil.disk_usage(root)
        info["disco_principal"] = root
        info["disco_total_gb"] = round(usage.total / (1024**3), 2)
        info["disco_libre_gb"] = round(usage.free / (1024**3), 2)
    except OSError:
        info["disco_principal"] = "no disponible"
        info["disco_total_gb"] = "no disponible"
        info["disco_libre_gb"] = "no disponible"

    return info


def main():
    info = get_system_info()
    DATA_DIR.mkdir(exist_ok=True)
    output_file = DATA_DIR / "system_info.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
