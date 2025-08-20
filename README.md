# Chatbot de IA para Cálculo II

Este proyecto es un servicio en **FastAPI + Sympy** que resuelve integrales paso a paso.

## 🚀 Cómo correrlo

1. Instalar dependencias:
--Los bloques con ```bash son comandos que se ejecutan en **PowerShell o CMD**--
    ```bash 
    pip install -r services/cas-python/requirements.txt
2. Ejecutar el servidor:
    ```bash
    uvicorn services.cas-python.app.main:app --reload
3. Abrir en el navegador:
    http://127.0.0.1:8000/docs

-Pruebas
Para ejecutar las pruebas automáticas:
    ```bash
    pytest services/cas-python/tests    
----------------------------------------------------------
