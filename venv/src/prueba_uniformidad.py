import tkinter as tk
from tkinter import ttk
import numpy as np
import scipy.stats as stats

class ChiSquareGUI(tk.Toplevel):  # Toplevel permite abrirlo como ventana secundaria
    def __init__(self, parent, datos):
        super().__init__(parent)
        self.title("Prueba de Uniformidad Chi-Cuadrado")
        self.geometry("700x400")
        self.datos = datos  # <- ✅ Almacenar la lista de r

        # Entradas de usuario
        tk.Label(self, text="Número de intervalos (k):").grid(row=0, column=0, padx=5, pady=5)
        self.k_entry = tk.Entry(self)
        self.k_entry.insert(0, "10")
        self.k_entry.grid(row=0, column=1)

        tk.Button(self, text="Ejecutar Prueba", command=self.ejecutar_prueba).grid(row=1, column=0, columnspan=2, pady=10)

        # Tabla de resultados
        self.tree = ttk.Treeview(self, columns=("Intervalo", "Oi", "Ei", "((Ei-Oi)^2)/Ei"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.grid(row=2, column=0, columnspan=2, padx=10)

        # Resultados finales
        self.result_label = tk.Label(self, text="", font=('Arial', 12), fg='blue')
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def ejecutar_prueba(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            datos = self.datos
            n = len(datos)
            k = int(self.k_entry.get())
        except ValueError:
            self.result_label.config(text="❌ Ingrese valores válidos.")
            return

        observados, edges = np.histogram(datos, bins=k, range=(0, 1))
        esperados = [n / k] * k
        chi2_components = [((ei - oi) ** 2) / ei for oi, ei in zip(observados, esperados)]

        for i in range(k):
            intervalo = f"[{edges[i]:.2f}, {edges[i+1]:.2f})"
            self.tree.insert("", "end", values=(intervalo, observados[i], f"{esperados[i]:.2f}", f"{chi2_components[i]:.4f}"))

        chi2_stat = sum(chi2_components)
        p_valor = 1 - stats.chi2.cdf(chi2_stat, df=k-1)

        alpha = 0.05
        decision = "✅ No se rechaza H0 (uniforme)" if p_valor > alpha else "❌ Se rechaza H0 (no uniforme)"
        resumen = f"Chi² = {chi2_stat:.4f} | p-valor = {p_valor:.4f}\n{decision}"
        self.result_label.config(text=resumen)
