from sympy import symbols, integrate, diff
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing.latex import latex

def _sanitize(text: str) -> str:
    # Permite inputs tipo "∫ x*exp(2*x) dx" o "integrate x*exp(2*x) dx"
    return (text.replace("∫","").replace("integrate","").replace("dx","").strip())

def solve_integral(text: str):
    x = symbols('x')
    expr = parse_expr(_sanitize(text), evaluate=False)
    res = integrate(expr, x)
    check = diff(res, x).simplify()
    ok = (check - expr).simplify() == 0

    steps = [
        r"Identificamos la integral en $x$.",
        r"Aplicamos reglas simbólicas (sustitución/partes según corresponda).",
        rf"Obtenemos: ${latex(res)} + C$",
    ]

    return {
        "problem_latex": rf"\\int {latex(expr)}\\,dx",
        "steps_latex": steps,
        "result_latex": rf"{latex(res)} + C",
        "checks": [rf"\\frac{{d}}{{dx}}\\left({latex(res)}\\right) = {latex(check)} \\\\ " + (r"\\text{✓ correcto}" if ok else r"\\text{✗ revisar}")],

        "plots": []
    }
