from modelos import Token, TipoToken as T

VALIDO = [
    # L1  # Proyecto de Lenguajes Formales
    (T.NUMERAL, '#', 1, 1, 1), (T.TEXTO, 'Proyecto de Lenguajes Formales', 1, 3),
    (T.SALTO_LINEA, '', 1, 33),
    # L2  Este curso combina **teoría** y *práctica*.
    (T.TEXTO, 'Este curso combina ', 2, 1), (T.NEGRITA, '**', 2, 20), (T.TEXTO, 'teoría', 2, 22),
    (T.NEGRITA, '**', 2, 28), (T.TEXTO, ' y ', 2, 30), (T.CURSIVA, '*', 2, 33),
    (T.TEXTO, 'práctica', 2, 34), (T.CURSIVA, '*', 2, 42), (T.TEXTO, '.', 2, 43),
    (T.SALTO_LINEA, '', 2, 44),
    # L3  - Análisis léxico
    (T.VIÑETA, '-', 3, 1), (T.TEXTO, 'Análisis léxico', 3, 3), (T.SALTO_LINEA, '', 3, 18),
    # L4    - Autómatas finitos
    (T.INDENT, '', 4, 3, 1), (T.VIÑETA, '-', 4, 3), (T.TEXTO, 'Autómatas finitos', 4, 5),
    (T.SALTO_LINEA, '', 4, 22),
    # L5      - AFD
    (T.INDENT, '', 5, 5, 1), (T.VIÑETA, '-', 5, 5), (T.TEXTO, 'AFD', 5, 7), (T.SALTO_LINEA, '', 5, 10),
    # L6  - Análisis sintáctico
    (T.DEDENT, '', 6, 1), (T.DEDENT, '', 6, 1), (T.VIÑETA, '-', 6, 1),
    (T.TEXTO, 'Análisis sintáctico', 6, 3), (T.SALTO_LINEA, '', 6, 22),
    # fin del archivo
    (T.FIN_ARCHIVO, '', 7, 1),
]

ERRORES = [
    # L1  # Proyecto con **negrita sin cerrar
    (T.NUMERAL, '#', 1, 1, 1), (T.TEXTO, 'Proyecto con ', 1, 3), (T.NEGRITA, '**', 1, 16),
    (T.TEXTO, 'negrita sin cerrar', 1, 18), (T.SALTO_LINEA, '', 1, 36),
    # L2  - Análisis léxico
    (T.VIÑETA, '-', 2, 1), (T.TEXTO, 'Análisis léxico', 2, 3), (T.SALTO_LINEA, '', 2, 18),
    # L3      - Salto de indentación inválido
    (T.INDENT, '', 3, 5, 2), (T.VIÑETA, '-', 3, 5), (T.TEXTO, 'Salto de indentación inválido', 3, 7),
    (T.SALTO_LINEA, '', 3, 36),
    # L4  - Análisis sintáctico
    (T.DEDENT, '', 4, 1), (T.VIÑETA, '-', 4, 1), (T.TEXTO, 'Análisis sintáctico', 4, 3),
    (T.SALTO_LINEA, '', 4, 22),
    # fin del archivo
    (T.FIN_ARCHIVO, '', 5, 1),
]


def obtener_tokens(nombre: str, hasta: int | None = None) -> list[Token]:
    """Tokens de 'valido' o 'errores'. Con hasta=N solo las líneas <= N del .md (para probar por partes)."""
    tokens = [Token(*fila) for fila in {"valido": VALIDO, "errores": ERRORES}[nombre]]
    if hasta is not None:
        tokens = [t for t in tokens if t.linea <= hasta and t.tipo != T.FIN_ARCHIVO]
        tokens.append(Token(T.FIN_ARCHIVO, "", hasta + 1, 1))
    return tokens
