"""
Uso:  python main.py valido|errores [--arbol] [--hasta N]
"""
import os
import sys

from analizador_sintactico import AnalizadorSintactico
from tokens_quemados import obtener_tokens

sys.setrecursionlimit(20000)       # las producciones recursivas por la derecha anidan llamadas


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("valido", "errores"):
        return print(__doc__)
    hasta = int(sys.argv[sys.argv.index("--hasta") + 1]) if "--hasta" in sys.argv else None
    parser = AnalizadorSintactico(obtener_tokens(sys.argv[1], hasta))
    arbol = parser.analizar()

    if "--arbol" in sys.argv:
        print(arbol.mostrar())
    os.makedirs("salida", exist_ok=True)
    with open("salida/arbol.dot", "w", encoding="utf-8") as f:
        f.write(arbol.a_dot())
    print("Árbol de derivación -> salida/arbol.dot   (dot -Tpng salida/arbol.dot -o salida/arbol.png)")

    if not parser.errores:
        return print("Análisis sintáctico exitoso: 0 errores")
    print(f"\nERRORES ({len(parser.errores)})")
    for i, e in enumerate(parser.errores, 1):
        print(f"{i:>2} | {e.tipo:<20} | {e.linea}:{e.columna:<3} | {e.descripcion}")


if __name__ == "__main__":
    main()
