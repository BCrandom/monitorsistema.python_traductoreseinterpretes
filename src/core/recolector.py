import sys
import os
import psutil
import time
from rich.console import Console
from rich.table import Table
from rich.columns import Columns

if sys.platform == "win32":
    os.system('') 

# Forzamos Truecolor y configuramos una sola instancia de consola
console = Console(color_system="truecolor")

# COLORES 
SNAP_COLOR = "#3e978b"
SYS_COLOR  = "#d2e603"
MARCO_COLOR = "#2ec1ac"
ADORN_COLOR = "#eff48e"


def obtener_top_procesos(imprimir=True): 
    processes = []
    # --- Bloque Memoria ---
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            p_info = proc.as_dict(['pid', 'name', 'memory_percent'])
            proc.cpu_percent(interval=None) 
            processes.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    mem_sorted = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
    
    # --- BLOQUE CPU MODIFICADO ---
    # 1. Obtener uso por núcleo y número de núcleos
    uso_nucleos = psutil.cpu_percent(interval=0.2, percpu=True)
    num_nucleos = len(uso_nucleos)
    
    # 2. Inicializar medición de CPU para todos los procesos
    procesos_para_medir = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            proc.cpu_percent(interval=None)  # Inicializar contador
            procesos_para_medir.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # 3. Pequeña pausa para medición precisa
    time.sleep(0.3)
    
    # 4. Obtener y normalizar valores de CPU
    procesos_con_cpu = []
    for proc in procesos_para_medir:
        try:
            cpu_bruto = proc.cpu_percent(interval=None)
            cpu_norm = cpu_bruto / num_nucleos
            
            # Filtrar solo procesos con uso significativo (> 0.5%)
            if cpu_norm > 0.5:
                procesos_con_cpu.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': cpu_bruto,        # Valor bruto (original)
                    'cpu_norm': cpu_norm,            # Valor normalizado
                    'cpu_display': f"{cpu_norm:.1f}" # Para mostrar
                })
        except:
            continue
    
    # 5. Ordenar por CPU normalizada y tomar top 5
    top_5_cpu = sorted(procesos_con_cpu, 
                       key=lambda x: x['cpu_norm'], 
                       reverse=True)[:5]

    # --- ESTILO VISUAL ---
    if imprimir:
        # Tabla RAM (SIN CAMBIOS)
        tabla_mem = Table(title=f"[bold {ADORN_COLOR}]TOP PROCESOS POR MEMORIA[/]", 
                         border_style=SNAP_COLOR, 
                         header_style=f"bold {SYS_COLOR}")
        tabla_mem.add_column("PID", justify="right", style="cyan")
        tabla_mem.add_column("Nombre", style="white")
        tabla_mem.add_column("Memoria %", justify="center", style=ADORN_COLOR)

        for p in mem_sorted:
            tabla_mem.add_row(str(p['pid']), p['name'][:25], f"{p['memory_percent']:6.2f}%")

        # Tabla CPU MODIFICADA (muestra valores normalizados)
        tabla_cpu = Table(title=f"[bold {ADORN_COLOR}]TOP PROCESOS POR CPU (Normalizado para {num_nucleos} núcleos)[/]", 
                         border_style=MARCO_COLOR, 
                         header_style=f"bold {SYS_COLOR}")
        tabla_cpu.add_column("PID", justify="right", style="cyan")
        tabla_cpu.add_column("NOMBRE", style="white")
        tabla_cpu.add_column("CPU %", justify="center", style=ADORN_COLOR)
        tabla_cpu.add_column("Núcleo Est.", justify="center", style="magenta")

        for i, p in enumerate(top_5_cpu, 1):
            # Determinar núcleo estimado basado en el índice
            nucleo_estimado = (i % num_nucleos) + 1
            tabla_cpu.add_row(str(p['pid']), 
                            p['name'][:25], 
                            f"{p['cpu_norm']:.1f}%",
                            f"~{nucleo_estimado}")

        # Mostrar información adicional sobre núcleos
        uso_promedio = sum(uso_nucleos) / num_nucleos
        uso_max = max(uso_nucleos)
        nucleo_max = uso_nucleos.index(uso_max) + 1
        
        # Info de núcleos como texto enriquecido
        info_nucleos = f"[bold {SYS_COLOR}]📊 Info Núcleos:[/] [cyan]{num_nucleos} núcleos[/] | "
        info_nucleos += f"[green]Prom: {uso_promedio:.1f}%[/] | "
        
        # Mostrar todo
        console.print("\n")
        console.print(info_nucleos)
        console.print("\n")
        console.print(Columns([tabla_mem, tabla_cpu]))
        
        # Adorno final
        console.print(f"\n[{MARCO_COLOR}]    ₊˚.༄  " + "˚‧⁺  ･ ˖ ·" * 8 + "[/]")

    # Retornamos los datos (manteniendo compatibilidad)
    return obtener_top_procesos_lista(mem_sorted, top_5_cpu)

def obtener_top_procesos_lista(mem_sorted, top_5_cpu):

    return mem_sorted, top_5_cpu
    






# def obtener_top_procesos():
   # print(f"\n{'PID':<10} {'NOMBRE':<25} {'CPU %':<10}")
   # procesos = []
   # for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
   #     try:
    #        procesos.append(proc.info)
    #    except (psutil.NoSuchProcess, psutil.AccessDenied):
     #       continue
    #top_5 = sorted(procesos, key=lambda x: x['cpu_percent'], reverse=True)[:5]
    #for p in top_5:
    #    print(f"{p['pid']:<10} {p['name'][:25]:<25} {p['cpu_percent']:<10}") 