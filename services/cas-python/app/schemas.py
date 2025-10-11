from pydantic import BaseModel

# Modelo de entrada: lo que el cliente envía al servidor
class IntegralRequest(BaseModel):
    expression: str # Ejemplo: "x*exp(2*x)"
    variable: str = "x" # Por defecto es "x" si no se manda otra variable

# Modelo de salida: lo que la API devuelve al cliente
class IntegralResponse(BaseModel):
    original: str
    result: str

# Modelo usado en los tests (compatibilidad con pruebas automatizadas)
class SolveRequest(BaseModel):
    type: str # tipo de operación, ej: "integral"
    input: str # expresión matemática, ej: "x*exp(2*x) dx"

# Notas:
# - Usamos Pydantic (BaseModel) para validar la entrada y salida.
# - Si se envía algo que no coincide con los modelos, FastAPI devuelve un error automáticamente.
# - Swagger (/docs) mostrará estos modelos y permitirá probar la API fácilmente.