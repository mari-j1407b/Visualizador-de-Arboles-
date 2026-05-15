from nodo import Nodo

class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar_rec(self.raiz, valor)

    def _insertar_rec(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_rec(nodo.derecho, valor)
        return nodo

    def buscar(self, valor):
        return self._buscar_rec(self.raiz, valor)

    def _buscar_rec(self, nodo, valor):
        if nodo is None or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self._buscar_rec(nodo.izquierdo, valor)
        return self._buscar_rec(nodo.derecho, valor)

    def eliminar(self, valor):
        self.raiz = self._eliminar_rec(self.raiz, valor)

    def _eliminar_rec(self, nodo, valor):
        if nodo is None:
            return None
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_rec(nodo.derecho, valor)
        else:
            # Caso 1: sin hijos
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            # Caso 2: un hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: dos hijos
            sucesor = self._min_valor_nodo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor.valor)
        return nodo

    def _min_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierdo:
            actual = actual.izquierdo
        return actual

    def recorrido_preorden(self):
        resultado = []
        self._preorden_rec(self.raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.valor)
            self._preorden_rec(nodo.izquierdo, resultado)
            self._preorden_rec(nodo.derecho, resultado)

    def recorrido_inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_rec(nodo.derecho, resultado)

    def recorrido_postorden(self):
        resultado = []
        self._postorden_rec(self.raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo, resultado):
        if nodo:
            self._postorden_rec(nodo.izquierdo, resultado)
            self._postorden_rec(nodo.derecho, resultado)
            resultado.append(nodo.valor)

    def altura(self):
        return self._altura_rec(self.raiz)

    def _altura_rec(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura_rec(nodo.izquierdo), self._altura_rec(nodo.derecho))

    def contar_nodos(self):
        return self._contar_rec(self.raiz)

    def _contar_rec(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_rec(nodo.izquierdo) + self._contar_rec(nodo.derecho)