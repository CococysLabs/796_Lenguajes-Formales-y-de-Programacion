from constantes import MAX_VELOCIDAD_PERMITIDA


#Definimos una clase
class Coche:

    #Constructor
    def __init__(self, marca,modelo):
        #Asignar los atributos
        self._marca=marca
        self._modelo=modelo
        self._velocidad=0 #iniciamos el coche con cero de velocidad

    def acelerar(self,cantidad):
        self._velocidad=min(self._velocidad+cantidad,MAX_VELOCIDAD_PERMITIDA)
        print(f" El {self._marca} aceleró." f"Velocidad actual: {self._velocidad} km/h")

    def mostrar_info(self):
        #Mostramos la información del coche
        print("--Info del coche--")
        print(f"Marca: {self._marca}")
        print(f"Modelo: {self._modelo}")
        print("--------")