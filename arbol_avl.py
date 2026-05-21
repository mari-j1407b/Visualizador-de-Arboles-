from arbol_bst import ArbolBST
from nodo import Nodo

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
            nuevo = Nodo(valor)
            yield nuevo, "insertado"
            return nuevo
            
        yield nodo, "visitando"
        if valor < nodo.valor:
            nodo.izquierdo = yield from self._insertar_rec(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = yield from self._insertar_rec(nodo.derecho, valor)
        else:
            return nodo

        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)

        # Rotaciones
        if balance > 1 and valor < nodo.izquierdo.valor:
            yield nodo, "rotacion_derecha"
            return self._rotacion_derecha(nodo)
        if balance < -1 and valor > nodo.derecho.valor:
            yield nodo, "rotacion_izquierda"
            return self._rotacion_izquierda(nodo)
        if balance > 1 and valor > nodo.izquierdo.valor:
            yield nodo, "rotacion_doble_izq_der"
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
        if balance < -1 and valor < nodo.derecho.valor:
            yield nodo, "rotacion_doble_der_izq"
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)
        return nodo

    def _eliminar_rec(self, nodo, valor):
        if nodo is None:
            return None
            
        yield nodo, "visitando"
        if valor < nodo.valor:
            nodo.izquierdo = yield from self._eliminar_rec(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = yield from self._eliminar_rec(nodo.derecho, valor)
        else:
            yield nodo, "eliminando"
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            
            sucesor = self._min_valor_nodo(nodo.derecho)
            nodo.valor = sucesor.valor
            yield nodo, "reemplazando_con_sucesor"
            nodo.derecho = yield from self._eliminar_rec(nodo.derecho, sucesor.valor)

        if nodo is None:
            return None

        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)

        # Rebalanceo post-eliminación
        if balance > 1 and self._factor_balance(nodo.izquierdo) >= 0:
            yield nodo, "rotacion_derecha"
            return self._rotacion_derecha(nodo)
        if balance > 1 and self._factor_balance(nodo.izquierdo) < 0:
            yield nodo, "rotacion_doble_izq_der"
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
        if balance < -1 and self._factor_balance(nodo.derecho) <= 0:
            yield nodo, "rotacion_izquierda"
            return self._rotacion_izquierda(nodo)
        if balance < -1 and self._factor_balance(nodo.derecho) > 0:
            yield nodo, "rotacion_doble_der_izq"
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)

        return nodo