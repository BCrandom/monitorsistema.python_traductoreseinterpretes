import os
import sys
import time
import datetime
from reportes import GeneradorReporte 
from core import recolector
from core import snapshotmkr
import Alpha_0_1
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.console import Group  # Necesario para agrupar elementos

if sys.platform == "win32":
    os.system('') 

# Forzamos Truecolor y configuramos una sola instancia de consola
console = Console(color_system="truecolor")

# COLORES 
SNAP_COLOR = "#3e978b"
SYS_COLOR  = "#d2e603"
MARCO_COLOR = "#2ec1ac"
ADORN_COLOR = "#eff48e"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_pantalla()

    # Construcción del Logo con no_wrap=True para que NO se rompa al encoger
    logo_text = Text(no_wrap=True) 

    logo_text.append("███████╗███╗   ██╗ █████╗ ██████╗     ", style=SNAP_COLOR)
    logo_text.append("███████╗██╗   ██╗███████╗\n", style=SYS_COLOR)
    logo_text.append("██╔════╝████╗  ██║██╔══██╗██╔══██╗    ", style=SNAP_COLOR)
    logo_text.append("██╔════╝╚██╗ ██╔╝██╔════╝\n", style=SYS_COLOR)
    logo_text.append("███████╗██╔██╗ ██║███████║██████╔╝    ", style=SNAP_COLOR)
    logo_text.append("███████╗ ╚████╔╝ ███████╗\n", style=SYS_COLOR)
    logo_text.append("╚════██║██║╚██╗██║██╔══██║██╔═══╝     ", style=SNAP_COLOR)
    logo_text.append("╚════██║  ╚██╔╝  ╚════██║\n", style=SYS_COLOR)
    logo_text.append("███████║██║ ╚████║██║  ██║██║         ", style=SNAP_COLOR)
    logo_text.append("███████║   ██║   ███████║\n", style=SYS_COLOR)
    logo_text.append("╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝         ", style=SNAP_COLOR)
    logo_text.append("╚══════╝   ╚═╝   ╚══════╝", style=SYS_COLOR)

    # Agrupamos para mantener la estructura interna
    # Definimos un ancho fijo (width=80) para que el marco no colapse
    banner_panel = Panel(
        Align.center(logo_text),
        title=f"[bold {ADORN_COLOR}]GROUP_#01[/]",
        border_style=MARCO_COLOR,
        subtitle=f"[{ADORN_COLOR}]Te-I  [•]  S01  L  3:2  100%[/]",
        expand=False,      # Evita que ocupe todo el ancho de la terminal
        width=84,          # <--- ESTO FIJA EL TAMAÑO (ajústalo según tu logo)
        padding=(1, 2)
    )

    # Centramos el panel rígido
    console.print(Align.center(banner_panel))
    
    console.print(Align.center(f"[bold {ADORN_COLOR}]SISTEMA DE MONITOREO PROFESIONAL V1.0[/]\n"))
    console.print(f"\n[{ADORN_COLOR}]    ₊˚.༄  " + "˚‧⁺  ･ ˖ ·" * 6 + "[/]\n")
    
    # Opciones
    console.print(f"  [{MARCO_COLOR}][/] [white]Seleccione una opcion del (1-5)[/]")
    console.print(f"  [{MARCO_COLOR}]1.[/] [white][CORE] Monitoreo en Tiempo Real[/]")
    console.print(f"  [{MARCO_COLOR}]2.[/] [white][CORE] Ver Top 5 Procesos[/]")
    console.print(f"  [{MARCO_COLOR}]3.[/] [white][ANALISIS] Snapshot del Sistema[/]")
    console.print(f"  [{MARCO_COLOR}]4.[/] [white][REPORTE] Generar Informe PDF[/]")
    console.print(f"  [bold red]5. Salir[/]")
    
    console.print(f"\n[{SYS_COLOR}]>>>>[/] " + f"[{ADORN_COLOR}]+--+  [/]" * 8)

def menu_principal():
    while True:
        mostrar_menu()
                # Input con el color turquesa del marco
        console.print(f"\n[{MARCO_COLOR}]S01@SNAP_SYS[/]:[bold white]~[/]$ ", end="")
        opcion = input()
        
        if opcion == "1":
            console.print(f"\n[{SYS_COLOR}][+][/] Iniciando monitoreo...")
            Alpha_0_1.monitoreo_envivo()
            input("\nPresiona Enter para volver...")
        
        elif opcion == "2":
            console.print(f"\n[{SYS_COLOR}][+][/] Analizando procesos...")
            recolector.obtener_top_procesos() 
            input("\nPresiona Enter para volver...")

        elif opcion == "3":
            console.print(f"\n[{SYS_COLOR}][+][/] Capturando estado...")
            # Crear snapshot
            snapshot = snapshotmkr.crear_snapshot_sistema()
    
            if snapshot:
                # Mostrar en pantalla
                snapshotmkr.mostrar_snapshot_pantalla(snapshot)
                
                # Preguntar si quiere guardar
                guardar = input("\n¿Desea guardar el snapshot? (s/n): ").lower()
                if guardar == 's':
                    formato = input("Formato (txt/json) [txt]: ").lower() or 'txt'
                    nombre = input(f"Nombre del archivo [snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}]: ")
                    snapshotmkr.crear_snapshot_sistema(nombre, formato)
                    input("\nPresiona Enter para volver...")

        elif opcion == "4":
            try:
                # El bloque 'with' abre el contexto de la barra
                with Progress(
                    SpinnerColumn(style=SYS_COLOR),
                    TextColumn(f"[{SNAP_COLOR}]" + "{task.description}"),
                    BarColumn(bar_width=None, complete_style=SYS_COLOR, finished_style=SNAP_COLOR),
                    TextColumn(f"[{ADORN_COLOR}]" + "{task.percentage:>3.0f}%"),
                    console=console
                ) as progress:
                    
                    # Esta línea debe tener UN NIVEL más de sangría que el 'with'
                    task = progress.add_task("Procesando...", total=3)
                    
                    progress.update(task, description="Extrayendo métricas...")
                    datos = Alpha_0_1.obtener_datos_reporte()
                    progress.advance(task)
                    
                    progress.update(task, description="Analizando procesos...")
                    mem_sorted, top_5 = recolector.obtener_top_procesos(imprimir=False)
                    datos["mem_sorted"] = mem_sorted
                    datos["top_5"] = top_5
                    progress.advance(task)
                    
                    progress.update(task, description="Generando PDF...")
                    reporte = GeneradorReporte(datos)
                    reporte.crear_reporte()
                    progress.advance(task)

                console.print(f"\n[bold #00ff00] [ÉXITO] Reporte generado correctamente.[/]")
                input("\nPresiona Enter para volver...")
                
            except Exception as e:
                console.print(f"\n[bold red][ERROR]: {e}[/]")
                input("\nPresiona Enter para volver...")

        elif opcion == "5":
            console.print(f"\n[{SNAP_COLOR}]Cerrando SNAP SYS...[/]")
            sys.exit()
        else:
            console.print("\n[bold yellow][!] Opción no válida.[/]")
            time.sleep(1.2)

if __name__ == "__main__":
    menu_principal()