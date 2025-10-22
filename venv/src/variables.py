import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from scipy import stats

class GeneradorVariables:
    """Clase para generar variables aleatorias con diferentes distribuciones"""
    
    def __init__(self, semilla=None):
        if semilla is not None:
            np.random.seed(semilla)
    
    def uniforme(self, n, minimo, maximo):
        """Genera n variables aleatorias con distribución Uniforme(min, max)"""
        return np.random.uniform(minimo, maximo, n)
    
    def exponencial(self, n, media):
        """Genera n variables aleatorias con distribución Exponencial(media)"""
        return np.random.exponential(media, n)
    
    def k_erlang(self, n, k, media):
        """Genera n variables aleatorias con distribución k-Erlang(k, media)"""
        beta = media / k
        return np.random.gamma(k, beta, n)
    
    def gamma_dist(self, n, media, varianza):
        """Genera n variables aleatorias con distribución Gamma(media, varianza)"""
        shape = (media ** 2) / varianza
        scale = varianza / media
        return np.random.gamma(shape, scale, n)
    
    def normal(self, n, media, varianza):
        """Genera n variables aleatorias con distribución Normal(media, varianza)"""
        desviacion = np.sqrt(varianza)
        return np.random.normal(media, desviacion, n)
    
    def weibull(self, n, alpha, beta, gamma_param):
        """Genera n variables aleatorias con distribución Weibull(alpha, beta, gamma)"""
        return gamma_param + beta * np.random.weibull(alpha, n)
    
    # ============= DISTRIBUCIONES DISCRETAS =============
    
    def bernoulli(self, n, p):
        """Genera n variables aleatorias con distribución Bernoulli(p)"""
        return np.random.binomial(1, p, n)
    
    def binomial(self, n_vars, n_trials, p):
        """Genera n_vars variables aleatorias con distribución Binomial(n_trials, p)"""
        return np.random.binomial(n_trials, p, n_vars)
    
    def poisson(self, n, lambda_param):
        """Genera n variables aleatorias con distribución Poisson(lambda)"""
        return np.random.poisson(lambda_param, n)


class InterfazVariables:
    """Interfaz gráfica para generación de variables aleatorias"""
    
    def __init__(self, root, main_window=None):
        self.root = root
        self.main_window = main_window
        self.root.title("Generador de Variables Aleatorias")
        
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Configurar ventana para ocupar la mitad izquierda de la pantalla
        window_width = screen_width // 2
        window_height = screen_height
        x_position = 0
        y_position = 0
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        self.variables_generadas = None
        self.df_resultados = None
        self.distribucion_actual = None
        self.es_discreta = False
        
        # Configurar el evento de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.volver_atras)
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Botón volver en la parte superior
        btn_volver = ttk.Button(main_frame, text="⬅ Volver Atrás", command=self.volver_atras)
        btn_volver.pack(anchor='w', pady=(0, 10))
        
        # Título
        titulo = ttk.Label(main_frame, text="GENERADOR DE VARIABLES ALEATORIAS", 
                          font=('Arial', 18, 'bold'))
        titulo.pack(pady=10)
        
        # Frame de configuración general
        config_frame = ttk.LabelFrame(main_frame, text="Configuración General", padding="10")
        config_frame.pack(fill='x', pady=5)
        
        # Semilla
        ttk.Label(config_frame, text="Semilla:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.entry_semilla = ttk.Entry(config_frame, width=20, font=('Arial', 10))
        self.entry_semilla.grid(row=0, column=1, pady=5, padx=5)
        
        # Cantidad
        ttk.Label(config_frame, text="Cantidad a generar (n):", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.entry_cantidad = ttk.Entry(config_frame, width=20, font=('Arial', 10))
        self.entry_cantidad.grid(row=0, column=3, pady=5, padx=5)
        self.entry_cantidad.insert(0, "100")
        
        # Frame de selección de distribución
        distrib_frame = ttk.LabelFrame(main_frame, text="Tipo de Distribución", padding="10")
        distrib_frame.pack(fill='x', pady=5)
        
        self.distribucion_var = tk.StringVar(value="uniforme")
        
        # Distribuciones Continuas
        ttk.Label(distrib_frame, text="Variables :", 
                 font=('Arial', 10, 'bold', 'underline')).grid(row=0, column=0, columnspan=3, sticky='w', pady=5)
        
        distribuciones_continuas = [
            ("Uniforme", "uniforme"),
            ("Exponencial", "exponencial"),
            ("k-Erlang", "k_erlang"),
            ("Gamma", "gamma"),
            ("Normal", "normal"),
            ("Weibull", "weibull")
        ]
        
        for i, (texto, valor) in enumerate(distribuciones_continuas):
            ttk.Radiobutton(distrib_frame, text=texto, variable=self.distribucion_var,
                           value=valor, command=self.cambiar_distribucion).grid(
                               row=1, column=i, padx=10, pady=5)
        
        # Distribuciones Discretas
        ttk.Label(distrib_frame, text="variables:", 
                 font=('Arial', 10, 'bold', 'underline')).grid(row=2, column=0, columnspan=3, sticky='w', pady=(15,5))
        
        distribuciones_discretas = [
            ("Bernoulli", "bernoulli"),
            ("Binomial", "binomial"),
            ("Poisson", "poisson")
        ]
        
        for i, (texto, valor) in enumerate(distribuciones_discretas):
            ttk.Radiobutton(distrib_frame, text=texto, variable=self.distribucion_var,
                           value=valor, command=self.cambiar_distribucion).grid(
                               row=3, column=i, padx=10, pady=5)
        
        # Frame de parámetros (dinámico según distribución)
        self.params_frame = ttk.LabelFrame(main_frame, text="Parámetros de la Distribución", 
                                          padding="15")
        self.params_frame.pack(fill='x', pady=5)
        
        self.crear_parametros_uniforme()
        
        # Botones de acción
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(pady=10)
        
        ttk.Button(botones_frame, text="Generar Variables", 
                  command=self.generar_variables,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        ttk.Button(botones_frame, text="Limpiar", 
                  command=self.limpiar_todo).pack(side='left', padx=5)
        
        ttk.Button(botones_frame, text="Exportar a Excel", 
                  command=self.exportar_excel).pack(side='left', padx=5)
        
        # Notebook para resultados
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=5)
        
        # Pestaña de tabla
        self.frame_tabla = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_tabla, text="Tabla de Datos")
        self.crear_tabla()
        
        # Pestaña de gráfico
        self.frame_grafico = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_grafico, text="Histograma")
    
    def crear_tabla(self):
        """Crea la tabla para mostrar datos"""
        tabla_container = ttk.Frame(self.frame_tabla)
        tabla_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Nro', 'Valor')
        self.tree = ttk.Treeview(tabla_container, columns=columns, show='headings', height=20)
        
        self.tree.heading('Nro', text='Nro')
        self.tree.heading('Valor', text='Valor')
        
        self.tree.column('Nro', width=100, anchor='center')
        self.tree.column('Valor', width=200, anchor='center')
        
        scrollbar = ttk.Scrollbar(tabla_container, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def cambiar_distribucion(self):
        """Cambia los parámetros según la distribución seleccionada"""
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        distribucion = self.distribucion_var.get()
        
        if distribucion == "uniforme":
            self.crear_parametros_uniforme()
            self.es_discreta = False
        elif distribucion == "exponencial":
            self.crear_parametros_exponencial()
            self.es_discreta = False
        elif distribucion == "k_erlang":
            self.crear_parametros_k_erlang()
            self.es_discreta = False
        elif distribucion == "gamma":
            self.crear_parametros_gamma()
            self.es_discreta = False
        elif distribucion == "normal":
            self.crear_parametros_normal()
            self.es_discreta = False
        elif distribucion == "weibull":
            self.crear_parametros_weibull()
            self.es_discreta = False
        elif distribucion == "bernoulli":
            self.crear_parametros_bernoulli()
            self.es_discreta = True
        elif distribucion == "binomial":
            self.crear_parametros_binomial()
            self.es_discreta = True
        elif distribucion == "poisson":
            self.crear_parametros_poisson()
            self.es_discreta = True
    
    def crear_parametros_uniforme(self):
        """Crea campos para distribución Uniforme(min, max)"""
        ttk.Label(self.params_frame, text="Mínimo (min):", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.param1 = ttk.Entry(self.params_frame, width=20)
        self.param1.grid(row=0, column=1, pady=5, padx=10)
        self.param1.insert(0, "0")
        
        ttk.Label(self.params_frame, text="Máximo (max):", 
                 font=('Arial', 10)).grid(row=0, column=2, sticky='w', pady=5, padx=10)
        self.param2 = ttk.Entry(self.params_frame, width=20)
        self.param2.grid(row=0, column=3, pady=5, padx=10)
        self.param2.insert(0, "1")
        
        self.param3 = None
    
    def crear_parametros_exponencial(self):
        """Crea campos para distribución Exponencial(media)"""
        ttk.Label(self.params_frame, text="Media:", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.param1 = ttk.Entry(self.params_frame, width=20)
        self.param1.grid(row=0, column=1, pady=5, padx=10)
        self.param1.insert(0, "1")
        
        self.param2 = None
        self.param3 = None
    
    def crear_parametros_k_erlang(self):
        """Crea campos para distribución k-Erlang(k, media)"""
        ttk.Label(self.params_frame, text="k (forma):", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.param1 = ttk.Entry(self.params_frame, width=20)
        self.param1.grid(row=0, column=1, pady=5, padx=10)
        self.param1.insert(0, "2")
        
        ttk.Label(self.params_frame, text="Media:", 
                 font=('Arial', 10)).grid(row=0, column=2, sticky='w', pady=5, padx=10)
        self.param2 = ttk.Entry(self.params_frame, width=20)
        self.param2.grid(row=0, column=3, pady=5, padx=10)
        self.param2.insert(0, "2")
        
        self.param3 = None
    
    def crear_parametros_gamma(self):
        """Crea campos para distribución Gamma(media, varianza)"""
        ttk.Label(self.params_frame, text="Media:", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.param1 = ttk.Entry(self.params_frame, width=20)
        self.param1.grid(row=0, column=1, pady=5, padx=10)
        self.param1.insert(0, "2")
        
        ttk.Label(self.params_frame, text="Varianza:", 
                 font=('Arial', 10)).grid(row=0, column=2, sticky='w', pady=5, padx=10)
        self.param2 = ttk.Entry(self.params_frame, width=20)
        self.param2.grid(row=0, column=3, pady=5, padx=10)
        self.param2.insert(0, "1")
        
        self.param3 = None
    
    def crear_parametros_normal(self):
        """Crea campos para distribución Normal(media, varianza)"""
        ttk.Label(self.params_frame, text="Media:", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.param1 = ttk.Entry(self.params_frame, width=20)
        self.param1.grid(row=0, column=1, pady=5, padx=10)
        self.param1.insert(0, "0")
        
        ttk.Label(self.params_frame, text="Varianza:", 
                 font=('Arial', 10)).grid(row=0, column=2, sticky='w', pady=5, padx=10)
        self.param2 = ttk.Entry(self.params_frame, width=20)
        self.param2.grid(row=0, column=3, pady=5, padx=10)
        self.param2.insert(0, "1")
        
        self.param3 = None
    
    def crear_parametros_weibull(self):
        """Crea campos para distribución Weibull(alpha, beta, gamma)"""
        ttk.Label(self.params_frame, text="Alpha (α - forma):", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.param1 = ttk.Entry(self.params_frame, width=15)
        self.param1.grid(row=0, column=1, pady=5, padx=5)
        self.param1.insert(0, "1.5")
        
        ttk.Label(self.params_frame, text="Beta (β - escala):", 
                 font=('Arial', 10)).grid(row=0, column=2, sticky='w', pady=5, padx=10)
        self.param2 = ttk.Entry(self.params_frame, width=15)
        self.param2.grid(row=0, column=3, pady=5, padx=5)
        self.param2.insert(0, "1")
        
        ttk.Label(self.params_frame, text="Gamma (γ - ubicación):", 
                 font=('Arial', 10)).grid(row=0, column=4, sticky='w', pady=5, padx=10)
        self.param3 = ttk.Entry(self.params_frame, width=15)
        self.param3.grid(row=0, column=5, pady=5, padx=5)
        self.param3.insert(0, "0")
    
    # ============= PARÁMETROS PARA DISTRIBUCIONES DISCRETAS =============
    
    def crear_parametros_bernoulli(self):
        """Crea campos para distribución Bernoulli(p)"""
        ttk.Label(self.params_frame, text="Probabilidad de éxito (p) [0,1]:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.param1 = ttk.Entry(self.params_frame, width=20)
        self.param1.grid(row=0, column=1, pady=5, padx=10)
        self.param1.insert(0, "0.5")
        
        # Info adicional
        ttk.Label(self.params_frame, text="Media: p  |  Varianza: p(1-p)", 
                 font=('Arial', 9, 'italic'), foreground='blue').grid(row=1, column=0, columnspan=2, sticky='w', pady=5, padx=10)
        
        self.param2 = None
        self.param3 = None
    
    def crear_parametros_binomial(self):
        """Crea campos para distribución Binomial(n, p)"""
        ttk.Label(self.params_frame, text="Número de intentos (n):", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.param1 = ttk.Entry(self.params_frame, width=20)
        self.param1.grid(row=0, column=1, pady=5, padx=10)
        self.param1.insert(0, "10")
        
        ttk.Label(self.params_frame, text="Probabilidad de éxito (p) [0,1]:", 
                 font=('Arial', 10)).grid(row=0, column=2, sticky='w', pady=5, padx=10)
        self.param2 = ttk.Entry(self.params_frame, width=20)
        self.param2.grid(row=0, column=3, pady=5, padx=10)
        self.param2.insert(0, "0.5")
        
        # Info adicional
        ttk.Label(self.params_frame, text="Media: np  |  Varianza: np(1-p)", 
                 font=('Arial', 9, 'italic'), foreground='blue').grid(row=1, column=0, columnspan=4, sticky='w', pady=5, padx=10)
        
        self.param3 = None
    
    def crear_parametros_poisson(self):
        """Crea campos para distribución Poisson(lambda)"""
        ttk.Label(self.params_frame, text="Lambda (λ - tasa de ocurrencia) > 0:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5, padx=10)
        self.param1 = ttk.Entry(self.params_frame, width=20)
        self.param1.grid(row=0, column=1, pady=5, padx=10)
        self.param1.insert(0, "3")
        
        # Info adicional
        ttk.Label(self.params_frame, text="Media: λ  |  Varianza: λ", 
                 font=('Arial', 9, 'italic'), foreground='blue').grid(row=1, column=0, columnspan=2, sticky='w', pady=5, padx=10)
        
        self.param2 = None
        self.param3 = None
    
    def generar_variables(self):
        """Genera las variables aleatorias según la distribución seleccionada"""
        try:
            # Validar semilla
            semilla_text = self.entry_semilla.get().strip()
            if not semilla_text:
                messagebox.showerror("Error", "Debe ingresar una semilla")
                return
            semilla = int(semilla_text)
            
            # Obtener cantidad
            n = int(self.entry_cantidad.get())
            if n <= 0 or n > 10000:
                messagebox.showerror("Error", "La cantidad debe estar entre 1 y 10000")
                return
            
            # Crear generador
            generador = GeneradorVariables(semilla)
            
            distribucion = self.distribucion_var.get()
            
            # ========== DISTRIBUCIONES y variables ==========
            if distribucion == "uniforme":
                minimo = float(self.param1.get())
                maximo = float(self.param2.get())
                if minimo >= maximo:
                    messagebox.showerror("Error", "El mínimo debe ser menor que el máximo")
                    return
                self.variables_generadas = generador.uniforme(n, minimo, maximo)
                self.distribucion_actual = f"Uniforme(min={minimo}, max={maximo})"
                
            elif distribucion == "exponencial":
                media = float(self.param1.get())
                if media <= 0:
                    messagebox.showerror("Error", "La media debe ser mayor a 0")
                    return
                self.variables_generadas = generador.exponencial(n, media)
                self.distribucion_actual = f"Exponencial(media={media})"
                
            elif distribucion == "k_erlang":
                k = int(self.param1.get())
                media = float(self.param2.get())
                if k <= 0 or media <= 0:
                    messagebox.showerror("Error", "k y la media deben ser mayores a 0")
                    return
                self.variables_generadas = generador.k_erlang(n, k, media)
                self.distribucion_actual = f"k-Erlang(k={k}, media={media})"
                
            elif distribucion == "gamma":
                media = float(self.param1.get())
                varianza = float(self.param2.get())
                if media <= 0 or varianza <= 0:
                    messagebox.showerror("Error", "La media y varianza deben ser mayores a 0")
                    return
                self.variables_generadas = generador.gamma_dist(n, media, varianza)
                self.distribucion_actual = f"Gamma(media={media}, varianza={varianza})"
                
            elif distribucion == "normal":
                media = float(self.param1.get())
                varianza = float(self.param2.get())
                if varianza <= 0:
                    messagebox.showerror("Error", "La varianza debe ser mayor a 0")
                    return
                self.variables_generadas = generador.normal(n, media, varianza)
                self.distribucion_actual = f"Normal(μ={media}, σ²={varianza})"
                
            elif distribucion == "weibull":
                alpha = float(self.param1.get())
                beta = float(self.param2.get())
                gamma_p = float(self.param3.get())
                if alpha <= 0 or beta <= 0:
                    messagebox.showerror("Error", "Alpha y Beta deben ser mayores a 0")
                    return
                self.variables_generadas = generador.weibull(n, alpha, beta, gamma_p)
                self.distribucion_actual = f"Weibull(α={alpha}, β={beta}, γ={gamma_p})"
            
            # ========== DISTRIBUCIONES DISCRETAS ==========
            elif distribucion == "bernoulli":
                p = float(self.param1.get())
                if not (0 <= p <= 1):
                    messagebox.showerror("Error", "La probabilidad p debe estar entre 0 y 1")
                    return
                self.variables_generadas = generador.bernoulli(n, p)
                self.distribucion_actual = f"Bernoulli(p={p})"
                
            elif distribucion == "binomial":
                n_trials = int(self.param1.get())
                p = float(self.param2.get())
                if n_trials <= 0:
                    messagebox.showerror("Error", "El número de intentos debe ser mayor a 0")
                    return
                if not (0 <= p <= 1):
                    messagebox.showerror("Error", "La probabilidad p debe estar entre 0 y 1")
                    return
                self.variables_generadas = generador.binomial(n, n_trials, p)
                self.distribucion_actual = f"Binomial(n={n_trials}, p={p})"
                
            elif distribucion == "poisson":
                lambda_param = float(self.param1.get())
                if lambda_param <= 0:
                    messagebox.showerror("Error", "Lambda debe ser mayor a 0")
                    return
                self.variables_generadas = generador.poisson(n, lambda_param)
                self.distribucion_actual = f"Poisson(λ={lambda_param})"
            
            # Crear DataFrame
            if self.es_discreta:
                # Para discretas, mostrar valores enteros
                self.df_resultados = pd.DataFrame({
                    'Nro': range(1, n + 1),
                    'Valor': self.variables_generadas.astype(int)
                })
            else:
                # Para continuas, 2 decimales
                self.df_resultados = pd.DataFrame({
                    'Nro': range(1, n + 1),
                    'Valor': np.round(self.variables_generadas, 2)
                })
            
            # Mostrar resultados
            self.mostrar_tabla()
            self.mostrar_histograma()
            
            messagebox.showinfo("Éxito", f"{n} variables aleatorias generadas\nSemilla: {semilla}")
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar variables: {str(e)}")
    
    def mostrar_tabla(self):
        """Muestra los datos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar datos
        for _, row in self.df_resultados.iterrows():
            if self.es_discreta:
                self.tree.insert('', 'end', values=(
                    int(row['Nro']),
                    int(row['Valor'])
                ))
            else:
                self.tree.insert('', 'end', values=(
                    int(row['Nro']),
                    f"{row['Valor']:.2f}"
                ))
    
    def mostrar_histograma(self):
        """Muestra el histograma de los datos"""
        # Limpiar gráfico anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if self.es_discreta:
            # Para distribuciones discretas, usar barras
            valores_unicos = np.unique(self.variables_generadas)
            conteos = [np.sum(self.variables_generadas == v) for v in valores_unicos]
            
            ax.bar(valores_unicos, conteos, color='skyblue', 
                   edgecolor='navy', alpha=0.7, width=0.8)
            ax.set_xlabel('Valor', fontsize=11)
            ax.set_ylabel('Frecuencia', fontsize=11)
        else:
            # Para distribuciones continuas, usar histograma tradicional
            ax.hist(self.variables_generadas, bins=30, color='skyblue', 
                    edgecolor='navy', alpha=0.7, density=True)
            ax.set_xlabel('Valor', fontsize=11)
            ax.set_ylabel('Densidad', fontsize=11)
        
        ax.set_title(f'Histograma - Distribución {self.distribucion_actual}', 
                    fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def exportar_excel(self):
        """Exporta los resultados a Excel"""
        if self.df_resultados is None:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"variables_aleatorias_{timestamp}.xlsx"
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                self.df_resultados.to_excel(writer, sheet_name='Datos', index=False)
            
            messagebox.showinfo("Éxito", f"Archivo exportado:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def limpiar_todo(self):
        """Limpia todos los campos y resultados"""
        self.entry_semilla.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "100")
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        
        self.variables_generadas = None
        self.df_resultados = None
        self.distribucion_actual = None
        self.es_discreta = False
    
    def volver_atras(self):
        """Vuelve a la ventana principal"""
        if self.main_window:
            self.main_window.deiconify()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = InterfazVariables(root)
    root.mainloop()


if __name__ == "__main__":
    main()