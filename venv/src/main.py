import tkinter as tk
import subprocess
import sys
import os

# Función para abrir otros scripts
def abrir_script(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    if sys.platform.startswith("win"):
        subprocess.Popen(["python", ruta], shell=True)
    else:  # Linux/Mac
        subprocess.Popen(["python3", ruta])

# Crear ventana principal
root = tk.Tk()
root.title("Sistemas y Simulación")
root.geometry("900x00")

# Título centrado
titulo = tk.Label(root, text="SISTEMAS Y SIMULACIÓN", font=("Arial", 16, "bold"))
titulo.pack(pady=40)

# Botones del menú
boton1 = tk.Button(root, text="Algoritmos de Cuadrados Medios", width=30, height=2,
                   command=lambda: abrir_script("clase1.py"))
boton1.pack(pady=5)

boton2 = tk.Button(root, text="Algoritmos de Cuadrados", width=30, height=2,
                   command=lambda: abrir_script("clase2.py"))
boton2.pack(pady=5)

boton3 = tk.Button(root, text="Algoritmo multiplicador constante", width=30, height=2,
                   command=lambda: abrir_script("clase3.py"))
boton3.pack(pady=5)

boton4 = tk.Button(root, text="Varios 2", width=30, height=2)
boton4.pack(pady=5)

boton5 = tk.Button(root, text="Varios 3", width=30, height=2)
boton5.pack(pady=5)

boton6 = tk.Button(root, text="Varios 4", width=30, height=2)
boton6.pack(pady=5)

# Iniciar loop de la GUI
root.mainloop()
