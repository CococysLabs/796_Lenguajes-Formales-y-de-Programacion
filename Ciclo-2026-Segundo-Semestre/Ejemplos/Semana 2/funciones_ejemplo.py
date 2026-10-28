#1. Sin parámetros y sin retorno
def mostrar_menu():
    print("="*30)
    print("Menú de opciones")
    print("1. Sumar y restar")
    print("2. verificar si un número es par")
    print("3. Mostrar información de un coche")
    print("4. Salir")
    print("="*30)

#2. Con parámetros y sin retorno

def imprimir_resultado(operacion, resultado):
    print(f"El resultado de {operacion} es:{resultado}" )

#3. Sin parámetros y con retorno

def obtener_valor_por_defecto():
    return 10 #Valor por defecto

#4. Con parámetros y con retorno

def es_par(numero):

    return numero % 2 ==0