import psutil
import os
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

LISTA_BLANCA_NOMBRES = [
    "system", "idle", "explorer.exe", "services.exe", "lsass.exe", 
    "wininit.exe", "smss.exe", "csrss.exe", "registry", "python.exe",
    "svchost.exe", "winlogon.exe", "system idle process"
]

RUTAS_PROTEGIDAS = ["C:\\Windows\\System32", "C:\\Windows\\SysWOW64"]

def listar_candidatos_eliminacion():
    num_nucleos_fisicos = psutil.cpu_count(logical=False)
    num_nucleos_logicos = psutil.cpu_count(logical=True)
    table = Table(title="[bold red]PROCESOS DE ALTO CONSUMO (MODO GESTIÓN) - [/]", 
                  border_style="red", header_style="bold yellow")
    
    table.add_column("PID", justify="right", style="cyan")
    table.add_column("Nombre", style="white")
    table.add_column("CPU %", justify="center")
    table.add_column("RAM %", justify="center")
    table.add_column("Riesgo", justify="center")

    candidatos = []
    
    # --- NUEVA ESTRATEGIA: MUESTREO POR BLOQUE ---
    with console.status("[bold yellow]Muestreando actividad del procesador (1s)...[/]"):
        # 1. Obtenemos la lista de procesos una sola vez
        procesos_activos = []
        for p in psutil.process_iter(['pid', 'name', 'exe', 'memory_percent']):
            try:
                # El primer llamado "prepara" el contador interno del objeto
                p.cpu_percent(interval=None)
                procesos_activos.append(p)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # 2. Una espera corta pero suficiente (0.5s a 1s basta para psutil)
        time.sleep(0.5)

    for p in procesos_activos:
        try:
            # 3. El segundo llamado ahora sí tiene una referencia temporal previa
            cpu_total = p.cpu_percent(interval=None)
            
            # 4. OPCIONAL: Mostrar el valor real por núcleo o el normalizado
            cpu_norm = cpu_total / psutil.cpu_count() 

            info = p.info
            mem = info['memory_percent']
            path = info['exe'] or ""
            nombre = info['name'] or "Desconocido"

            es_vital = (
                nombre.lower() in LISTA_BLANCA_NOMBRES or 
                any(ruta.lower() in path.lower() for ruta in RUTAS_PROTEGIDAS)
            )

            # Si el CPU es mayor a 0.0 o la RAM es significativa, lo mostramos
            if not es_vital and (cpu_norm > 0.0 or mem > 1.0):
                riesgo = "[green]BAJO[/]" if cpu_norm < 10 else "[bold yellow]MEDIO[/]"
                if cpu_norm > 30: riesgo = "[bold red]ALTO[/]"
                
                table.add_row(str(info['pid']), nombre[:25], f"{cpu_norm:.1f}%", f"{mem:.1f}%", riesgo)
                candidatos.append(info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    console.print(table)
    return candidatos

def eliminar_proceso_seguro():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel.fit("[bold red]🚀 GESTOR DE OPTIMIZACIÓN DE RECURSOS[/]\n"
                            "[white]Analizando procesos no vitales. Escribe 'no' para salir.[/]"))

    pids_disponibles = listar_candidatos_eliminacion()

    if not pids_disponibles:
        console.print("[bold green]✔ No se detectaron procesos activos fuera de la lista blanca.[/]")
        input("\nPresiona Enter para continuar...")
        return

    target = Prompt.ask("\n[bold cyan]Ingrese el PID para finalizar[/] (o escribe [bold red]'no'[/] para salir)")

    if target.lower() == 'no':
        return

    try:
        pid_int = int(target)
        if pid_int in pids_disponibles:
            proc = psutil.Process(pid_int)
            nombre = proc.name()
            if Prompt.ask(f"¿Matar {nombre}?", choices=["s", "n"]) == "s":
                proc.terminate()
                console.print(f"[bold green]✔ Proceso finalizado.[/]")
        else:
            console.print("[bold red]⚠ PID inválido o protegido.[/]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")

    input("\nPresiona Enter para continuar...")