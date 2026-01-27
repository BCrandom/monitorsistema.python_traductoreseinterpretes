# reportes/generador.py
import os
import datetime
from fpdf import FPDF

class GeneradorReporte:
    def __init__(self, datos=None):
        self.datos = datos
        self.pdf = FPDF()

    def crear_reporte(self):
        # --- Configuración del PDF (Igual que antes) ---
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "REPORTE DE ACTIVIDAD DEL SISTEMA", ln=True, align='C')
        self.pdf.ln(10)

        if not self.datos:
            self.pdf.set_text_color(200, 0, 0)
            self.pdf.set_font("Arial", "B", 12)
            self.pdf.multi_cell(0, 10, "ADVERTENCIA: No se han recolectado datos del sistema todavía.", border=1, align='C')
        
        # --- LÓGICA DE ALMACENAMIENTO ---
        
        # 1. Definir el nombre de la carpeta (dentro del proyecto)
        nombre_carpeta = "reportes_generados"
        
        # 2. Crear la carpeta si no existe
        if not os.path.exists(nombre_carpeta):
            os.makedirs(nombre_carpeta)
            print(f"[SISTEMA] Carpeta '{nombre_carpeta}' creada con éxito.")

        # 3. Crear un nombre de archivo único con fecha y hora
        # Ejemplo: reporte_20240520_153022.pdf
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_{timestamp}.pdf"
        
        # 4. Unir la carpeta con el nombre del archivo
        ruta_final = os.path.join(nombre_carpeta, nombre_archivo)

        # 5. Guardar el PDF en esa ruta
        self.pdf.output(ruta_final)
        
        print(f"\n[ÉXITO] Reporte guardado en: {ruta_final}")