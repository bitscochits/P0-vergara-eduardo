"""Configuracion de pytest: permite importar los modulos de src/."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
