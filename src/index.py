import os
import sys
import time
from reportes import GeneradorReporte 

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_pantalla()
    print("==========================================")
    print("   SISTEMA DE MONITOREO PROFESIONAL V1.0")
    print("==========================================")
    print("1. [CORE] Monitoreo en Tiempo Real (CPU/RAM/Disco)")
    print("2. [CORE] Ver Top 5 Procesos (Consumo Crítico)")
    print("3. [ANALISIS] Snapshot del Sistema (Uptime/Hilos)")
    print("4. [DATOS] Configurar Guardado Automático (CSV)")
    print("5. [REPORTE] Generar Informe PDF de Anomalías")
    print("6. Salir")
    print("==========================================")
        
def menu_principal():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ")

        if opcion == "1":
            print("\nIniciando monitoreo... (Ctrl+C para volver)")
            # llamar_a: nucleo.recolector.monitoreo_vivo()
            input("\nPresiona Enter para volver...")
        
        elif opcion == "2":
            print("\nBuscando procesos pesados...")
            # llamar_a: nucleo.recolector.obtener_top_procesos()
            input("\nPresiona Enter para volver...")

        elif opcion == "3":
            print("\nCapturando estado del sistema...")
            # llamar_a: nucleo.analizador.obtener_instantanea()
            input("\nPresiona Enter para volver...")

        elif opcion == "4":
            print("\nConfigurando registro en segundo plano...")
            # llamar_a: datos.almacenamiento.configurar_logging()
            input("\nConfiguración guardada. Presiona Enter...")

        elif opcion == "5":
            print("\nGenerando reporte PDF con gráficas...")
            reporte = GeneradorReporte() 
            reporte.crear_reporte()
            input("\nReporte listo en la carpeta /reportes. Presiona Enter...")

        elif opcion == "6":
            print("\nCerrando el sistema. ¡Hasta luego!")
            sys.exit()
            
        else:
            print("\nOpción no válida. Intenta de nuevo.")
            time.sleep(1.5)

if __name__ == "__main__":
    menu_principal()