from arbol_bst import ArbolBST

class ArbolAVL(ArbolBST):
    def _obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo):
        if nodo:
            nodo.altura = 1 + max(self._obtener_altura(nodo.izquierdo), self._obtener_altura(nodo.derecho))

    def _factor_balance(self, nodo):
        return self._obtener_altura(nodo.izquierdo) - self._obtener_altura(nodo.derecho)

    def _rotacion_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho
        x.derecho = y
        y.izquierdo = T2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotacion_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo
        y.izquierdo = x
        x.derecho = T2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _insertar_rec(self, nodo, valor):
        if nodo is None:
            return nodo(valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_rec(nodo.derecho, valor)
        else:
            return nodo

        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)

        # Rotaciones
        if balance > 1 and valor < nodo.izquierdo.valor:
            return self._rotacion_derecha(nodo)
        if balance < -1 and valor > nodo.derecho.valor:
            return self._rotacion_izquierda(nodo)
        if balance > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
        if balance < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)
        return nodo