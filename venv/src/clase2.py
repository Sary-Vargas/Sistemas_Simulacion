# src/clase2.py
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from prueba_medias import PruebaMediasApp

def productos_medios(a, b, n):
    """
    Método de los productos medios:
    - a, b: semillas iniciales
    - n: cantidad de números a generar
    Retorna lista de tuplas (a, b, a*b, x, r)
    """
    resultados = []
    for _ in range(n):
        ab = a * b
        ab_str = str(ab).zfill(8)  # asegurar al menos 8 dígitos
        x = int(ab_str[2:6])       # tomar 4 dígitos centrales
        r = x / 10000.0
        resultados.append((a, b, ab, x, r))
        a, b = b, x
    return resultados

class Clase2App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clase 2 - Método de Productos Medios")
        self.geometry("1000x620")
        self.resizable(False, False)

        self.paso = 1
        self.a = None
        self.b = None
        self.n = None
        self.resultados = None

        # ---------------- Barra superior ----------------
        top_bar = tk.Frame(self)
        top_bar.pack(fill="x", padx=10, pady=5)

        # Botón prueba de medias
        self.btn_prueba_medias = tk.Button(
            top_bar, text="Prueba de Medias", width=20, height=1,
            command=self.abrir_prueba_medias
        )
        self.btn_prueba_medias.pack(side="right")

        # ---------------- Título ----------------
        title = tk.Label(self, text="SISTEMAS Y SIMULACIÓN\nMÉTODO DE PRODUCTOS MEDIOS",
                         font=("Arial", 14, "bold"), justify="center")
        title.pack(pady=8)

        # ---------------- Marco principal ----------------
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=6)

        # Left: calculadora / entradas
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", padx=8, pady=4)

        self.label_msg = tk.Label(left_frame, text="Ingrese valor de la semilla A:", font=("Arial", 11))
        self.label_msg.grid(row=0, column=0, columnspan=3, pady=(4, 8))

        self.entry_input = tk.Entry(left_frame, width=18, font=("Arial", 14), justify="center")
        self.entry_input.grid(row=1, column=0, columnspan=3, pady=(0, 8))
        self.entry_input.focus_set()
        self.entry_input.bind("<Return>", self.guardar_valor)

        # Botones numéricos
        botones = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2),
            ("←", 5, 0), ("0", 5, 1), ("C", 5, 2),
        ]
        for (txt, r, c) in botones:
            if txt == "←":
                cmd = self.borrar_uno
            elif txt == "C":
                cmd = self.limpiar
            else:
                cmd = lambda t=txt: self.agregar_numero(t)
            tk.Button(left_frame, text=txt, width=6, height=2, command=cmd).grid(row=r, column=c, padx=4, pady=4)

        tk.Button(left_frame, text="Enter (Confirmar)", width=20, height=2,
                  command=self.guardar_valor).grid(row=6, column=0, columnspan=3, pady=(8, 6))

        # Botón Generar (oculto hasta completar A, B, n)
        self.btn_generar = tk.Button(left_frame, text="Generar", width=20, height=2, command=self.generar)
        self.btn_generar.grid(row=7, column=0, columnspan=3, pady=(6, 4))
        self.btn_generar.grid_remove()

        tk.Button(left_frame, text="Resetear entradas", width=20, height=1,
                  command=self.resetear_entradas).grid(row=8, column=0, columnspan=3, pady=(6, 4))

        # Right: tabla de resultados
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=6)

        cols = ("a", "b", "a*b", "x", "r")
        self.tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=18)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bottom
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill="x", padx=12, pady=8)
        tk.Button(bottom_frame, text="Volver atrás", width=16, command=self.volver_atras).pack(side="left")
        tk.Button(bottom_frame, text="Salir", width=16, command=self.quit).pack(side="right")

    # ---------------- Helpers ----------------
    def agregar_numero(self, digito):
        if self.entry_input.cget("state") == "disabled": return
        self.entry_input.insert(tk.END, digito)

    def borrar_uno(self):
        if self.entry_input.cget("state") == "disabled": return
        s = self.entry_input.get()
        if s:
            self.entry_input.delete(len(s) - 1, tk.END)

    def limpiar(self):
        if self.entry_input.cget("state") == "disabled": return
        self.entry_input.delete(0, tk.END)

    def guardar_valor(self, event=None):
        valor = self.entry_input.get().strip()
        if valor == "":
            messagebox.showwarning("Atención", "Ingrese un número y presione Enter o el botón Enter.")
            return
        if not valor.isdigit():
            messagebox.showerror("Error", "Solo se permiten números enteros positivos.")
            return

        if self.paso == 1:
            self.a = int(valor)
            self.paso = 2
            self.entry_input.delete(0, tk.END)
            self.label_msg.config(text="Ingrese valor de la semilla B:")
            return

        if self.paso == 2:
            self.b = int(valor)
            self.paso = 3
            self.entry_input.delete(0, tk.END)
            self.label_msg.config(text="Ingrese cantidad de números a generar:")
            return

        if self.paso == 3:
            n_val = int(valor)
            if n_val <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor que 0.")
                return
            self.n = n_val
            self.paso = 4
            self.entry_input.delete(0, tk.END)
            self.entry_input.config(state="disabled")
            self.label_msg.config(text="Listo. Presione 'Generar' para producir la secuencia.")
            self.btn_generar.grid()
            return

    def generar(self):
        if self.a is None or self.b is None or self.n is None:
            messagebox.showerror("Error", "Faltan valores (A, B o n).")
            return

        self.resultados = productos_medios(self.a, self.b, self.n)

        # Limpiar tabla
        for it in self.tree.get_children():
            self.tree.delete(it)

        # Insertar resultados
        for a, b, ab, x, r in self.resultados:
            self.tree.insert("", "end", values=(a, b, ab, x, f"{r:.4f}"))

    def abrir_prueba_medias(self):
        if not self.resultados:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return

        r_values = [r for (_, _, _, _, r) in self.resultados]
        PruebaMediasApp(self, r_values)

    def resetear_entradas(self):
        self.paso = 1
        self.a = None
        self.b = None
        self.n = None
        self.resultados = None
        self.entry_input.config(state="normal")
        self.entry_input.delete(0, tk.END)
        self.label_msg.config(text="Ingrese valor de la semilla A:")
        self.btn_generar.grid_remove()
        for it in self.tree.get_children():
            self.tree.delete(it)

    def volver_atras(self):
        ruta_main = os.path.join(os.path.dirname(__file__), "main.py")
        if not os.path.exists(ruta_main):
            self.destroy()
            return
        try:
            subprocess.Popen([sys.executable, ruta_main])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir main.py: {e}")
        finally:
            self.destroy()


if __name__ == "__main__":
    app = Clase2App()
    app.mainloop()
