import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os
import pandas as pd
from prueba_medias import PruebaMediasApp  
from prueba_varianza import PruebaVarianzaApp 
from prueba_uniformidad import ChiSquareGUI   


def cuadrados_medios(seed, n):
    resultados = []
    a = seed
    for _ in range(n):
        a2 = a * a
        a2_str = str(a2).zfill(8)   # asegurar al menos 8 dígitos
        x = int(a2_str[2:6])        # tomar 4 dígitos centrales
        r = x / 10000.0
        resultados.append((a, a2, x, r))
        a = x
    return resultados


class Clase1App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clase 1 - Algoritmo de Cuadrados Medios")
        self.geometry("1000x620")
        self.resizable(False, False)
        self.configure(bg="#f0f4f7")  # 🎨 Fondo más suave

        # ----------- Estilos -----------
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TButton",
                        font=("Arial", 10, "bold"),
                        padding=6,
                        background="#4CAF50",
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#45a049")])

        style.configure("Danger.TButton",
                        font=("Arial", 10, "bold"),
                        padding=6,
                        background="#e53935",
                        foreground="white")
        style.map("Danger.TButton",
                  background=[("active", "#c62828")])

        style.configure("Secondary.TButton",
                        font=("Arial", 10, "bold"),
                        padding=6,
                        background="#2196F3",
                        foreground="white")
        style.map("Secondary.TButton",
                  background=[("active", "#1976D2")])

        style.configure("TLabel", font=("Arial", 11), background="#f0f4f7")

        # ---------------- Barra superior ----------------
        top_bar = tk.Frame(self, bg="#f0f4f7")
        top_bar.pack(fill="x", padx=10, pady=5)

        self.btn_prueba_medias = ttk.Button(
            top_bar, text="Prueba de Medias", style="Secondary.TButton",
            command=self.abrir_prueba_medias
        )
        self.btn_prueba_medias.pack(side="right", padx=5)
        self.btn_prueba_medias.config(state="disabled") 

        self.btn_prueba_varianza = ttk.Button(
            top_bar, text="Prueba de Varianza", style="Secondary.TButton",
            command=self.abrir_prueba_varianza
        )
        self.btn_prueba_varianza.pack(side="right", padx=5)
        self.btn_prueba_varianza.config(state="disabled")

        self.btn_prueba_chi2 = ttk.Button(
            top_bar, text="Prueba Chi²", style="Secondary.TButton",
            command=self.abrir_prueba_chi2
        )
        self.btn_prueba_chi2.pack(side="right", padx=5)
        self.btn_prueba_chi2.config(state="disabled")

        self.btn_exportar_excel = ttk.Button(
            top_bar, text="Exportar a Excel", style="TButton",
            state="disabled", command=self.exportar_a_excel
        )
        self.btn_exportar_excel.pack(side="right", padx=5)

        # ---------------- Título ----------------
        title = tk.Label(self, text="📊 SISTEMAS Y SIMULACIÓN\nMÉTODO DE LOS CUADRADOS MEDIOS",
                         font=("Arial", 16, "bold"), fg="#333", bg="#f0f4f7", justify="center")
        title.pack(pady=10)

        # ---------------- Menu principal ----------------
        main_frame = tk.Frame(self, bg="#f0f4f7")
        main_frame.pack(fill="both", expand=True, padx=10, pady=6)

        # Left
        left_frame = tk.Frame(main_frame, bg="#f0f4f7")
        left_frame.pack(side="left", padx=8, pady=4)

        self.label_msg = tk.Label(left_frame, text="Ingrese valor de la semilla A:",
                                  font=("Arial", 11, "bold"), bg="#f0f4f7", fg="#222")
        self.label_msg.grid(row=0, column=0, columnspan=3, pady=(4, 8))

        self.entry_input = tk.Entry(left_frame, width=20, font=("Arial", 14), justify="center", bd=3, relief="groove")
        self.entry_input.grid(row=1, column=0, columnspan=3, pady=(0, 8))
        self.entry_input.focus_set()
        self.entry_input.bind("<Return>", self.guardar_valor)

        # botones numéricos
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
                cmd = (lambda t=txt: self.agregar_numero(t))
            ttk.Button(left_frame, text=txt, style="TButton", width=8, command=cmd).grid(row=r, column=c, padx=4, pady=4)

        ttk.Button(left_frame, text="Enter (Confirmar)", style="TButton", width=20,
                   command=self.guardar_valor).grid(row=6, column=0, columnspan=3, pady=(8, 6))

        self.btn_generar = ttk.Button(left_frame, text="Generar", style="Secondary.TButton", width=20,
                                      command=self.generar)
        self.btn_generar.grid(row=7, column=0, columnspan=3, pady=(6, 4))
        self.btn_generar.grid_remove()

        ttk.Button(left_frame, text="Resetear entradas", style="Danger.TButton", width=20,
                   command=self.resetear_entradas).grid(row=8, column=0, columnspan=3, pady=(6, 4))

        # Right (tabla)
        right_frame = tk.Frame(main_frame, bg="#f0f4f7")
        right_frame.pack(side="right", fill="both", expand=True, padx=6)

        cols = ("a", "a^2", "x", "r")
        self.tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=18)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bottom
        bottom_frame = tk.Frame(self, bg="#f0f4f7")
        bottom_frame.pack(fill="x", padx=12, pady=8)

        ttk.Button(bottom_frame, text="Volver atrás", style="Secondary.TButton", width=16,
                   command=self.volver_atras).pack(side="left")
        ttk.Button(bottom_frame, text="Salir", style="Danger.TButton", width=16,
                   command=self.quit).pack(side="right")

    # ---------------- Funciones ----------------
    def agregar_numero(self, digito):
        if self.entry_input.cget("state") == "disabled":
            return
        self.entry_input.insert(tk.END, digito)

    def borrar_uno(self):
        if self.entry_input.cget("state") == "disabled":
            return
        s = self.entry_input.get()
        if s:
            self.entry_input.delete(len(s) - 1, tk.END)

    def limpiar(self):
        if self.entry_input.cget("state") == "disabled":
            return
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
            self.seed = int(valor)
            self.paso = 2
            self.entry_input.delete(0, tk.END)
            self.label_msg.config(text="Ingrese cantidad de números a generar:")
            return

        if self.paso == 2:
            n_val = int(valor)
            if n_val <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor que 0.")
                return
            self.n = n_val
            self.paso = 3
            self.entry_input.delete(0, tk.END)
            self.entry_input.config(state="disabled")
            self.label_msg.config(text="Listo. Presione 'Generar' para producir la secuencia.")
            self.btn_generar.grid()
            return

    def generar(self):
        if self.seed is None or self.n is None:
            messagebox.showerror("Error", "Faltan valores (semilla o cantidad).")
            return

        self.resultados = cuadrados_medios(self.seed, self.n)
        self.btn_exportar_excel.config(state="normal")  # ✅ activar exportar

        for it in self.tree.get_children():
            self.tree.delete(it)

        for a, a2, x, r in self.resultados:
            self.tree.insert("", "end", values=(a, a2, x, f"{r:.4f}"))
        # Habilitar botones de pruebas
        self.btn_prueba_medias.config(state="normal")
        self.btn_prueba_varianza.config(state="normal")
        self.btn_prueba_chi2.config(state="normal")

    def abrir_prueba_medias(self):
        if not self.resultados:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return
        r_values = [r for (_, _, _, r) in self.resultados]
        PruebaMediasApp(self, r_values)

    def abrir_prueba_varianza(self):
        if not self.resultados:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return
        r_values = [r for (_, _, _, r) in self.resultados]
        PruebaVarianzaApp(self, r_values)

    def abrir_prueba_chi2(self):
        if not self.resultados:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return
        r_values = [r for (_, _, _, r) in self.resultados]
        ChiSquareGUI(self, r_values)

    def exportar_a_excel(self):
        if not self.resultados:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return

        df = pd.DataFrame(self.resultados, columns=["a", "a^2", "x", "r"])

        # Diálogo para guardar archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivo Excel", "*.xlsx")],
            title="Guardar como"
        )

        if not file_path:
            return  # cancelado por el usuario

        try:
            df.to_excel(file_path, index=False, engine="openpyxl")
            messagebox.showinfo("Éxito", f"Archivo guardado correctamente:\n{file_path}")
        except PermissionError:
            messagebox.showerror("Error", "No se pudo guardar el archivo. ¿Está abierto en Excel?")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar el archivo:\n{e}")

    def resetear_entradas(self):
        self.paso = 1
        self.seed = None
        self.n = None
        self.resultados = None
        self.btn_exportar_excel.config(state="disabled")
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
    app = Clase1App()
    app.mainloop()
