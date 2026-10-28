from analizador_lexico import analizar

def main():
    codigo="int x = 10; if (x == 10) { x = x + 1; }"
    lista_tokens=analizar(codigo)

    for token in lista_tokens:
        print(f"{token.tipo.value}:{token.valor}")

if __name__=="__main__":
    main()