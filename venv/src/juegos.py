#juego de vida
#juego.py
import tkinter as tk
import numpy as np
import time
import threading

CELL_SIZE = 30

class GameOfLife2D:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)

    def _expand_if_needed(self):
        expand_top = np.any(self.grid[0, :] == 1)
        expand_bottom = np.any(self.grid[-1, :] == 1)
        expand_left = np.any(self.grid[:, 0] == 1)
        expand_right = np.any(self.grid[:, -1] == 1)

        if expand_top:
            self.grid = np.vstack([np.zeros((1, self.cols), dtype=int), self.grid])
            self.rows += 1
        if expand_bottom:
            self.grid = np.vstack([self.grid, np.zeros((1, self.cols), dtype=int)])
            self.rows += 1
        if expand_left:
            self.grid = np.hstack([np.zeros((self.rows, 1), dtype=int), self.grid])
            self.cols += 1
        if expand_right:
            self.grid = np.hstack([self.grid, np.zeros((self.rows, 1), dtype=int)])
            self.cols += 1

    def step(self):
        self._expand_if_needed()
        new = np.zeros_like(self.grid)
        for r in range(self.rows):
            for c in range(self.cols):
                total = np.sum(self.grid[max(0, r-1):r+2, max(0, c-1):c+2]) - self.grid[r, c]
                if self.grid[r, c] == 1:
                    if total in (2, 3):
                        new[r, c] = 1
                else:
                    if total == 3:
                        new[r, c] = 1
        self.grid = new


class GameOfLifeApp:
    def __init__(self, root, main_window=None):
        self.root = root
        self.main_window = main_window
        self.root.title("Juego de la Vida 2D (Expansión dinámica)")
        
        # Configurar el evento de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.volver_atras)

        # Frame superior para el botón Volver
        top_frame = tk.Frame(root, bg='white')
        top_frame.pack(fill='x', padx=10, pady=5)
        
        self.volver_btn = tk.Button(top_frame, text="⬅ Volver Atrás", 
                                     command=self.volver_atras,
                                     font=("Arial", 10, "bold"),
                                     bg="#607D8B", fg="white")
        self.volver_btn.pack(side="left")

        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(fill='both', expand=True)

        self.sim = GameOfLife2D()
        self.running = False

        self.canvas.bind("<Button-1>", self._on_click)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.step_btn = tk.Button(btn_frame, text="Paso", command=self._step,
                                  font=("Arial", 10), width=10)
        self.step_btn.pack(side="left", padx=5)

        self.run_btn = tk.Button(btn_frame, text="Ejecutar", command=self._toggle_run,
                                font=("Arial", 10), width=10, bg="#4CAF50", fg="white")
        self.run_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Reiniciar", command=self._reset,
                                   font=("Arial", 10), width=10, bg="#FF5722", fg="white")
        self.reset_btn.pack(side="left", padx=5)

        self._draw_grid()

    def _draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.sim.rows):
            for c in range(self.sim.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                fill = "black" if self.sim.grid[r, c] else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray")

        # Redimensionar canvas automáticamente
        self.canvas.config(width=self.sim.cols * CELL_SIZE, height=self.sim.rows * CELL_SIZE)

    def _on_click(self, event):
        if self.running:
            return
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < self.sim.rows and 0 <= col < self.sim.cols:
            self.sim.grid[row, col] = 1 - self.sim.grid[row, col]
            self._draw_grid()

    def _step(self):
        self.sim.step()
        self._draw_grid()

    def _toggle_run(self):
        self.running = not self.running
        self.run_btn.config(text="Parar" if self.running else "Ejecutar",
                           bg="#F44336" if self.running else "#4CAF50")
        if self.running:
            self._run_loop()

    def _run_loop(self):
        def loop():
            while self.running:
                time.sleep(0.4)
                self.root.after(0, self._step)
        threading.Thread(target=loop, daemon=True).start()

    def _reset(self):
        self.running = False
        self.run_btn.config(text="Ejecutar", bg="#4CAF50")
        self.sim = GameOfLife2D()
        self._draw_grid()

    def volver_atras(self):
        """Vuelve a la ventana principal"""
        self.running = False
        if self.main_window:
            self.main_window.deiconify()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = GameOfLifeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()