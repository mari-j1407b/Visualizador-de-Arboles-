import tkinter as tk

class VisualizadorArbol:
    def __init__(self, canvas, ancho=800, alto=500):
        self.canvas = canvas
        self.ancho = ancho
        self.alto = alto
        self.radio_nodo = 20

    def dibujar(self, nodo, x, y, dx):
        if nodo is None:
            return
        # Líneas a hijos
        if nodo.izquierdo:
            self.canvas.create_line(x, y, x - dx, y + 60, width=2)
            self.dibujar(nodo.izquierdo, x - dx, y + 60, dx // 2)
        if nodo.derecho:
            self.canvas.create_line(x, y, x + dx, y + 60, width=2)
            self.dibujar(nodo.derecho, x + dx, y + 60, dx // 2)
        # Nodo
        self.canvas.create_oval(x - self.radio_nodo, y - self.radio_nodo,
                                x + self.radio_nodo, y + self.radio_nodo,
                                fill="lightblue", tags=(f"nodo_{nodo.valor}", "nodo"))
        self.canvas.create_text(x, y, text=str(nodo.valor), tags=(f"texto_{nodo.valor}", "texto"))

    def resaltar_nodo(self, valor, color="yellow"):
        self.canvas.itemconfig(f"nodo_{valor}", fill=color)

    def restaurar_colores(self):
        self.canvas.itemconfig("nodo", fill="lightblue")