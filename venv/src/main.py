import tkinter as tk
import os
from tkinter import messagebox
from salir import SalirApp  # tu ventana con mensaje oculto

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
root.geometry("550x600")
root.configure(bg="#2c3e50")  # Fondo azul oscuro

# Marco principal para organizar el contenido
main_frame = tk.Frame(root, bg="#2c3e50")
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Título con mejor estilo
title_label = tk.Label(main_frame, 
                       text="SISTEMAS Y SIMULACIÓN", 
                       font=("Arial", 20, "bold"), 
                       bg="#2c3e50", 
                       fg="#ecf0f1")
title_label.pack(pady=(10, 30))

# Marco para los botones de opciones
button_frame = tk.Frame(main_frame, bg="#2c3e50")
button_frame.pack(pady=10)

# Botones de scripts con colores atractivos
opciones = [
    ("Algoritmo de Cuadrados Medios", "clase1.py", "#3498db"),
    ("Algoritmo de Productos Medios", "clase2.py", "#2ecc71"),
    ("Algoritmo Multiplicador Constante", "clase3.py", "#e74c3c"),
]

for texto, archivo, color in opciones:
    btn = tk.Button(button_frame, 
                    text=texto, 
                    width=35, 
                    height=2,
                    font=("Arial", 12, "bold"),
                    bg=color,
                    fg="white",
                    activebackground=color,
                    activeforeground="white",
                    relief="raised",
                    bd=3,
                    cursor="hand2",
                    command=lambda a=archivo: abrir_script(a))
    btn.pack(pady=8)

# Marco para botones inferiores
bottom_frame = tk.Frame(main_frame, bg="#2c3e50")
bottom_frame.pack(pady=(30, 10))

# ----------------- BOTÓN MENSAJE ------------------
msg_btn = tk.Button(bottom_frame, 
                    text="Mensaje", 
                    width=20, 
                    height=2,
                    bg="#9b59b6", 
                    fg="white", 
                    font=("Arial", 12, "bold"),
                    activebackground="#8e44ad",
                    activeforeground="white",
                    relief="raised",
                    bd=3,
                    cursor="hand2",
                    command=lambda: SalirApp(root=root))
msg_btn.pack(pady=10)

# ----------------- BOTÓN CERRAR ------------------
close_btn = tk.Button(bottom_frame, 
                      text="Cerrar", 
                      width=20, 
                      height=2,
                      bg="#e74c3c", 
                      fg="white", 
                      font=("Arial", 12, "bold"),
                      activebackground="#c0392b",
                      activeforeground="white",
                      relief="raised",
                      bd=3,
                      cursor="hand2",
                      command=root.destroy)
close_btn.pack(pady=10)

# Añadir un pequeño pie de página
footer_label = tk.Label(root, 
                        text="© 2023 - Sistemas y Simulación", 
                        font=("Arial", 8), 
                        bg="#2c3e50", 
                        fg="#bdc3c7")
footer_label.pack(side="bottom", pady=5)

root.mainloop()