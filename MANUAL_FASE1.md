---

# 📘 Manual de Fase 1 — Proyecto *Calc2 Bot*

## 🎯 Objetivo

Dejar listo un **MVP mínimo** que:

* Resuelva integrales indefinidas con **SymPy**.
* Exponga una **API en FastAPI** (`/health`, `/solve`).
* Incluya una **UI HTML básica** con MathJax.
* Esté versionado en **GitHub** con pruebas automáticas (CI).

---

## 🛠️ Pasos realizados

### 1. Crear repositorio

En GitHub:

* Crear repositorio nuevo llamado **`calc2-bot`**.
* Clonarlo en tu máquina:

```powershell
git clone https://github.com/<tu-usuario-o-org>/calc2-bot.git
cd calc2-bot
```

---

### 2. Estructura del proyecto

Dentro del repo creamos esta estructura:

```
calc2-bot/
├─ services/
│  └─ cas-python/
│     ├─ app/
│     │  ├─ main.py
│     │  └─ solver.py
│     ├─ tests/
│     │  └─ test_integrals.py
│     └─ requirements.txt
├─ .github/
│  └─ workflows/
│     └─ python-ci.yml
└─ README.md
```

---

### 3. Instalar entorno virtual (local, fuera de Google Drive)

En **PowerShell**:

```powershell
cd <ruta_local_fuera_de_drive>\calc2-bot\services\cas-python

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

📌 Si cerrás PowerShell, cuando vuelvas hacé:

```powershell
cd <ruta>\calc2-bot\services\cas-python
.venv\Scripts\Activate.ps1
```

---

### 4. Contenido de los archivos

#### `requirements.txt`

```txt
fastapi
uvicorn
sympy
pytest
```

#### `app/solver.py`

```python
from sympy import symbols, integrate, sympify, latex, diff

x = symbols("x")

def solve_integral(expr: str):
    expr = expr.replace("dx", "").strip()
    f = sympify(expr)
    result = integrate(f, x)
    steps = [f"Integrar {latex(f)} respecto a x"]
    checks = [f"\\frac{{d}}{{dx}}({latex(result)}) = {latex(diff(result, x))}"]
    return {
        "problem_latex": latex(f),
        "result_latex": latex(result),
        "steps_latex": steps,
        "checks": checks
    }
```

#### `app/main.py`

*(la versión final con UI que me mostraste tú — ya lista)* ✅

#### `tests/test_integrals.py`

```python
from app.solver import solve_integral

def test_exp_integral():
    result = solve_integral("x*exp(2*x)")
    assert "result_latex" in result
```

#### `.github/workflows/python-ci.yml`

```yaml
name: Python CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: services/cas-python
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -q
```

#### `README.md`

````markdown
# Calc2 Bot

MVP inicial para resolver integrales en **Cálculo II**.

## Cómo correr localmente
```bash
cd services/cas-python
.venv\Scripts\Activate.ps1   # En PowerShell
uvicorn app.main:app --reload
````

Abrir en navegador:

* API: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* UI básica: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

````

---

### 5. Ejecutar API en local  

Con el entorno activado:  

```powershell
cd services\cas-python
uvicorn app.main:app --reload
````

✅ Abrir navegador:

* [http://127.0.0.1:8000/](http://127.0.0.1:8000/) → UI HTML con textarea.
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) → Swagger UI para probar `/solve`.

---

## ✅ Resultado de la Fase 1

* Proyecto funcional en GitHub.
* CI configurado con GitHub Actions.
* API y UI mínimas corriendo en local.
* Solver capaz de resolver **integrales indefinidas simples**.

---

👉 Con esto se cierra oficialmente la **Fase 1**.

---