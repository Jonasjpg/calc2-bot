Manual básico de Xdx
==========================

1) ¿Qué es Xdx?
---------------------
Xdx es una aplicación web realizada por estudiantes del curso Cálculo II. Le escribes
una integral como texto (por ejemplo: x*exp(2*x) dx) y te devuelve:
- La fórmula final en formato “bonito” (LaTeX).
- Unos pasos orientativos de cómo se llega al resultado.
- Una verificación rápida: deriva el resultado y comprueba que recupera lo que escribiste.

El propósito es usarlo como apoyo para estudiar: ver resultados, repasar técnicas, y
confirmar si una cuenta parece consistente.


2) ¿Qué es LaTeX y por qué lo usamos aquí?
------------------------------------------
LaTeX es una forma estándar de escribir fórmulas matemáticas con texto plano. Se usa
mucho en apuntes, papers y libros porque deja las fórmulas prolijas y legibles.
Ejemplos de cómo se ven fórmulas en LaTeX:
- \int x e^{2x} \, dx
- \frac{d}{dx} (\sin x) = \cos x
- e^{i\pi} + 1 = 0

En Xdx:
- El servidor prepara el resultado en LaTeX.
- En la página web, una librería llamada “MathJax” lo dibuja de forma clara en el navegador.
- Ventaja: ves la misma notación que usarías a mano en tus apuntes.


3) ¿Qué es SymPy y qué hace por nosotros?
-----------------------------------------
SymPy es una biblioteca de Python para “álgebra simbólica”. A diferencia de una simple
calculadora numérica, SymPy trabaja con expresiones matemáticas como objetos: puede
derivar, integrar, simplificar, factorizar, etc., sin necesidad de “poner números”.

En este proyecto SymPy se usa para:
- Interpretar la expresión que se escribe (parsear el texto).
- Calcular la integral indefinida de forma simbólica.
- Derivar el resultado y verificar que se obtiene la expresión original.
- Convertir el resultado a LaTeX para mostrarlo lindo en la web.

Lo importante: no hace aproximaciones numéricas; maneja la fórmula “tal cual”, como lo
harías con lápiz y papel.


4) Cómo funciona Xdx, paso a paso
---------------------------------------
A. Escribes la integral en una caja de texto, por ejemplo:  x*exp(2*x) dx
B. El servidor limpia un poco el texto (por ejemplo, remueve “dx” para el cálculo) y lo
   convierte a una expresión matemática interna.
C. SymPy intenta integrar esa expresión con respecto a x.
D. El resultado simbólico se transforma a LaTeX.
E. Para verificar, se deriva el resultado y se compara con la expresión original.
   - Si coincide, marcamos que el chequeo es “correcto”.
F. El servidor arma una respuesta con:
   - problem_latex: cómo se ve el problema (\int ... dx).
   - result_latex: el resultado de la integral (con + C).
   - steps_latex: pasos orientativos.
   - checks: una línea de verificación mostrando la derivada del resultado.
G. La página muestra todo con MathJax para que se lea bien.


5) Cómo escribir las integrales (guía corta)
--------------------------------------------
- Usá * para multiplicar y ^ para potencias.
- Escribí paréntesis cuando haga falta: (a + b)/x, (x^2 + 1)*sin(x), etc.
- Indicá la variable con “dx” al final (por ahora se integra respecto de x).
- Funciones comunes: sin(x), cos(x), tan(x), exp(x), log(x), etc.
- Ejemplos válidos:
  - x*exp(2*x) dx
  - sin(x) dx
  - x^2 * cos(x) dx
  - (e^(3*x) + 1)/x dx


6) Cómo usar la aplicación web
------------------------------
1) Abrir la página principal.
2) Escribir la integral en la caja de texto.
3) Tocar “Resolver”.
4) Abajo vas a ver:
   - Problema (en LaTeX): la integral como \int ... dx.
   - Resultado: la antiderivada + C.
   - Pasos: breve descripción del método.
   - Chequeo: derivada del resultado, comparada con tu expresión.

Consejo: copiar el LaTeX si quieres pegarlo en tus apuntes o informes.


7) Preguntas frecuentes
------------------------
- ¿Hace integrales definidas?
  Por ahora el foco es integrales indefinidas. Es posible extenderlo más adelante.

- ¿Solo integra respecto de x?
  Sí, el MVP asume la variable x. Se puede mejorar para elegir variable luego.

- ¿Qué pasa si la integral no tiene antiderivada elemental?
  SymPy puede no encontrar una forma “cerrada”. En esos casos puede fallar o devolver
  una expresión especial. La recomendación es empezar por casos estándar.

- ¿Siempre hay pasos “paso a paso”?
  Los pasos son descriptivos y cortos. Para una guía más pedagógica habría que ampliar
  esa parte para distintos tipos de integrales (sustitución, por partes, etc.).


8) Estructura mínima del proyecto (solo referencia)
----------------------------------------------------
- services/cas-python/app/main.py     Página + rutas de la API.
- services/cas-python/app/solver.py   Lógica con SymPy (integrar y verificar).
- services/cas-python/app/schemas.py  Formato de entrada/salida (Pydantic).
- services/cas-python/tests/          Pruebas automatizadas simples.

Este manual es una introducción básica. La idea es que puedas usar la herramienta
rápido y, si te interesa, profundizar después en LaTeX y SymPy. El objetivo es ayudarte
a practicar y validar tus resultados de Cálculo II.