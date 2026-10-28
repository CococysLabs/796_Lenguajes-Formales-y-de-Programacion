"""
Analizador sintáctico DESCENDENTE RECURSIVO (gramática simplificada).

Regla:  UNA FUNCIÓN POR CADA NO TERMINAL, y el token actual (lookahead) decide qué hacer.

  <documento>  ::= <bloque> <documento> | ε
  <bloque>     ::= <encabezado> | <lista> | <parrafo>
  <encabezado> ::= NUMERAL <texto> SALTO_LINEA
  <parrafo>    ::= <texto> SALTO_LINEA
  <lista>      ::= <item> <lista> | <item>
  <item>       ::= VIÑETA <texto> SALTO_LINEA <sublista> | VIÑETA <texto> SALTO_LINEA
  <sublista>   ::= INDENT <lista> DEDENT
  <texto>      ::= <elemento> <texto> | ε
  <elemento>   ::= <negrita> | <cursiva> | TEXTO
  <negrita>    ::= NEGRITA <texto> NEGRITA
  <cursiva>    ::= CURSIVA <texto> CURSIVA

"""

from modelos import Error, NodoAST, Token, TipoToken as T

FIRST_TEXTO=frozenset({T.TEXTO, T.NEGRITA, T.CURSIVA})
FIRST_BLOQUE = frozenset({T.NUMERAL, T.VIÑETA}) | FIRST_TEXTO 

class AnalizadorSintactico:
    def __init__(self, tokens:list[Token]):
        self.tokens, self.pos,self.errores=tokens,0,[]

    # ---- primitivas
    @property
    def actual(self)->Token:
        return self.tokens[self.pos]

    def avanzar(self) -> Token:
        tk = self.actual
        if tk.tipo != T.FIN_ARCHIVO:
            self.pos += 1
        return tk

    def error(self, tipo: str, token: Token, descripcion: str):
        self.errores.append(Error(tipo,token.lexema or token.tipo.name, descripcion, token.linea,token.columna))

    def consumir(self, tipo: T, contexto:str) -> NodoAST:
        a=self.actual
        if a.tipo==tipo:
            return NodoAST(a.tipo.name,self.avanzar())
        self.error("TOKEN_INESPERADO", a, f"Se esperaba {tipo.name} en {contexto}, se contró {a.tipo.name}")
        return NodoAST(tipo.name, Token(tipo, "",a.linea,a.columna)) 

    def cerrar(self,tipo:T,apertura: Token, error: str, frase: str) -> NodoAST:
        if self.actual.tipo==tipo:
            return NodoAST(tipo.name,self.avanzar())
        self.error(error,apertura,f"{frase} en línea {apertura.linea}, columna {apertura.columna}")
        return NodoAST(tipo.name, Token(tipo,"",apertura.linea, apertura.columna))

    def sincronizar(self,conjunto):
        while self.actual.tipo not in conjunto:
            self.avanzar()

    def analizar(self)->NodoAST:
        return self.parse_documento()

    def parse_documento(self) -> NodoAST:
        nodo = NodoAST("<documento>")
        if self.actual.tipo == T.FIN_ARCHIVO:
            nodo.agregar(NodoAST("ε"))
            return nodo
        if self.actual.tipo in FIRST_BLOQUE:
            nodo.agregar(self.parse_bloque())
        else:
            self.error("TOKEN_INESPERADO", self.actual, f"Token inesperado {self.actual.tipo.name}")
            self.avanzar()
            self.sincronizar(FIRST_BLOQUE | {T.FIN_ARCHIVO})
        nodo.agregar(self.parse_documento())
        return nodo

    def parse_bloque(self)->NodoAST:
        nodo = NodoAST("<bloque>")
        if self.actual.tipo==T.NUMERAL:
            nodo.agregar(self.parse_encabezado())
        elif self.actual.tipo==T.VIÑETA:
            nodo.agregar(self.parse_lista())
        else:
            nodo.agregar(self.parse_parrafo())
        return nodo
    def parse_encabezado(self) -> NodoAST:
        
        nodo = NodoAST("<encabezado>")
        nodo.agregar(self.consumir(T.NUMERAL, "<encabezado>"))       
        nodo.agregar(self.parse_texto(frozenset()))
        nodo.agregar(self.consumir(T.SALTO_LINEA, "<encabezado>"))
        return nodo

    def parse_negrita(self, cierres: frozenset) -> NodoAST:
        
        nodo = NodoAST("<negrita>")
        apertura = self.actual                                       # se guarda para reportar el error
        nodo.agregar(self.consumir(T.NEGRITA, "<negrita>"))
        nodo.agregar(self.parse_texto(cierres | {T.NEGRITA}))       
        nodo.agregar(self.cerrar(T.NEGRITA, apertura, "NEGRITA_SIN_CERRAR", "Negrita sin cerrar iniciada"))
        return nodo


    def parse_parrafo(self) -> NodoAST:
        
        nodo = NodoAST("<parrafo>")
        nodo.agregar(self.parse_texto(frozenset()))
        nodo.agregar(self.consumir(T.SALTO_LINEA, "<parrafo>"))
        return nodo

    def parse_lista(self) -> NodoAST:
        
        nodo = NodoAST("<lista>")
        nodo.agregar(self.parse_item())
        if self.actual.tipo == T.VIÑETA:                     
            nodo.agregar(self.parse_lista())
        return nodo

    def parse_item(self) -> NodoAST:
        
        nodo = NodoAST("<item>")
        nodo.agregar(self.consumir(T.VIÑETA, "<item>"))
        nodo.agregar(self.parse_texto(frozenset()))
        nodo.agregar(self.consumir(T.SALTO_LINEA, "<item>"))
        if self.actual.tipo == T.INDENT:                     # opcional: solo si hay sublista
            nodo.agregar(self.parse_sublista())
        return nodo

    def parse_sublista(self) -> NodoAST:
        
        nodo = NodoAST("<sublista>")
        indent = self.actual
        if indent.valor and indent.valor > 1:                # subió más de un nivel de una sola vez
            self.error("INDENTACION_INVALIDA", indent,
                       f"Indentación inválida en línea {indent.linea}, columna {indent.columna}")
        nodo.agregar(self.consumir(T.INDENT, "<sublista>"))
        nodo.agregar(self.parse_lista())                     # <- una lista dentro de una lista
        nodo.agregar(self.consumir(T.DEDENT, "<sublista>"))
        return nodo

    def parse_texto(self, cierres: frozenset) -> NodoAST:

        nodo = NodoAST("<texto>")
        if self.actual.tipo in FIRST_TEXTO and self.actual.tipo not in cierres:
            nodo.agregar(self.parse_elemento(cierres))
            nodo.agregar(self.parse_texto(cierres))
        else:
            nodo.agregar(NodoAST("ε"))
        return nodo

    def parse_elemento(self, cierres: frozenset) -> NodoAST:

        nodo = NodoAST("<elemento>")
        if self.actual.tipo == T.NEGRITA:
            nodo.agregar(self.parse_negrita(cierres))
        elif self.actual.tipo == T.CURSIVA:
            nodo.agregar(self.parse_cursiva(cierres))
        else:
            nodo.agregar(self.consumir(T.TEXTO, "<elemento>"))
        return nodo

    def parse_cursiva(self, cierres: frozenset) -> NodoAST:

        nodo = NodoAST("<cursiva>")
        apertura = self.actual
        nodo.agregar(self.consumir(T.CURSIVA, "<cursiva>"))
        nodo.agregar(self.parse_texto(cierres | {T.CURSIVA}))
        nodo.agregar(self.cerrar(T.CURSIVA, apertura, "CURSIVA_SIN_CERRAR", "Cursiva sin cerrar iniciada"))
        return nodo
