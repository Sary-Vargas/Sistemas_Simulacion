import tkinter as tk
import os
from tkinter import messagebox
from salir import SalirApp  # tu ventana con mensaje oculto
import clase1
import clase2
import clase3

def abrir_script(nombre_archivo):
    """Abre otro script Python como módulo independiente."""
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


# Ventana principal
root = tk.Tk()
root.title("Sistemas y Simulación")
root.geometry("500x520")
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

# ----------------- BOTÓN MENSAJE ------------------
tk.Button(root, text="Mensaje", width=20, height=2,
          bg="blue", fg="white", font=("Arial", 10, "bold"),
          command=lambda: SalirApp(root=root)).pack(pady=10)

# ----------------- BOTÓN CERRAR ------------------
tk.Button(root, text="Cerrar", width=20, height=2,
          bg="red", fg="white", font=("Arial", 10, "bold"),
          command=root.destroy).pack(side="bottom", pady=20)

root.mainloop()
