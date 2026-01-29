import os
import datetime
from fpdf import FPDF

class GeneradorReporte:
    def __init__(self, datos=None):
        self.datos = datos if datos else {}
        self.pdf = FPDF()

    def crear_reporte(self):
        d = self.datos
        self.pdf.add_page()
        
        # --- ENCABEZADO ---
        self.pdf.set_fill_color(30, 50, 100)
        self.pdf.rect(0, 0, 210, 35, 'F')
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("Arial", "B", 18)
        self.pdf.cell(0, 12, "AUDITORIA TECNICA DETALLADA", ln=True, align='C')
        self.pdf.set_font("Arial", "I", 10)
        self.pdf.cell(0, 8, f"Captura: {d.get('timestamp', datetime.datetime.now().strftime('%H:%M:%S'))}", ln=True, align='C')
        self.pdf.ln(12)
        self.pdf.set_text_color(0, 0, 0)
        
        def fila_dato(label, valor):
            self.pdf.set_font("Arial", "B", 10)
            self.pdf.set_fill_color(245, 245, 245)
            self.pdf.cell(65, 8, f" {label}:", border=1, fill=True)
            self.pdf.set_font("Arial", "", 10)
            self.pdf.cell(125, 8, f" {str(valor)}", border=1, ln=True)

        # --- SECCION I: HARDWARE Y GRAFICOS ---
        self.pdf.set_font("Arial", "B", 11)
        self.pdf.cell(0, 8, "I. COMPONENTES DE HARDWARE", ln=True)
        fila_dato("Sistema Operativo", f"{d.get('os_caption')} (v.{d.get('os_version')})")
        fila_dato("Procesador", d.get('cpu_name'))
        fila_dato("GPU", d.get('gpu_name'))
        fila_dato("VRAM (Memoria Video)", d.get('vram')) # Verifica que en Alpha_0_1 se llame 'vram'
        self.pdf.ln(4)

        # --- SECCION II: ESTADO DE MEMORIA (AQUI ESTA EL SWAP) ---
        self.pdf.set_font("Arial", "B", 11)
        self.pdf.cell(0, 8, "II. MEMORIA Y RENDIMIENTO", ln=True)
        fila_dato("CPU en Uso Real", f"{d.get('cpu_final')}%")
        fila_dato("RAM Total", f"{d.get('ram_total')} GB")
        fila_dato("RAM Disponible", f"{d.get('ram_disp')} GB")
        fila_dato("RAM Usada (%)", f"{d.get('ram_uso_p')}%")
        # LLAVE CRITICA: Asegúrate que en Alpha_0_1 sea 'swap_info'
        fila_dato("MEMORIA SWAP", d.get('swap_info', 'Error: Dato SWAP no recibido')) 
        self.pdf.ln(4)

        # --- SECCION III: ALMACENAMIENTO ---
        self.pdf.set_font("Arial", "B", 11)
        self.pdf.cell(0, 8, "III. ALMACENAMIENTO (DISCO C:)", ln=True)
        # Mostramos capacidad total y libre
        total_d = d.get('disco_total', '103.00')
        libre_d = d.get('disco_c_libre', 0)
        fila_dato("Capacidad Total", f"{total_d} GB")
        fila_dato("Espacio Libre", f"{libre_d:.2f} GB")
        fila_dato("Actividad I/O", f"Lectura: {d.get('disco_io_r')} | Escritura: {d.get('disco_io_w')}")
        self.pdf.ln(4)

        # --- SECCION IV: SISTEMA Y SESION ---
        self.pdf.set_font("Arial", "B", 11)
        self.pdf.cell(0, 8, "IV. ESTADO DEL SISTEMA", ln=True)
        fila_dato("Procesos Activos", d.get('pids'))
        fila_dato("Tiempo Activo", d.get('uptime'))
        fila_dato("Usuarios Activos", d.get('user'))
        fila_dato("Bateria", f"{d.get('bat_p')}%")
        fila_dato("Cargando", "SI" if d.get('bat_c') else "NO")
        self.pdf.ln(10)

        # --- DIAGNOSTICO SEMANTICO ---
        if float(d.get('ram_uso_p', 0)) > 85 or float(d.get('disco_c_libre', 10)) < 5:
            self.pdf.set_fill_color(255, 230, 230); self.pdf.set_text_color(150, 0, 0)
            msg = "DIAGNOSTICO: ESTADO CRITICO - RECURSOS LIMITADOS"
        else:
            self.pdf.set_fill_color(230, 255, 230); self.pdf.set_text_color(0, 100, 0)
            msg = "DIAGNOSTICO: SISTEMA SALUDABLE"
        
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 12, f"  {msg}", border=1, ln=True, fill=True)

        # Guardar y abrir
        if not os.path.exists("reportes_generados"): os.makedirs("reportes_generados")
        ruta = os.path.join("reportes_generados", f"Reporte_{datetime.datetime.now().strftime('%H%M%S')}.pdf")
        self.pdf.output(ruta)
        os.startfile(os.path.abspath(ruta))