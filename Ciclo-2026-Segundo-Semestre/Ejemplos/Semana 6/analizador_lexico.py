#Módulo: Analizador léxico

from tokens import TipoToken,Token

PALABRAS_RESERVADAS={"int","if","else","while"}

def es_reservada(palabra):

    return palabra in PALABRAS_RESERVADAS

def analizar(entrada):
    #Recorre la cadena entrada y retorna una lista de Tokens

    tokens=[]
    i=0
    n=len(entrada)
    while i<n:
        caracter = entrada[i]

        #1. Ignorar los espacios en blanco
        if caracter.isspace():
            i+=1
            continue
        #2. Identificador o palabra reservada (empieza con una letra)
        if caracter.isalpha():
            buffer=""
            while i<n and entrada[i].isalnum():
                buffer+= entrada[i]
                i+=1

            if es_reservada(buffer):
                tokens.append(Token(TipoToken.RESERVADA,buffer))

            else:
                tokens.append(Token(TipoToken.IDENTIFICADOR,buffer))
            continue

        #Número (secuencia de dígitos)
        if caracter.isdigit():
            buffer=""
            while i<n and entrada[i].isdigit():
                buffer+=entrada[i]
                i+=1

            tokens.append(Token(TipoToken.NUMERO,buffer))
            continue

        #4. Operador doble "=="
        if caracter=="=" and 1+i<n and entrada[i+1]=="=":
            tokens.append(Token(TipoToken.OPERADOR,"=="))
            i+=2
            continue
        #5. Operadores simples
        if caracter in "+-*/=":
            tokens.append(Token(TipoToken.OPERADOR,caracter))
            i+=1
            continue

        #6. Paréntesis
        if caracter in "()\{\}":
            tokens.append(Token(TipoToken.PARENTESIS,caracter))
            i+=1
            continue
        #7. Paréntesis
        if caracter == ";":
            tokens.append(Token(TipoToken.PUNTOYCOMA,";"))
            i+=1
            continue

        #8. Cualquier caracter no reconocido -> error léxico
        
        tokens.append(Token(TipoToken.DESCONOCIDO,caracter))
        i+=1

    return tokens