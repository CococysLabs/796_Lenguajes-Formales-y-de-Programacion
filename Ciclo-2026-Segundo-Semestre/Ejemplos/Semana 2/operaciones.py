# Ejemplo de funciones

from constantes import TASA_IMPUESTO

def sumar(a,b):
    #Recibimos dos números y devolvemos la suma
    return a+b

def restar(a,b):
    #Recibimos dos números y devolvemos la resta
    return a-b

def calcular_precio_final(precio, impuesto= TASA_IMPUESTO):
    #Recibimos el precio sin impuesto y devolvemos el precio con impuesto
    return precio *(1+impuesto)