from scheptk.util import sorted_index_desc, sorted_index_asc

def EDD(instancia):
    # `instancia` es ya un objeto de FlowShopHibrido, no es necesario crear uno nuevo
    secuencia = sorted_index_asc(instancia.dd)
    return secuencia

def LPT(instancia):
    # `instancia` es ya un objeto de FlowShopHibrido, sumamos directamente
    sum_pt = [0 for i in range(instancia.jobs)]
    for i in range(instancia.jobs):
        sum_pt[i] += min(instancia.pt[0][i], instancia.pt[1][i], instancia.pt[2][i])
        sum_pt[i] += min(instancia.pt[3][i], instancia.pt[4][i])
        sum_pt[i] += instancia.pt[5][i]
    secuencia = sorted_index_desc(sum_pt)
    return secuencia

def WSPT(instancia):
    # `instancia` es ya un objeto de FlowShopHibrido, usamos directamente los datos
    wspt = [0 for i in range(instancia.jobs)]
    sum_pt = [0 for i in range(instancia.jobs)]
    for i in range(instancia.jobs):
        sum_pt[i] = sum(instancia.pt[j][i] for j in range(instancia.machines))
    for i in range(instancia.jobs):
        wspt[i] = instancia.w[i] / sum_pt[i]
    secuencia = sorted_index_desc(wspt)
    return secuencia

