import os
import sys
import time
import datetime
# Importación de módulos propios (Capas de Lógica y Reporte)
from reportes import GeneradorReporte 
from core import recolector
from core import snapshotmkr
import Alpha_0_1 # Módulo de monitoreo en vivo
# Librerías de Rich para una UI avanzada en terminal
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.console import Group  # Necesario para agrupar elementos
from core import gestor_kill # Módulo para finalizar procesos (Opción 5)
# Configuración de compatibilidad para Windows (habilita colores ANSI)
if sys.platform == "win32":
    os.system('') 

# Instancia global de consola con soporte de color de 24 bits
console = Console(color_system="truecolor")

# PALETA DE COLORES (Variables constantes para mantener consistencia visual)
SNAP_COLOR = "#3e978b"  # Turquesa oscuro
SYS_COLOR  = "#d2e603"  # Lima/Amarillo
MARCO_COLOR = "#2ec1ac" # Turquesa brillante
ADORN_COLOR = "#eff48e" # Crema/Amarillo claro

def limpiar_pantalla():
    # Limpia la terminal según el Sistema Operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
     # Genera y renderiza el Banner ASCII y las opciones del menú
    limpiar_pantalla()

    # Creación del logo ASCII con manejo de no_wrap para evitar deformaciones
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

    # Empaquetado del logo en un Panel rígido (width=84) para evitar colapsos visuales
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
    console.print(f"  [{MARCO_COLOR}][/] [white]Seleccione una opcion del (1-6)[/]")
    console.print(f"  [{MARCO_COLOR}]1.[/] [white][CORE] Monitoreo en Tiempo Real[/]")
    console.print(f"  [{MARCO_COLOR}]2.[/] [white][CORE] Ver Top 5 Procesos[/]")
    console.print(f"  [{MARCO_COLOR}]3.[/] [white][ANALISIS] Snapshot del Sistema[/]")
    console.print(f"  [{MARCO_COLOR}]4.[/] [white][REPORTE] Generar Informe PDF[/]")
    console.print(f"  [{MARCO_COLOR}]5.[/] [red][kill] eliminar procesos[/]")
    console.print(f"  [bold red]6. Salir[/]")
    
    console.print(f"\n[{SYS_COLOR}]>>>>[/] " + f"[{ADORN_COLOR}]+--+  [/]" * 8)

def menu_principal():
    while True:
        mostrar_menu()
                # Input con el color turquesa del marco
        console.print(f"\n[{MARCO_COLOR}]S01@SNAP_SYS[/]:[bold white]~[/]$ ", end="")
        opcion = input()
        # --- LÓGICA DE RUTEO (Cada opción llama a una función del CORE) ---
        if opcion == "1":# Monitoreo en vivo (Uso de CPU/RAM dinámico)
            console.print(f"\n[{SYS_COLOR}][+][/] Iniciando monitoreo...")
            Alpha_0_1.monitoreo_envivo()
            input("\nPresiona Enter para volver...")
        
        elif opcion == "2":# Análisis de los 5 procesos más pesados
            console.print(f"\n[{SYS_COLOR}][+][/] Analizando procesos...")
            recolector.obtener_top_procesos() 
            input("\nPresiona Enter para volver...")

        elif opcion == "3":# Foto instantánea del estado del sistema
            with console.status(f"[bold {SYS_COLOR}]🔍 Accediendo a sensores...[/]", spinner="dots"):
                # Crear snapshot
                snapshot = snapshotmkr.crear_snapshot_sistema()
    
            if snapshot:
                # Mostrar en pantalla con el nuevo estilo Rich que definimos
                snapshotmkr.mostrar_snapshot_pantalla(snapshot)
                # Interacción para guardar en TXT o JSON
                # --- INTERACCIÓN ESTILIZADA ---
                console.print(f"\n[{MARCO_COLOR}]┌─[[/][bold white] ¿Desea exportar este reporte? [/][{MARCO_COLOR}]] [/]")
                guardar = console.input(f"[{MARCO_COLOR}]└─> [/][{ADORN_COLOR}](s/n): [/]").lower()

                if guardar == 's':
                    console.print(f"\n[{ADORN_COLOR}]📂 Formato de salida (txt/json):[/]")
                    formato = console.input(f"[{MARCO_COLOR}]>> [/][white][txt]: [/]").lower() or 'txt'
                    
                    # Generar nombre sugerido por defecto
                    sug_nombre = f"snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    console.print(f"[{ADORN_COLOR}]📛 Nombre del archivo (Enter para sugerido):[/]")
                    nombre = console.input(f"[{MARCO_COLOR}]>> [/][white][{sug_nombre}]: [/]") or sug_nombre
                    
                    # Guardamos usando la función que ya tienes
                    # Usamos los datos ya capturados para no volver a estresar el CPU
                    snapshotmkr.guardar_snapshot(snapshot, nombre, formato)
                    
                    console.print(f"\n[bold green]✔ ¡Archivo generado exitosamente en la carpeta /snapshots![/]")
                
                console.print(f"\n[{SYS_COLOR}]⏎ Presiona Enter para volver al centro de mando...[/]")
                input()

        elif opcion == "4":# Generación de informe profesional en PDF
            try:
                # Uso de barra de progreso dinámica de Rich
                with Progress(
                    SpinnerColumn(style=SYS_COLOR),
                    TextColumn(f"[{SNAP_COLOR}]" + "{task.description}"),
                    BarColumn(bar_width=None, complete_style=SYS_COLOR, finished_style=SNAP_COLOR),
                    TextColumn(f"[{ADORN_COLOR}]" + "{task.percentage:>3.0f}%"),
                    console=console
                ) as progress:
                    
                    # Esta línea debe tener UN NIVEL más de sangría que el 'with'
                    task = progress.add_task("Procesando...", total=3)
                    # Paso 1: Recolección, Paso 2: Análisis, Paso 3: PDF
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
        elif opcion == "5":# Acceso al gestor de eliminación de procesos

            gestor_kill.eliminar_proceso_seguro()

        elif opcion == "6": # Cierre seguro de la aplicación
            console.print(f"\n[{SNAP_COLOR}]Cerrando SNAP SYS...[/]")
            sys.exit()
        else:
            console.print("\n[bold yellow][!] Opción no válida.[/]")
            time.sleep(1.2)
# Punto de entrada del script
if __name__ == "__main__":
    menu_principal()