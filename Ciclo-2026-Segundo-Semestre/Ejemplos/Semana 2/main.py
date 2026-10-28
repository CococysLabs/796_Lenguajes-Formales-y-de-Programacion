import operaciones
from coche import Coche
from funciones_ejemplo import (
    mostrar_menu,
    imprimir_resultado,
    obtener_valor_por_defecto,
    es_par
)

def main():
    mostrar_menu()

    #Uso del módulo de operaciones
    resultado_suma = operaciones.sumar(5,7)
    resultado_resta = operaciones.restar(10,3)
    imprimir_resultado ("La suma", resultado_suma)
    imprimir_resultado("La resta", resultado_resta)

    precio_final=operaciones.calcular_precio_final(100)
    print(f"Precio final con impuesto Q{precio_final}")

    print()

    valor= obtener_valor_por_defecto()
    print(f"Valor por defecto {valor}")

    numero = 10
    if es_par(numero):
        print(f"El número {numero} es par")
    else:
        print(f"El número {numero} es impar ")

    print()

    mi_coche = Coche("Toyota", "Yaris")
    mi_coche.mostrar_info()
    mi_coche.acelerar(200)

if __name__=="__main__":
    main()