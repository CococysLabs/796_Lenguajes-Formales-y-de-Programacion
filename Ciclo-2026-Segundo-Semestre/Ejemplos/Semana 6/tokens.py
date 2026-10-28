#Módulo de tokens

from enum import Enum
from dataclasses import dataclass

class TipoToken(Enum):
    #Cada tipo de token que puede reconocer el analizador léxico
    IDENTIFICADOR="IDENTIFICADOR"
    NUMERO="NUMERO"
    RESERVADA="RESERVADA"
    OPERADOR="OPERADOR"
    PARENTESIS="PARENTESIS"
    PUNTOYCOMA="PUNTOYCOMA"
    DESCONOCIDO="DESCONOCIDO" #Para manejar errores léxicos

@dataclass
class Token:
    #Representa un token individual: su tipo y el texto (valor)
    #que feu reconocido en el código fuente

    tipo:TipoToken
    valor:str
