from pydantic import BaseModel

# Modelo de entrada: lo que el cliente envía al servidor
class IntegralRequest(BaseModel):
    expression: str # Ejemplo: "x*exp(2*x)"
    variable: str = "x" # Por defecto es "x" si no se manda otra variable

# Modelo de salida: lo que la API devuelve al cliente
class IntegralResponse(BaseModel):
    original: str
    result: str

# Que hice aquí?
# Usamos Pydantic (BaseModel) para validar la entrada y salida.
# Si se envía algo que no coincide con IntegralRequest, FastAPI devuelve un error automáticamente.
# Swagger (/docs) mostrará estos modelos y permitirá probar la API fácilmente.