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

# ── Colores y nombres candidatos ───────────────────────────────────────────
COLORES = {
    'ivan_cepeda':              '#7c3aed',
    'abelardo_de_la_espriella': '#ea580c',
    'paloma_valencia':          '#38bdf8',
    'sergio_fajardo':           '#ca8a04',
}
NOMBRES = {
    'ivan_cepeda':              'Iván Cepeda',
    'abelardo_de_la_espriella': 'De La Espriella',
    'paloma_valencia':          'Paloma Valencia',
    'sergio_fajardo':           'Sergio Fajardo',
}

CANDIDATOS = list(COLORES.keys())

# ── Template HTML ──────────────────────────────────────────────────────────
def html_template(titulo, subtitulo, fuente, chart_id, labels_json,
                  datasets_json, altura_canvas, max_eje):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{
    background:#f4f2ed;
    font-family:'DejaVu Sans','Helvetica Neue',Arial,sans-serif;
    padding:32px 40px 40px;
  }}
  h1{{font-size:20px;font-weight:700;color:#3d3b3d;line-height:1.25;margin-bottom:6px}}
  .sub{{font-size:13px;color:#787e57;margin-bottom:4px}}
  .fuente{{font-size:11px;color:#787e57;font-style:italic;margin-bottom:28px}}
  .chart-wrap{{position:relative;width:100%;height:{altura_canvas}px}}
  .legend{{
    display:flex;flex-wrap:wrap;gap:20px;
    margin-top:20px;
    padding:12px 16px;
    background:#fff;
    border:1px solid #d6d3ca;
    border-radius:6px;
    width:fit-content;
    margin-left:auto;
  }}
  .leg-item{{display:flex;align-items:center;gap:7px;font-size:12px;color:#3d3b3d}}
  .leg-dot{{width:12px;height:12px;border-radius:2px;flex-shrink:0}}
</style>
</head>
<body>
<h1>{titulo}</h1>
<p class="sub">{subtitulo}</p>
<p class="fuente">{fuente}</p>

<div class="chart-wrap">
  <canvas id="{chart_id}"
    role="img"
    aria-label="Gráfica de barras horizontales agrupadas mostrando votos por candidato"
  ></canvas>
</div>

<div class="legend">
  <div class="leg-item"><div class="leg-dot" style="background:#7c3aed"></div>Iván Cepeda</div>
  <div class="leg-item"><div class="leg-dot" style="background:#ea580c"></div>De La Espriella</div>
  <div class="leg-item"><div class="leg-dot" style="background:#38bdf8"></div>Paloma Valencia</div>
  <div class="leg-item"><div class="leg-dot" style="background:#ca8a04"></div>Sergio Fajardo</div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
const ctx = document.getElementById('{chart_id}');
new Chart(ctx, {{
  type: 'bar',
  data: {{
    labels: {labels_json},
    datasets: {datasets_json}
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: ctx => ' ' + ctx.dataset.label + ': ' +
            ctx.parsed.x.toLocaleString('es-CO')
        }}
      }}
    }},
    scales: {{
      x: {{
        max: {max_eje},
        grid: {{
          color: '#d6d3ca',
          lineWidth: 0.8,
        }},
        border: {{ display: false }},
        ticks: {{
          color: '#787e57',
          font: {{ size: 11 }},
          callback: v => v.toLocaleString('es-CO')
        }}
      }},
      y: {{
        grid: {{ display: false }},
        border: {{ display: false }},
        ticks: {{
          color: '#3d3b3d',
          font: {{ size: 12 }},
          crossAlign: 'far',
        }}
      }}
    }},
    layout: {{ padding: {{ left: 4, right: 16 }} }}
  }}
}});
</script>
</body>
</html>"""


def build_datasets(df, candidatos):
    datasets = []
    for cand in candidatos:
        datasets.append({
            'label':           NOMBRES[cand],
            'data':            df[cand].tolist(),
            'backgroundColor': COLORES[cand] + 'eb',
            'borderColor':     COLORES[cand],
            'borderWidth':     0,
            'borderRadius':    3,
            'borderSkipped':   False,
        })
    return datasets


# ══════════════════════════════════════════════════════════════════════════
# GRÁFICA 1 — Comunas de Medellín
# ══════════════════════════════════════════════════════════════════════════
df = pd.read_csv(RUTA_CSV_MED)
df = df[~df['codigo'].isin([90, 98, 99])].copy()
df = df.sort_values('ivan_cepeda', ascending=True)

labels_med   = df['comuna'].tolist()
datasets_med = build_datasets(df, CANDIDATOS)
max_med      = int(df[CANDIDATOS].max().max() * 1.08)
altura_med   = max(480, len(labels_med) * 44 + 80)

html = html_template(
    titulo         = 'Resultados electorales por comuna — Medellín',
    subtitulo      = 'Elecciones legislativas 08/03/2026 · Votos por candidato en las 16 comunas',
    fuente         = 'Fuente: Datos internos campaña · Registraduría Nacional del Estado Civil · Ciencia, Economía y Sociedad M.L.',
    chart_id       = 'chartMedellin',
    labels_json    = json.dumps(labels_med, ensure_ascii=False),
    datasets_json  = json.dumps(datasets_med, ensure_ascii=False),
    altura_canvas  = altura_med,
    max_eje        = max_med,
)

ruta_html = os.path.join(RUTA_OUT, 'grafica_electoral_medellin.html')
with open(ruta_html, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"✓  {ruta_html}")


# ══════════════════════════════════════════════════════════════════════════
# GRÁFICA 2 — Municipios del Valle de Aburrá (sin Medellín)
# ══════════════════════════════════════════════════════════════════════════
df_valle = pd.read_csv(RUTA_CSV_VALLE)
df_valle = df_valle.sort_values('ivan_cepeda', ascending=True)

labels_valle   = df_valle['municipio'].tolist()
datasets_valle = build_datasets(df_valle, CANDIDATOS)
max_valle      = int(df_valle[CANDIDATOS].max().max() * 1.08)
altura_valle   = max(360, len(labels_valle) * 44 + 80)

html2 = html_template(
    titulo         = 'Resultados electorales por municipio — Valle de Aburrá (sin Medellín)',
    subtitulo      = 'Elecciones presidenciales 31/05/2026 · 9 municipios del Área Metropolitana',
    fuente         = 'Fuente: Preconteo Registraduría Nacional del Estado Civil · Ciencia, Economía y Sociedad M.L.',
    chart_id       = 'chartValle',
    labels_json    = json.dumps(labels_valle, ensure_ascii=False),
    datasets_json  = json.dumps(datasets_valle, ensure_ascii=False),
    altura_canvas  = altura_valle,
    max_eje        = max_valle,
)

ruta_html2 = os.path.join(RUTA_OUT, 'grafica_valle_aburra_sin_medellin.html')
with open(ruta_html2, 'w', encoding='utf-8') as f:
    f.write(html2)
print(f"✓  {ruta_html2}")