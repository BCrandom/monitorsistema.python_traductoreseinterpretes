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
    # --- Bloque Memoria (TU CÓDIGO INTACTO) ---
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            p_info = proc.as_dict(['pid', 'name', 'memory_percent'])
            proc.cpu_percent(interval=None) 
            processes.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    mem_sorted = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
    
    # --- Bloque CPU (TU CÓDIGO INTACTO) ---
    procesos_cpu = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            procesos_cpu.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_5 = sorted(procesos_cpu, key=lambda x: x['cpu_percent'], reverse=True)[:5]

    # --- ESTILO VISUAL (Solo cambiamos los prints) ---
    if imprimir:
        # Tabla RAM
        tabla_mem = Table(title=f"[bold {ADORN_COLOR}]TOP PROCESOS POR MEMORIA[/]", border_style=SNAP_COLOR, header_style=f"bold {SYS_COLOR}")
        tabla_mem.add_column("PID", justify="right", style="cyan")
        tabla_mem.add_column("Nombre", style="white")
        tabla_mem.add_column("Memoria %", justify="center", style=ADORN_COLOR)

        for p in mem_sorted:
            # Usamos tus variables exactas: p['pid'], p['name'], p['memory_percent']
            tabla_mem.add_row(str(p['pid']), p['name'][:25], f"{p['memory_percent']:6.2f}%")

        # Tabla CPU
        tabla_cpu = Table(title=f"[bold {ADORN_COLOR}]TOP PROCESOS POR CPU[/]", border_style=MARCO_COLOR, header_style=f"bold {SYS_COLOR}")
        tabla_cpu.add_column("PID", justify="right", style="cyan")
        tabla_cpu.add_column("NOMBRE", style="white")
        tabla_cpu.add_column("CPU %", justify="center", style=ADORN_COLOR)

        for p in top_5:
            # Usamos tus variables exactas: p['pid'], p['name'], p['cpu_percent']
            tabla_cpu.add_row(str(p['pid']), p['name'][:25], f"{p['cpu_percent']}")

        # Mostramos las tablas una al lado de la otra
        console.print("\n")
        console.print(Columns([tabla_mem, tabla_cpu]))
        
        # Tu adorno final
        console.print(f"\n[{MARCO_COLOR}]    ₊˚.༄  " + "˚‧⁺  ･ ˖ ·" * 8 + "[/]")

    # Retornamos los datos tal cual los pediste
    return obtener_top_procesos_lista(mem_sorted, top_5)

def obtener_top_procesos_lista(mem_sorted, top_5):

    return  mem_sorted, top_5


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