import tkinter as tk
from tkinter import ttk, messagebox, filedialog  # <--- Agregamos filedialog aquí
from arbol_bst import ArbolBST
from arbol_avl import ArbolAVL
from visualizador import VisualizadorArbol
from persistencia import guardar_arbol, cargar_arbol

class App:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Visualizador de Árboles")
        self.ventana.geometry("1000x650")
        
        # Selección de tipo de árbol
        self.tipo_arbol = tk.StringVar(value="BST")
        
        # Frame superior para controles
        frame_superior = tk.Frame(self.ventana)
        frame_superior.pack(pady=10)
        
        tk.Label(frame_superior, text="Tipo de árbol:").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame_superior, text="BST", variable=self.tipo_arbol, value="BST", command=self.cambiar_arbol).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame_superior, text="AVL", variable=self.tipo_arbol, value="AVL", command=self.cambiar_arbol).pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_superior, text="Valor:").pack(side=tk.LEFT, padx=5)
        self.entry_valor = tk.Entry(frame_superior, width=10)
        self.entry_valor.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_superior, text="Insertar", command=self.insertar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_superior, text="Buscar", command=self.buscar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_superior, text="Eliminar", command=self.eliminar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_superior, text="Guardar", command=self.guardar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_superior, text="Cargar", command=self.cargar).pack(side=tk.LEFT, padx=5)
        
        # Frame para recorridos
        frame_recorridos = tk.Frame(self.ventana)
        frame_recorridos.pack(pady=5)
        
        tk.Button(frame_recorridos, text="Preorden", command=self.mostrar_preorden).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_recorridos, text="Inorden", command=self.mostrar_inorden).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_recorridos, text="Postorden", command=self.mostrar_postorden).pack(side=tk.LEFT, padx=5)
        
        # Frame para información
        frame_info = tk.Frame(self.ventana)
        frame_info.pack(pady=5)
        
        self.label_info = tk.Label(frame_info, text="Altura: 0 | Nodos: 0 | Raíz: None", font=("Arial", 12))
        self.label_info.pack()
        
        # Canvas para dibujar el árbol
        self.canvas = tk.Canvas(self.ventana, width=950, height=450, bg="white")
        self.canvas.pack(pady=10)
        
        self.visualizador = VisualizadorArbol(self.canvas, ancho=950, alto=450)
        
        # Inicializar árbol BST por defecto
        self.arbol = ArbolBST()
        self.actualizar_vista()
        
        self.ventana.mainloop()
    
    def cambiar_arbol(self):
        """Cambia entre BST y AVL"""
        if self.tipo_arbol.get() == "BST":
            self.arbol = ArbolBST()
        else:
            self.arbol = ArbolAVL()
        messagebox.showinfo("Cambio de árbol", f"Ahora trabajando con árbol {self.tipo_arbol.get()}")
        self.actualizar_vista()
    
    def ejecutar_paso_animacion(self, generador, titulo):
        try:
            resultado = next(generador)
            if resultado is not None and isinstance(resultado, tuple):
                val, accion = resultado
                
                if "fin_" not in accion:
                    self.visualizador.restaurar_colores()
                
                if val and hasattr(val, 'valor'):
                    color = "yellow"
                    if "rotacion" in accion: color = "orange"
                    elif "eliminando" in accion: color = "red"
                    elif "insertado" in accion: color = "green"
                    elif accion == "encontrado": color = "green"
                    
                    self.visualizador.resaltar_nodo(val.valor, color)
                
                if accion.startswith("fin_"):
                    self.actualizar_vista()
                    if "busqueda" in accion:
                        if val:
                            messagebox.showinfo(titulo, f"Valor encontrado en el árbol")
                        else:
                            messagebox.showinfo(titulo, f"Valor NO encontrado")
                    elif "orden:" in accion:
                        messagebox.showinfo(titulo, accion.split(":", 1)[1])
                    return
            
            self.ventana.after(600, self.ejecutar_paso_animacion, generador, titulo)
        except StopIteration:
            self.actualizar_vista()

    def insertar(self):
        try:
            valor = int(self.entry_valor.get())
            generador = self.arbol.insertar(valor)
            self.entry_valor.delete(0, tk.END)
            self.ejecutar_paso_animacion(generador, "Inserción")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero válido")
    
    def buscar(self):
        try:
            valor = int(self.entry_valor.get())
            generador = self.arbol.buscar(valor)
            self.ejecutar_paso_animacion(generador, "Búsqueda")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero válido")
    
    def eliminar(self):
        try:
            valor = int(self.entry_valor.get())
            generador = self.arbol.eliminar(valor)
            self.entry_valor.delete(0, tk.END)
            self.ejecutar_paso_animacion(generador, "Eliminación")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero válido")
    
    def mostrar_preorden(self):
        generador = self.arbol.recorrido_preorden()
        self.ejecutar_paso_animacion(generador, "Recorrido Preorden")
    
    def mostrar_inorden(self):
        generador = self.arbol.recorrido_inorden()
        self.ejecutar_paso_animacion(generador, "Recorrido Inorden")
    
    def mostrar_postorden(self):
        generador = self.arbol.recorrido_postorden()
        self.ejecutar_paso_animacion(generador, "Recorrido Postorden")
    
    def guardar(self):
            # Abre el explorador de archivos para elegir dónde y con qué nombre guardar
            ruta_archivo = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
                title="Guardar Árbol"
            )
            
            # Si el usuario no cancela el cuadro de diálogo
            if ruta_archivo:
                guardar_arbol(self.arbol.raiz, ruta_archivo)
                # Extraemos solo el nombre del archivo para mostrarlo en el mensaje
                import os
                nombre_archivo = os.path.basename(ruta_archivo)
                messagebox.showinfo("Guardar", f"Árbol guardado exitosamente como '{nombre_archivo}'")

    def cargar(self):
        from nodo import Nodo  # Necesario para deserializar
        
        # Abre el explorador de archivos para seleccionar qué árbol abrir
        ruta_archivo = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Seleccionar Árbol para Cargar"
        )
        
        # Si el usuario selecciona un archivo
        if ruta_archivo:
            # Determinamos el tipo de árbol correcto según la selección actual de la GUI
            tipo_actual = ArbolBST if self.tipo_arbol.get() == "BST" else ArbolAVL
            
            arbol_cargado = cargar_arbol(ruta_archivo, tipo_actual)
            if arbol_cargado:
                self.arbol = arbol_cargado
                self.actualizar_vista()
                messagebox.showinfo("Cargar", "Árbol cargado correctamente")
    
    def actualizar_vista(self):
        """Actualiza el canvas y la información del árbol"""
        self.canvas.delete("all")
        if self.arbol.raiz:
            self.visualizador.dibujar(self.arbol.raiz, self.visualizador.ancho // 2, 50, 200)
        
        altura = self.arbol.altura()
        nodos = self.arbol.contar_nodos()
        raiz = self.arbol.raiz.valor if self.arbol.raiz else "None"
        self.label_info.config(text=f"Altura: {altura} | Nodos: {nodos} | Raíz: {raiz}")

if __name__ == "__main__":
    app = App()