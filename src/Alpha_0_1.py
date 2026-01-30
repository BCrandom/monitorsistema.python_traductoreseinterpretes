import os
import sys
import psutil, datetime
import wmi
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich import box

if sys.platform == "win32":
    os.system('') 

# Forzamos Truecolor y configuramos una sola instancia de consola
console = Console(color_system="truecolor")

# COLORES 
SNAP_COLOR = "#3e978b"
SYS_COLOR  = "#d2e603"
MARCO_COLOR = "#2ec1ac"
ADORN_COLOR = "#eff48e"

def monitoreo_envivo():
    d_libre_C = 0 
    try:
        c = wmi.WMI()
        # CAPTURA DE DATOS
        v_ram = psutil.virtual_memory()
        v_swap = psutil.swap_memory()
        v_net = psutil.net_io_counters()
        v_stats = psutil.cpu_stats()
        v_boot_time = psutil.boot_time()
        v_disk_io = psutil.disk_io_counters()
        battery = psutil.sensors_battery()
        cpu_p = psutil.cpu_percent(interval=1) # <--- ESTA LÍNEA DEBE ESTAR ARRIBA

        # --- PANEL 1: IDENTIDAD DEL SISTEMA ---
        sys_text = Text()
        for os_info in c.Win32_OperatingSystem():
            sys_text.append(f"OS: {os_info.Caption}\n", style=ADORN_COLOR)
            sys_text.append(f"Versión: {os_info.Version}\n", style="white")
        
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(v_boot_time)
        sys_text.append(f"Uptime: {str(uptime).split('.')[0]}\n", style=SYS_COLOR)
        sys_text.append(f"Arranque: {datetime.datetime.fromtimestamp(v_boot_time).strftime('%Y-%m-%d %H:%M:%S')}", style="grey70")
        
        p_sys = Panel(sys_text, title=f"[{MARCO_COLOR}]💻 SISTEMA[/]", border_style=MARCO_COLOR, expand=True)

        # --- PANEL 2: CPU DETALLADA (TODA LA INFO WMI) ---
        cpu_table = Table(show_header=False, box=None, padding=(0, 1))

        color_carga = "green" if cpu_p < 70 else "yellow" if cpu_p < 85 else "red"
        cpu_table.add_row(f"[{SYS_COLOR}]USO ACTUAL DE CPU:[/]", f"[bold {color_carga}]{cpu_p}%[/]")
        cpu_table.add_row("", "") # Una línea de espacio para que respire el diseño

        for proc in c.Win32_Processor():
            cpu_table.add_row(f"[{SNAP_COLOR}]Nombre:[/]", proc.Name.strip())
            cpu_table.add_row(f"[{SNAP_COLOR}]Fabricante:[/]", proc.Manufacturer)
            cpu_table.add_row(f"[{SNAP_COLOR}]Núcleos/Hilos:[/]", f"{proc.NumberOfCores} / {proc.NumberOfLogicalProcessors}")
            cpu_table.add_row(f"[{SNAP_COLOR}]Arquitectura:[/]", f"{proc.AddressWidth} bits")
            cpu_table.add_row(f"[{SNAP_COLOR}]Frecuencia:[/]", f"{proc.CurrentClockSpeed} / {proc.MaxClockSpeed} MHz")
            cpu_table.add_row(f"[{SNAP_COLOR}]Socket/ID:[/]", f"{proc.SocketDesignation} / {proc.ProcessorId}")
            cpu_table.add_row(f"[{SNAP_COLOR}]Caché L2/L3:[/]", f"{proc.L2CacheSize}KB / {proc.L3CacheSize}KB")
        
        p_cpu = Panel(cpu_table, title=f"[{MARCO_COLOR}]⚙️ PROCESADOR[/]", border_style=MARCO_COLOR, expand=True)

        # --- PANEL 3: MEMORIA Y RED ---
        mem_net_table = Table(show_header=False, box=None)
        mem_net_table.add_row(f"[{SYS_COLOR}]RAM Total:[/]", f"{round(v_ram.total / (1024**3), 2)} GB")
        mem_net_table.add_row(f"[{SYS_COLOR}]RAM Libre:[/]", f"{round(v_ram.available / (1024**3), 2)} GB")
        mem_net_table.add_row(f"[{SYS_COLOR}]RAM Uso:[/]", f"{v_ram.percent}%")
        mem_net_table.add_row(f"[{SYS_COLOR}]SWAP Uso:[/]", f"{v_swap.percent}% ({v_swap.free / (1024**3):.2f} GB lib)")
        mem_net_table.add_row("", "") # Espacio
        mem_net_table.add_row(f"[{ADORN_COLOR}]RED Enviado:[/]", f"{v_net.bytes_sent / (1024**2):.2f} MB")
        mem_net_table.add_row(f"[{ADORN_COLOR}]RED Recibido:[/]", f"{v_net.bytes_recv / (1024**2):.2f} MB")
        
        p_mem = Panel(mem_net_table, title=f"[{MARCO_COLOR}]📊 MEMORIA & RED[/]", border_style=MARCO_COLOR, expand=True)

        # Imprimir primera fila de paneles
        console.print(Columns([p_sys, p_cpu, p_mem]))

        # --- PANEL 4: ALMACENAMIENTO E I/O ---
        disk_table = Table(box=box.SIMPLE, header_style=SYS_COLOR, expand=True)
        disk_table.add_column("Unidad")
        disk_table.add_column("Total")
        disk_table.add_column("Libre")
        disk_table.add_column("Uso I/O")

        for disco in c.Win32_LogicalDisk(DriveType=3):
            d_total = int(disco.Size) / (1024**3)
            d_libre = int(disco.FreeSpace) / (1024**3)
            if disco.DeviceID == "C:": d_libre_C = d_libre
            disk_table.add_row(
                disco.DeviceID, 
                f"{d_total:.2f} GB", 
                f"{d_libre:.2f} GB",
                f"L: {v_disk_io.read_bytes / (1024**2):.1f}MB | E: {v_disk_io.write_bytes / (1024**2):.1f}MB"
            )
        
        p_disk = Panel(disk_table, title=f"[{MARCO_COLOR}]💾 ALMACENAMIENTO[/]", border_style=MARCO_COLOR)

        # --- PANEL 5: GRÁFICOS Y SENSORES ---
        sensor_text = Text()
        sensor_text.append("--- GPU ---\n", style=ADORN_COLOR)
        for gpu in c.Win32_VideoController():
            v_vram = abs(int(gpu.AdapterRAM)) / (1024**2) if gpu.AdapterRAM else 0
            sensor_text.append(f"{gpu.Name} | VRAM: {v_vram:.2f} MB\n")
        
        sensor_text.append("\n--- VENTILADORES ---\n", style=ADORN_COLOR)
        fan_found = False
        try:
            for fan in c.Win32_Fan():
                if fan.DescriptiveName: 
                    sensor_text.append(f"  {fan.DescriptiveName}: {fan.DesiredSpeed} RPM\n")
                    fan_found = True
        except: pass
        if not fan_found: sensor_text.append("No se detectan RPM (WMI Limitado)\n", style="grey50")

        # Temperatura (Solo si hay acceso)
        try:
            w_temp = wmi.WMI(namespace="root\\wmi")
            temp_raw = w_temp.MSAcpi_ThermalZoneTemperature()
            if temp_raw:
                temp_c = (temp_raw[0].CurrentTemperature / 10.0) - 273.15
                sensor_text.append(f"\nTEMPERATURA CPU: {temp_c:.1f} °C", style="bold orange1")
        except:
            sensor_text.append("\nTEMP: No disponible (Sin Admin)", style="grey50")

        p_sensor = Panel(sensor_text, title=f"[{MARCO_COLOR}]🌡️ HARDWARE & FANS[/]", border_style=MARCO_COLOR, expand=True)

        # Imprimir segunda fila
        console.print(Columns([p_disk, p_sensor]))

        # --- PANEL FINAL: ESTADO Y PROCESOS ---
        pids = psutil.pids()
        usuarios = psutil.users()
        usr_str = ', '.join([u.name for u in usuarios]) if usuarios else "Ninguno"
        
        footer_text = Text()
        footer_text.append(f"Procesos Activos: {len(pids)}  |  Context Switches: {v_stats.ctx_switches}  |  Usuarios: {usr_str}\n", style="white")
        
        if battery:
            estado_bat = "🔌 Cargando" if battery.power_plugged else "🔋 Sin cargar"
            footer_text.append(f"BATERÍA: {battery.percent}% [{estado_bat}]\n", style=SYS_COLOR)

        # Semáforo
        if v_ram.percent > 85 or d_libre_C < 5:
            footer_text.append("🔴 ESTADO CRÍTICO: Recursos casi agotados.", style="bold red")
        elif v_ram.percent > 70:
            footer_text.append("🟡 ESTADO ADVERTENCIA: Carga elevada.", style="bold yellow")
        else:
            footer_text.append("🟢 SISTEMA SALUDABLE", style="bold green")

        console.print(Panel(footer_text, title=f"[{MARCO_COLOR}]📝 RESUMEN DE EJECUCIÓN[/]", border_style=MARCO_COLOR))

    except Exception as e:
        console.print(f"[bold red]❌ Error crítico: {e}[/]")

    console.print(f"\n[{ADORN_COLOR}]    ₊˚.༄  " + "˚‧⁺  ･ ˖ ·" * 8 + "[/]")
def obtener_datos_reporte():
    c = wmi.WMI()
    v_ram = psutil.virtual_memory()
    v_swap = psutil.swap_memory()
    v_net = psutil.net_io_counters()
    v_stats = psutil.cpu_stats()
    v_boot_time = psutil.boot_time()
    v_disk_io = psutil.disk_io_counters()
    cpu_f = psutil.cpu_percent(interval=1.0)
    processor = c.Win32_Processor()[0]
    
    fan_data = []
    try:
        # Intento 1: Clase Win32_Fan
        for fan in c.Win32_Fan():
            nombre = fan.DescriptiveName if fan.DescriptiveName else "Ventilador Sistema"
            velocidad = fan.DesiredSpeed if fan.DesiredSpeed else "N/A"
            fan_data.append(f"{nombre}: {velocidad} RPM")
            
        # Intento 2: Sensores que mencionen "fan"
        for sensor in c.Win32_TemperatureProbe():
            if sensor.Name and "fan" in sensor.Name.lower():
                fan_data.append(f"{sensor.Name}: {sensor.CurrentReading} RPM")
    except:
        pass
    
    # Convertimos la lista a un string o mensaje por defecto
    ventiladores_str = " | ".join(fan_data) if fan_data else "No detectados por WMI"
    
    # ESTE BLOQUE AHORA TIENE SANGRIÓN (4 ESPACIOS)
    datos = {
        # Sección 1
        "os_caption": c.Win32_OperatingSystem()[0].Caption,
        "os_version": c.Win32_OperatingSystem()[0].Version,
        "cpu_name": c.Win32_Processor()[0].Name,
        "cpu_manufacturer": processor.Manufacturer,
        "cpu_cores": processor.NumberOfCores,
        "cpu_logical": processor.NumberOfLogicalProcessors,
        "cpu_bits": processor.AddressWidth,
        "cpu_speed_cur": processor.CurrentClockSpeed,
        "cpu_speed_max": processor.MaxClockSpeed,
        "cpu_socket": processor.SocketDesignation,
        "cpu_id": processor.ProcessorId,
        "cpu_l2": processor.L2CacheSize,
        "cpu_l3": processor.L3CacheSize,
        # Sección 2
        "red_env": f"{v_net.bytes_sent / (1024**2):.2f} MB",
        "red_rec": f"{v_net.bytes_recv / (1024**2):.2f} MB",
        # Sección 3
        "gpu_name": c.Win32_VideoController()[0].Name,
        "vram": f"{abs(int(c.Win32_VideoController()[0].AdapterRAM)) / (1024**2):.2f} MB" if c.Win32_VideoController()[0].AdapterRAM else "0.00 MB",
        # Sección 4 (Asegúrate que d_libre_C esté definido arriba o usa psutil directamente)
        "disco_c_libre": psutil.disk_usage('C:').free / (1024**3),
        "disco_io_r": f"{v_disk_io.read_bytes / (1024**2):.2f} MB",
        "disco_io_w": f"{v_disk_io.write_bytes / (1024**2):.2f} MB",
        # Sección 5 y 6
        "pids": len(psutil.pids()),
        "ctx": v_stats.ctx_switches,
        "swap_info": f"{v_swap.percent}% usado ({v_swap.free / (1024**3):.2f} GB libres)",
        "uptime": str(datetime.datetime.now() - datetime.datetime.fromtimestamp(v_boot_time)).split('.')[0],
        "user": ", ".join([u.name for u in psutil.users()]) if psutil.users() else "eduardo",
        # Métricas Finales
        "cpu_final": cpu_f,
        "ram_total": round(v_ram.total / (1024**3), 2),
        "ram_disp": round(v_ram.available / (1024**3), 2),
        "ram_uso_p": v_ram.percent,
        "bat_p": psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A",
        "bat_c": psutil.sensors_battery().power_plugged if psutil.sensors_battery() else False,
        "f_arranque": str(datetime.datetime.fromtimestamp(v_boot_time))
    }
    
    # EL RETURN TAMBIÉN TIENE SANGRÍA
    return datos
