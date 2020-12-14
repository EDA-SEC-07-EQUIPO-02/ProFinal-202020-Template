"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

taxisfile = 'taxi-trips-wrvz-psew-subset-small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("***********************")
    print("Bienvenido")
    print("1 - Inicializar el catalogo")
    print("2 - Cargar datos")
    print("3 - Req. 1: Reporte de Información Compañias y Taxis")
    print("4- req- C3: Consulta del Mejor Horario en Taxi entre 2 “community areas")
    print("5 - Req. 2: Ranking de taxis por puntos en una fecha determinada")
    print("6 - Req. 2: Ranking de taxis por puntos en un rango de fechas")
    print("0 - Salir")
    print("***********************")


"""
Menu principal
"""

while True:
    printMenu()
    inputs = input("Seleccione una opción: ")

    if int(inputs[0]) == 1:
        cont = controller.init()
    
    elif int(inputs[0]) == 2:
        controller.loadData(cont, taxisfile)
    
    elif int(inputs[0]) == 3:
        M = int(input("Ingrese el tamaño deseado del ranking (taxis): "))
        N = int(input("Ingrese el tamaño deseado del ranking (servicios): "))
        tamTaxis = controller.taxisSize(cont)
        tamCompanies = controller.companiesSize(cont)
        print("\n")
        print("Taxis registrados: " + str(tamTaxis))
        print("Compañias registradas: " + str(tamCompanies))
        print("\n")
        print("Ranking compañias por número de taxis afiliados: ")
        controller.companyRanking(cont, M)
        print("\n")
        print("Ranking compañias por servicios prestados: ")
        controller.servicesRanking(cont, N)
        rank = controller.servicesRanking(cont, N)

    elif int(inputs[0]==4):
        origin=(input("ingrese zona de origen"))
        destination=(input("ingrese zona de destino"))
        initial_date=(input("hora inicial(YYYY-MM-DD")))
        final_date=(input("hora final(YYYY-MM-DDuu"))
        R= controller.mejorHorario(analyzer, origin, destination, initial_date, final_date):
        print("\n")
        print(R)
    
    elif int(inputs[0]) == 4:
        N = int(input("Ingrese el tamaño deseado del ranking (puntos): "))
        fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
        print("\n")
        controller.taxisPointsByDate(cont, N, fecha)
    
    elif int(inputs[0]) == 5:
        M = int(input("Ingrese el tamaño deseado del ranking (puntos): "))
        fecha1 = input("Ingrese la primera fecha (YYYY-MM-DD): ")
        fecha2 = input("Ingrese la segunda fecha (YYYY-MM-DD): ")
        print("\n")
        controller.taxisPointsByDateRange(cont, M, fecha1, fecha2)

    else:
        sys.exit(0)
sys.exit(0)
