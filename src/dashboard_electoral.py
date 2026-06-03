import pandas as pd
import json
import os

# ── Rutas ──────────────────────────────────────────────────────────────────
# El script vive en src/ — data/ y outputs/ están en la raíz del proyecto
SRC  = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SRC)
RUTA_CSV_MED   = os.path.join(BASE, 'data', 'electoral_medellin.csv')
RUTA_CSV_VALLE = os.path.join(BASE, 'data', 'valle_aburra_presidencial_2026.csv')
RUTA_OUT       = os.path.join(BASE, 'outputs')
os.makedirs(RUTA_OUT, exist_ok=True)

# ── Censo electoral estimado por municipio (Registraduría / DANE 2026) ─────
CENSO = {
    'Bello':       337000,
    'Itagüí':      242000,
    'Envigado':    248000,
    'Caldas':       74000,
    'Copacabana':   88000,
    'Sabaneta':    106000,
    'La Estrella':  75000,
    'Girardota':    55000,
    'Barbosa':      40000,
}

# ── Leer y preparar datos de comunas ──────────────────────────────────────
df_med = pd.read_csv(RUTA_CSV_MED)
df_med = df_med[~df_med['codigo'].isin([90, 98, 99])].copy()

total_med = (df_med['ivan_cepeda'] + df_med['abelardo_de_la_espriella'] +
             df_med['paloma_valencia'] + df_med['sergio_fajardo'])

df_med['votos']    = total_med
df_med['cepeda']   = (df_med['ivan_cepeda']              / total_med * 100).round(1)
df_med['abelardo'] = (df_med['abelardo_de_la_espriella'] / total_med * 100).round(1)
df_med['paloma']   = (df_med['paloma_valencia']          / total_med * 100).round(1)
df_med['fajardo']  = (df_med['sergio_fajardo']           / total_med * 100).round(1)
df_med['fajpal']   = (df_med['paloma'] + df_med['fajardo']).round(1)

comunas_js = []
for _, r in df_med.iterrows():
    comunas_js.append({
        'name':     r['comuna'],
        'cepeda':   r['cepeda'],
        'abelardo': r['abelardo'],
        'paloma':   r['paloma'],
        'fajardo':  r['fajardo'],
        'fajpal':   r['fajpal'],
        'votos':    int(r['votos']),
        'vcep':     int(r['ivan_cepeda']),
        'vabe':     int(r['abelardo_de_la_espriella']),
        'vpal':     int(r['paloma_valencia']),
        'vfaj':     int(r['sergio_fajardo']),
    })

# ── Leer y preparar datos de municipios ───────────────────────────────────
df_val = pd.read_csv(RUTA_CSV_VALLE)

municipios_js = []
for _, r in df_val.iterrows():
    nombre = r['municipio']
    votos  = int(r['ivan_cepeda'] + r['abelardo_de_la_espriella'] +
                 r['paloma_valencia'] + r['sergio_fajardo'])
    municipios_js.append({
        'name':     nombre,
        'cepeda':   round(float(r['pct_cepeda']),  1),
        'abelardo': round(float(r['pct_abelardo']), 1),
        'paloma':   round(float(r['pct_paloma']),   1),
        'fajardo':  round(float(r['pct_fajardo']),  1),
        'fajpal':   round(float(r['pct_paloma']) + float(r['pct_fajardo']), 1),
        'votos':    votos,
        'vcep':     int(r['ivan_cepeda']),
        'vabe':     int(r['abelardo_de_la_espriella']),
        'vpal':     int(r['paloma_valencia']),
        'vfaj':     int(r['sergio_fajardo']),
        'censo':    CENSO.get(nombre, 0),
    })

# ── Serializar a JSON ──────────────────────────────────────────────────────
comunas_json    = json.dumps(comunas_js,    ensure_ascii=False, indent=2)
municipios_json = json.dumps(municipios_js, ensure_ascii=False, indent=2)

# ── Generar HTML ───────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Electoral Valle de Aburrá — CES M.L.</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  :root{{
    --cep:#7c3aed;--abe:#ea580c;--pal:#0284c7;--faj:#ca8a04;--fajpal:#059669;
    --abst:#94a3b8;--bg:#f8f7f4;--card:#fff;--text:#1a1a1a;--muted:#6b7280;
    --border:#e5e7eb;
  }}
  body{{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);font-size:14px;line-height:1.5}}
  .header{{background:#fff;border-bottom:1px solid var(--border);padding:20px 28px;position:sticky;top:0;z-index:100}}
  .header-top{{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px}}
  .header h1{{font-size:18px;font-weight:700;color:#111;letter-spacing:-0.3px}}
  .header-sub{{font-size:12px;color:var(--muted);margin-top:2px}}
  .badge{{display:inline-block;background:#f3f0ff;color:#7c3aed;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;border:1px solid #d8b4fe}}
  .tabs{{display:flex;gap:0;border-bottom:1px solid var(--border);background:#fff;padding:0 28px;position:sticky;top:73px;z-index:99}}
  .tab{{padding:12px 18px;font-size:13px;font-weight:500;color:var(--muted);cursor:pointer;border-bottom:2px solid transparent;transition:all .15s;white-space:nowrap}}
  .tab.active{{color:#7c3aed;border-bottom-color:#7c3aed}}
  .tab:hover:not(.active){{color:#374151}}
  .content{{padding:24px 28px;max-width:1200px;margin:0 auto}}
  .section{{display:none}}.section.active{{display:block}}
  .legend{{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:20px;padding:14px 16px;background:#fff;border:1px solid var(--border);border-radius:8px}}
  .leg-item{{display:flex;align-items:center;gap:6px;font-size:12px;color:#374151}}
  .leg-dot{{width:12px;height:12px;border-radius:3px;flex-shrink:0}}
  .chart-title{{font-size:14px;font-weight:600;color:#111;margin-bottom:4px}}
  .chart-sub{{font-size:12px;color:var(--muted);margin-bottom:16px}}
  .bar-chart-wrap{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:20px 16px;margin-bottom:20px;overflow-x:auto}}
  .bar-row{{display:flex;align-items:center;margin-bottom:10px;gap:10px}}
  .bar-label{{width:130px;flex-shrink:0;font-size:12px;font-weight:500;color:#374151;text-align:right;line-height:1.3}}
  .bar-track{{flex:1;min-width:0;position:relative;height:26px}}
  .bar-stack{{height:100%;display:flex;border-radius:4px;overflow:hidden;position:relative}}
  .bar-seg{{height:100%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:600;color:#fff;overflow:hidden;transition:opacity .15s;cursor:pointer}}
  .bar-seg:hover{{opacity:.82}}
  .bar-seg span{{white-space:nowrap;padding:0 3px}}
  .bar-total{{width:62px;flex-shrink:0;font-size:11px;color:var(--muted);text-align:left;padding-left:2px}}
  .sortbar{{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;align-items:center}}
  .sort-label{{font-size:12px;color:var(--muted);font-weight:500}}
  .sort-btn{{padding:5px 12px;font-size:12px;border:1px solid var(--border);border-radius:20px;background:#fff;cursor:pointer;color:#374151;transition:all .15s}}
  .sort-btn.active{{background:#7c3aed;color:#fff;border-color:#7c3aed}}
  .scale-note{{font-size:11px;color:var(--muted);margin-bottom:12px;font-style:italic}}
  .tooltip{{position:fixed;background:#111;color:#fff;padding:8px 12px;border-radius:6px;font-size:12px;pointer-events:none;z-index:1000;opacity:0;transition:opacity .1s;max-width:220px;line-height:1.6}}
  .abst-bar-row{{display:flex;align-items:center;gap:10px;margin-bottom:12px}}
  .abst-bar-label{{width:110px;flex-shrink:0;font-size:12px;font-weight:500;color:#374151;text-align:right}}
  .abst-bar-outer{{flex:1;background:#f1f5f9;border-radius:4px;height:22px;overflow:hidden;position:relative}}
  .abst-bar-inner{{height:100%;border-radius:4px;display:flex;align-items:center;padding-left:8px}}
  .abst-bar-pct{{font-size:11px;font-weight:600;color:#fff}}
  .abst-bar-extra{{position:absolute;right:0;top:0;bottom:0;display:flex;align-items:center;padding-right:8px;font-size:11px;color:#6b7280}}
  .key-insight{{background:#faf5ff;border-left:3px solid #7c3aed;padding:12px 16px;margin:12px 0;border-radius:0 8px 8px 0;font-size:13px;color:#374151;line-height:1.6}}
  .key-insight strong{{color:#6d28d9;font-weight:600}}
  .analysis-note{{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:14px 16px;margin-bottom:20px;font-size:13px;color:#166534;line-height:1.6}}
  .analysis-note strong{{color:#14532d}}
  .section-head{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--muted);margin:24px 0 12px}}
  .muni-card{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:16px}}
  .muni-card-name{{font-size:14px;font-weight:600;color:#111;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}}
  .footer{{text-align:center;font-size:11px;color:var(--muted);padding:24px;border-top:1px solid var(--border);margin-top:8px}}
</style>
</head>
<body>

<div class="header">
  <div class="header-top">
    <div>
      <h1>Análisis Electoral Valle de Aburrá</h1>
      <div class="header-sub">Legislativas 08/03/2026 (comunas Medellín) · Presidenciales 31/05/2026 (municipios)</div>
    </div>
    <span class="badge">CES M.L.</span>
  </div>
</div>

<div class="tabs">
  <div class="tab active" onclick="showTab('comunas')">Comunas Medellín</div>
  <div class="tab" onclick="showTab('municipios')">Municipios Valle de Aburrá</div>
  <div class="tab" onclick="showTab('abstencion')">Abstención y segunda vuelta</div>
</div>

<div class="tooltip" id="tt"></div>

<div id="sec-comunas" class="content section active">
  <div class="chart-title">Resultados por comuna — Medellín</div>
  <div class="chart-sub">Barras apiladas · el largo de cada barra es proporcional al total de votos de esa comuna</div>
  <div class="legend">
    <div class="leg-item"><div class="leg-dot" style="background:#7c3aed"></div> Iván Cepeda</div>
    <div class="leg-item"><div class="leg-dot" style="background:#ea580c"></div> De La Espriella</div>
    <div class="leg-item"><div class="leg-dot" style="background:#0284c7"></div> Paloma Valencia</div>
    <div class="leg-item"><div class="leg-dot" style="background:#ca8a04"></div> Sergio Fajardo</div>
    <div class="leg-item"><div class="leg-dot" style="background:#059669"></div> Fajardo + Paloma</div>
  </div>
  <div class="sortbar">
    <span class="sort-label">Ordenar por:</span>
    <button class="sort-btn active" onclick="sortComunas('cepeda')">% Cepeda ↓</button>
    <button class="sort-btn" onclick="sortComunas('abelardo')">% Abelardo ↓</button>
    <button class="sort-btn" onclick="sortComunas('fajpal')">% Faj+Pal ↓</button>
    <button class="sort-btn" onclick="sortComunas('votos')">Votos totales</button>
  </div>
  <p class="scale-note">La longitud de cada barra refleja el peso electoral de la comuna. Las proporciones de color muestran la distribución porcentual de candidatos.</p>
  <div class="bar-chart-wrap" id="chart-comunas"></div>
</div>

<div id="sec-municipios" class="content section">
  <div class="chart-title">Resultados por municipio — Valle de Aburrá (sin Medellín)</div>
  <div class="chart-sub">Barras apiladas · el largo de cada barra es proporcional al total de votos del municipio · Presidenciales 31/05/2026</div>
  <div class="legend">
    <div class="leg-item"><div class="leg-dot" style="background:#7c3aed"></div> Iván Cepeda</div>
    <div class="leg-item"><div class="leg-dot" style="background:#ea580c"></div> De La Espriella</div>
    <div class="leg-item"><div class="leg-dot" style="background:#0284c7"></div> Paloma Valencia</div>
    <div class="leg-item"><div class="leg-dot" style="background:#ca8a04"></div> Sergio Fajardo</div>
  </div>
  <div class="sortbar">
    <span class="sort-label">Ordenar por:</span>
    <button class="sort-btn active" onclick="sortMunis('cepeda')">% Cepeda ↓</button>
    <button class="sort-btn" onclick="sortMunis('abelardo')">% Abelardo ↓</button>
    <button class="sort-btn" onclick="sortMunis('fajpal')">% Faj+Pal ↓</button>
    <button class="sort-btn" onclick="sortMunis('votos')">Votos absolutos</button>
  </div>
  <p class="scale-note">La longitud de cada barra refleja el peso electoral del municipio. Las proporciones de color muestran la distribución porcentual de candidatos.</p>
  <div class="bar-chart-wrap" id="chart-munis"></div>
</div>

<div id="sec-abstencion" class="content section">
  <div class="analysis-note">
    <strong>Pregunta estratégica:</strong> ¿vale más movilizar al abstencionista o convertir al votante de Fajardo/Paloma? Aquí se cruzan ambas variables por municipio para orientar el esfuerzo de campaña en segunda vuelta.
    <br><small style="opacity:.7">Nota: la abstención se calcula sobre estimados de censo electoral 2026. El total de votos incluye blancos y nulos (~5–7% adicional sobre los 4 candidatos principales).</small>
  </div>
  <div class="section-head">Abstención estimada por municipio</div>
  <div class="bar-chart-wrap"><div id="abst-bars"></div></div>
  <div class="section-head">Potencial de segunda vuelta: abstencionistas + votantes Fajardo/Paloma</div>
  <div class="key-insight">
    <strong>Lectura:</strong> Para cada municipio se comparan tres magnitudes contra la misma escala. La <strong style="color:#7c3aed">barra morada</strong> es el voto actual de Cepeda. La gris son los abstencionistas estimados. La verde el bloque Fajardo+Paloma disponible para transferencia.
  </div>
  <div class="bar-chart-wrap" id="potencial-bars"></div>
  <div class="section-head">Análisis por municipio — composición detallada</div>
  <div id="muni-detail-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px"></div>
</div>

<div class="footer">
  Fuente: Datos internos campaña · Preconteo Registraduría Nacional del Estado Civil · Estimados censo electoral DANE/Registraduría<br>
  Ciencia, Economía y Sociedad M.L. · Medellín, junio 2026
</div>

<script>
const CEPEDA='#7c3aed', ABEL='#ea580c', PAL='#0284c7', FAJ='#ca8a04', FAJPAL='#059669', ABST='#94a3b8';

const comunas = {comunas_json};

const municipios = {municipios_json};

const tt = document.getElementById('tt');
function showTT(e, html){{ tt.innerHTML=html; tt.style.opacity=1; moveTT(e); }}
function moveTT(e){{ tt.style.left=(e.clientX+14)+'px'; tt.style.top=(e.clientY-10)+'px'; }}
function hideTT(){{ tt.style.opacity=0; }}
document.addEventListener('mousemove', moveTT);
function fmt(n){{ return n.toLocaleString('es-CO'); }}
function fmtpct(p){{ return p.toFixed(1)+'%'; }}

function renderStackedBars(container, data, sortKey='cepeda'){{
  let sorted = [...data];
  if(sortKey==='cepeda')   sorted.sort((a,b)=>b.cepeda-a.cepeda);
  if(sortKey==='abelardo') sorted.sort((a,b)=>b.abelardo-a.abelardo);
  if(sortKey==='fajpal')   sorted.sort((a,b)=>b.fajpal-a.fajpal);
  if(sortKey==='votos')    sorted.sort((a,b)=>b.votos-a.votos);

  const maxVotos = Math.max(...sorted.map(d=>d.votos));
  const segs = [
    {{key:'cepeda',  color:CEPEDA, label:'Cepeda',  vkey:'vcep'}},
    {{key:'abelardo',color:ABEL,   label:'Abelardo', vkey:'vabe'}},
    {{key:'paloma',  color:PAL,    label:'Paloma',   vkey:'vpal'}},
    {{key:'fajardo', color:FAJ,    label:'Fajardo',  vkey:'vfaj'}},
  ];

  let html = '';
  for(const d of sorted){{
    const trackPct = (d.votos / maxVotos * 100).toFixed(2);
    html += `<div class="bar-row">
      <div class="bar-label">${{d.name}}</div>
      <div class="bar-track">
        <div class="bar-stack" style="width:${{trackPct}}%">`;
    for(const s of segs){{
      const pct   = d[s.key];
      const votos = d[s.vkey];
      const show  = pct >= 7;
      html += `<div class="bar-seg" style="width:${{pct}}%;background:${{s.color}}"
        onmouseenter="showTT(event,'<b>${{s.label}}</b><br>${{fmtpct(pct)}}<br>${{fmt(votos)}} votos')"
        onmouseleave="hideTT()">
        ${{show ? `<span>${{pct.toFixed(0)}}%</span>` : ''}}
      </div>`;
    }}
    html += `</div></div>
      <div class="bar-total">${{fmt(d.votos)}}</div>
    </div>`;
  }}
  container.innerHTML = html;
}}

function sortComunas(k){{
  document.querySelectorAll('#sec-comunas .sort-btn').forEach(b=>b.classList.remove('active'));
  event.target.classList.add('active');
  renderStackedBars(document.getElementById('chart-comunas'), comunas, k);
}}
function sortMunis(k){{
  document.querySelectorAll('#sec-municipios .sort-btn').forEach(b=>b.classList.remove('active'));
  event.target.classList.add('active');
  renderStackedBars(document.getElementById('chart-munis'), municipios, k);
}}

function renderAbstencion(){{
  const munis = municipios.map(m => {{
    const totalReal  = Math.round(m.votos / 0.93);
    const abst_votos = m.censo - totalReal;
    const abst_pct   = (abst_votos / m.censo * 100);
    const vfajpal    = m.vpal + m.vfaj;
    const potencial  = abst_votos + vfajpal;
    return {{...m, abst_pct, abst_votos, totalReal, vfajpal, potencial}};
  }}).sort((a,b)=>b.abst_pct-a.abst_pct);

  let html = '';
  for(const m of munis){{
    const color = m.abst_pct > 44 ? '#ef4444' : m.abst_pct > 38 ? '#f97316' : '#64748b';
    html += `<div class="abst-bar-row">
      <div class="abst-bar-label">${{m.name}}</div>
      <div class="abst-bar-outer">
        <div class="abst-bar-inner" style="width:${{m.abst_pct.toFixed(1)}}%;background:${{color}}">
          <span class="abst-bar-pct">${{m.abst_pct.toFixed(1)}}%</span>
        </div>
        <span class="abst-bar-extra">~${{fmt(m.abst_votos)}} no votaron</span>
      </div>
    </div>`;
  }}
  document.getElementById('abst-bars').innerHTML = html;

  const maxPot = Math.max(...munis.map(m=>m.potencial));
  let html2 = '';
  for(const m of munis.sort((a,b)=>b.potencial-a.potencial)){{
    const pctCep  = (m.vcep / maxPot * 100).toFixed(1);
    const pctAbst = (m.abst_votos / maxPot * 100).toFixed(1);
    const pctFP   = (m.vfajpal / maxPot * 100).toFixed(1);
    html2 += `<div style="margin-bottom:16px">
      <div style="font-size:12px;font-weight:600;color:#374151;margin-bottom:6px">${{m.name}}</div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
        <div style="width:80px;font-size:11px;color:var(--muted);text-align:right">Voto actual</div>
        <div style="flex:1;background:#f1f5f9;border-radius:4px;overflow:hidden;height:20px">
          <div style="width:${{pctCep}}%;background:${{CEPEDA}};height:100%;display:flex;align-items:center;padding-left:6px">
            <span style="font-size:10px;font-weight:600;color:#fff">${{fmt(m.vcep)}}</span>
          </div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
        <div style="width:80px;font-size:11px;color:var(--muted);text-align:right">Abstencionistas</div>
        <div style="flex:1;background:#f1f5f9;border-radius:4px;overflow:hidden;height:20px">
          <div style="width:${{pctAbst}}%;background:${{ABST}};height:100%;display:flex;align-items:center;padding-left:6px">
            <span style="font-size:10px;font-weight:600;color:#fff">~${{fmt(m.abst_votos)}}</span>
          </div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <div style="width:80px;font-size:11px;color:var(--muted);text-align:right">Faj+Paloma</div>
        <div style="flex:1;background:#f1f5f9;border-radius:4px;overflow:hidden;height:20px">
          <div style="width:${{pctFP}}%;background:${{FAJPAL}};height:100%;display:flex;align-items:center;padding-left:6px">
            <span style="font-size:10px;font-weight:600;color:#fff">${{fmt(m.vfajpal)}}</span>
          </div>
        </div>
      </div>
    </div>`;
  }}
  document.getElementById('potencial-bars').innerHTML = html2;

  let cards = '';
  for(const m of munis.sort((a,b)=>b.vcep-a.vcep)){{
    const ratio     = (m.potencial / m.vcep).toFixed(1);
    const prio      = m.potencial > 100000 ? 'Alta prioridad' : m.potencial > 40000 ? 'Prioridad media' : 'Secundario';
    const prioColor = m.potencial > 100000 ? '#7c3aed' : m.potencial > 40000 ? '#ca8a04' : '#6b7280';
    cards += `<div class="muni-card">
      <div class="muni-card-name">
        <span>${{m.name}}</span>
        <span style="font-size:11px;color:${{prioColor}};font-weight:600;background:${{prioColor}}18;padding:3px 8px;border-radius:12px">${{prio}}</span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px">
        <div style="background:#f5f3ff;border-radius:6px;padding:10px;text-align:center">
          <div style="font-size:18px;font-weight:700;color:#7c3aed">${{fmt(m.vcep)}}</div>
          <div style="font-size:10px;color:#6d28d9">voto Cepeda</div>
        </div>
        <div style="background:#f0fdf4;border-radius:6px;padding:10px;text-align:center">
          <div style="font-size:18px;font-weight:700;color:#059669">${{fmt(m.potencial)}}</div>
          <div style="font-size:10px;color:#065f46">potencial 2ª vuelta</div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-bottom:8px">
        <div style="text-align:center;padding:6px;background:#f9fafb;border-radius:6px">
          <div style="font-size:12px;font-weight:600;color:#475569">~${{m.abst_pct.toFixed(0)}}%</div>
          <div style="font-size:10px;color:var(--muted)">abstención</div>
        </div>
        <div style="text-align:center;padding:6px;background:#f9fafb;border-radius:6px">
          <div style="font-size:12px;font-weight:600;color:#059669">${{fmtpct(m.fajpal)}}</div>
          <div style="font-size:10px;color:var(--muted)">Faj+Pal</div>
        </div>
        <div style="text-align:center;padding:6px;background:#f9fafb;border-radius:6px">
          <div style="font-size:12px;font-weight:600;color:#374151">${{ratio}}×</div>
          <div style="font-size:10px;color:var(--muted)">mult. Cepeda</div>
        </div>
      </div>
      <div style="font-size:11px;color:var(--muted);border-top:1px solid var(--border);padding-top:8px">
        Abelardo ${{fmtpct(m.abelardo)}} · Censo ≈${{fmt(m.censo)}}
      </div>
    </div>`;
  }}
  document.getElementById('muni-detail-grid').innerHTML = cards;
}}

function showTab(name){{
  document.querySelectorAll('.tab').forEach((t,i)=>{{
    t.classList.toggle('active', ['comunas','municipios','abstencion'][i]===name);
  }});
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.getElementById('sec-'+name).classList.add('active');
}}

renderStackedBars(document.getElementById('chart-comunas'), comunas, 'cepeda');
renderStackedBars(document.getElementById('chart-munis'),   municipios, 'cepeda');
renderAbstencion();
</script>
</body>
</html>"""

ruta = os.path.join(RUTA_OUT, 'dashboard_electoral_ces.html')
with open(ruta, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"✓  {ruta}")
