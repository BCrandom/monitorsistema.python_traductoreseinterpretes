import psutil

def monitoreo_vivo():
    print("\n--- ESTADO DEL SISTEMA ---")
    cpu_uso = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    print(f"CPU: {cpu_uso}% | RAM: {memoria.percent}%")

def obtener_top_procesos():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            p_info = proc.as_dict(['pid', 'name', 'memory_percent'])
            # Inicializar el contador de CPU
            proc.cpu_percent(interval=None) # He visto que sin evaluar el cpu dos veces, siempre devuelve que el porcentaje usado es 0, por éso dejo ésta línea
            processes.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    # Ordenar por uso de CPU y memoria
    mem_sorted = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
    
    print("\nTop procesos por Memoria:")
    for p in mem_sorted:
        print(f"PID: {p['pid']:>6}, Nombre: {p['name']:25}, Memoria: {p['memory_percent']:6.2f}%")

    print("\nTop procesos por CPU:")
    print(f"{'PID':<10} {'NOMBRE':<25} {'CPU %':<10}")
    procesos = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            procesos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    top_5 = sorted(procesos, key=lambda x: x['cpu_percent'], reverse=True)[:5]
    for p in top_5:
        print(f"{p['pid']:<10} {p['name'][:25]:<25} {p['cpu_percent']:<10}")



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