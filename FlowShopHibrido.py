from scheptk.scheptk import Model
from scheptk.util import read_tag

class FlowShopHibrido(Model):
    def __init__(self, filename):
        # Usamos esta funcion para leer los datos de las instancias generadas aleatoriamente
        self.jobs = read_tag(filename, 'JOBS')
        self.machines = read_tag(filename, 'MACHINES')
        self.pt = [
            read_tag(filename, 'PT_MEC1'),  
            read_tag(filename, 'PT_MEC2'),  
            read_tag(filename, 'PT_MEC3'),  
            read_tag(filename, 'PT_SOL1'),  
            read_tag(filename, 'PT_SOL2'),  
            read_tag(filename, 'PT_MONT')  
        ]
        self.setup = [  # Tiempos de setup para la etapa 2 (Soldadura)
            read_tag(filename, 'SS_SOL1'),
            read_tag(filename, 'SS_SOL2')
        ]
        self.a = read_tag(filename, 'A') # A es la ocupación inicial
        self.dd = read_tag(filename, 'DD')
        self.w = read_tag(filename, 'W')
        self.refs = read_tag(filename, 'REFS')
       
        # Para calcular sumapt de cada producto, escogemos de cada etapa la máquina con menor pt
        sumapt = [0 for i in range(self.jobs)]
        for i in range(self.jobs):
            sumapt[i] += min( self.pt[0][i],self.pt[1][i],self.pt[2][i] )
            sumapt[i] += min( self.pt[3][i],self.pt[4][i] )
            sumapt[i] += self.pt[5][i]
           
    def ct(self, solution):
        # Fucnión que calcula los completion times de cada trabajo
        ct = [[0 for j in range(self.jobs)] for i in range(6)]
       
        # Para el cálculo de tiempos de cada trabajo, inicializamos con 'a',
        # tiempo de ocupación inicial de cada máquina
       
        t_disp_mec1 = self.a[0]
        t_disp_mec2 = self.a[1]
        t_disp_mec3 = self.a[2]
        t_disp_sol1 = self.a[3]
        t_disp_sol2 = self.a[4]
        t_disp_mont = self.a[5]
       
        for j, job in enumerate(solution):
           
            # ETAPA 1 de (MECANIZADO)
           
            # ct de cada máquina
            tiempos = [
                t_disp_mec1 + self.pt[0][job],  
                t_disp_mec2 + self.pt[1][job],  
                t_disp_mec3 + self.pt[2][job]  
            ]
           
            # Buscamos la máquina con el menor ct
            maquina_seleccionada = tiempos.index(min(tiempos))
           
            # Actualizamos el ct del trabajo en la máquina que hemos seleccionado
            t_fin_mec = 0
            if maquina_seleccionada == 0:
                ct[0][j] = t_disp_mec1 + self.pt[0][job]
                t_disp_mec1 = ct[0][j]
                t_fin_mec += ct[0][j]
            elif maquina_seleccionada == 1:
                ct[1][j] = t_disp_mec2 + self.pt[1][job]
                t_disp_mec2 = ct[1][j]
                t_fin_mec += ct[1][j]
            else:
                ct[2][j] = t_disp_mec3 + self.pt[2][job]
                t_disp_mec3 = ct[2][j]
                t_fin_mec += ct[2][j]
           
            # ETAPA 2 (SOLDADURA)
           
            tiempos_sol = [
               max(t_fin_mec, t_disp_sol1) + self.setup[0][job] + self.pt[3][job],
               max(t_fin_mec, t_disp_sol2) + self.setup[1][job] + self.pt[4][job]
               ]
            maquina_seleccionada = tiempos_sol.index(min(tiempos_sol))
           
            if maquina_seleccionada == 0:
                ct[3][j] = max(t_fin_mec, t_disp_sol1) + self.setup[0][job] + self.pt[3][job]
                t_disp_sol1 = ct[3][j]
                t_fin_sol = ct[3][j]
            else:
                ct[4][j] = max(t_fin_mec, t_disp_sol2) + self.setup[1][job] + self.pt[4][job]
                t_disp_sol2 = ct[4][j]
                t_fin_sol = ct[4][j]
                       
            # ETAPA 3 (ENSAMBLAJE)
           
            ct[5][j] = max(t_disp_mont, t_fin_sol) + self.pt[5][job]
           
            t_disp_mont = ct[5][j]

        return ct, solution
