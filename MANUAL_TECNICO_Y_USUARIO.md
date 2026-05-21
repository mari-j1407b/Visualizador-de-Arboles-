# Manual Técnico y de Usuario: Visualizador de Árboles

Este documento contiene la explicación técnica completa del funcionamiento del sistema, la arquitectura implementada y la guía de usuario para interactuar con la aplicación. 

---

## 1. Guía de Usuario (Cómo usar el sistema)

Para iniciar el programa, asegúrate de estar en el directorio del proyecto y ejecuta el siguiente comando en la terminal:
```bash
python main.py
```

### Interfaz Principal
Al abrir la aplicación, verás un gran lienzo en blanco (el Canvas) y un panel superior de controles:
- **Tipo de Árbol:** Selecciona si quieres trabajar con un árbol de Búsqueda Binaria Normal (BST) o un árbol balanceado (AVL). ¡Cuidado! Si cambias de tipo de árbol, el árbol actual se reiniciará.
- **Entrada de Valor:** Un campo de texto donde debes ingresar números enteros (ej. 15, 20, 5).
- **Botones de Operación:**
  - **Insertar:** Añade el número ingresado al árbol y muestra la animación de descenso hasta encontrar su lugar.
  - **Buscar:** Recorre el árbol paso a paso buscando el valor. Al finalizar, te avisará si lo encontró o no.
  - **Eliminar:** Busca el nodo y lo borra aplicando las reglas correspondientes (y rebalanceando si es AVL).
  - **Guardar / Cargar:** Te permite guardar el estado actual del árbol en un archivo `arbol_guardado.json` para no perder el progreso.
- **Botones de Recorridos:** Anima el recorrido completo por todos los nodos del árbol en orden **Preorden**, **Inorden** o **Postorden**.

### Código de Colores (Animaciones)
Mientras el programa ejecuta una operación, notarás que los nodos cambian de color para que puedas entender qué está decidiendo el algoritmo:
- 🟡 **Amarillo:** El nodo está siendo "visitado" en este instante. El algoritmo está comprobando si es mayor, menor o igual.
- 🟢 **Verde:** ¡Éxito! Aquí se acaba de crear el nodo nuevo, o se acaba de encontrar el número que estabas buscando.
- 🔴 **Rojo:** Precaución. Este nodo fue marcado para ser eliminado del sistema en el siguiente paso.
- 🟠 **Naranja:** Exclusivo del AVL. Este nodo ha causado un desbalance en el árbol y está a punto de sufrir una rotación (Simple o Doble).

---

## 2. Arquitectura y Explicación Técnica (Para Defensa del Proyecto)

El sistema ha sido construido respetando estrictamente los principios de Programación Orientada a Objetos y **Recursividad**. Está dividido en cuatro pilares fundamentales:

### A. Las Estructuras de Datos (Nodos y Árboles)
- **`nodo.py`**: Define la clase `Nodo`. Un objeto simple que almacena el valor numérico, la altura (para AVL), y punteros (referencias) a un nodo hijo izquierdo y un nodo hijo derecho.
- **`arbol_bst.py`**: Contiene la clase `ArbolBST` que define las operaciones de un Árbol Binario de Búsqueda. La regla de oro aquí es: *Todo valor menor va a la rama izquierda, y todo valor mayor va a la derecha*.
- **`arbol_avl.py`**: Contiene la clase `ArbolAVL` que **hereda** de `ArbolBST`. Su característica especial es la capacidad de auto-balancearse para mantener una eficiencia óptima. Sobrescribe la inserción y la eliminación para calcular el **Factor de Balance** después de cada cambio y ejecutar **rotaciones** si el árbol se inclina demasiado hacia un lado.

### B. El Motor de Animaciones Asíncronas (La magia del Generador)
El desafío más grande del proyecto fue: *"¿Cómo animar la búsqueda o los recorridos sin bloquear la interfaz de usuario, manteniendo la obligación de usar recursividad?"*

La solución implementada utiliza **Generadores de Python** (la instrucción `yield`).
En lugar de que una función recursiva corra de principio a fin de un solo golpe, se pausa en cada paso clave:
```python
yield nodo_actual, "visitando"
# ... continua recursividad
```
Esto le "lanza" temporalmente el control de nuevo a `main.py`. La interfaz entonces puede:
1. Recibir el nodo.
2. Pintarlo de amarillo (o del color que corresponda).
3. Pedirle a Tkinter (`self.ventana.after(600, ...)`) que espere 600 milisegundos.
4. Finalizada la pausa, retomar la recursividad exactamente donde se quedó.

Esto permite visualizar los recorridos paso a paso sin violar la regla de utilizar soluciones recursivas.

### C. Renderizado Visual (`visualizador.py`)
Utiliza la librería nativa `tkinter` y su componente `Canvas`.
- Para dibujar el árbol de manera proporcional, se usa también una función recursiva. Se dibuja la raíz, y luego se dibuja el hijo izquierdo con una coordenada `x` menor (hacia la izquierda), y el derecho con una coordenada `x` mayor.
- Para cambiar los colores durante las animaciones **sin redibujar todo**, se utilizan las **Etiquetas (Tags)** de Tkinter. Al dibujar cada círculo, se le asigna un tag único como `"nodo_15"`. Así, el animador solo le pide al Canvas que cambie el color del objeto que coincida con esa etiqueta.

### D. Persistencia (`persistencia.py`)
Permite guardar y cargar el árbol usando el formato JSON.
- **Guardar:** Serializa el objeto. Empieza por la raíz y recursivamente crea un diccionario anidado convirtiendo las referencias de los nodos a texto estructurado.
- **Cargar:** Deserializa el JSON. Lee el archivo y comienza a instanciar nuevos objetos `Nodo`, asignándoles recursivamente sus hijos izquierdo y derecho reconstruyendo la jerarquía en la memoria RAM antes de inyectarla al visualizador.
