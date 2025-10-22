import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime

class GeneradorAleatorio:
    """Clase para generar números pseudoaleatorios"""
    
    @staticmethod
    def generar_uniformes(n, semilla=None):
        if semilla is not None:
            np.random.seed(semilla)
        numeros = np.random.uniform(0, 1, n)
        # Redondear a 4 decimales
        return np.round(numeros, 4)
    
    @staticmethod
    def generar_rango(n, minimo, maximo, semilla=None):
        if semilla is not None:
            np.random.seed(semilla)
        return np.random.randint(minimo, maximo + 1, n)

class SimuladorClientes:
    """Clase para simular la llegada de clientes"""
    
    def __init__(self, n_simulaciones, min_clientes, max_clientes):
        self.n_simulaciones = n_simulaciones
        self.min_clientes = min_clientes
        self.max_clientes = max_clientes
        self.numeros_aleatorios = []
        self.clientes_por_periodo = []
        
    def simular(self, semilla=None):
        """Ejecuta la simulación"""
        generador = GeneradorAleatorio()
        self.numeros_aleatorios = generador.generar_uniformes(self.n_simulaciones, semilla)
        self.clientes_por_periodo = generador.generar_rango(
            self.n_simulaciones, 
            self.min_clientes, 
            self.max_clientes,
            semilla
        )
        return self.obtener_resultados()
    
    def obtener_resultados(self):
        """Retorna los resultados en formato DataFrame"""
        df = pd.DataFrame({
            'Nro': range(1, self.n_simulaciones + 1),
            'aleatorio': self.numeros_aleatorios,
            'Cliente / 10 min': self.clientes_por_periodo
        })
        return df

class InterfazSimulador:
    """Interfaz gráfica principal"""
    
    def __init__(self, root, main_window=None):
        self.root = root
        self.main_window = main_window  # Referencia a la ventana principal
        self.root.title("Simulador de Llegada de Clientes")
        self.root.geometry("1200x800")
        
        self.df_resultados = None
        self.canvas_grafico = None
        
        # Configurar el evento de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.volver_atras)
        
        self.crear_menu()
        self.crear_notebook()
        
    def crear_menu(self):
        """Crea el menú principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nueva Simulación", command=self.limpiar_simulacion)
        menu_archivo.add_command(label="Exportar a Excel", command=self.exportar_excel)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Volver al Menú Principal", command=self.volver_atras)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
    
    def crear_notebook(self):
        """Crea las pestañas principales"""
        # Frame contenedor principal
        container = ttk.Frame(self.root)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Notebook
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestaña 1: Generador
        self.frame_generador = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_generador, text="Generador de Números")
        self.crear_pestaña_generador()
        
        # Pestaña 2: Resultados
        self.frame_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_resultados, text="Resultados y Gráficos")
        self.crear_pestaña_resultados()
        
        # Botón Volver Atrás en la parte inferior
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(btn_frame, text="⬅ Volver Atrás", 
                  command=self.volver_atras,
                  style='Accent.TButton').pack(side='left', padx=5)
    
    def crear_pestaña_generador(self):
        """Crea la pestaña de configuración y generación"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.frame_generador, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Configuración de Simulación", 
                          font=('Arial', 16, 'bold'))
        titulo.pack(pady=10)
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Parámetros", padding="15")
        config_frame.pack(fill='x', pady=10)
        
        # N (cantidad de simulaciones)
        ttk.Label(config_frame, text="N (Cantidad de simulaciones):", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.entry_n = ttk.Entry(config_frame, width=20, font=('Arial', 10))
        self.entry_n.grid(row=0, column=1, pady=5, padx=10)
        
        # Mínimo de clientes
        ttk.Label(config_frame, text="Mínimo de clientes por periodo:", 
                 font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.entry_min = ttk.Entry(config_frame, width=20, font=('Arial', 10))
        self.entry_min.grid(row=1, column=1, pady=5, padx=10)
        
        # Máximo de clientes
        ttk.Label(config_frame, text="Máximo de clientes por periodo:", 
                 font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.entry_max = ttk.Entry(config_frame, width=20, font=('Arial', 10))
        self.entry_max.grid(row=2, column=1, pady=5, padx=10)
        
        # Semilla 
        ttk.Label(config_frame, text="Semilla :", 
                 font=('Arial', 10)).grid(row=3, column=0, sticky='w', pady=5)
        self.entry_semilla = ttk.Entry(config_frame, width=20, font=('Arial', 10))
        self.entry_semilla.grid(row=3, column=1, pady=5, padx=10)
        
        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(pady=20)
        
        self.btn_generar = ttk.Button(botones_frame, text="Generar Simulación", 
                                      command=self.ejecutar_simulacion)
        self.btn_generar.pack(side='left', padx=5)
        
        ttk.Button(botones_frame, text="Limpiar", 
                  command=self.limpiar_campos).pack(side='left', padx=5)
        
        # Área de información
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.pack(fill='both', expand=True, pady=10)
        
        info_text = """
        Instrucciones:
        
        1. Ingrese N: cantidad de periodos de 10 minutos a simular
        2. Ingrese el mínimo
        3. Ingrese el máximo 
        4. Ingrese una semilla para generar los pseualeatorios
        5. Presione "Generar Simulación" para ejecutar
        
        Los resultados se mostrarán en la pestaña "Resultados y Gráficos"
        
        by: Sary Vargas
        """
        
        ttk.Label(info_frame, text=info_text, justify='left', font=('Arial', 9)).pack()
    
    def crear_pestaña_resultados(self):
        """Crea la pestaña de resultados"""
        # Frame principal
        main_frame = ttk.Frame(self.frame_resultados)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame superior para la tabla
        tabla_frame = ttk.LabelFrame(main_frame, text="Tabla de Resultados", padding="10")
        tabla_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Crear Treeview para la tabla
        columns = ('Nro', 'aleatorio', 'Cliente / 10 min')
        self.tree = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.tree.heading('Nro', text='Nro')
        self.tree.heading('aleatorio', text='Aleatorio')
        self.tree.heading('Cliente / 10 min', text='Cliente / 10 min')
        
        self.tree.column('Nro', width=100, anchor='center')
        self.tree.column('aleatorio', width=150, anchor='center')
        self.tree.column('Cliente / 10 min', width=150, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame inferior para el gráfico
        grafico_frame = ttk.LabelFrame(main_frame, text="Gráfico de Distribución", padding="10")
        grafico_frame.pack(fill='both', expand=True)
        
        self.frame_grafico = grafico_frame
        
        # Botón de exportar
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        self.btn_exportar = ttk.Button(btn_frame, text="📊 Exportar a Excel", 
                                       command=self.exportar_excel)
        self.btn_exportar.pack()
    
    def ejecutar_simulacion(self):
        """Ejecuta la simulación con los parámetros ingresados"""
        try:
            # Obtener valores
            n = int(self.entry_n.get())
            minimo = int(self.entry_min.get())
            maximo = int(self.entry_max.get())
            
            semilla_text = self.entry_semilla.get()
            semilla = int(semilla_text) if semilla_text else None
            
            # Validaciones
            if n <= 0:
                messagebox.showerror("Error", "N debe ser mayor a 0")
                return
            if minimo < 0 or maximo < 0:
                messagebox.showerror("Error", "Los valores mínimo y máximo deben ser positivos")
                return
            if minimo > maximo:
                messagebox.showerror("Error", "El mínimo no puede ser mayor al máximo")
                return
            
            # Crear simulador y ejecutar
            simulador = SimuladorClientes(n, minimo, maximo)
            self.df_resultados = simulador.simular(semilla)
            
            # Mostrar resultados
            self.mostrar_tabla()
            self.mostrar_estadisticas_basicas()
            self.mostrar_grafico()
            
            # Cambiar a pestaña de resultados
            self.notebook.select(1)
            
            messagebox.showinfo("Éxito", f"Simulación completada con {n} periodos")
            
        except ValueError as e:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar simulación: {str(e)}")
    
    def mostrar_tabla(self):
        """Muestra los resultados en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar datos (los números ya vienen con 4 decimales)
        for _, row in self.df_resultados.iterrows():
            self.tree.insert('', 'end', values=(
                int(row['Nro']),
                f"{row['aleatorio']:.4f}",
                int(row['Cliente / 10 min'])
            ))
    
    def mostrar_grafico(self):
        """Muestra el gráfico de distribución"""
        # Limpiar gráfico anterior
        for widget in self.frame_grafico.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 5))
        
        clientes = self.df_resultados['Cliente / 10 min']
        periodos = self.df_resultados['Nro']
        
        # Crear gráfico de barras
        bars = ax.bar(periodos, clientes, color='skyblue', edgecolor='navy', alpha=0.7)
        
        # Añadir etiquetas en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=8)
        
        ax.set_xlabel('Periodo (Nro)', fontsize=10)
        ax.set_ylabel('Clientes por 10 min', fontsize=10)
        ax.set_title('Distribución de Clientes por Periodo', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.canvas_grafico = canvas
    
    def exportar_excel(self):
        """Exporta los resultados a Excel con datos y gráfico"""
        if self.df_resultados is None:
            messagebox.showwarning("Advertencia", "No hay datos para exportar. Ejecute primero una simulación.")
            return
        
        try:
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simulacion_clientes_{timestamp}.xlsx"
            
            # Crear writer de Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Exportar datos principales
                self.df_resultados.to_excel(writer, sheet_name='Datos', index=False, startrow=0)
                
                # Obtener el workbook y worksheet
                workbook = writer.book
                worksheet = writer.sheets['Datos']
                
                # Crear el gráfico
                from openpyxl.chart import BarChart, Reference
                
                chart = BarChart()
                chart.type = "col"
                chart.style = 10
                chart.title = "Distribución de Clientes "
                chart.y_axis.title = 'Clientes por 10 min'
                chart.x_axis.title = 'Periodo (Nro)'
                
                # Datos para el gráfico
                data = Reference(worksheet, min_col=3, min_row=1, 
                               max_row=len(self.df_resultados) + 1)
                cats = Reference(worksheet, min_col=1, min_row=2, 
                               max_row=len(self.df_resultados) + 1)
                
                chart.add_data(data, titles_from_data=True)
                chart.set_categories(cats)
                chart.height = 10
                chart.width = 20
                
                # Posicionar el gráfico
                worksheet.add_chart(chart, "E2")
            
            messagebox.showinfo("Éxito", f"Archivo exportado exitosamente:\n{filename}\n\nContiene:\n- Tabla de datos\n- Gráfico de barras")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def limpiar_campos(self):
        """Limpia los campos de entrada"""
        self.entry_n.delete(0, tk.END)
        self.entry_min.delete(0, tk.END)
        self.entry_max.delete(0, tk.END)
        self.entry_semilla.delete(0, tk.END)
    
    def limpiar_simulacion(self):
        """Reinicia la simulación"""
        self.limpiar_campos()
        self.df_resultados = None
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.label_stats.config(text="")
        
        if self.canvas_grafico:
            self.canvas_grafico.get_tk_widget().destroy()
        
        self.notebook.select(0)
    
    def volver_atras(self):
        """Vuelve a la ventana principal"""
        if self.main_window:
            self.main_window.deiconify()  # Mostrar ventana principal
        self.root.destroy()  # Cerrar ventana del simulador
    
    def mostrar_acerca_de(self):
        """Muestra información sobre el programa"""
        mensaje = """
Simulador de Llegada de Clientes
Versión 1.0

Desarrollado en Python 3.10+
Librerías: tkinter, numpy, matplotlib, pandas

Sistema de simulación de llegada de clientes
a una tienda basado en números pseudoaleatorios.

Características:
- Generación de números aleatorios (4 decimales)
- Simulación configurable
- Visualización gráfica
- Exportación a Excel

By: Sary Vargas
        """
        messagebox.showinfo("Acerca de", mensaje)

def main():
    root = tk.Tk()
    app = InterfazSimulador(root)
    root.mainloop()

if __name__ == "__main__":
    main()