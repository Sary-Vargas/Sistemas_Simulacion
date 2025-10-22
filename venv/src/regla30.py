import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime

class Regla30:
    """Clase para implementar el autómata celular Regla 30"""
    
    def __init__(self, c0, num_generaciones):
        """
        Inicializa el autómata celular
        c0: Estado inicial (string de 0s y 1s)
        num_generaciones: Número de generaciones a calcular
        """
        self.c0 = c0
        self.num_generaciones = num_generaciones
        self.generaciones = []
        self.regla = {
            '111': '0',
            '110': '0',
            '101': '0',
            '100': '1',
            '011': '1',
            '010': '1',
            '001': '1',
            '000': '0'
        }
    
    def aplicar_regla(self, izq, centro, der):
        """Aplica la regla 30 a tres células"""
        patron = str(izq) + str(centro) + str(der)
        return self.regla[patron]
    
    def generar(self):
        """Genera todas las generaciones del autómata"""
        # Convertir c0 a lista
        celulas_actuales = list(self.c0)
        self.generaciones = [celulas_actuales.copy()]
        
        for _ in range(self.num_generaciones):
            nuevas_celulas = []
            n = len(celulas_actuales)
            
            for i in range(n):
                # Obtener vecinos (con condiciones de borde: asumir 0 fuera)
                izq = celulas_actuales[i - 1] if i > 0 else '0'
                centro = celulas_actuales[i]
                der = celulas_actuales[i + 1] if i < n - 1 else '0'
                
                # Aplicar regla
                nuevo_estado = self.aplicar_regla(izq, centro, der)
                nuevas_celulas.append(nuevo_estado)
            
            celulas_actuales = nuevas_celulas
            self.generaciones.append(celulas_actuales.copy())
        
        return self.generaciones
    
    def obtener_dataframe(self):
        """Convierte las generaciones a DataFrame"""
        data = {}
        for i, gen in enumerate(self.generaciones):
            data[f'c{i}'] = gen
        
        df = pd.DataFrame(data)
        return df


class InterfazRegla30:
    """Interfaz gráfica para el autómata celular Regla 30"""
    
    def __init__(self, root, main_window=None):
        self.root = root
        self.main_window = main_window
        self.root.title("Autómata Celular - Regla 30")
        self.root.geometry("1000x700")
        
        self.automata = None
        self.df_resultados = None
        
        # Configurar el evento de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.volver_atras)
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="AUTÓMATA CELULAR - REGLA 30", 
                          font=('Arial', 18, 'bold'))
        titulo.pack(pady=15)
        
        # Información sobre la Regla 30
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.pack(fill='x', pady=10)
        
        info_text = """La Regla 30 es un autómata celular elemental descubierto por Stephen Wolfram.
Es conocida por generar patrones caóticos a partir de condiciones iniciales simples.

Regla 30: 111→0  110→0  101→0  100→1  011→1  010→1  001→1  000→0"""
        
        ttk.Label(info_frame, text=info_text, justify='left').pack()
        
        # Frame de entrada
        entrada_frame = ttk.LabelFrame(main_frame, text="Parámetros de Entrada", padding="15")
        entrada_frame.pack(fill='x', pady=10)
        
        # C0 - Estado inicial
        ttk.Label(entrada_frame, text="C0 (Estado inicial - ej: 110110):", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.entry_c0 = ttk.Entry(entrada_frame, width=30, font=('Arial', 10))
        self.entry_c0.grid(row=0, column=1, pady=5, padx=10)
        self.entry_c0.insert(0, "110110")  # Valor por defecto
        
        # C - Cantidad de generaciones
        ttk.Label(entrada_frame, text="C (Cantidad de generaciones):", 
                 font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.entry_c = ttk.Entry(entrada_frame, width=30, font=('Arial', 10))
        self.entry_c.grid(row=1, column=1, pady=5, padx=10)
        self.entry_c.insert(0, "10")  # Valor por defecto
        
        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(pady=15)
        
        ttk.Button(botones_frame, text="Generar Autómata", 
                  command=self.generar_automata).pack(side='left', padx=5)
        
        ttk.Button(botones_frame, text="Limpiar", 
                  command=self.limpiar_campos).pack(side='left', padx=5)
        
        ttk.Button(botones_frame, text="Exportar a Excel", 
                  command=self.exportar_excel).pack(side='left', padx=5)
        
        # Frame para la tabla de resultados
        tabla_frame = ttk.LabelFrame(main_frame, text="Generaciones del Autómata", padding="10")
        tabla_frame.pack(fill='both', expand=True, pady=10)
        
        # Canvas con scrollbar para la tabla
        canvas = tk.Canvas(tabla_frame, bg='white')
        scrollbar_y = ttk.Scrollbar(tabla_frame, orient='vertical', command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(tabla_frame, orient='horizontal', command=canvas.xview)
        
        self.frame_tabla = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        canvas.pack(side='left', fill='both', expand=True)
        
        canvas.create_window((0, 0), window=self.frame_tabla, anchor='nw')
        
        self.canvas = canvas
        
        # Botón volver
        btn_volver_frame = ttk.Frame(main_frame)
        btn_volver_frame.pack(pady=10)
        
        ttk.Button(btn_volver_frame, text="⬅ Volver Atrás", 
                  command=self.volver_atras).pack()
    
    def validar_entrada(self, c0, c):
        """Valida los datos de entrada"""
        # Validar C0
        if not c0:
            messagebox.showerror("Error", "Debe ingresar un estado inicial C0")
            return False
        
        if not all(bit in '01' for bit in c0):
            messagebox.showerror("Error", "C0 debe contener solo 0s y 1s")
            return False
        
        # Validar C
        try:
            num_gen = int(c)
            if num_gen <= 0:
                messagebox.showerror("Error", "La cantidad de generaciones debe ser mayor a 0")
                return False
            if num_gen > 50:
                messagebox.showwarning("Advertencia", "Se recomienda un máximo de 50 generaciones para mejor visualización")
        except ValueError:
            messagebox.showerror("Error", "La cantidad de generaciones debe ser un número entero")
            return False
        
        return True
    
    def generar_automata(self):
        """Genera y muestra el autómata celular"""
        c0 = self.entry_c0.get().strip()
        c = self.entry_c.get().strip()
        
        if not self.validar_entrada(c0, c):
            return
        
        try:
            num_generaciones = int(c)
            
            # Crear y generar el autómata
            self.automata = Regla30(c0, num_generaciones)
            generaciones = self.automata.generar()
            self.df_resultados = self.automata.obtener_dataframe()
            
            # Mostrar resultados
            self.mostrar_tabla(generaciones)
            
            messagebox.showinfo("Éxito", f"Autómata generado con {num_generaciones} generaciones")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar autómata: {str(e)}")
    
    def mostrar_tabla(self, generaciones):
        """Muestra las generaciones en formato de tabla visual"""
        # Limpiar tabla anterior
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()
        
        # Colores
        color_0 = '#87CEEB'  # Celeste (0)
        color_1 = '#FFA07A'  # Naranja (1)
        
        # Crear encabezado
        ttk.Label(self.frame_tabla, text="", width=5, 
                 font=('Arial', 9, 'bold')).grid(row=0, column=0, padx=1, pady=1)
        
        for i in range(len(generaciones[0])):
            ttk.Label(self.frame_tabla, text=str(i), width=5, 
                     font=('Arial', 9, 'bold'), 
                     relief='raised').grid(row=0, column=i+1, padx=1, pady=1)
        
        # Crear filas
        for gen_num, generacion in enumerate(generaciones):
            # Etiqueta de generación
            ttk.Label(self.frame_tabla, text=str(gen_num), 
                     font=('Arial', 9, 'bold'),
                     relief='raised').grid(row=gen_num+1, column=0, padx=1, pady=1)
            
            # Células
            for i, celula in enumerate(generacion):
                color = color_1 if celula == '1' else color_0
                tk.Label(self.frame_tabla, text=celula, width=5, height=2,
                        bg=color, fg='black', font=('Arial', 9, 'bold'),
                        relief='solid', borderwidth=1).grid(row=gen_num+1, column=i+1, 
                                                            padx=1, pady=1)
        
        # Actualizar scroll region
        self.frame_tabla.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
    
    def exportar_excel(self):
        """Exporta los resultados a Excel"""
        if self.df_resultados is None:
            messagebox.showwarning("Advertencia", "No hay datos para exportar. Genere primero el autómata.")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"regla30_automata_{timestamp}.xlsx"
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Exportar datos
                self.df_resultados.to_excel(writer, sheet_name='Regla 30', index=False)
                
                # Obtener worksheet para formato
                workbook = writer.book
                worksheet = writer.sheets['Regla 30']
                
                # Aplicar formato condicional
                from openpyxl.styles import PatternFill
                
                fill_0 = PatternFill(start_color="87CEEB", end_color="87CEEB", fill_type="solid")
                fill_1 = PatternFill(start_color="FFA07A", end_color="FFA07A", fill_type="solid")
                
                for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row,
                                              min_col=1, max_col=worksheet.max_column):
                    for cell in row:
                        if cell.value == '0':
                            cell.fill = fill_0
                        elif cell.value == '1':
                            cell.fill = fill_1
                
                # Ajustar ancho de columnas
                for col in worksheet.columns:
                    worksheet.column_dimensions[col[0].column_letter].width = 5
            
            messagebox.showinfo("Éxito", f"Archivo exportado exitosamente:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def limpiar_campos(self):
        """Limpia los campos de entrada y la tabla"""
        self.entry_c0.delete(0, tk.END)
        self.entry_c0.insert(0, "110110")
        self.entry_c.delete(0, tk.END)
        self.entry_c.insert(0, "10")
        
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()
        
        self.automata = None
        self.df_resultados = None
    
    def volver_atras(self):
        """Vuelve a la ventana principal"""
        if self.main_window:
            self.main_window.deiconify()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = InterfazRegla30(root)
    root.mainloop()


if __name__ == "__main__":
    main()