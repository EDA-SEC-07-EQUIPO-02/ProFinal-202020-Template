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

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    analyzer = model.analyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, taxisfile):

    taxisfile = cf.data_dir + taxisfile
    input_file = csv.DictReader(open(taxisfile, encoding="utf-8"), delimiter = ",")

    for trip in input_file:
        model.addTrip(analyzer, trip)
        model.addTaxi(analyzer, trip)
        model.addCompany(analyzer, trip)
        model.addCompanyTaxi(analyzer, trip)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def companiesSize(analyzer):
    tam = model.companiesSize(analyzer)
    return tam

def taxisSize(analyzer):
    tam = model.taxisSize(analyzer)
    return tam

def companyRanking(analyzer, M):
    maxComp = model.companyRanking(analyzer, M)
    return maxComp

def servicesRanking(analyzer, N):
    rank = model.servicesRanking(analyzer, N)
    return rank

def taxisPointsByDate(analyzer, N, fecha):
    rank = model.taxisPointsByDate(analyzer, N, fecha)
    return rank

def taxisPointsByDateRange(analyzer, M, fecha1, fecha2):
    rank = model.taxisPointsByDateRange(analyzer, M, fecha1, fecha2)
    return rank
    
def mejorHorario(analyzer, origin, destination, initial_date, final_date):
    r=model-mejorHorario(analyzer, origin, destination, initial_date, final_date):
    return r   
