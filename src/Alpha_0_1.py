
import psutil, datetime
import wmi

def monitoreo_envivo():
    # Inicializamos d_libre_C fuera para que los diccionarios siempre lo encuentren
    d_libre_C = 0 
    
    try:
        c = wmi.WMI()
        # 0. CAPTURA PREVIA
        v_ram = psutil.virtual_memory()
        v_swap = psutil.swap_memory()
        v_net = psutil.net_io_counters()
        v_stats = psutil.cpu_stats()
        v_boot_time = psutil.boot_time()

        # 1. INFORMACIÓN DEL SISTEMA
        for os in c.Win32_OperatingSystem():
            print("-" * 13)
            print(f"OS: {os.Caption} | Versión: {os.Version}")
        for cpu_info in c.Win32_Processor():
            print(f"Procesador: {cpu_info.Name}")
        print("-" * 13)

        # 2. RED
        print(f"RED: Enviado: {v_net.bytes_sent / (1024**2):.2f} MB | Recibido: {v_net.bytes_recv / (1024**2):.2f} MB")
        print("-" * 13)

        # 3. GRÁFICOS E INFORMACIÓN DE LA CPU
        print("--- GRÁFICOS ---")
        for gpu in c.Win32_VideoController():
            v_vram = abs(int(gpu.AdapterRAM)) / (1024**2) if gpu.AdapterRAM else 0
            print(f"GPU: {gpu.Name} | VRAM: {v_vram:.2f} MB")
        print("-" * 13)

        print("--- INFORMACIÓN DE LA CPU ---")
        for processor in c.Win32_Processor():
            print(f"== PROCESADOR: {processor.Name.strip()} ==")
            print(f"Fabricante: {processor.Manufacturer}")
            print(f"Núcleos: {processor.NumberOfCores}")
            print(f"Procesadores lógicos: {processor.NumberOfLogicalProcessors}")
            print(f"Arquitectura: {processor.AddressWidth} bits")
            print(f"Velocidad actual: {processor.CurrentClockSpeed} MHz")
            print(f"Velocidad máxima: {processor.MaxClockSpeed} MHz")
            print(f"Socket: {processor.SocketDesignation}")
            print(f"ID: {processor.ProcessorId}")
            print(f"Nivel de caché L2: {processor.L2CacheSize} KB")
            print(f"Nivel de caché L3: {processor.L3CacheSize} KB")
        print("-" * 50)
    
        # 4. Ventilador (La librería WMI tiene limitaciones y LibreHardware requiere más trabajo de implementar)
        fan_speeds = {}
        try:
            for fan in c.Win32_Fan():
                if fan.DescriptiveName:  # Verificar que tenga nombre
                # DesiredSpeed es la velocidad deseada/actual
                    fan_speeds[fan.DescriptiveName] = fan.DesiredSpeed
        except:
            pass  # Si no existe la clase, continuamos
    
        for sensor in c.Win32_TemperatureProbe():
         # Buscamos sensores que mencionen "fan" en el nombre
            if "fan" in sensor.Name.lower():
                # CurrentReading es la lectura actual
                fan_speeds[sensor.Name] = sensor.CurrentReading
        
        speeds = fan_speeds
    
        if speeds:
            print("Ventiladores encontrados:")
            for fan, speed in speeds.items():
                print(f"  {fan}: {speed} RPM")
        else:
         print("No se encontraron datos de ventiladores, es posible que su hardware no exponga datos mediante WMI")

        # 5. ALMACENAMIENTO
        print("\n--- ALMACENAMIENTO ---")
        for disco in c.Win32_LogicalDisk(DriveType=3):
            d_total = int(disco.Size) / (1024**3)
            d_libre = int(disco.FreeSpace) / (1024**3)
            if disco.DeviceID == "C:": d_libre_C = d_libre
            print(f"Unidad {disco.DeviceID} | {d_total:.2f} GB Totales | {d_libre:.2f} GB Libres")
            
        v_disk_io = psutil.disk_io_counters()
        print(f"Actividad I/O: Lectura: {v_disk_io.read_bytes / (1024**2):.2f} MB | Escritura: {v_disk_io.write_bytes / (1024**2):.2f} MB")
        print("-" * 13)

        # 6. RESUMEN DE EJECUCIÓN
        pids = psutil.pids()
        print(f"Procesos activos: {len(pids)} | Cambios de Contexto: {v_stats.ctx_switches}")
        print(f"MEMORIA SWAP: {v_swap.percent}% usado ({v_swap.free / (1024**3):.2f} GB libres)")

        # 7. TIEMPO ACTIVO Y USUARIOS
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(v_boot_time)
        print(f"TIEMPO ACTIVO: {str(uptime).split('.')[0]}")

        usuarios = psutil.users()
        if usuarios:
            print(f"USUARIOS ACTIVOS: {', '.join([u.name for u in usuarios])}")
        
        # 8. TEMPERATURA (Sub-bloque protegido)
        try:
            w_temp = wmi.WMI(namespace="root\\wmi")
            temp_raw = w_temp.MSAcpi_ThermalZoneTemperature()
            if temp_raw:
                temp_c = (temp_raw[0].CurrentTemperature / 10.0) - 273.15
                print(f"TEMPERATURA CPU: {temp_c:.1f} °C")
        except:
            print("TEMPERATURA: No disponible (requiere Admin)")

        # 9. ANÁLISIS DE ANOMALÍAS (El Semáforo)
        print("\n>>> ANÁLISIS SEMÁNTICO:")
        if v_ram.percent > 85 or d_libre_C < 5:
            print("🔴 ESTADO: CRÍTICO - Recursos agotados.")
        elif v_ram.percent > 70:
            print("🟡 ESTADO: ADVERTENCIA - Carga elevada.")
        else:
            print("🟢 ESTADO: SALUDABLE")
        print("=" * 15)

    except Exception as e:
        print(f"❌ Error crítico en el monitoreo: {e}")
        return None

    # --- REPARACIÓN DE LOS PRINTS Y RECOLECCIÓN ---
    # Salimos del bloque try para los prints finales
    print("Porcentaje de CPU usado:" , psutil.cpu_percent(interval=1))
    print("-------------")
    print("Cantidad total de RAM:" , round(v_ram.total / (1024**3), 2), "GB")
    print("-------------")
    print("RAM disponible:" , round(v_ram.available / (1024**3), 2), "GB")
    print("-------------")
    print("Porcentaje de RAM usada:" , v_ram.percent, "%")
    print("-------------")
    
    battery = psutil.sensors_battery()
    if battery:
        print("Porcentaje de batería:" , battery.percent, "%" )
        print("-------------")
        print("¿Se está cargando el dispositivo?:" , battery.power_plugged)
    
    print("-------------")
    print("Fecha de arranque: ", datetime.datetime.fromtimestamp(v_boot_time))

def obtener_datos_reporte():
    c = wmi.WMI()
    v_ram = psutil.virtual_memory()
    v_swap = psutil.swap_memory()
    v_net = psutil.net_io_counters()
    v_stats = psutil.cpu_stats()
    v_boot_time = psutil.boot_time()
    v_disk_io = psutil.disk_io_counters()
    cpu_f = psutil.cpu_percent(interval=1.0)
    
    # ESTE BLOQUE AHORA TIENE SANGRIÓN (4 ESPACIOS)
    datos = {
        # Sección 1
        "os_caption": c.Win32_OperatingSystem()[0].Caption,
        "os_version": c.Win32_OperatingSystem()[0].Version,
        "cpu_name": c.Win32_Processor()[0].Name,
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
