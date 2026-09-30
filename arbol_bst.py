"""
Árbol Binario de Búsqueda (ABB) de palabras a partir de una oración.

El programa:
  1. Solicita al usuario una línea de texto.
  2. Divide la oración en palabras.
  3. Inserta las palabras en un árbol binario de búsqueda.
  4. Inserción: menor -> izquierda, mayor -> derecha,
     duplicado -> se incrementa un contador de frecuencia en el nodo existente.
  5. Muestra los recorridos inorden, preorden y postorden.
  6. Calcula el total de nodos, los nodos internos y la palabra con máximo valor alfabético.
  7. Muestra la información almacenada en las hojas y en los nodos internos.

Decisiones de diseño (ver README.md):
  - Las palabras se normalizan a minúsculas y se eliminan signos de puntuación.
  - El orden alfabético ignora acentos y coloca la "ñ" después de la "n"
    (orden del alfabeto español). Si dos palabras sólo difieren en acentos
    ("papa" / "papá"), se desempata por su forma original y son palabras distintas.
  - Duplicados: NO se crea un nodo nuevo; se incrementa la frecuencia del nodo.
  - Nodo interno: nodo con al menos un hijo (incluye la raíz si tiene hijos).
    Hoja: nodo sin hijos.
"""

import re
import sys
import unicodedata


# ----------------------------------------------------------------------
# Utilidades de texto
# ----------------------------------------------------------------------

def dividir_en_palabras(texto):
    """Convierte el texto a minúsculas y devuelve la lista de palabras.

    Se consideran palabras las secuencias de letras (incluye acentos y ñ)
    y dígitos; la puntuación se descarta.
    """
    return re.findall(r"[^\W_]+", texto.lower())


def clave_alfabetica(palabra):
    """Clave de comparación alfabética en español.

    - Quita los acentos (á -> a, ü -> u) para comparar la letra base.
    - La ñ se transforma en "n~"; como "~" es mayor que cualquier letra,
      la ñ queda después de toda la "n" y antes de la "o".
    - Se devuelve una tupla (forma_normalizada, palabra) para que
      "papa" y "papá" no se consideren iguales.
    """
    temp = palabra.replace("ñ", "n~")
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFD", temp)
        if unicodedata.category(c) != "Mn"
    )
    return (sin_acentos, palabra)


# ----------------------------------------------------------------------
# Estructura del árbol
# ----------------------------------------------------------------------

class Nodo:
    def __init__(self, palabra):
        self.palabra = palabra
        self.frecuencia = 1
        self.izquierdo = None
        self.derecho = None

    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None

    def __repr__(self):
        return f"{self.palabra}({self.frecuencia})"


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    # --- Inserción -----------------------------------------------------
    def insertar(self, palabra):
        """Inserta una palabra de forma iterativa.

        Devuelve True si se creó un nodo nuevo, False si era duplicada.
        """
        if self.raiz is None:
            self.raiz = Nodo(palabra)
            return True

        clave = clave_alfabetica(palabra)
        actual = self.raiz
        while True:
            clave_actual = clave_alfabetica(actual.palabra)
            if clave < clave_actual:
                if actual.izquierdo is None:
                    actual.izquierdo = Nodo(palabra)
                    return True
                actual = actual.izquierdo
            elif clave > clave_actual:
                if actual.derecho is None:
                    actual.derecho = Nodo(palabra)
                    return True
                actual = actual.derecho
            else:
                actual.frecuencia += 1
                return False

    def insertar_oracion(self, texto):
        for palabra in dividir_en_palabras(texto):
            self.insertar(palabra)

    def buscar(self, palabra):
        clave = clave_alfabetica(palabra.lower())
        actual = self.raiz
        while actual is not None:
            clave_actual = clave_alfabetica(actual.palabra)
            if clave == clave_actual:
                return actual
            actual = actual.izquierdo if clave < clave_actual else actual.derecho
        return None

    # --- Recorridos ----------------------------------------------------
    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo is not None:
            self._inorden(nodo.izquierdo, resultado)
            resultado.append(nodo.palabra)
            self._inorden(nodo.derecho, resultado)

    def preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.palabra)
            self._preorden(nodo.izquierdo, resultado)
            self._preorden(nodo.derecho, resultado)

    def postorden(self):
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado

    def _postorden(self, nodo, resultado):
        if nodo is not None:
            self._postorden(nodo.izquierdo, resultado)
            self._postorden(nodo.derecho, resultado)
            resultado.append(nodo.palabra)

    # --- Cálculos ------------------------------------------------------
    def total_nodos(self):
        return self._contar(self.raiz)

    def _contar(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar(nodo.izquierdo) + self._contar(nodo.derecho)

    def hojas(self):
        """Lista de nodos sin hijos, en orden alfabético."""
        return [n for n in self._nodos_inorden() if n.es_hoja()]

    def nodos_internos(self):
        """Lista de nodos con al menos un hijo, en orden alfabético."""
        return [n for n in self._nodos_inorden() if not n.es_hoja()]

    def total_nodos_internos(self):
        return len(self.nodos_internos())

    def palabra_maxima(self):
        """La palabra alfabéticamente mayor es el nodo más a la derecha."""
        if self.raiz is None:
            return None
        actual = self.raiz
        while actual.derecho is not None:
            actual = actual.derecho
        return actual.palabra

    def altura(self):
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def _nodos_inorden(self):
        nodos = []

        def visitar(nodo):
            if nodo is not None:
                visitar(nodo.izquierdo)
                nodos.append(nodo)
                visitar(nodo.derecho)

        visitar(self.raiz)
        return nodos

    # --- Representación ------------------------------------------------
    def diagrama(self):
        """Devuelve una representación en texto del árbol.

        (I) indica hijo izquierdo y (D) hijo derecho.
        """
        if self.raiz is None:
            return "(árbol vacío)"
        lineas = [f"{self.raiz.palabra} [{self.raiz.frecuencia}]"]
        self._diagrama(self.raiz, "", lineas)
        return "\n".join(lineas)

    def _diagrama(self, nodo, prefijo, lineas):
        hijos = [("I", nodo.izquierdo), ("D", nodo.derecho)]
        hijos = [(lado, h) for lado, h in hijos if h is not None]
        for i, (lado, hijo) in enumerate(hijos):
            ultimo = i == len(hijos) - 1
            conector = "└── " if ultimo else "├── "
            lineas.append(f"{prefijo}{conector}({lado}) {hijo.palabra} [{hijo.frecuencia}]")
            self._diagrama(hijo, prefijo + ("    " if ultimo else "│   "), lineas)


# ----------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------

def formatear_nodos(nodos):
    if not nodos:
        return "(ninguno)"
    return ", ".join(f"{n.palabra} (frecuencia: {n.frecuencia})" for n in nodos)


def generar_reporte(texto):
    arbol = ArbolBinarioBusqueda()
    palabras = dividir_en_palabras(texto)
    for palabra in palabras:
        arbol.insertar(palabra)

    lineas = []
    lineas.append(f"Palabras leídas ({len(palabras)}): {palabras}")
    if arbol.raiz is None:
        lineas.append("No se encontraron palabras. El árbol está vacío.")
        return "\n".join(lineas)

    lineas.append("")
    lineas.append("=== Diagrama del árbol ===  (I = izquierdo, D = derecho, [n] = frecuencia)")
    lineas.append(arbol.diagrama())
    lineas.append("")
    lineas.append("=== Recorridos ===")
    lineas.append("Inorden   : " + " ".join(arbol.inorden()))
    lineas.append("Preorden  : " + " ".join(arbol.preorden()))
    lineas.append("Postorden : " + " ".join(arbol.postorden()))
    lineas.append("")
    lineas.append("=== Cálculos ===")
    lineas.append(f"Número total de nodos       : {arbol.total_nodos()}")
    lineas.append(f"Número de nodos internos    : {arbol.total_nodos_internos()}")
    lineas.append(f"Número de hojas             : {len(arbol.hojas())}")
    lineas.append(f"Altura del árbol            : {arbol.altura()}")
    lineas.append(f"Palabra con máximo valor alfabético: {arbol.palabra_maxima()}")
    lineas.append("")
    lineas.append("=== Información almacenada ===")
    lineas.append("Hojas           : " + formatear_nodos(arbol.hojas()))
    lineas.append("Nodos internos  : " + formatear_nodos(arbol.nodos_internos()))
    return "\n".join(lineas)


def main():
    if len(sys.argv) > 1:
        texto = " ".join(sys.argv[1:])
    else:
        texto = input("Escribe una oración: ")
    print(generar_reporte(texto))


if __name__ == "__main__":
    main()
