from dataclasses import dataclass
from enum import Enum, auto


class TipoToken(Enum):
    NUMERAL = auto()       # #            (valor = nivel del encabezado)
    VIÑETA = auto()        # -            al inicio de línea
    INDENT = auto()        # virtual: sube de nivel   (valor = niveles que sube)
    DEDENT = auto()        # virtual: baja un nivel
    NEGRITA = auto()       # **
    CURSIVA = auto()       # *
    TEXTO = auto()         # texto plano
    SALTO_LINEA = auto()   # fin de línea
    FIN_ARCHIVO = auto()


@dataclass
class Token:
    tipo: TipoToken
    lexema: str
    linea: int
    columna: int
    valor: object = None


@dataclass
class Error:
    tipo: str
    lexema: str
    descripcion: str
    linea: int
    columna: int


class NodoAST:
    """Nodo del árbol de derivación: no terminal (simbolo='<lista>') u hoja (token terminal o ε)."""

    def __init__(self, simbolo: str, token: Token | None = None):
        self.simbolo, self.token, self.hijos = simbolo, token, []

    @property
    def es_terminal(self):
        return self.token is not None or self.simbolo == "ε"

    def agregar(self, hijo: "NodoAST") -> "NodoAST":
        self.hijos.append(hijo)
        return hijo

    def mostrar(self, nivel=0) -> str:
        etiqueta = self.simbolo + (f" {self.token.lexema!r}" if self.token and self.token.lexema.strip() else "")
        return "\n".join(["    " * nivel + etiqueta] + [h.mostrar(nivel + 1) for h in self.hijos])

    def a_dot(self) -> str:
        """Graphviz: raíz azul, no terminales celeste, terminales amarillo."""
        lineas, n = ["digraph Arbol {", '    node [shape=box, style=filled, fontname="Arial"];'], [0]

        def visitar(nodo, raiz=False):
            mi_id = n[0]
            color = "#2E75B6" if raiz else "#F9E79F" if nodo.es_terminal else "#D6EAF8"
            texto = nodo.token.tipo.name if nodo.token else nodo.simbolo
            if nodo.token and nodo.token.lexema.strip():
                texto += "\\n" + nodo.token.lexema.replace('"', '\\"')
            lineas.append(f'    n{mi_id} [label="{texto}", fillcolor="{color}"' + (", fontcolor=white" if raiz else "") + "];")
            for h in nodo.hijos:
                n[0] += 1
                lineas.append(f"    n{mi_id} -> n{n[0]};")
                visitar(h)

        visitar(self, raiz=True)
        return "\n".join(lineas + ["}"])