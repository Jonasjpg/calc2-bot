from typing import Dict
import re
from sympy import (
    symbols, Symbol, integrate, diff, sin, cos, tan, exp, log, sqrt,
    asin, acos, atan, sinh, cosh, tanh, E, pi
)
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, convert_xor, implicit_multiplication_application
)
from sympy.printing.latex import latex

# Lista blanca de funciones/constantes permitidas
SAFE_FUNCS: Dict[str, object] = {
    "E": E, "pi": pi,
    "sin": sin, "cos": cos, "tan": tan,
    "asin": asin, "acos": acos, "atan": atan,
    "sinh": sinh, "cosh": cosh, "tanh": tanh,
    "exp": exp, "log": log, "sqrt": sqrt,
}

# Transformaciones del parser:
# convert_xor: interpreta '^' como potencia en lugar de XOR
# implicit_multiplication_application: 2x -> 2*x, sin x -> sin(x)
TRANSFORMS = standard_transformations + (
    convert_xor,
    implicit_multiplication_application,
)

# Soportar entradas con dx/dy/dt, con o sin símbolo integral delante
_DX_RE = re.compile(r"^(?:∫)?\s*(?P<expr>.+?)\s*d(?P<var>[a-zA-Z])\s*$")

def _parse_input(user_text: str):
    text = user_text.strip()

    m = _DX_RE.match(text)
    if m:
        expr_str = m.group("expr").strip()
        var_str  = m.group("var")
    else:
        # sin dx, asumimos variable 'x'
        expr_str, var_str = text, "x"

    # declarar símbolo de la variable
    var = Symbol(var_str)

    # diccionario local seguro (sin builtins peligrosos)
    local = {var_str: var, **SAFE_FUNCS}

    # parsear la expresión de manera segura
    expr = parse_expr(expr_str, local_dict=local, transformations=TRANSFORMS, evaluate=False)
    return expr, var

def solve_integral(user_text: str):
    """
    Resuelve una integral indefinida desde un texto de usuario.
    Acepta formatos como: '∫ x^2 dx', 'x^2 dx', '(2x+1)*exp(x) dx'.
    """
    expr, var = _parse_input(user_text)

    # integración
    res = integrate(expr, var)

    # verificación por derivación
    check = diff(res, var)
    ok = (check.simplify() - expr.simplify()) == 0

    steps = [
        rf"Identificamos variable: ${latex(var)}$",
        rf"Planteamos: $\int {latex(expr)}\,d{latex(var)}$",
        rf"Obtenemos: ${latex(res)} + C$",
    ]

    checks = [
        rf"\frac{{d}}{{d{latex(var)}}}\left({latex(res)}\right) = {latex(check)} \ "
        + (r"\text{✓ correcto}" if ok else r"\text{✗ revisar}")
    ]

    return {
        "problem_latex": rf"\int {latex(expr)}\,d{latex(var)}",
        "steps_latex": steps,
        "result_latex": rf"{latex(res)} + C",
        "checks": checks,
        "plots": []
    }
