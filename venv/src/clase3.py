# src/clase3.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os
import pandas as pd
from prueba_medias import PruebaMediasApp 
from prueba_varianza import PruebaVarianzaApp 
from prueba_uniformidad import ChiSquareGUI 
def producto_constante(constante, semilla, n):

    resultados = []
    a = semilla
    c = constante
    for _ in range(n):
        resultado = a * c
        res_str = str(resultado).zfill(8)
        x = int(res_str[2:6])  # 4 dígitos centrales
        r = x / 10000.0
        resultados.append((c, a, resultado, x, r))
        a = x  # la nueva semilla es X
    return resultados


class Clase3App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algoritmo Multiplicador Constante")
        self.geometry("1000x620")
        self.resizable(False, False)

        # flujo de entradas
        self.paso = 1   # 1=constante, 2=semilla, 3=n, 4=listo
        self.constante = None
        self.semilla = None
        self.n = None
        self.resultados = None  # <--- Guardar resultados generados

        # ---------------- título ----------------
        title = tk.Label(self,
                         text="SISTEMAS Y SIMULACIÓN\nMÉTODO DEL PRODUCTO CONSTANTE",
                         font=("Arial", 14, "bold"), justify="center")
        title.pack(pady=8)

        # ---------------- barra superior ----------------
        top_bar = tk.Frame(self)
        top_bar.pack(fill="x", padx=10, pady=5)
        #boton de prueba medias
        self.btn_prueba_medias = tk.Button(
            top_bar, text="Prueba de Medias", width=20, height=1,
            command=self.abrir_prueba_medias
        )
        self.btn_prueba_medias.pack(side="right")
        self.btn_prueba_medias.config(state="disabled")  

        # Botón prueba de varianza
        self.btn_prueba_varianza = tk.Button(
            top_bar, text="Prueba de Varianza", width=20, height=1,
            command=self.abrir_prueba_varianza
        )
        self.btn_prueba_varianza.pack(side="right", padx=5)
        self.btn_prueba_medias.config(state="disabled")

        # Botón prueba chi2
        self.btn_prueba_chi2 = tk.Button(
            top_bar, text="Prueba Chi²", width=20, height=1,
            command=self.abrir_prueba_chi2
        )
        self.btn_prueba_chi2.pack(side="right", padx=5)
        self.btn_prueba_chi2.config(state="disabled")

        # Botón Exportar a Excel
        self.btn_exportar_excel = tk.Button(
            top_bar, text="Exportar a Excel", width=20, height=1,
            state="disabled",  # desactivado inicialmente
            command=self.exportar_a_excel
        )
        self.btn_exportar_excel.pack(side="right", padx=5)

        # menu principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=6)

        # ---------------- izquierda: calculadora ----------------
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", padx=8, pady=4)

        self.label_msg = tk.Label(left_frame, text="Ingrese la constante:", font=("Arial", 11))
        self.label_msg.grid(row=0, column=0, columnspan=3, pady=(4,8))

        self.entry_input = tk.Entry(left_frame, width=20, font=("Arial", 14), justify="center")
        self.entry_input.grid(row=1, column=0, columnspan=3, pady=(0,8))
        self.entry_input.focus_set()
        self.entry_input.bind("<Return>", self.guardar_valor)

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
                  command=self.guardar_valor).grid(row=6, column=0, columnspan=3, pady=(8,6))

        self.btn_generar = tk.Button(left_frame, text="Generar", width=20, height=2,
                                     command=self.generar)
        self.btn_generar.grid(row=7, column=0, columnspan=3, pady=(6,4))
        self.btn_generar.grid_remove()

        tk.Button(left_frame, text="Resetear entradas", width=20, height=1,
                  command=self.resetear_entradas).grid(row=8, column=0, columnspan=3, pady=(6,4))

        # ---------------- derecha: tabla ----------------
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=6)

        cols = ("Constante", "Semilla", "Resultado", "X", "R")
        self.tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=18)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ---------------- abajo: volver / salir ----------------
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill="x", padx=12, pady=8)

        tk.Button(bottom_frame, text="Volver atrás", width=16, command=self.volver_atras).pack(side="left")
        tk.Button(bottom_frame, text="Salir", width=16, command=self.quit).pack(side="right")

    # def
    def agregar_numero(self, digito):
        if self.entry_input.cget("state") == "disabled":
            return
        self.entry_input.insert(tk.END, digito)

    def borrar_uno(self):
        if self.entry_input.cget("state") == "disabled":
            return
        s = self.entry_input.get()
        if s:
            self.entry_input.delete(len(s)-1, tk.END)

    def limpiar(self):
        if self.entry_input.cget("state") == "disabled":
            return
        self.entry_input.delete(0, tk.END)

    # ---- flujo guiado ----
    def guardar_valor(self, event=None):
        valor = self.entry_input.get().strip()
        if not valor.isdigit():
            messagebox.showerror("Error", "Ingrese solo números enteros positivos")
            return

        if self.paso == 1:
            self.constante = int(valor)
            self.paso = 2
            self.label_msg.config(text="Ingrese la semilla inicial:")
            self.entry_input.delete(0, tk.END)

        elif self.paso == 2:
            self.semilla = int(valor)
            self.paso = 3
            self.label_msg.config(text="Ingrese cantidad de números a generar:")
            self.entry_input.delete(0, tk.END)

        elif self.paso == 3:
            n_val = int(valor)
            if n_val <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor que 0")
                return
            self.n = n_val
            self.paso = 4
            self.entry_input.delete(0, tk.END)
            self.entry_input.config(state="disabled")
            self.label_msg.config(text="Listo. Presione 'Generar'")
            self.btn_generar.grid()

    def generar(self):
        if self.constante is None or self.semilla is None or self.n is None:
            messagebox.showerror("Error", "Faltan valores")
            return

        self.resultados = producto_constante(self.constante, self.semilla, self.n)
        self.btn_exportar_excel.config(state="normal") 

        for it in self.tree.get_children():
            self.tree.delete(it)

        for c, a, res, x, r in self.resultados:
            self.tree.insert("", "end", values=(c, a, res, x, f"{r:.4f}"))

        ## Habilitar botones de pruebas
        self.btn_prueba_medias.config(state="normal")
        self.btn_prueba_varianza.config(state="normal")
        self.btn_prueba_chi2.config(state="normal")

    # prueba de medias 
    def abrir_prueba_medias(self):
        if not self.resultados:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return
        r_values = [r for (_, _, _, _, r) in self.resultados]
        PruebaMediasApp(self, r_values)
    def abrir_prueba_varianza(self):
        if not self.resultados:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return  # <- ahora correctamente indentado

        r_values = [r for (_, _, _, _, r) in self.resultados]
        PruebaVarianzaApp(self, r_values)

    def abrir_prueba_chi2(self):
        if not self.resultados:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return
        r_values = [r for (_, _, _, _, r) in self.resultados]
        ChiSquareGUI(self, r_values)
    
    def exportar_a_excel(self):
        if not self.resultados:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return
        df = pd.DataFrame(self.resultados, columns=["Constante", "Semilla", "Resultado", "X", "R"])

        # Diálogo para guardar archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivo Excel", "*.xlsx")],
            title="Guardar como"
        )

        if not file_path:
            return 

        try:
            df.to_excel(file_path, index=False, engine="openpyxl")
            messagebox.showinfo("Éxito", f"Archivo guardado correctamente:\n{file_path}")
        except PermissionError:
            messagebox.showerror("Error", "No se pudo guardar el archivo. ¿Está abierto en Excel?")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar el archivo:\n{e}")

    def resetear_entradas(self):
        self.paso = 1
        self.constante = None
        self.semilla = None
        self.n = None
        self.resultados = None
        self.btn_exportar_excel.config(state="disabled")
        self.entry_input.config(state="normal")
        self.entry_input.delete(0, tk.END)
        self.label_msg.config(text="Ingrese la constante:")
        self.btn_generar.grid_remove()
        self.btn_prueba_medias.config(state="disabled")
        for it in self.tree.get_children():
            self.tree.delete(it)

    def volver_atras(self):
        # Determinar la ruta correcta al archivo principal
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        ruta_main = os.path.join(parent_dir, "main.py")
        
        # Verificar si el archivo existe
        if not os.path.exists(ruta_main):
            messagebox.showerror("Error", "No se puede encontrar el menú principal.")
            return
            
        try:
            # Cerrar esta ventana
            self.destroy()
            # Ejecutar el archivo principal
            subprocess.Popen([sys.executable, ruta_main])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el menú principal: {e}")

    def on_close(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir?"):
            self.destroy()


if __name__ == "__main__":
    app = Clase3App()
    app.mainloop()
