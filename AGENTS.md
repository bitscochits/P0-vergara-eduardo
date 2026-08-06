# AGENTS.md

Instrucciones permanentes para OpenCode en este repositorio.

## Proposito del proyecto

Proyecto P0 del curso "Metodos computacionales en obras civiles" (Universidad de los Andes).
Prepara el ambiente de trabajo y presenta un desarrollo incremental:
informacion del computador, una multiplicacion de matrices con ciclos de Python,
pruebas automaticas y un benchmark contra la operacion optimizada de NumPy.

## Estructura del repositorio

```
P0-vergara-eduardo/
├── README.md
├── AGENTS.md
├── requirements.txt
├── conftest.py          # permite importar modulos de src/ en las pruebas
├── src/
│   ├── system_info.py   # informacion del computador -> data/system_info.json
│   ├── mimatmul.py      # multiplicacion de matrices con ciclos de Python
│   └── benchmark.py     # benchmark -> data/benchmark_results.csv y figures/benchmark.png
├── tests/
│   └── test_mimatmul.py # pruebas de pytest
├── data/
│   ├── system_info.json
│   └── benchmark_results.csv
└── figures/
    └── benchmark.png
```

## Reglas de trabajo

- Ejecutar las pruebas con: `python -m pytest` (desde la raiz del repositorio).
- Mantener el codigo sencillo y legible. No agregar funcionalidad innecesaria.
- Prohibido inventar mediciones o resultados: todo numero en `data/` debe provenir
  de una ejecucion real en este computador.
- Conservar los datos originales sin modificarlos a mano. Si se vuelve a ejecutar
  un script, los nuevos archivos sobrescriben los anteriores (es aceptable).
- Despues de modificar codigo, ejecutar las pruebas de nuevo.
- Prohibido crear matrices tan grandes que puedan agotar la memoria del computador
  (equipo con 16 GB de RAM; mimatmul escala como n^3 y se vuelve muy lento).
- Prohibido ejecutar operaciones destructivas de Git (force push, reset, rebase,
  borrado de historial).
- El estudiante debe revisar todos los cambios antes de cualquier commit o push;
  no commitear sin su aprobacion explicita.
