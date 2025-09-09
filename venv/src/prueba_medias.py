# src/prueba_medias.py 
import math 
import tkinter as tk 
from tkinter import ttk, messagebox 
from scipy.stats import norm 

# ------------------- Funciones estadísticas ------------------- 
def media(x): return sum(x) / len(x)
def limite_inferior_media(alpha, n): 
    alpha_limite = 1 - alpha/2 
    z = norm.ppf(alpha_limite, loc=0, scale=1) 
    return 0.5 - z * (1 / math.sqrt(12*n)) 
def limite_superior_media(alpha, n): 
    alpha_limite = 1 - alpha/2 
    z = norm.ppf(alpha_limite, loc=0, scale=1) 
    return 0.5 + z * (1 / math.sqrt(12*n)) 
def prueba_media(alpha, x): 
    mu_x = media(x) 
    li_mu = limite_inferior_media(alpha, len(x)) 
    ls_mu = limite_superior_media(alpha, len(x)) 
    if li_mu <= mu_x <= ls_mu: 
        return f"✅ El valor de mu = {mu_x:.4f} está dentro de los límites [{li_mu:.4f}, {ls_mu:.4f}]" 
    else: 
        return f"❌ El valor de mu = {mu_x:.4f} está FUERA de los límites [{li_mu:.4f}, {ls_mu:.4f}]"

# ------------------- Interfaz gráfica ------------------- 
class PruebaMediasApp(tk.Toplevel): 
    def __init__(self, master, valores_r): 
        super().__init__(master) 
        self.title("Prueba de Medias") 
        self.geometry("420x220") 
        self.valores_r = valores_r 
        # Etiqueta título 
        tk.Label(self, text="Prueba de Medias", font=("Arial", 14, "bold")).pack(pady=10) 
        # Combobox para seleccionar confianza 
        frame_conf = tk.Frame(self) 
        frame_conf.pack(pady=10) 
        tk.Label(frame_conf, text="Nivel de confianza:").grid(row=0, column=0, padx=5) 
        self.combo_conf = ttk.Combobox(frame_conf, values=["90%", "95%", "99%"], state="readonly", width=10) 
        self.combo_conf.grid(row=0, column=1, padx=5) 
        self.combo_conf.current(1) # por defecto 95% 
        # Botón ejecutar prueba 
        tk.Button(self, text="Ejecutar Prueba", width=18, command=self.ejecutar_prueba).pack(pady=15) 
        # Botón cerrar 
        tk.Button(self, text="Cerrar", width=18, command=self.destroy).pack(pady=5) 

    def ejecutar_prueba(self): 
        if not self.valores_r: 
            messagebox.showwarning("Atención", "No hay valores para analizar.") 
            return 
        # Convertir confianza a alpha 
        conf_str = self.combo_conf.get() 
        confianza = int(conf_str.replace("%", "")) 
        alpha = 1 - (confianza / 100) 
        resultado = prueba_media(alpha, self.valores_r) 
        messagebox.showinfo("Resultado", resultado)
