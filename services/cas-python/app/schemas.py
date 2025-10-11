from pydantic import BaseModel

# Modelos de datos para validación con Pydantic (entrada y salida de la API)

# Modelo de entrada: contenido que el cliente envía al servidor
class IntegralRequest(BaseModel):
    expression: str  # Ejemplo: "x*exp(2*x)"
    variable: str = "x"  # Variable de integración; por defecto "x"

# Modelo de salida: contenido que la API devuelve al cliente
class IntegralResponse(BaseModel):
    original: str
    result: str

# Modelo usado en pruebas (mantiene compatibilidad con tests automatizados)
class SolveRequest(BaseModel):
    type: str   # Tipo de operación, por ejemplo: "integral"
    input: str  # Expresión matemática, por ejemplo: "x*exp(2*x) dx"

# Notas:
# - Pydantic valida estructura y tipos; si no coincide, FastAPI devuelve error automáticamente.
# - La documentación interactiva en /docs (Swagger) muestra estos modelos y permite probar la API.