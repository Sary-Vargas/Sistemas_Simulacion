#main.py
import tkinter as tk
import os
from tkinter import messagebox
from salir import SalirApp  # tu ventana con mensaje oculto
import clase1
import clase2
import clase3

def abrir_script(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    if not os.path.exists(ruta):
        messagebox.showerror("Error", f"No se encontró el archivo: {nombre_archivo}")
        return
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            code = f.read()
        exec(code, {"__name__": "__main__"})
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar {nombre_archivo}:\n{e}")

def abrir_simulador_clientes():
    """Abre el simulador de llegada de clientes"""
    try:
        root.withdraw()
        from simulador_clientes import InterfazSimulador
        ventana_simulador = tk.Toplevel()
        app_simulador = InterfazSimulador(ventana_simulador, root)
    except ImportError:
        messagebox.showerror("Error", "No se encontró el archivo simulador_clientes.py")
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir el simulador:\n{e}")
        root.deiconify()

def abrir_regla30():
    """Abre el autómata celular Regla 30"""
    try:
        root.withdraw()
        from regla30 import InterfazRegla30
        ventana_regla30 = tk.Toplevel()
        app_regla30 = InterfazRegla30(ventana_regla30, root)
    except ImportError:
        messagebox.showerror("Error", "No se encontró el archivo regla30.py")
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir Regla 30:\n{e}")
        root.deiconify()

def abrir_regla90():
    """Abre el autómata celular Regla 90"""
    try:
        root.withdraw()
        from regla90 import InterfazRegla90
        ventana_regla90 = tk.Toplevel()
        app_regla90 = InterfazRegla90(ventana_regla90, root)
    except ImportError:
        messagebox.showerror("Error", "No se encontró el archivo regla90.py")
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir Regla 90:\n{e}")
        root.deiconify()

def abrir_regla_lineal():
    """Abre el autómata celular Regla Lineal"""
    try:
        root.withdraw()
        from reglalineal import InterfazReglaLineal
        ventana_lineal = tk.Toplevel()
        app_lineal = InterfazReglaLineal(ventana_lineal, root)
    except ImportError:
        messagebox.showerror("Error", "No se encontró el archivo reglalineal.py")
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir Regla Lineal:\n{e}")
        root.deiconify()

def abrir_variables():
    """Abre el generador de variables aleatorias"""
    try:
        root.withdraw()
        from variables import InterfazVariables
        ventana_variables = tk.Toplevel()
        app_variables = InterfazVariables(ventana_variables, root)
    except ImportError:
        messagebox.showerror("Error", "No se encontró el archivo variables.py")
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir Variables Aleatorias:\n{e}")
        root.deiconify()

def abrir_juego_vida():
    """Abre el Juego de la Vida"""
    try:
        root.withdraw()
        from juego import GameOfLifeApp
        ventana_juego = tk.Toplevel()
        app_juego = GameOfLifeApp(ventana_juego, root)
    except ImportError:
        messagebox.showerror("Error", "No se encontró el archivo juego.py")
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir Juego de la Vida:\n{e}")
        root.deiconify()

def abrir_covid():
    """Abre la simulación COVID-19"""
    try:
        root.withdraw()
        from covid import GameOfLifeApp as CovidApp
        ventana_covid = tk.Toplevel()
        app_covid = CovidApp(ventana_covid, root)
    except ImportError:
        messagebox.showerror("Error", "No se encontró el archivo covid.py")
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir COVID-19:\n{e}")
        root.deiconify()

# Ventana principal
root = tk.Tk()
root.title("Sistemas y Simulación")
root.geometry("500x900")
root.configure(bg="#f0f0f0")

# Título
tk.Label(root, text="SISTEMAS Y SIMULACIÓN", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=30)

# Botones de scripts
opciones = [
    ("Algoritmo de Cuadrados Medios", "clase1.py"),
    ("Algoritmo de Productos Medios", "clase2.py"),
    ("Algoritmo Multiplicador Constante", "clase3.py"),
]

for texto, archivo in opciones:
    tk.Button(root, text=texto, width=30, height=2,
              command=lambda a=archivo: abrir_script(a)).pack(pady=6)

# ----------------- BOTÓN LLEGADA DE CLIENTES ------------------
tk.Button(root, text="Llegada de Clientes", width=30, height=2,
          bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
          command=abrir_simulador_clientes).pack(pady=6)

# ----------------- BOTÓN REGLA 30 ------------------
tk.Button(root, text="Autómata Celular - Regla 30", width=30, height=2,
          bg="#9C27B0", fg="white", font=("Arial", 10, "bold"),
          command=abrir_regla30).pack(pady=6)

# ----------------- BOTÓN REGLA 90 ------------------
tk.Button(root, text="Autómata Celular - Regla 90", width=30, height=2,
          bg="#FF5722", fg="white", font=("Arial", 10, "bold"),
          command=abrir_regla90).pack(pady=6)

# ----------------- BOTÓN REGLA LINEAL ------------------
tk.Button(root, text="Autómata Celular - Regla Lineal", width=30, height=2,
          bg="#00BCD4", fg="white", font=("Arial", 10, "bold"),
          command=abrir_regla_lineal).pack(pady=6)

# ----------------- BOTÓN VARIABLES ALEATORIAS ------------------
tk.Button(root, text="Variables Aleatorias", width=30, height=2,
          bg="#FFC107", fg="black", font=("Arial", 10, "bold"),
          command=abrir_variables).pack(pady=6)

# ----------------- BOTÓN JUEGO DE LA VIDA ------------------
tk.Button(root, text="Juego de la Vida", width=30, height=2,
          bg="#8BC34A", fg="white", font=("Arial", 10, "bold"),
          command=abrir_juego_vida).pack(pady=6)

# ----------------- BOTÓN COVID-19 ------------------
tk.Button(root, text="COVID-19 Simulación", width=30, height=2,
          bg="#E91E63", fg="white", font=("Arial", 10, "bold"),
          command=abrir_covid).pack(pady=6)

# ----------------- BOTÓN MENSAJE ------------------
tk.Button(root, text="Mensaje", width=20, height=2,
          bg="blue", fg="white", font=("Arial", 10, "bold"),
          command=lambda: SalirApp(root=root)).pack(pady=10)

# ----------------- BOTÓN CERRAR ------------------
tk.Button(root, text="Cerrar", width=20, height=2,
          bg="red", fg="white", font=("Arial", 10, "bold"),
          command=root.destroy).pack(side="bottom", pady=20)

root.mainloop()