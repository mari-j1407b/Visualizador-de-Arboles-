from nodo import Nodo

class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = yield from self._insertar_rec(self.raiz, valor)
        yield None, "fin_insercion"

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
        return nodo

    def buscar(self, valor):
        res = yield from self._buscar_rec(self.raiz, valor)
        yield res, "fin_busqueda"
        return res

    def _buscar_rec(self, nodo, valor):
        if nodo is None:
            yield None, "no_encontrado"
            return None
            
        yield nodo, "visitando"
        if nodo.valor == valor:
            yield nodo, "encontrado"
            return nodo
            
        if valor < nodo.valor:
            return (yield from self._buscar_rec(nodo.izquierdo, valor))
        return (yield from self._buscar_rec(nodo.derecho, valor))

    def eliminar(self, valor):
        self.raiz = yield from self._eliminar_rec(self.raiz, valor)
        yield None, "fin_eliminacion"

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
            yield nodo, "reemplazando_con_sucesor"
            nodo.derecho = yield from self._eliminar_rec(nodo.derecho, sucesor.valor)
        return nodo

    def _min_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierdo:
            actual = actual.izquierdo
        return actual

    def recorrido_preorden(self):
        resultado = []
        yield from self._preorden_rec(self.raiz, resultado)
        yield None, f"fin_preorden:{resultado}"

    def _preorden_rec(self, nodo, resultado):
        if nodo:
            yield nodo, "visitando"
            resultado.append(nodo.valor)
            yield from self._preorden_rec(nodo.izquierdo, resultado)
            yield from self._preorden_rec(nodo.derecho, resultado)

    def recorrido_inorden(self):
        resultado = []
        yield from self._inorden_rec(self.raiz, resultado)
        yield None, f"fin_inorden:{resultado}"

    def _inorden_rec(self, nodo, resultado):
        if nodo:
            yield from self._inorden_rec(nodo.izquierdo, resultado)
            yield nodo, "visitando"
            resultado.append(nodo.valor)
            yield from self._inorden_rec(nodo.derecho, resultado)

    def recorrido_postorden(self):
        resultado = []
        yield from self._postorden_rec(self.raiz, resultado)
        yield None, f"fin_postorden:{resultado}"

    def _postorden_rec(self, nodo, resultado):
        if nodo:
            yield from self._postorden_rec(nodo.izquierdo, resultado)
            yield from self._postorden_rec(nodo.derecho, resultado)
            yield nodo, "visitando"
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