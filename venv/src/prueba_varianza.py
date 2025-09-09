# prueba_varianza.py
import tkinter as tk
from tkinter import ttk, messagebox
from scipy.stats import chi2

# ------------------- Funciones estadísticas -------------------
def media(X):
    return sum(X) / len(X)

def varianza(X):
    m = media(X)
    acumulado = sum((x - m)**2 for x in X)
    return acumulado / (len(X) - 1)  # varianza muestral

# Para H0: sigma^2 = 1/12 (varianza de U(0,1))
def limite_inferior_varianza(alpha, n):
    chi_cuadrada = chi2.ppf(alpha / 2, n - 1)
    return ((n - 1) * (1/12)) / chi_cuadrada

def limite_superior_varianza(alpha, n):
    chi_cuadrada = chi2.ppf(1 - (alpha / 2), n - 1)
    return ((n - 1) * (1/12)) / chi_cuadrada

def prueba_varianza(alpha, X):
    var_x = varianza(X)
    li_var = limite_inferior_varianza(alpha, len(X))
    ls_var = limite_superior_varianza(alpha, len(X))

    if li_var <= var_x <= ls_var:
        return f"✅ La varianza = {var_x:.4f} está dentro de los límites [{li_var:.4f}, {ls_var:.4f}]"
    else:
        return f"❌ La varianza = {var_x:.4f} NO está dentro de los límites [{li_var:.4f}, {ls_var:.4f}]"

# ------------------- Interfaz gráfica -------------------
class PruebaVarianzaApp(tk.Toplevel):
    def __init__(self, master, valores_r):
        super().__init__(master)
        self.title("Prueba de Varianza")
        self.geometry("450x220")
        self.valores_r = valores_r

        tk.Label(self, text="Prueba de Varianza", font=("Arial", 14, "bold")).pack(pady=10)

        frame_conf = tk.Frame(self)
        frame_conf.pack(pady=10)
        tk.Label(frame_conf, text="Nivel de confianza:").grid(row=0, column=0, padx=5)
        self.combo_conf = ttk.Combobox(frame_conf, values=["90%", "95%", "99%"], state="readonly", width=10)
        self.combo_conf.grid(row=0, column=1, padx=5)
        self.combo_conf.current(1)  # por defecto 95%

        tk.Button(self, text="Ejecutar Prueba", width=18, command=self.ejecutar_prueba).pack(pady=15)
        tk.Button(self, text="Cerrar", width=18, command=self.destroy).pack(pady=5)

    def ejecutar_prueba(self):
        if not self.valores_r:
            messagebox.showwarning("Atención", "No hay valores para analizar.")
            return

        conf_str = self.combo_conf.get()
        confianza = int(conf_str.replace("%", ""))
        alpha = 1 - (confianza / 100)

        resultado = prueba_varianza(alpha, self.valores_r)
        messagebox.showinfo("Resultado", resultado)

# ------------------- Prueba rápida desde consola -------------------
if __name__ == '__main__':
    X = [0.552, 0.1733, 0.2222, 0.2645, 0.3214]
    app = tk.Tk()
    app.withdraw()
    PruebaVarianzaApp(app, X)
    app.mainloop()
