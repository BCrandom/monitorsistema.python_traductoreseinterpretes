import psutil
import time

def monitoreo_vivo():
    print("\n--- ESTADO DEL SISTEMA ---")
    cpu_uso = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    print(f"CPU: {cpu_uso}% | RAM: {memoria.percent}%")

def obtener_top_procesos(imprimir=True): # Añadimos el interruptor
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
    
    # Solo imprimimos si imprimir es True
    if imprimir:
        print("\nTop procesos por Memoria:")
        for p in mem_sorted:
            print(f"PID: {p['pid']:>6}, Nombre: {p['name']:25}, Memoria: {p['memory_percent']:6.2f}%")

    # --- Bloque CPU ---
    if imprimir:
        print("\nTop procesos por CPU:")
        print(f"{'PID':<10} {'NOMBRE':<25} {'CPU %':<10}")
        
    procesos_cpu = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            procesos_cpu.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_5 = sorted(procesos_cpu, key=lambda x: x['cpu_percent'], reverse=True)[:5]
    
    if imprimir:
        for p in top_5:
            print(f"{p['pid']:<10} {p['name'][:25]:<25} {p['cpu_percent']:<10}")

    # Retornamos los datos pasando por la función puente
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