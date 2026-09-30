# Registro de interacciones con la IA

**Herramienta:** Google AI Studio — https://aistudio.google.com
**Modelo:** _(anotar el modelo usado, p. ej. Gemini 2.5 Flash)_
**Fecha(s):** _(anotar)_

> Instrucciones para el equipo: copien cada *prompt* tal cual en Google AI Studio,
> peguen aquí la parte relevante de la respuesta, guarden la captura en la carpeta
> `capturas/` con el nombre indicado y completen la tabla de verificación (sección 4).

---

## 3. Interacciones relevantes

### Interacción 1 — Estructura del nodo y del árbol
**Prompt:**
```
Estoy haciendo un programa en Python que construye un árbol binario de búsqueda
a partir de las palabras de una oración. Dame la clase Nodo (con palabra,
hijo izquierdo, hijo derecho y un contador de frecuencia) y la clase
ArbolBinarioBusqueda con un método insertar. Si la palabra es alfabéticamente
menor va a la izquierda, si es mayor a la derecha. No uses bibliotecas externas.
```
**Respuesta (resumen / fragmento relevante):**
_(pegar aquí)_

**Captura:** `capturas/01_estructura.png`

**Qué usamos / qué cambiamos:**
_(p. ej. "usamos la clase Nodo; cambiamos la inserción recursiva por iterativa")_

---

### Interacción 2 — Manejo de duplicados
**Prompt:**
```
¿Qué opciones hay para manejar palabras duplicadas en un árbol binario de
búsqueda? Compara: ignorarlas, insertarlas a la derecha o llevar un contador
de frecuencia en el nodo. ¿Cuál conserva mejor la propiedad del ABB?
```
**Respuesta:** _(pegar aquí)_

**Captura:** `capturas/02_duplicados.png`

**Decisión del equipo:** usar un contador de `frecuencia` en el nodo (ver README).

---

### Interacción 3 — Recorridos
**Prompt:**
```
Escribe en Python los recorridos inorden, preorden y postorden para mi clase
ArbolBinarioBusqueda. Cada uno debe devolver una lista de palabras.
```
**Respuesta:** _(pegar aquí)_

**Captura:** `capturas/03_recorridos.png`

---

### Interacción 4 — Conteo de nodos, nodos internos, hojas y máximo
**Prompt:**
```
Agrega métodos para: contar el total de nodos, contar los nodos internos,
obtener la lista de hojas, obtener la lista de nodos internos y obtener la
palabra con el máximo valor alfabético. Explica qué se considera nodo interno.
```
**Respuesta:** _(pegar aquí)_

**Captura:** `capturas/04_calculos.png`

---

### Interacción 5 — Acentos, ñ y mayúsculas
**Prompt:**
```
En Python, ¿"árbol" < "zorro" da True o False? ¿Cómo comparo palabras en
español para que los acentos no afecten el orden y la ñ quede entre la n y la o?
También necesito quitar signos de puntuación como ¡ ¿ , .
```
**Respuesta:** _(pegar aquí)_

**Captura:** `capturas/05_acentos.png`

---

### Interacción 6 — Revisión del código final
**Prompt:**
```
Revisa este código de árbol binario de búsqueda y dime si tiene errores o
casos que no maneja (entrada vacía, una sola palabra, palabras repetidas):
<pegar arbol_bst.py>
```
**Respuesta:** _(pegar aquí)_

**Captura:** `capturas/06_revision.png`

---

## 4. Tabla de verificación de las respuestas obtenidas

La columna **"Cómo se verificó"** describe la prueba concreta que se hizo sobre la
respuesta de la IA. Completen **"Resultado"** con lo que realmente pasó.

| # | Respuesta de la IA sobre… | Cómo se verificó | Error típico a revisar | Resultado (✅ correcta / ⚠️ corregida / ❌ descartada) | Corrección aplicada |
|---|---|---|---|---|---|
| 1 | Clase `Nodo` e inserción | Insertar `el perro come carne y el gato come pescado` y comparar el árbol con el dibujado a mano | Que un duplicado se inserte como nodo nuevo o que se compare `<=` en lugar de `<` | | |
| 2 | Manejo de duplicados | CP-02 y CP-09: `sol sol sol` debe dar 1 nodo con frecuencia 3 | Duplicados que desbalancean el árbol o que se pierden sin contarse | | |
| 3 | Recorrido inorden | El inorden debe salir ordenado alfabéticamente (CP-10) | Orden de las llamadas recursivas intercambiado | | |
| 4 | Recorridos preorden / postorden | Comparar con el recorrido hecho a mano sobre el diagrama | Confundir preorden con postorden | | |
| 5 | Total de nodos | 9 palabras con 2 repetidas → 7 nodos | Contar palabras en lugar de nodos | | |
| 6 | Nodos internos | CP-07: una palabra → 0 internos; CP-01 → 4 internos | Contar sólo nodos con **dos** hijos, o excluir siempre la raíz | | |
| 7 | Palabra máxima | Debe ser el nodo más a la derecha; CP-04 → `zorro` | Usar `max()` sobre cadenas con acentos (`"árbol" > "zorro"` es `True` en Python) | | |
| 8 | Acentos y ñ | CP-04: inorden `árbol nube ñandú oso zorro` | Comparación por código Unicode; `ñ` quedando al final del alfabeto | | |
| 9 | Puntuación y mayúsculas | CP-03: `¡Hola, Mundo! hola.` → `hola` frecuencia 2 | `split()` deja `"hola,"` y `"hola."` como palabras distintas | | |
| 10 | Revisión final | Ejecutar `python3 -m unittest -v test_arbol_bst.py` | Sugerencias que rompen pruebas que ya pasaban | | |
