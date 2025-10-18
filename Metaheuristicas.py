import random
from copy import deepcopy
import math
from scheptk.util import random_sequence
from Dispatching_rules import LPT, EDD, WSPT

def iterated_greedy(instancia, solucion_inicial, T, delta):
    """
    Algoritmo de Iterated Greedy para Flowshop Híbrido.
    Args:
        instancia: Objeto FlowShopHibrido con los datos del problema.
        solucion_inicial: Solución inicial válida (lista de índices de trabajos).
        T: Temperatura inicial (control de aceptación probabilística).
        delta: Número de elementos a destruir/reconstruir en cada iteración.
    """
    # Validar la solución inicial
    if not solucion_inicial or len(solucion_inicial) != instancia.jobs:
        raise ValueError("La solución inicial no es válida o no coincide con el número de trabajos.")
   
    # Copiar la solución inicial
    solucion_actual = deepcopy(solucion_inicial)
    mejor_solucion = deepcopy(solucion_inicial)

    # Evaluar la solución inicial
    obj_actual = instancia.SumWjTj(solucion_actual)
    mejor_objetivo = obj_actual

    while T < 0.4 :
        # **Fase de destrucción**
        solucion_reducida = deepcopy(solucion_actual)
        elementos_removidos = []

        for _ in range(delta):
            if not solucion_reducida:  # Evitar acceso a lista vacía
                break
            idx = random.randint(0, len(solucion_reducida) - 1)
            elementos_removidos.append(solucion_reducida.pop(idx))

        # **Fase de reconstrucción**
        for elemento in elementos_removidos:
            mejor_posicion = None
            mejor_obj_temporal = float('inf')

            for i in range(len(solucion_reducida) + 1):  # Insertar en cualquier posición
                solucion_temporal = deepcopy(solucion_reducida)
                solucion_temporal.insert(i, elemento)
                obj_temporal = instancia.SumWjTj(solucion_temporal)

                if obj_temporal < mejor_obj_temporal:
                    mejor_obj_temporal = obj_temporal
                    mejor_posicion = i

            # Insertar el elemento en la mejor posición encontrada
            solucion_reducida.insert(mejor_posicion, elemento)

        # Evaluar la nueva solución reconstruida
        obj_vecino = instancia.SumWjTj(solucion_reducida)

        # **Actualizar mejor solución encontrada**
        if obj_vecino < mejor_objetivo:
            mejor_solucion = deepcopy(solucion_reducida)
            mejor_objetivo = obj_vecino

        # **Aceptación probabilística**
        if obj_vecino < obj_actual or random.random() <= math.exp(-(obj_vecino - obj_actual) / T):
            solucion_actual = deepcopy(solucion_reducida)
            obj_actual = obj_vecino

        # Aumentar la temperatura
        T += 0.1

    return mejor_solucion, mejor_objetivo


def generar_poblacion(instancia, numero_individuos=10):
    
    # Las primeras soluciones que genere serán aplicando dispatching rules, las siguientes serán aleatorioas.
    poblacion = [] 
    
    poblacion.append( EDD(instancia) )
    poblacion.append( LPT(instancia) )
    poblacion.append( WSPT(instancia) )
    
    for i in range(3, numero_individuos):
        poblacion.append( random_sequence( instancia.jobs ) )
    
    return poblacion

def fitness(instancia, secuencia):
    return instancia.SumWjTj(secuencia)

def seleccionar_padres(instancia, poblacion): 

    # Aquellos individuos con mejor fitness van a tener más probabilidades de ser escogidos.
    #Primero cálculamos el fitness de cada elemento para obtener los pesos
    
    return random.choices(poblacion, weights=[fitness(instancia, i) for i in poblacion], k=2) 

def crear_hijo(padre, madre):

    # Seleccionamos en que punto cortaremos al padre
    p = random.randint(1, len(padre)-1 ) 
    trabajos_sobrantes = padre[:p]
    # Hacemos una copia de la madre para no modificar a la madre original
    madre_copiada = madre[:] 
    # Eliminamos a la madre los trabajos del padre
    for i in trabajos_sobrantes:
        madre_copiada.remove(i)
    
    hijo = padre[:p] + madre_copiada
    
    return hijo

def mutacion(individuo, probabilidad=0.2):
    
    numero_aleatorio = random.random()
    if numero_aleatorio < probabilidad:
        # Hay mutación (método de inserción)
        
        job = random.choices(individuo, weights=None, k=1) # Seleccionamos un trabajo aleatorio
        posicion = random.randint(0, len(individuo)) # Seleccionamos la posición de destino
        
        individuo.remove(job[0])
        individuo.insert(posicion, job[0])
    
    return individuo

def genetic_algorithm_hybrid(instancia, numero_generaciones=50):
  
    # Inicializar la población
    poblacion = generar_poblacion(instancia, 20)
    mejor_fitness = float('inf')
    mejor_solucion = None

    for _ in range(numero_generaciones):
        # Evaluar la población actual
        fitness_actual = [instancia.SumWjTj(individuo) for individuo in poblacion]

        # Encontrar los dos mejores individuos
        indices_mejores = sorted(range(len(fitness_actual)), key=lambda k: fitness_actual[k])[:2]
        elite = [poblacion[i] for i in indices_mejores]

        # Verificar si se encontró una nueva mejor solución
        if fitness_actual[indices_mejores[0]] < mejor_fitness:
            mejor_fitness = fitness_actual[indices_mejores[0]]
            mejor_solucion = elite[0]

        # Generar la nueva población
        nueva_poblacion = elite.copy()
        while len(nueva_poblacion) < len(poblacion):
            padre, madre = random.choices(poblacion, weights=fitness_actual, k=2)
            hijo = crear_hijo(padre, madre)
            hijo = mutacion(hijo)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    return mejor_solucion, mejor_fitness