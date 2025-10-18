from FlowShopHibrido import FlowShopHibrido
from Generador_de_instancias import generar_instancia, guardar_resultados_excel
from Dispatching_rules import LPT, EDD, WSPT
from Heuristicas_constructivas import MinimumSlack, CheapestInsertion, ApparentTardinessCost
from Metaheuristicas import iterated_greedy, genetic_algorithm_hybrid
import copy


# Configuración inicial
excel_path = 'Datos_PO.xlsx'
resultados_despacho, resultados_heuristicas, resultados_metaheuristicas = [], [], []

# Evaluar todas las instancias
for i in range(1, 31):
    # Determinar número de trabajos
    numero_trabajos = 10 if i < 11 else 20 if i < 21 else 30

    # Generar instancia
    nombre_instancia = f'Instancia{i}.txt'
    print(f'\n\nInstancia número {i}\n')
    generar_instancia(nombre_instancia, numero_trabajos)
    instancia = FlowShopHibrido(nombre_instancia)

    # Dispatching rules
    # En el main, usar la instancia ya creada en vez de pasar la ruta del archivo
    reglas = {"EDD": EDD(instancia),"LPT": LPT(instancia),"WSPT": WSPT(instancia)}

    resultados_reglas = {regla: instancia.SumWjTj(secuencia) for regla, secuencia in reglas.items()}
    mejor_regla, mejor_resultado_d = min(resultados_reglas.items(), key=lambda x: x[1])
    mejor_secuencia_d = copy.deepcopy(reglas[mejor_regla])
    referencias_despacho = [instancia.refs[job] for job in mejor_secuencia_d]

    # Imprimir resultados de reglas
    print(f"Mejor regla de despacho: {mejor_regla}")
    print(f"Secuencia de índices: {mejor_secuencia_d}")
    print(f"Secuencia de referencias: {referencias_despacho}\n")

    # Guardar resultados de reglas
    resultados_despacho.append({
        "Instancia": i, **{regla: round(resultado, 2) for regla, resultado in resultados_reglas.items()},
        "Mejor Regla": mejor_regla, "Mejor Valor": round(mejor_resultado_d, 2)
    })

    # Heurísticas constructivas
    sec = EDD(instancia)
    heuristicas = {
        "CI": CheapestInsertion(instancia, sec),
        "MS": MinimumSlack(instancia),
        "ATC": ApparentTardinessCost(instancia)
    }
    resultados_heuristicas_ind = {heur: resultado for heur, (secuencia, resultado) in heuristicas.items()}
    mejor_heuristica, mejor_resultado_h = min(resultados_heuristicas_ind.items(), key=lambda x: x[1])
    mejor_secuencia_h = heuristicas[mejor_heuristica][0]
    referencias_heuristicas = [instancia.refs[job] for job in mejor_secuencia_h]

    # Imprimir resultados de heurísticas
    print(f"Mejor heurística: {mejor_heuristica}")
    print(f"Secuencia de índices: {mejor_secuencia_h}")
    print(f"Secuencia de referencias: {referencias_heuristicas}\n")

    # Guardar resultados de heurísticas
    resultados_heuristicas.append({
        "Instancia": i, **{heur: round(resultado, 2) for heur, resultado in resultados_heuristicas_ind.items()},
        "Mejor Heurística": mejor_heuristica, "Mejor Valor": round(mejor_resultado_h, 2)
    })

    # Metaheurísticas
    secuencia_ig, resultado_ig = iterated_greedy(instancia, mejor_secuencia_h, T=0.1, delta=2)
    best_fitness, best_solution = genetic_algorithm_hybrid(instancia, 100)
    mejor_metaheuristica, mejor_valor_meta = ("IG", resultado_ig) if resultado_ig < best_solution else ("GA", best_solution)
    mejor_secuencia_meta = secuencia_ig if mejor_metaheuristica == "IG" else best_fitness
    referencias_meta = [str(instancia.refs[job]) for job in mejor_secuencia_meta]

    # Imprimir resultados de metaheurísticas
    print(f"Mejor metaheurística: {mejor_metaheuristica}")
    print(f"Mejor resultado objetivo: {mejor_valor_meta}")
    print(f"Secuencia de índices: {mejor_secuencia_meta}")
    print(f"Secuencia de referencias: {referencias_meta}\n")

    # Guardar resultados de metaheurísticas
    resultados_metaheuristicas.append({
    "Instancia": i,
    "IG": round(resultado_ig, 2),
    "GA": round(best_solution, 2),
    "Mejor Metaheurística": mejor_metaheuristica,
    "Mejor Valor": round(mejor_valor_meta, 2),
    "Secuencia Referencias": referencias_meta  # Aquí se añaden las referencias
    })

# Guardar resultados en Excel
guardar_resultados_excel(excel_path, resultados_despacho, resultados_heuristicas, resultados_metaheuristicas)

