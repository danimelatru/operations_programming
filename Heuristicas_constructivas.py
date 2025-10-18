from FlowShopHibrido import FlowShopHibrido 
from copy import deepcopy
import Dispatching_rules
import math
from scheptk.util import random_sequence

def MinimumSlack(instancia):
    
    S = []  # Secuencia óptima
    U = list(range(instancia.jobs))  # Trabajos pendientes
    tiempo_actual = 0  # Tiempo acumulado en la programación
   
    while U:
        # Calcular la holgura (slack) de cada trabajo pendiente
        slack = {j: max(instancia.dd[j] - tiempo_actual - sum(instancia.pt[i][j] for i in range(6)), 0) for j in U}
        # Seleccionar el trabajo con la mínima holgura
        siguiente = min(slack, key=slack.get)
        S.append(siguiente)
        U.remove(siguiente)
        tiempo_actual += sum(instancia.pt[i][siguiente] for i in range(6))
   
    # Calcular el valor de la función objetivo (SUM Tj)
    sum_tj = instancia.SumWjTj(S)
    return S, sum_tj


def CheapestInsertion(instancia, secuencia_inicial):
    
    if instancia.SumWjTj( [secuencia_inicial[0], secuencia_inicial[1]] ) <= instancia.SumWjTj( [secuencia_inicial[1], secuencia_inicial[0]] ):
        secuencia_CI = [ secuencia_inicial[0], secuencia_inicial[1] ]
    else: 
        secuencia_CI = [ secuencia_inicial[1], secuencia_inicial[0] ]
    
    # Iteramos para los siguientes trabajos
    for k in range(2, len(secuencia_inicial)):
        trabajo = secuencia_inicial[k]
        
        valores_FO = []
        
        for indice in range( len(secuencia_CI)+1 ):
            secuencia_CI.insert(indice, trabajo)
            valores_FO.append(instancia.SumWjTj(secuencia_CI))
            secuencia_CI.remove(trabajo)
        
        mejor_resultado = min(valores_FO)
        posicion_final = valores_FO.index(mejor_resultado)
        
        secuencia_CI.insert(posicion_final, trabajo)
    
    valor_secuencia_CI = instancia.SumWjTj(secuencia_CI)
   
            
    return secuencia_CI, valor_secuencia_CI


def ApparentTardinessCost(instancia, k=2):

   
    secuencia = []  # Secuencia óptima
    U = list(range(instancia.jobs))  # Trabajos pendientes
    tiempo_actual = 0  # Tiempo acumulado en la programación
   
    while U:
        # Calcular la prioridad ATC para cada trabajo pendiente
        atc = {
            j: (instancia.w[j] / max(instancia.dd[j] - tiempo_actual, 1)) *
                math.exp(-max(instancia.dd[j] - tiempo_actual - sum(instancia.pt[i][j] for i in range(6)), 0) / (k * instancia.dd[j]))
            for j in U
        }
       
        # Seleccionar el trabajo con la mayor prioridad ATC
        siguiente = max(atc, key=atc.get)
        secuencia.append(siguiente)
        U.remove(siguiente)
        tiempo_actual += sum(instancia.pt[i][siguiente] for i in range(6))
   
    # Calcular el valor de la función objetivo (SUM WjTj)
    sum_wjtj = instancia.SumWjTj(secuencia)
    return secuencia, sum_wjtj
