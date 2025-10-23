# Notas:
# - Siempre respondemos JSON en /solve (también en errores) para evitar "Unexpected token" en el frontend.
# - El endpoint /health lo usa Render para marcar el servicio como "ready".
# - La UI simple está embebida en este archivo para evitar dependencias extra.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from .solver import solve_integral
from .schemas import SolveRequest

app = FastAPI(title="Calc2 Bot MVP (Python)", version="1.0.0")
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="services/cas-python/app/static"), name="static")

# CORS (en prod conviene limitar orígenes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    # Render hace ping a este path: si responde 200, considera que el servicio está "ready"
    return {"ok": True}


@app.post("/solve")
def solve(req: SolveRequest):
    """
    Procesa integrales. Siempre retorna JSON.
    Si type != "integral", devolvemos 422 con mensaje claro.
    Ante errores de parseo, 400 con detalle.
    """
    if not hasattr(req, "type") or req.type is None:
        return JSONResponse({"error": "Falta 'type'."}, status_code=422)
    if req.type.lower() != "integral":
        return JSONResponse({"error": "Tipo no soportado. Usa 'integral'."}, status_code=422)
    if not getattr(req, "input", None):
        return JSONResponse({"error": "Falta 'input' con la expresión."}, status_code=422)
    try:
        data = solve_integral(req.input)
        return JSONResponse(status_code=200, content=data)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": "No pude interpretar la expresión. Revisa sintaxis (usa ^ o ** para potencias).", "detail": str(e)},
        )

# UI simple (HTML embebido) — sin dependencias extra
@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Xdx - integrales</title>

<!-- Fijar el tema antes del primer render (si no hay preferencia, inicia en modo oscuro) -->
<script>
  (function(){
    var theme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", theme);
  })();
</script>

<!-- MathJax para render LaTeX -->
<script>
  window.MathJax = {
    tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] },
    svg: { fontCache: 'global' }
  };
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>

<style>
  /* Variables de tema (oscuro por defecto) */
  :root{
    --bg:#0f1222; --fg:#0b0f1a; --fg-2:#151a2b;
    --txt:#eaf0ff; --muted:#9aa3b2;
    --primary:#7c9cff; --primary-2:#8fb0ff; --accent:#00e0b8;
    --danger:#ff6b6b; --ring:rgba(124,156,255,.55);
    --card:rgba(255,255,255,.06); --card-border:rgba(255,255,255,.14);
    --shadow:0 10px 30px rgba(10,15,40,.35);

    /* Variables para el brillo que sigue al cursor */
    --mx: 50vw;
    --my: 50vh;
    --glow: rgba(0,224,184,.085); /* turquesa muy leve */
  }

  /* Tema claro cuando html[data-theme="light"] */
  :root[data-theme="light"]{
    --bg:#eef2fb; --fg:#e7ecfa; --fg-2:#f6f8ff;
    --txt:#1e2435; --muted:#596580;
    --primary:#3558ff; --primary-2:#5f7cff; --accent:#10a98f;
    --card:rgba(255,255,255,.72); --card-border:rgba(10,15,40,.06);
    --shadow:0 8px 18px rgba(25,35,80,.10);
    --glow: rgba(0,224,184,.02); /* más tenue en claro */
  }

  /* Superficies (textarea y cajas) */
  html[data-theme="light"] textarea,
  html[data-theme="light"] .box{
    /* mezcla la superficie con un gris-azulado suave para bajar el blanco puro */
    background: color-mix(in srgb, var(--fg-2) 80%, #e9eefb);
  }

  /* El glassmorphism del tema claro un poco menos saturado/brillante */
  html[data-theme="light"] .card{
    backdrop-filter: blur(12px) saturate(108%);
    -webkit-backdrop-filter: blur(12px) saturate(108%);
  }


  *{box-sizing:border-box}
  html,body{height:100%}

  /* Fondo con glow que sigue al cursor + degradados */
  body{
    margin:0;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial;
    color:var(--txt);
    background:
      radial-gradient(220px 220px at var(--mx) var(--my), var(--glow), transparent 60%),
      radial-gradient(1200px 600px at 10% -20%, #2a3cff22 15%, transparent 50%),
      radial-gradient(1300px 700px at 110% 0%, #00e0b822 10%, transparent 55%),
      linear-gradient(180deg, var(--bg), var(--fg));
  }

  .wrap{max-width:980px;margin-inline:auto;padding:32px 18px 80px}
  .nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}
  .brand{display:flex;gap:12px;align-items:center}
        .logo {
          width: 38px;
          height: 38px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .logo img {
          width: 100%;
          height: auto;
          border-radius: 12px; /* opcional: si querés mantener bordes suaves */
        }

  /* Tarjetas con glassmorphism (transparencia + blur) */
  .card{
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 18px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(14px) saturate(120%);
    -webkit-backdrop-filter: blur(14px) saturate(120%); /* Safari/iOS */
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

  /* Contenedores de texto con glassmorphism */
  .box{
    background: color-mix(in srgb, var(--fg-2) 70%, transparent);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 12px;
    overflow: auto;
    backdrop-filter: blur(10px) saturate(120%);
    -webkit-backdrop-filter: blur(10px) saturate(120%);
  }

  /* Realce leve al pasar el mouse por elementos relevantes */
  .card:hover, .box:hover, textarea:hover{
    border-color: color-mix(in srgb, var(--primary-2) 60%, transparent);
    box-shadow: 0 0 0 1px color-mix(in srgb, var(--primary-2) 35%, transparent);
  }

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

  /* ===== Easter egg: Constante de integración (+ C) ===== */
  .right-tools{ display:flex; align-items:center; gap:10px }

    #constC{
    position:relative;
    display:inline-flex; align-items:center; justify-content:center;
    padding:6px 10px; border-radius:999px; font-weight:800; letter-spacing:.3px;
    font-size:13px; line-height:1; user-select:none; cursor:pointer;
    border:1px solid var(--card-border);
    background: color-mix(in srgb, var(--fg-2) 70%, transparent);
    color:var(--txt);
    box-shadow: var(--shadow);
    backdrop-filter: blur(8px) saturate(120%);
    -webkit-backdrop-filter: blur(8px) saturate(120%);
    transition: transform .18s cubic-bezier(.2,.8,.2,1), border-color .15s, box-shadow .15s;
  }
  #constC::after{
    content:''; position:absolute; inset:-6px; border-radius:inherit; pointer-events:none;
    background: radial-gradient(120px 120px at 50% 40%, rgba(0,224,184,.15), transparent 60%);
    opacity:0; transition: opacity .2s;
  }
  #constC:hover::after{ opacity:.85 }

  @media (prefers-reduced-motion: reduce){
    #constC{ transition: border-color .15s, box-shadow .15s; }
  }
</style>
</head>
<body>
  <div class="wrap">
    <header class="nav">
      <div class="brand">
        <div class="logo">
          <img src="/static/logo_xdx.png" alt="Logo xdx" />
        </div>
      
        <div>
          <div class="title">xdx</div>
          <div class="sub">FastAPI + SymPy = Integrales con verificación</div>
        </div>
      </div>
      <div class="right-tools">
      <button id="themeBtn" class="btn ghost" title="Cambiar tema">🌓</button>
        <div class="egg-wrap">
          <button id="constC" title="Constante de integración">+ C</button>
        </div>
      </div>
    </header>

    <section class="card">
      <div class="label">Ingresa la integral (Ctrl+Enter para resolver)</div>
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
    <footer class="footer">
      Aplicación creada por "Los Cálculos Renales"
      <br>
      
    </footer>
  </div>

<script>
  const $ = (s) => document.querySelector(s);
  
  // Toggle claro/oscuro con data-theme
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

  // Toast simple
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

  // Resolver (manejo robusto de respuesta)
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
        headers:{ "Content-Type":"application/json", "Accept":"application/json" },
        body: JSON.stringify({type:"integral", input:expr})
      });

      const ct = r.headers.get("content-type") || "";
      const raw = await r.text();     // siempre leo texto primero
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

  // Atajo Ctrl + Enter
  window.addEventListener("keydown",(e)=>{
    if((e.metaKey || e.ctrlKey) && e.key === "Enter"){ e.preventDefault(); solve(); }
  });

  /* Glow que sigue al cursor: actualiza --mx y --my con easing para efecto suave */
  (()=>{
    const root = document.documentElement;
    let tx = innerWidth * 0.5, ty = innerHeight * 0.5; // target
    let cx = tx, cy = ty;                              // current
    const set = (x, y) => { root.style.setProperty("--mx", x + "px"); root.style.setProperty("--my", y + "px"); }
    const lerp = (a,b,t)=>a+(b-a)*t;
    set(tx, ty);

    function loop(){ cx = lerp(cx, tx, 0.12); cy = lerp(cy, ty, 0.12); set(cx, cy); requestAnimationFrame(loop); }
    loop();

    addEventListener("pointermove", (e)=>{ tx = e.clientX; ty = e.clientY; }, {passive:true});
    addEventListener("resize", ()=>{ tx = innerWidth * 0.5; ty = innerHeight * 0.5; });
  })();

    /* ===== Easter egg "+ C" =====
    - Cerca del puntero → el botón “+ C” salta un poco (se “escapa”).
    - Vuelve a su posición tras ~1.4s.
    - Click → copia "+ C" al portapapeles y, si existe showToast, avisa.
  */
  (() => {
    const btn = document.getElementById('constC');
    if (!btn) return;

    let respawnTO = null;
    const clamp = (v,min,max) => Math.max(min, Math.min(max, v));

    function jump(e){
      const r = btn.getBoundingClientRect();
      const cx = r.left + r.width/2;
      const cy = r.top  + r.height/2;

      const p = e.touches ? e.touches[0] : e;
      const mx = p.clientX, my = p.clientY;

      let dx = cx - mx, dy = cy - my;
      const len = Math.hypot(dx,dy) || 1;
      dx /= len; dy /= len;

      const dist = 90 + Math.random()*120;            // distancia del “salto”
      let tx = dx*dist, ty = dy*dist;

      const vw = window.innerWidth, vh = window.innerHeight;
      tx = clamp(tx, -r.left + 12,  vw - r.right  - 12);
      ty = clamp(ty, -r.top  + 12,  vh - r.bottom - 12);

      btn.style.transform = `translate(${tx}px, ${ty}px) rotate(${(Math.random()*10-5).toFixed(1)}deg)`;

      clearTimeout(respawnTO);
      respawnTO = setTimeout(() => { btn.style.transform = 'translate(0, 0)'; }, 1400);
    }

    btn.addEventListener('mouseenter', jump);
    btn.addEventListener('mousemove', jump);
    btn.addEventListener('touchstart', jump, {passive:true});

    btn.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText('+ C'); } catch {}
      if (typeof window.showToast === 'function') showToast('+ C copiado');
    });
  })();
</script>
</body>
</html>
"""
# Fin de main.py