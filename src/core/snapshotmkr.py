import psutil
import datetime
from collections import OrderedDict
import socket
import platform
import json
import wmi
import os

def crear_snapshot_sistema(nombre_archivo=None, formato='txt'):
    """
    Crea una instantánea completa del sistema
    formatos soportados: 'txt y json'
    """
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    snapshot = OrderedDict()
    snapshot['timestamp'] = timestamp
    
    try:
        # 1. INFORMACIÓN BÁSICA DEL SISTEMA
        snapshot['sistema'] = {
            'hostname': socket.gethostname(),
            'sistema_operativo': platform.system(),
            'version_os': platform.version(),
            'arquitectura': platform.architecture()[0],
            'procesador': platform.processor(),
            'maquina': platform.machine()
        }
        
        # 2. INFORMACIÓN DE HARDWARE (usando WMI como en tu Alpha_0_1)
        try:
            c = wmi.WMI()
            for os_info in c.Win32_OperatingSystem():
                snapshot['sistema']['os_caption'] = os_info.Caption
                snapshot['sistema']['os_version'] = os_info.Version
                break
                
            for cpu_info in c.Win32_Processor():
                snapshot['cpu_detallada'] = {
                    'nombre': cpu_info.Name.strip(),
                    'fabricante': cpu_info.Manufacturer,
                    'nucleos': cpu_info.NumberOfCores,
                    'procesadores_logicos': cpu_info.NumberOfLogicalProcessors,
                    'velocidad_actual_mhz': cpu_info.CurrentClockSpeed,
                    'velocidad_max_mhz': cpu_info.MaxClockSpeed,
                    'arquitectura_bits': f"{cpu_info.AddressWidth} bits",
                    'cache_l2_kb': cpu_info.L2CacheSize,
                    'cache_l3_kb': cpu_info.L3CacheSize,
                    'socket': cpu_info.SocketDesignation
                }
                break
        except:
            snapshot['cpu_detallada'] = "Información WMI no disponible"
        
        # 3. MÉTRICAS DE RENDIMIENTO EN TIEMPO REAL
        snapshot['rendimiento'] = {
            'cpu': {
                'porcentaje_uso': psutil.cpu_percent(interval=0.5),
                'porcentaje_por_nucleo': psutil.cpu_percent(interval=0.5, percpu=True),
                'frecuencia_actual': psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
                'frecuencia_max': psutil.cpu_freq().max if psutil.cpu_freq() else "N/A",
                'conteo_fisico': psutil.cpu_count(logical=False),
                'conteo_logico': psutil.cpu_count(logical=True)
            },
            'memoria': {
                'total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'disponible_gb': round(psutil.virtual_memory().available / (1024**3), 2),
                'usado_gb': round(psutil.virtual_memory().used / (1024**3), 2),
                'porcentaje_usado': psutil.virtual_memory().percent,
                'swap_total_gb': round(psutil.swap_memory().total / (1024**3), 2),
                'swap_usado_gb': round(psutil.swap_memory().used / (1024**3), 2),
                'swap_porcentaje': psutil.swap_memory().percent
            }
        }
        
        # 4. ALMACENAMIENTO
        particiones = []
        for particion in psutil.disk_partitions():
            try:
                uso = psutil.disk_usage(particion.mountpoint)
                particiones.append({
                    'dispositivo': particion.device,
                    'punto_montaje': particion.mountpoint,
                    'sistema_archivos': particion.fstype,
                    'total_gb': round(uso.total / (1024**3), 2),
                    'usado_gb': round(uso.used / (1024**3), 2),
                    'libre_gb': round(uso.free / (1024**3), 2),
                    'porcentaje_usado': uso.percent
                })
            except:
                continue
        
        snapshot['almacenamiento'] = {
            'particiones': particiones,
            'io_counters': {
                'lecturas_totales': psutil.disk_io_counters().read_count if psutil.disk_io_counters() else 0,
                'escrituras_totales': psutil.disk_io_counters().write_count if psutil.disk_io_counters() else 0,
                'bytes_leidos_mb': round(psutil.disk_io_counters().read_bytes / (1024**2), 2) if psutil.disk_io_counters() else 0,
                'bytes_escritos_mb': round(psutil.disk_io_counters().write_bytes / (1024**2), 2) if psutil.disk_io_counters() else 0
            }
        }
        
        # 5. RED
        snapshot['red'] = {
            'direcciones_ip': [],
            'estadisticas': {
                'bytes_enviados_mb': round(psutil.net_io_counters().bytes_sent / (1024**2), 2),
                'bytes_recibidos_mb': round(psutil.net_io_counters().bytes_recv / (1024**2), 2),
                'paquetes_enviados': psutil.net_io_counters().packets_sent,
                'paquetes_recibidos': psutil.net_io_counters().packets_recv
            }
        }
        
        # Obtener todas las interfaces y sus IPs
        for interfaz, addrs in psutil.net_if_addrs().items():
            ips = []
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
                    ips.append(addr.address)
                elif addr.family == socket.AF_INET6:  # IPv6
                    ips.append(addr.address)
            
            if ips:
                snapshot['red']['direcciones_ip'].append({
                    'interfaz': interfaz,
                    'direcciones': ips
                })
        
        # 6. PROCESOS (Top 5 por CPU y Memoria)
        procesos = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                proc.cpu_percent()  # Primera llamada para inicializar
                info = proc.info
                procesos.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Ordenar y tomar top
        top_cpu = sorted(procesos, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:5]
        top_mem = sorted(procesos, key=lambda x: x.get('memory_percent', 0), reverse=True)[:5]
        
        snapshot['procesos'] = {
            'total_procesos': len(psutil.pids()),
            'top_10_cpu': top_cpu,
            'top_10_memoria': top_mem
        }
        
        # 7. INFORMACIÓN DE TIEMPO
        snapshot['tiempo'] = {
            'hora_sistema': timestamp,
            'fecha_arranque': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 8. USUARIOS CONECTADOS
        usuarios = []
        for user in psutil.users():
            usuarios.append({
                'nombre': user.name,
                'terminal': user.terminal,
                'host': user.host,
                'inicio_sesion': datetime.datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        snapshot['usuarios'] = usuarios
        
        # 9. ANÁLISIS DE SALUD DEL SISTEMA
        snapshot['salud_sistema'] = {
            'cpu_critico': snapshot['rendimiento']['cpu']['porcentaje_uso'] > 85,
            'ram_critico': snapshot['rendimiento']['memoria']['porcentaje_usado'] > 85,
            'swap_critico': snapshot['rendimiento']['memoria']['swap_porcentaje'] > 85,
            'disco_critico': any(p['porcentaje_usado'] > 90 for p in particiones),
            'recomendaciones': []
        }
        
        # Generar recomendaciones
        recomendaciones = []
        if snapshot['rendimiento']['cpu']['porcentaje_uso'] > 80:
            recomendaciones.append("CPU con uso elevado. Revisar procesos en top_cpu.")
        if snapshot['rendimiento']['memoria']['porcentaje_usado'] > 80:
            recomendaciones.append("RAM con uso elevado. Considerar cerrar aplicaciones.")
        
        for particion in particiones:
            if particion['porcentaje_usado'] > 90:
                recomendaciones.append(f"Particion {particion['punto_montaje']} casi llena ({particion['porcentaje_usado']}%)")
        
        snapshot['salud_sistema']['recomendaciones'] = recomendaciones
        
        # 10. GUARDAR SNAPSHOT EN EL FORMATO SOLICITADO
        if nombre_archivo:
            guardar_snapshot(snapshot, nombre_archivo, formato)
        
        return snapshot
        
    except Exception as e:
        print(f"Error creando snapshot: {e}")
        return None

def guardar_snapshot(snapshot, nombre_archivo, formato='txt'):
    """Guarda el snapshot en diferentes formatos"""
    
    timestamp = snapshot['timestamp'].replace(':', '-').replace(' ', '_')
    
    if not nombre_archivo:
        nombre_archivo = f"snapshot_{timestamp}"

    # Crear carpeta 'snapshots' si no existe
    CARPETA_SNAPSHOTS = "snapshots"
    if not os.path.exists(CARPETA_SNAPSHOTS):
        os.makedirs(CARPETA_SNAPSHOTS)

    
    try:
        if formato == 'txt':
            ruta_completa = os.path.join(CARPETA_SNAPSHOTS, f"{nombre_archivo}.txt")
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write(f"SNAPSHOT DEL SISTEMA - {snapshot['timestamp']}\n")
                f.write("="*60 + "\n\n")
                
                # Sistema
                f.write("1. INFORMACIÓN DEL SISTEMA:\n")
                f.write("-"*40 + "\n")
                for key, value in snapshot['sistema'].items():
                    f.write(f"  {key.replace('_', ' ').title()}: {value}\n")
                
                # CPU Detallada
                f.write("\n2. PROCESADOR:\n")
                f.write("-"*40 + "\n")
                if isinstance(snapshot['cpu_detallada'], dict):
                    for key, value in snapshot['cpu_detallada'].items():
                        f.write(f"  {key.replace('_', ' ').title()}: {value}\n")
                
                # Rendimiento
                f.write("\n3. RENDIMIENTO ACTUAL:\n")
                f.write("-"*40 + "\n")
                f.write(f"  CPU Total: {snapshot['rendimiento']['cpu']['porcentaje_uso']}%\n")
                f.write(f"  RAM Usada: {snapshot['rendimiento']['memoria']['porcentaje_usado']}%\n")
                f.write(f"  Swap Usado: {snapshot['rendimiento']['memoria']['swap_porcentaje']}%\n")
                
                # Almacenamiento
                f.write("\n4. ALMACENAMIENTO:\n")
                f.write("-"*40 + "\n")
                for part in snapshot['almacenamiento']['particiones']:
                    f.write(f"  {part['punto_montaje']}: {part['porcentaje_usado']}% usado ")
                    f.write(f"({part['libre_gb']} GB libre de {part['total_gb']} GB)\n")
                
                # Procesos
                f.write("\n5. TOP 5 PROCESOS POR CPU:\n")
                f.write("-"*40 + "\n")
                for i, proc in enumerate(snapshot['procesos']['top_10_cpu'][:5], 1):
                    f.write(f"  {i}. {proc['name']} (PID: {proc['pid']}) - CPU: {proc.get('cpu_percent', 0)}%\n")
                
                # Salud del sistema
                f.write("\n6. ANÁLISIS DE SALUD:\n")
                f.write("-"*40 + "\n")
                if snapshot['salud_sistema']['recomendaciones']:
                    f.write("  ⚠️  RECOMENDACIONES:\n")
                    for rec in snapshot['salud_sistema']['recomendaciones']:
                        f.write(f"    • {rec}\n")
                else:
                    f.write("  ✅ Sistema en estado óptimo\n")
                
                f.write("\n" + "="*60 + "\n")
                f.write(f"Snapshot generado el: {snapshot['timestamp']}\n")
                f.write("="*60 + "\n")
            print(f"Snapshot guardado en: snapshots/{nombre_archivo}.txt")

        elif formato == 'json':
            ruta_completa = os.path.join(CARPETA_SNAPSHOTS, f"{nombre_archivo}.json")
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=4, default=str)
            print(f"Snapshot guardado en: snapshots/{nombre_archivo}.json")
    except Exception as e:
        print(f"Error guardando snapshot: {e}")

def mostrar_snapshot_pantalla(snapshot):
    """Muestra el snapshot de forma legible en pantalla"""
    
    print("\n" + "="*70)
    print(f"📸 SNAPSHOT DEL SISTEMA - {snapshot['timestamp']}")
    print("="*70)
    
    print(f"\n🖥️  SISTEMA: {snapshot['sistema'].get('hostname', 'N/A')}")
    print(f"   OS: {snapshot['sistema'].get('os_caption', 'N/A')}")
    
    print(f"\n⚡ RENDIMIENTO:")
    print(f"   CPU: {snapshot['rendimiento']['cpu']['porcentaje_uso']}% | ", end="")
    print(f"RAM: {snapshot['rendimiento']['memoria']['porcentaje_usado']}% | ", end="")
    print(f"Swap: {snapshot['rendimiento']['memoria']['swap_porcentaje']}%")
    
    print(f"\n💾 ALMACENAMIENTO:")
    for part in snapshot['almacenamiento']['particiones'][:3]:  # Mostrar solo 3 particiones
        print(f"   {part['punto_montaje']}: {part['porcentaje_usado']}% usado")
    
    print(f"   Procesos activos: {snapshot['procesos']['total_procesos']}")
    
    print(f"\n👤 USUARIOS: {len(snapshot['usuarios'])} conectados")
    
    print(f"\n🔝 TOP 3 PROCESOS (CPU):")
    for i, proc in enumerate(snapshot['procesos']['top_10_cpu'][:3], 1):
        print(f"   {i}. {proc['name'][:20]:20} - {proc.get('cpu_percent', 0):5.1f}% CPU")
    
    print(f"\n📊 ESTADO DEL SISTEMA:")
    if snapshot['salud_sistema']['recomendaciones']:
        print("   ⚠️  Atención requerida:")
        for rec in snapshot['salud_sistema']['recomendaciones'][:3]:
            print(f"     • {rec}")
    else:
        print("   ✅ Sistema saludable")
    
    print("\n" + "="*70)