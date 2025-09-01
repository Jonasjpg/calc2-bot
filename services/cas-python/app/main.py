# services/cas-python/app/main.py
# Notas:
# - Devuelve JSON también en errores para que el frontend no falle con "Unexpected token".
# - CORS abierto para pruebas. Restringir en producción.
# - La UI incluye tema claro/oscuro usando data-theme (sin @media) y manejo robusto del fetch.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from .solver import solve_integral
from .schemas import SolveRequest

app = FastAPI(title="Calc2 Bot MVP (Python)", version="1.0.0")

# CORS (abrir solo a nuestros dominios en prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/solve")
def solve(req: SolveRequest):
    # Manejo de errores para garantizar siempre JSON
    try:
        if req.type.lower() != "integral":
            return JSONResponse(
                status_code=400,
                content={"error": "MVP: solo integrales indefinidas (type='integral')"},
            )
        data = solve_integral(req.input)
        return JSONResponse(status_code=200, content=data)
    except Exception:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": "Error interno procesando la integral. Revisá la sintaxis (ej: x*exp(2*x) dx)."
            },
        )

# UI
@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Calc2 Bot — MVP</title>

<!-- Tema: fijar data-theme antes del primer render -->
<script>
  (function(){
    var theme = localStorage.getItem("theme") ||
                (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
    document.documentElement.setAttribute("data-theme", theme);
  })();
</script>

<!-- MathJax -->
<script>
  window.MathJax = {
    tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] },
    svg: { fontCache: 'global' }
  };
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>

<style>
  /* Tema por variables. Por defecto: oscuro */
  :root{
    --bg:#0f1222; --fg:#0b0f1a; --fg-2:#151a2b;
    --txt:#eaf0ff; --muted:#9aa3b2;
    --primary:#7c9cff; --primary-2:#8fb0ff; --accent:#00e0b8;
    --danger:#ff6b6b; --ring:rgba(124,156,255,.55);
    --card:rgba(255,255,255,.06); --card-border:rgba(255,255,255,.14);
    --shadow:0 10px 30px rgba(10,15,40,.35);
  }
  /* Claro cuando <html data-theme="light"> */
  :root[data-theme="light"]{
    --bg:#f6f8ff; --fg:#f2f4ff; --fg-2:#ffffff;
    --txt:#1a2033; --muted:#637089;
    --primary:#3558ff; --primary-2:#5f7cff; --accent:#0fba92;
    --card:rgba(255,255,255,.85); --card-border:rgba(10,15,40,.08);
    --shadow:0 10px 25px rgba(25,35,80,.15);
  }

  *{box-sizing:border-box}
  html,body{height:100%}
  body{
    margin:0;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial;
    color:var(--txt);
    background:
      radial-gradient(1200px 600px at 10% -20%, #2a3cff22 15%, transparent 50%),
      radial-gradient(1300px 700px at 110% 0%, #00e0b822 10%, transparent 55%),
      linear-gradient(180deg, var(--bg), var(--fg));
  }

  .wrap{max-width:980px;margin-inline:auto;padding:32px 18px 80px}
  .nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}
  .brand{display:flex;gap:12px;align-items:center}
  .logo{width:40px;height:40px;border-radius:12px;
        background: linear-gradient(135deg,var(--primary),var(--accent)); box-shadow: var(--shadow)}
  .title{font-weight:800;letter-spacing:.3px;font-size:22px}
  .sub{color:var(--muted);font-size:13px}

  .card{
    background:var(--card); border:1px solid var(--card-border);
    border-radius:18px; padding:18px; box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
  }
  .grid{display:grid;gap:16px}
  @media (min-width:960px){ .grid-2{grid-template-columns:1fr 1fr} }

  .label{font-size:14px;color:var(--muted);margin-bottom:6px}
  textarea{
    width:100%;min-height:120px;resize:vertical;
    background:var(--fg-2); color:var(--txt);
    border:1px solid var(--card-border); border-radius:14px;
    padding:14px 14px 36px 14px; line-height:1.5;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    outline:none; transition: box-shadow .15s, border-color .15s;
  }
  textarea:focus{ border-color: var(--primary-2); box-shadow: 0 0 0 4px var(--ring) }

  .row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:10px}
  .btn{
    appearance:none;border:0;border-radius:12px;padding:12px 16px;
    color:white;background: linear-gradient(135deg, var(--primary), var(--primary-2));
    cursor:pointer;font-weight:700;letter-spacing:.2px;
    box-shadow: var(--shadow);transition: transform .06s ease, opacity .15s;
  }
  .btn:active{ transform: translateY(1px) }
  .btn.secondary{ background:transparent;color:var(--txt);border:1px solid var(--card-border) }
  .btn.ghost{ background:transparent;color:var(--muted);border:0;padding:8px 10px;box-shadow:none }
  .btn[disabled]{opacity:.6;cursor:not-allowed}

  .chip{display:inline-flex;align-items:center;gap:6px;
        padding:8px 10px;border-radius:999px;border:1px dashed var(--card-border);
        color:var(--muted);font-size:13px;cursor:pointer;user-select:none}
  .chip:hover{border-style:solid;color:var(--txt)}

  .muted{color:var(--muted)}
  .error{color:var(--danger)}

  .result-kv{display:grid;gap:8px}
  .kv{display:flex;gap:8px;align-items:flex-start}
  .kv b{min-width:100px;display:inline-block}
  .box{background:var(--fg-2);border:1px solid var(--card-border);border-radius:12px;padding:12px;overflow:auto}

  .list{margin:0;padding-left:18px}
  .tools{display:flex;gap:8px;align-items:center;justify-content:flex-end}
  .footer{margin-top:22px;text-align:center;color:var(--muted);font-size:12px}

  .toast{position:fixed;inset:auto 16px 16px 16px;max-width:520px;margin-inline:auto;
         background:var(--card);border:1px solid var(--card-border);backdrop-filter:blur(8px);
         color:var(--txt);padding:12px 14px;border-radius:12px;display:none;box-shadow: var(--shadow)}
  .spinner{width:16px;height:16px;border-radius:50%;
           border:2px solid rgba(255,255,255,.35);border-top-color:#fff;
           animation: spin .8s linear infinite;display:inline-block;margin-right:8px}
  @keyframes spin{to{transform:rotate(1turn)}}
</style>
</head>
<body>
  <div class="wrap">
    <header class="nav">
      <div class="brand">
        <div class="logo"></div>
        <div>
          <div class="title">Calc2 Bot</div>
          <div class="sub">FastAPI + SymPy · Integrales con verificación</div>
        </div>
      </div>
      <button id="themeBtn" class="btn ghost" title="Cambiar tema">🌓</button>
    </header>

    <section class="card">
      <div class="label">Ingresá la integral (Ctrl/⌘+Enter para resolver)</div>
      <textarea id="expr" placeholder="Ej: x*exp(2*x) dx"></textarea>
      <div class="row">
        <button id="solveBtn" class="btn">Resolver</button>
        <button id="clearBtn" class="btn secondary">Limpiar</button>
        <span id="status" class="muted"></span>
      </div>

      <div class="row" style="margin-top:12px">
        <span class="muted">Ejemplos:</span>
        <span class="chip" data-eg="x*exp(2*x) dx">x·e^{2x}</span>
        <span class="chip" data-eg="sin(x) dx">∫ sin(x)</span>
        <span class="chip" data-eg="x^2 * cos(x) dx">x²·cos x</span>
        <span class="chip" data-eg="(e^(3*x) + 1)/x dx">(e^{3x}+1)/x</span>
      </div>
    </section>

    <section id="result" class="grid grid-2" style="margin-top:18px; display:none">
      <div class="card">
        <div class="row" style="justify-content:space-between;align-items:center;margin-bottom:8px">
          <h2 style="margin:0">Resultado</h2>
          <div class="tools">
            <button id="copyBtn" class="btn secondary" title="Copiar LaTeX">Copiar LaTeX</button>
          </div>
        </div>

        <div class="result-kv">
          <div class="kv"><b>Problema:</b> <div id="problem" class="box"></div></div>
          <div class="kv"><b>Resultado:</b> <div id="resultLatex" class="box"></div></div>
        </div>
      </div>

      <div class="card">
        <h3 style="margin-top:0">Pasos & Verificación</h3>
        <div class="kv"><b>Pasos:</b> <ol id="steps" class="list"></ol></div>
        <div class="kv"><b>Chequeos:</b> <div id="checks" class="box"></div></div>
      </div>
    </section>

    <div id="toast" class="toast"></div>
    <footer class="footer">Hecho con ❤️ para Cálculo II · MathJax en cliente</footer>
  </div>

<script>
  const $ = (s) => document.querySelector(s);

  // Tema claro/oscuro con data-theme
  const themeBtn = $("#themeBtn");
  let theme = document.documentElement.getAttribute("data-theme") || "dark";
  const applyTheme = () => document.documentElement.setAttribute("data-theme", theme);
  themeBtn.addEventListener("click", () => {
    theme = (theme === "light") ? "dark" : "light";
    localStorage.setItem("theme", theme);
    applyTheme();
  });

  // Autoresize del textarea
  const ta = $("#expr");
  const autoresize = () => { ta.style.height = "auto"; ta.style.height = (ta.scrollHeight+2) + "px"; }
  ta.addEventListener("input", autoresize); setTimeout(autoresize, 50);

  // Chips de ejemplo
  document.querySelectorAll(".chip").forEach(c=>{
    c.onclick = ()=>{ ta.value = c.dataset.eg; autoresize(); ta.focus(); }
  });

  const showToast = (msg) => {
    const t = $("#toast"); t.textContent = msg; t.style.display="block";
    setTimeout(()=>{ t.style.display="none"; }, 2600);
  }

  // Copiar LaTeX
  $("#copyBtn").addEventListener("click", async ()=>{
    const res = $("#resultLatex").textContent.trim();
    if(!res){ showToast("No hay resultado aún"); return; }
    try{ await navigator.clipboard.writeText(res.replace(/^\\$|\\$/g,"")); showToast("Copiado") }
    catch{ showToast("No se pudo copiar") }
  });

  // Limpiar
  $("#clearBtn").onclick = ()=>{ ta.value=""; autoresize(); $("#result").style.display="none"; };

  // Resolver con manejo robusto de respuesta
  const solve = async () => {
    const status = $("#status");
    const btn = $("#solveBtn");
    const result=$("#result"), problem=$("#problem"), out=$("#resultLatex"),
          steps=$("#steps"), checks=$("#checks");

    const expr = ta.value.trim();
    if(!expr){ showToast("Escribí una integral, por ejemplo: x*exp(2*x) dx"); return; }

    btn.disabled = true; status.innerHTML = '<span class="spinner"></span>Resolviendo…';

    try{
      const r = await fetch("/solve",{
        method:"POST",
        headers:{
          "Content-Type":"application/json",
          "Accept":"application/json"
        },
        body: JSON.stringify({type:"integral", input:expr})
      });

      const ct = r.headers.get("content-type") || "";
      const raw = await r.text();
      let data;
      if (ct.includes("application/json")) {
        try { data = JSON.parse(raw); } catch { throw new Error("Respuesta inválida"); }
      } else {
        if (!r.ok) throw new Error(raw || `HTTP ${r.status}`);
        throw new Error("Respuesta no válida del servidor.");
      }
      if (!r.ok || data.error) throw new Error(data.error || `HTTP ${r.status}`);

      problem.innerHTML = "$"+data.problem_latex+"$";
      out.innerHTML = "$"+data.result_latex+"$";

      steps.innerHTML = "";
      (data.steps_latex || []).forEach(s=>{
        const li = document.createElement("li");
        li.innerHTML = s.includes("$") ? s : "$"+s+"$";
        steps.appendChild(li);
      });

      checks.innerHTML = "";
      (data.checks || []).forEach(c=>{
        const p = document.createElement("p");
        p.innerHTML = "$"+c+"$";
        checks.appendChild(p);
      });

      result.style.display = "grid";
      await window.MathJax?.typesetPromise?.();
    }catch(e){
      showToast(e.message || "Error");
    }finally{
      btn.disabled = false;
      status.textContent = "";
    }
  };

  $("#solveBtn").addEventListener("click", solve);
  // Ctrl/⌘ + Enter
  window.addEventListener("keydown",(e)=>{
    if((e.metaKey || e.ctrlKey) && e.key === "Enter"){ e.preventDefault(); solve(); }
  });
</script>
</body>
</html>
"""
# Fin de main.py