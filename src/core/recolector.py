import psutil

def monitoreo_vivo():
    print("\n--- ESTADO DEL SISTEMA ---")
    cpu_uso = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    print(f"CPU: {cpu_uso}% | RAM: {memoria.percent}%")

def obtener_top_procesos():
    print(f"\n{'PID':<10} {'NOMBRE':<25} {'CPU %':<10}")
    procesos = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            procesos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    top_5 = sorted(procesos, key=lambda x: x['cpu_percent'], reverse=True)[:5]
    for p in top_5:
        print(f"{p['pid']:<10} {p['name'][:25]:<25} {p['cpu_percent']:<10}")