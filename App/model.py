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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Sorting import selectionsort as selsort
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo

def analyzer():
    analyzer = {"trips": None,
                "taxis": None,
                "companies": None,
                "companiesTaxis": None
                }
    
    analyzer["trips"] = lt.newList("ARRAY_LIST", None)
    analyzer["taxis"] = lt.newList("ARRAY_LIST", cmpTaxiId)
    analyzer["companies"] = lt.newList("ARRAY_LIST", None)
    analyzer["companiesTaxis"] = om.newMap(omaptype="BST", comparefunction=cmpCompanies)
    analyzer["companiesRanking"] = om.newMap(omaptype="BST", comparefunction=cmpCompanies)
    analyzer["companiesServices"] = om.newMap(omaptype="BST", comparefunction=cmpCompanies)
    analyzer["taxisPoints"] = om.newMap(omaptype="BST", comparefunction=cmpTaxiId)

    return analyzer


# ==============================
# Funciones de consulta
# ==============================

def addTrip(analyzer, trip):
    lt.addLast(analyzer["trips"], trip)
    return analyzer

def addTaxi(analyzer, trip):

    ids = analyzer["taxis"]
    newPoints = 0
    tripMiles = trip["trip_miles"]
    tripTotal = trip["trip_total"]
    timeStamp = trip["trip_start_timestamp"]
    tripDate = timeStamp[0:10]
    if tripTotal != "0.0" and tripTotal != "":
        newPoints = float(tripMiles) / float(tripTotal)
    else:
        newPoints = 0
    
    if trip["taxi_id"] not in ids["elements"]:
        lt.addLast(analyzer["taxis"], trip["taxi_id"])
        pointsDate = newPoints, tripDate
        pointsList = lt.newList("ARRAY_LIST", None)
        lt.addLast(pointsList, pointsDate)
        om.put(analyzer["taxisPoints"], trip["taxi_id"], pointsList)
    else:
        info = om.get(analyzer["taxisPoints"], trip["taxi_id"])
        pointsList = info["value"]
        pointsDate = lt.lastElement(pointsList)
        oldPoints = pointsDate[0]
        points = oldPoints + newPoints
        newPointsDate = points, tripDate
        lt.addLast(pointsList, newPointsDate)
        om.put(analyzer["taxisPoints"], trip["taxi_id"], pointsList)

    return analyzer

def addCompany(analyzer, trip):

    comps = analyzer["companies"]
    if trip["company"] not in comps["elements"]:
        lt.addLast(analyzer["companies"], trip["company"])
    return analyzer

def addCompanyTaxi(analyzer, trip):
    
    comp = trip["company"]
    taxi = trip["taxi_id"]

    if om.contains(analyzer["companiesTaxis"], comp) == True:
        taxis = om.get(analyzer["companiesTaxis"], comp)
        num = om.get(analyzer["companiesRanking"], comp)
        serv = om.get(analyzer["companiesServices"], comp)
        taxiList = taxis["value"]
        numTaxis = num["value"]
        services = serv["value"]
        
        services += 1
        om.put(analyzer["companiesServices"], comp, services)

        if taxi not in taxiList["elements"]:
            lt.addLast(taxiList, taxi)
            numTaxis += 1
            om.put(analyzer["companiesTaxis"], comp, taxiList)
            om.put(analyzer["companiesRanking"], comp, numTaxis)


    else:
        newTaxis = lt.newList("ARRAY_LIST", None)
        lt.addLast(newTaxis, taxi)
        om.put(analyzer["companiesTaxis"], comp, newTaxis)
        numTaxis = 1
        om.put(analyzer["companiesRanking"], comp, numTaxis)
        services = 1
        om.put(analyzer["companiesServices"], comp, services)
    
    return analyzer

def companyRanking(analyzer, M):
    
    companies = om.keySet(analyzer["companiesRanking"])
    taxis = om.valueSet(analyzer["companiesRanking"])
    mapa = om.newMap(omaptype="BST", comparefunction=cmpCompanies)

    for i in range(lt.size(companies)):

        empresa = lt.getElement(companies, i)
        numtaxi = lt.getElement(taxis, i)
        
        if om.contains(mapa, numtaxi) == True:
            infonum = om.get(mapa, numtaxi)
            empresas = infonum["value"]
            lt.addLast(empresas, empresa)
            om.put(mapa, numtaxi, empresas)
        else:
            empresas = lt.newList("ARRAY_LIST", None)
            lt.addLast(empresas, empresa)
            om.put(mapa, numtaxi, empresas)

    tam = om.size(mapa)
    tam = tam - 1

    for i in range(M):
        k = tam - i
        emp = om.select(mapa, k)
        pareja = om.get(mapa, emp)
        lista = pareja["value"]
        numt = lista["elements"]
        info = str(tam - k + 1) + ". " + str(numt[0]) + ": " + str(emp)
        print(info)

    result = ".."

    return result

def servicesRanking(analyzer, N):

    companies = om.keySet(analyzer["companiesServices"])
    services = om.valueSet(analyzer["companiesServices"])
    mapaServ = om.newMap(omaptype="BST", comparefunction=cmpCompanies)

    for i in range(lt.size(companies)):
        empresa = lt.getElement(companies, i)
        numserv = lt.getElement(services, i)

        if om.contains(mapaServ, numserv) == True:
            infoserv = om.get(mapaServ, numserv)
            empresas = infoserv["value"]
            lt.addLast(empresas, empresa)
            om.put(mapaServ, numserv, empresas)
        else:
            empresas = lt.newList("ARRAY_LIST", None)
            lt.addLast(empresas, empresa)
            om.put(mapaServ, numserv, empresas)
    
    tam = om.size(mapaServ)
    tam = tam - 1

    for i in range(N):
        k = tam - i
        emp = om.select(mapaServ, k)
        pareja = om.get(mapaServ, emp)
        lista = pareja["value"]
        nums = lista["elements"]
        info = str(tam - k + 1) + ". " + str(nums[0]) + ": " + str(emp)
        print(info)

def taxisPointsByDate(analyzer, N, fecha):

    taxis = om.keySet(analyzer["taxisPoints"])
    #pointsLists = om.valueSet(analyzer["taxisPoints"])
    rankingFechas = om.newMap(omaptype="BST", comparefunction=cmpTaxiId)

    for i in range(lt.size(taxis)):
        puntosLlave = 0.00000
        taxi = lt.getElement(taxis, i)
        info = om.get(analyzer["taxisPoints"], taxi)
        tuplas = info["value"]

        for j in range(lt.size(tuplas)):
            tupla = lt.getElement(tuplas, j)
            puntosFecha = tupla[1]
            if tupla[0] > puntosLlave and tupla[1] == fecha:
                puntosLlave = tupla[0]
                puntosFecha = tupla[1]

        if puntosFecha == fecha and om.contains(rankingFechas, puntosLlave) == False:

            taxiList = lt.newList("ARRAY_LIST", None)
            lt.addLast(taxiList, taxi)
            om.put(rankingFechas, puntosLlave, taxiList)
        elif puntosFecha == fecha and om.contains(rankingFechas, puntosLlave) == True:
            info = om.get(rankingFechas, puntosLlave)
            taxiList = info["value"]
            lt.addLast(taxiList, taxi)
            om.put(rankingFechas, puntosLlave, taxiList)

    tam = om.size(rankingFechas)
    tam = tam - 1

    for i in range(N):
        k = tam - i
        puntos = om.select(rankingFechas, k)
        pareja = om.get(rankingFechas, puntos)
        lista = pareja["value"]
        taxisN = lista["elements"]
        info = str(tam - k + 1) + ". Taxi ID: " + str(taxisN) + ", Puntos: " + str(puntos)
        print(info)

def taxisPointsByDateRange(analyzer, M, fecha1, fecha2):

    taxis = om.keySet(analyzer["taxisPoints"])
    rankingFechas = om.newMap(omaptype="BST", comparefunction=cmpTaxiId)
    dia1 = fecha1[8:10]
    mes1 = fecha1[5:7]
    año1 = fecha1[0:4]
    dia2 = fecha1[8:10]
    mes2 = fecha1[5:7]
    año2 = fecha1[0:4]

    for i in range(lt.size(taxis)):
        puntosLlave = 0.00000
        taxi = lt.getElement(taxis, i)
        info = om.get(analyzer["taxisPoints"], taxi)
        tuplas = info["value"]

        for j in range(lt.size(tuplas)):
            tupla = lt.getElement(tuplas, j)
            puntosFecha = tupla[1]
            dia = puntosFecha[8:10]
            mes = puntosFecha[5:7]
            año = puntosFecha[0:4]
            if (año1 < año and año < año2) or año1 == año or año2 == año:
                if (mes1 < mes and mes < mes2) or mes1 == mes or mes2 == mes:
                    if (dia1 < dia and dia < dia2) or dia1 == dia or dia2 == dia:
                        if tupla[0] > puntosLlave:
                            puntosLlave = tupla[0]
                            puntosFecha = tupla[1]

        if om.contains(rankingFechas, puntosLlave) == False:

            taxiList = lt.newList("ARRAY_LIST", None)
            lt.addLast(taxiList, taxi)
            om.put(rankingFechas, puntosLlave, taxiList)
        elif om.contains(rankingFechas, puntosLlave) == True:
            info = om.get(rankingFechas, puntosLlave)
            taxiList = info["value"]
            lt.addLast(taxiList, taxi)
            om.put(rankingFechas, puntosLlave, taxiList)

    tam = om.size(rankingFechas)
    tam = tam - 1

    for i in range(M):
        k = tam - i
        puntos = om.select(rankingFechas, k)
        pareja = om.get(rankingFechas, puntos)
        lista = pareja["value"]
        taxisN = lista["elements"]
        x = "x"
        info = str(tam - k + 1) + ". Taxi ID: " + str(taxisN) + ", Puntos: " + str(puntos)
        print(info)

def taxisSize(analyzer):
    tam = lt.size(analyzer["taxis"])
    return tam

def companiesSize(analyzer):
    tam = lt.size(analyzer["companies"])
    return tam


# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def cmpTrips(trip1, trip2):
    if trip1 == trip2:
        return 0
    elif trip1 > trip2:
        return 1
    else:
        return -1
    
def cmpTaxiId(taxiId1, taxiId2):
    if taxiId1 == taxiId2:
        return 0
    elif taxiId1 > taxiId2:
        return 1
    else:
        return -1

def cmpCompanies(comp1, comp2):
    if comp1 == comp2:
        return 0
    elif comp1 > comp2:
        return 1
    else:
        return -1
