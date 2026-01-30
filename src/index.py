import os
import sys
import time
from reportes import GeneradorReporte 
from core import recolector
import Alpha_0_1

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

banner = """
┌─── [ GROUP_#01 ] ────────────────────────────────────────┐
│                                                          │
│   ﹃                                                 ﹄  │
│      _____                      _____                    │
│     / ___/____  ____ _____     / ___/__  _______         │
│     \__ \/ __ \/ __ `/ __ \    \__ \/ / / / ___/         │
│    ___/ / / / / /_/ / /_/ /   ___/ / /_/ (__  )          │
│   /____/_/ /_/\__,_/ .___/   /____/\__, /____/           │
│                   /_/             /____/                 │
│                                                          │
│   ﹄                                                 ﹃  │
│             Te-I  [•]  S01  L  3:2  100% [===]           │
└──────────────────────────────────────────────────────────┘
"""

def mostrar_menu():
    limpiar_pantalla()
    print(" ▥  " + "|  |  " * 10)
    #print("==========================================")
    print(banner)
    print("   SISTEMA DE MONITOREO PROFESIONAL V1.0\n")
    print(" ▥  " + "|  |  " * 10 + "\n")
    #print("==========================================")
    print("1. [CORE] Monitoreo en Tiempo Real (CPU/RAM/Disco)")
    print("2. [CORE] Ver Top 5 Procesos (Consumo Crítico)")
    print("3. [ANALISIS] Snapshot del Sistema (Uptime/Hilos)")
    print("4. [REPORTE] Generar Informe PDF de Anomalías")
    print("5. Salir")
    print(" ₊˚.༄  " + "˚‧⁺  ･ ˖ ·" * 5)
    #print("==========================================")
        
def menu_principal():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ")

        if opcion == "1":
            print("\nIniciando monitoreo... (Ctrl+C para volver)")
            Alpha_0_1.monitoreo_envivo()
            input("\nPresiona Enter para volver...")
        
        elif opcion == "2":
            print("\nBuscando procesos pesados...")
            recolector.obtener_top_procesos() 
            input("\nPresiona Enter para volver...")

        elif opcion == "3":
            print("\nCapturando estado del sistema...")
            input("\nPresiona Enter para volver...")

        elif opcion == "4":
            print("\n[+] Iniciando recolección de datos...")
            # TODO ESTE BLOQUE DEBE ESTAR INDENTADO DENTRO DE LA OPCION 4
            try:
                datos = Alpha_0_1.obtener_datos_reporte() 
                mem_sorted, top_5= recolector.obtener_top_procesos(imprimir=False)
                
                # 3. Juntamos TODO en el mismo diccionario
                datos["mem_sorted"] = mem_sorted
                datos["top_5"] = top_5
                
                print("[+] Generando archivo PDF...")
                reporte = GeneradorReporte(datos)
                reporte.crear_reporte()
                
                print("\n[ÉXITO] El reporte se ha generado correctamente.")
                input("\nPresiona Enter para volver...")
                
            except Exception as e:
                print(f"\n[ERROR] No se pudo generar el reporte: {e}")
                input("\nPresiona Enter para volver...")

        elif opcion == "5":
            print("\nCerrando el sistema. ¡Hasta luego!")
            sys.exit()
            
        else:
            print("\nOpción no válida. Intenta de nuevo.")
            time.sleep(1.5)

if __name__ == "__main__":
    menu_principal()