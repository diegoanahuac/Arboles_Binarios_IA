"""Casos de prueba del árbol binario de búsqueda.

Ejecutar con:  python3 -m unittest -v test_arbol_bst.py
"""

import unittest

from arbol_bst import ArbolBinarioBusqueda, dividir_en_palabras, generar_reporte


def construir(texto):
    arbol = ArbolBinarioBusqueda()
    arbol.insertar_oracion(texto)
    return arbol


class PruebasArbol(unittest.TestCase):

    # CP-01: oración de prueba principal
    def test_oracion_principal(self):
        arbol = construir("el perro come carne y el gato come pescado")
        self.assertEqual(arbol.inorden(),
                         ["carne", "come", "el", "gato", "perro", "pescado", "y"])
        self.assertEqual(arbol.preorden(),
                         ["el", "come", "carne", "perro", "gato", "y", "pescado"])
        self.assertEqual(arbol.postorden(),
                         ["carne", "come", "gato", "pescado", "y", "perro", "el"])
        self.assertEqual(arbol.total_nodos(), 7)
        self.assertEqual(arbol.total_nodos_internos(), 4)
        self.assertEqual(arbol.palabra_maxima(), "y")
        self.assertEqual([n.palabra for n in arbol.hojas()],
                         ["carne", "gato", "pescado"])
        self.assertEqual([n.palabra for n in arbol.nodos_internos()],
                         ["come", "el", "perro", "y"])

    # CP-02: duplicados incrementan la frecuencia y no crean nodos
    def test_duplicados(self):
        arbol = construir("el perro come carne y el gato come pescado")
        self.assertEqual(arbol.buscar("el").frecuencia, 2)
        self.assertEqual(arbol.buscar("come").frecuencia, 2)
        self.assertEqual(arbol.buscar("gato").frecuencia, 1)

    # CP-03: mayúsculas y puntuación
    def test_mayusculas_y_puntuacion(self):
        self.assertEqual(dividir_en_palabras("¡Hola, Mundo! hola."),
                         ["hola", "mundo", "hola"])
        arbol = construir("¡Hola, Mundo! hola.")
        self.assertEqual(arbol.total_nodos(), 2)
        self.assertEqual(arbol.buscar("HOLA").frecuencia, 2)

    # CP-04: acentos y ñ en orden alfabético español
    def test_acentos_y_enie(self):
        arbol = construir("oso ñandú nube árbol zorro")
        self.assertEqual(arbol.inorden(), ["árbol", "nube", "ñandú", "oso", "zorro"])
        self.assertEqual(arbol.palabra_maxima(), "zorro")

    # CP-05: palabras que sólo difieren en acento son distintas
    def test_palabras_con_y_sin_acento(self):
        arbol = construir("papá papa")
        self.assertEqual(arbol.total_nodos(), 2)
        self.assertEqual(arbol.inorden(), ["papa", "papá"])

    # CP-06: entrada vacía
    def test_entrada_vacia(self):
        arbol = construir("   ")
        self.assertEqual(arbol.total_nodos(), 0)
        self.assertEqual(arbol.total_nodos_internos(), 0)
        self.assertIsNone(arbol.palabra_maxima())
        self.assertEqual(arbol.inorden(), [])
        self.assertIn("vacío", generar_reporte("  ...  "))

    # CP-07: una sola palabra (la raíz es hoja, no nodo interno)
    def test_una_palabra(self):
        arbol = construir("hola")
        self.assertEqual(arbol.total_nodos(), 1)
        self.assertEqual(arbol.total_nodos_internos(), 0)
        self.assertEqual([n.palabra for n in arbol.hojas()], ["hola"])

    # CP-08: palabras en orden ascendente -> árbol degenerado (lista)
    def test_orden_ascendente(self):
        arbol = construir("a b c d e")
        self.assertEqual(arbol.altura(), 5)
        self.assertEqual(arbol.total_nodos_internos(), 4)
        self.assertEqual([n.palabra for n in arbol.hojas()], ["e"])
        self.assertEqual(arbol.preorden(), ["a", "b", "c", "d", "e"])

    # CP-09: todas las palabras iguales
    def test_todas_iguales(self):
        arbol = construir("sol sol sol")
        self.assertEqual(arbol.total_nodos(), 1)
        self.assertEqual(arbol.raiz.frecuencia, 3)

    # CP-10: invariante del ABB -> el inorden siempre queda ordenado
    def test_inorden_ordenado(self):
        texto = "la inteligencia artificial ayuda pero el programador verifica el código"
        arbol = construir(texto)
        palabras_unicas = set(dividir_en_palabras(texto))
        self.assertEqual(len(arbol.inorden()), len(palabras_unicas))
        self.assertEqual(sorted(arbol.inorden()), sorted(palabras_unicas))
        # hojas + internos = total
        self.assertEqual(len(arbol.hojas()) + arbol.total_nodos_internos(),
                         arbol.total_nodos())


if __name__ == "__main__":
    unittest.main()
