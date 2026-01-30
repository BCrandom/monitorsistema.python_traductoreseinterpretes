import os
import sys
import time
from reportes import GeneradorReporte 
import Alpha_0_1

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
    print("4. [REPORTE] Generar Informe PDF de Anomalías")
    print("5. Salir")
    print("==========================================")
        
def menu_principal():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ")

        if opcion == "1":
            print("\nIniciando monitoreo... (Ctrl+C para volver)")
            Alpha_0_1.monitoreo_envivo()
            input("\nPresiona Enter para volver...")
        
        elif opcion == "2":
            print("\nBuscando procesos pesados...")
            # recolector.obtener_top_procesos() # Asegúrate de que recolector esté importado
            input("\nPresiona Enter para volver...")

        elif opcion == "3":
            print("\nCapturando estado del sistema...")
            input("\nPresiona Enter para volver...")

        elif opcion == "4":
            print("\nConfigurando registro en segundo plano...")
            input("\nConfiguración guardada. Presiona Enter...")

        elif opcion == "4":
            print("\n[+] Iniciando recolección de datos...")
            # TODO ESTE BLOQUE DEBE ESTAR INDENTADO DENTRO DE LA OPCION 5
            try:
                datos = Alpha_0_1.obtener_datos_reporte() 
                
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