import json
from nodo import Nodo

def guardar_arbol(nodo, archivo):
    def serializar(n):
        if n is None:
            return None
        return {
            "valor": n.valor,
            "izquierdo": serializar(n.izquierdo),
            "derecho": serializar(n.derecho)
        }
    with open(archivo, "w") as f:
        json.dump(serializar(nodo), f, indent=4)

def cargar_arbol(archivo, clase_arbol):
    with open(archivo, "r") as f:
        data = json.load(f)
    def deserializar(d):
        if d is None:
            return None
        nodo = Nodo(d["valor"])
        nodo.izquierdo = deserializar(d["izquierdo"])
        nodo.derecho = deserializar(d["derecho"])
        return nodo
    arbol = clase_arbol()
    arbol.raiz = deserializar(data)
    return arbol