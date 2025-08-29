from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .solver import solve_integral
from .schemas import SolveRequest   # 👈 ahora importamos el modelo aquí

app = FastAPI(title="Calc2 Bot MVP (Python)", version="1.0.0")

# Configuración CORS para permitir acceso desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Abierto: permite cualquier origen (útil para pruebas)
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],            # Authorization, Content-Type, etc.
)

# Endpoint de salud
@app.get("/health")
def health():
    return {"ok": True}

# Endpoint principal para resolver integrales
@app.post("/solve")
def solve(req: SolveRequest):
    if req.type.lower() != "integral":
        return {"error": "MVP: solo integrales indefinidas (type='integral')"}
    return solve_integral(req.input)

# UI mínima con MathJax para probar rápido
@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!doctype html><html lang="es"><head>
<meta charset="utf-8"/><title>Calc2 Bot — MVP</title>
<script>window.MathJax={tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']]},svg:{fontCache:'global'}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<style>
body{font-family:system-ui;max-width:900px;margin:2rem auto;padding:0 1rem;line-height:1.5}
.card{border:1px solid #ddd;border-radius:12px;padding:16px;margin:12px 0}
textarea{width:100%;min-height:90px;padding:10px;border-radius:8px;border:1px solid #ccc;font-family:Consolas,monospace}
button{padding:10px 16px;border-radius:8px;border:0;background:#1a73e8;color:#fff;cursor:pointer}
.muted{color:#666;font-size:.9rem}.error{color:#b00020}
</style></head>
<body>
<h1>Calc2 Bot — MVP (FastAPI + SymPy)</h1>
<p class="muted">Escribí la integral (ej: <code>x*exp(2*x) dx</code>)</p>

<div class="card">
  <textarea id="expr" placeholder="x*exp(2*x) dx"></textarea>
  <div style="margin-top:10px">
    <button id="solveBtn">Resolver</button>
    <span id="status" class="muted"></span>
  </div>
</div>

<div id="result" class="card" style="display:none">
  <h2>Resultado</h2>
  <p><strong>Problema:</strong> <span id="problem"></span></p>
  <p><strong>Resultado:</strong> <span id="resultLatex"></span></p>
  <div><strong>Pasos:</strong><ol id="steps"></ol></div>
  <div><strong>Verificación:</strong><div id="checks"></div></div>
</div>

<div id="error" class="card error" style="display:none"></div>

<script>
const $=s=>document.querySelector(s);
$("#solveBtn").addEventListener("click", async ()=>{
  const expr=$("#expr").value, status=$("#status"), error=$("#error"),
        result=$("#result"), problem=$("#problem"), out=$("#resultLatex"),
        steps=$("#steps"), checks=$("#checks");
  error.style.display="none"; result.style.display="none"; status.textContent="Resolviendo…";
  try{
    const r=await fetch("/solve",{method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({type:"integral",input:expr})});
    const data=await r.json();
    if(!r.ok||data.error) throw new Error(data.error||"Error");
    problem.innerHTML="$"+data.problem_latex+"$";
    out.innerHTML="$"+data.result_latex+"$";
    steps.innerHTML="";
    (data.steps_latex||[]).forEach(s=>{const li=document.createElement("li"); li.innerHTML=s.includes("$")?s:"$"+s+"$"; steps.appendChild(li);});
    checks.innerHTML="";
    (data.checks||[]).forEach(c=>{const p=document.createElement("p"); p.innerHTML="$"+c+"$"; checks.appendChild(p);});
    result.style.display="block"; window.MathJax?.typeset?.();
  }catch(e){ error.textContent=e.message; error.style.display="block"; }
  finally{ status.textContent=""; }
});
</script>
</body></html>
"""