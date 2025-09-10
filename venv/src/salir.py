import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import os
import sys

def extraer_mensaje_oculto(imagen_path):
    """Extrae el mensaje oculto de los LSB de la imagen."""
    img = Image.open(imagen_path).convert("RGB")
    pixels = list(img.getdata())
    bits = []

    for pixel in pixels:
        for channel in pixel[:3]:
            bits.append(channel & 1)

    mensaje = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        valor = 0
        for bit in byte:
            valor = (valor << 1) | bit
        if valor == 0:  # fin del mensaje
            break
        mensaje += chr(valor)
    return mensaje

class SalirApp(tk.Toplevel):
    """Ventana de agradecimiento con mensaje oculto."""
    def __init__(self, parent=None, root=None):
        super().__init__(parent)
        self.root = root  # Referencia a la ventana principal
        self.title("Gracias por usar la aplicación")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        # Centrar ventana
        ancho, alto =800, 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Imagen
        imagen_path = os.path.join(os.path.dirname(__file__), "gracias.png")
        if not os.path.exists(imagen_path):
            messagebox.showerror("Error", f"No se encontró la imagen: {imagen_path}")
            self.destroy()
            return

        img = Image.open(imagen_path)
        img.thumbnail((400, 300))
        self.photo = ImageTk.PhotoImage(img)
        tk.Label(self, image=self.photo, bg="#f0f0f0").pack(pady=15)

        # Mensaje oculto
        mensaje_oculto = extraer_mensaje_oculto(imagen_path)
        print(f"Mensaje oculto extraído: {mensaje_oculto}")  # Consola

        frame_text = tk.Frame(self, bg="#f0f0f0")
        frame_text.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(frame_text, text="💡 Mensaje oculto:", font=("Arial", 12, "bold"),
                 bg="#f0f0f0").pack(anchor="w")

        text_area = scrolledtext.ScrolledText(frame_text, wrap=tk.WORD, height=6, font=("Arial", 11))
        text_area.pack(fill="both", expand=True)
        text_area.insert(tk.END, mensaje_oculto)
        text_area.configure(state="disabled")

        # Botón Cerrar todo
        tk.Button(self, text="Cerrar", width=18, height=2,
                  bg="#d9534f", fg="white", font=("Arial", 12, "bold"),
                  command=self.cerrar_todo).pack(pady=15)

    def cerrar_todo(self):
        """Cierra toda la aplicación, incluyendo root y esta ventana."""
        try:
            if self.root:
                self.root.quit()      # termina el mainloop
                self.root.destroy()   # cierra la ventana principal
            self.destroy()           # cierra SalirApp
        except:
            # Aseguramos que Python termine completamente
            sys.exit(0)
