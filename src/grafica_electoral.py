import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import rcParams
 
# ── Sistema de diseño inspirado en La Silla Vacía ─────────────────────────
rcParams['font.family']        = 'DejaVu Sans'
rcParams['axes.spines.top']    = False
rcParams['axes.spines.right']  = False
rcParams['axes.spines.left']   = False
rcParams['axes.spines.bottom'] = False
 
FONDO       = '#f4f2ed'
TEXTO_PRINC = '#3d3b3d'
TEXTO_SEC   = '#787e57'
GRID_COLOR  = '#d6d3ca'
 
# ── Colores candidatos ─────────────────────────────────────────────────────
COLORES = {
    'ivan_cepeda':               '#7c3aed',
    'abelardo_de_la_espriella':  '#ea580c',
    'paloma_valencia':           '#38bdf8',
    'sergio_fajardo':            '#ca8a04',
}
NOMBRES = {
    'ivan_cepeda':               'Iván Cepeda',
    'abelardo_de_la_espriella':  'De La Espriella',
    'paloma_valencia':           'Paloma Valencia',
    'sergio_fajardo':            'Sergio Fajardo',
}
 
# ── Datos ──────────────────────────────────────────────────────────────────
df = pd.read_csv(r'C:\Users\david\Downloads\ces_analisis_electoral\data\electoral_medellin.csv')
df = df[~df['codigo'].isin([90, 98, 99])].copy()
df = df.sort_values('ivan_cepeda', ascending=True)
 
candidatos = list(COLORES.keys())
n          = len(df)
bar_h      = 0.19
y          = range(n)
 
# ── Figura ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor(FONDO)
ax.set_facecolor(FONDO)
 
for i, cand in enumerate(candidatos):
    offset = (i - 1.5) * bar_h
    ax.barh(
        [yi + offset for yi in y],
        df[cand],
        height=bar_h,
        color=COLORES[cand],
        label=NOMBRES[cand],
        alpha=0.92,
        zorder=3
    )
 
# ── Ejes ───────────────────────────────────────────────────────────────────
ax.set_yticks(list(y))
ax.set_yticklabels(df['comuna'], fontsize=11, color=TEXTO_PRINC)
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.'))
)
ax.tick_params(axis='x', labelsize=9, colors=TEXTO_SEC, length=0)
ax.tick_params(axis='y', length=0)
ax.set_xlabel('Votos', fontsize=10, color=TEXTO_SEC, labelpad=12)
ax.grid(axis='x', linestyle='--', linewidth=0.6,
        alpha=0.6, color=GRID_COLOR, zorder=0)
ax.axvline(0, color=GRID_COLOR, linewidth=1, zorder=2)
 
# ── Títulos ────────────────────────────────────────────────────────────────
fig.text(
    0.07, 0.97,
    'Resultados electorales por comuna — Medellín',
    ha='left', va='top',
    fontsize=17, fontweight='bold', color=TEXTO_PRINC
)
fig.text(
    0.07, 0.935,
    'Elecciones legislativas 08/03/2026 · Votos por candidato en las 16 comunas',
    ha='left', va='top',
    fontsize=11, color=TEXTO_SEC
)
fig.text(
    0.07, 0.905,
    'Fuente: Datos internos campaña · Registraduría Nacional del Estado Civil · Ciencia, Economía y Sociedad M.L.',
    ha='left', va='top',
    fontsize=9, color=TEXTO_SEC, style='italic'
)
 
# ── Leyenda ────────────────────────────────────────────────────────────────
ax.legend(
    loc='lower right',
    fontsize=10,
    framealpha=1,
    edgecolor=GRID_COLOR,
    facecolor=FONDO,
    labelcolor=TEXTO_PRINC
)
 
plt.tight_layout(rect=[0, 0, 1, 0.90])
plt.savefig(
    r'C:\Users\david\Downloads\ces_analisis_electoral\outputs\grafica_electoral_medellin.png',
    dpi=160,
    bbox_inches='tight',
    facecolor=FONDO
)
print("Gráfica guardada.")
 
 
# ══════════════════════════════════════════════════════════════════════════════
# GRÁFICA 2 — Municipios del Valle de Aburrá (sin Medellín)
# ══════════════════════════════════════════════════════════════════════════════
 
# ── Datos Valle de Aburrá ─────────────────────────────────────────────────
df_valle = pd.read_csv(r'C:\Users\david\Downloads\ces_analisis_electoral\data\valle_aburra_presidencial_2026.csv')
df_valle = df_valle.sort_values('ivan_cepeda', ascending=True)
 
n2    = len(df_valle)
y2    = range(n2)
 
fig2, ax2 = plt.subplots(figsize=(13, 7))
fig2.patch.set_facecolor(FONDO)
ax2.set_facecolor(FONDO)
 
COLORES_VALLE = {
    'ivan_cepeda':               '#7c3aed',
    'abelardo_de_la_espriella':  '#ea580c',
    'paloma_valencia':           '#38bdf8',
    'sergio_fajardo':            '#ca8a04',
}
 
for i, cand in enumerate(COLORES_VALLE.keys()):
    offset = (i - 1.5) * bar_h
    ax2.barh(
        [yi + offset for yi in y2],
        df_valle[cand],
        height=bar_h,
        color=COLORES_VALLE[cand],
        label=NOMBRES[cand],
        alpha=0.92,
        zorder=3
    )
 
ax2.set_yticks(list(y2))
ax2.set_yticklabels(df_valle['municipio'], fontsize=11, color=TEXTO_PRINC)
ax2.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.'))
)
ax2.tick_params(axis='x', labelsize=9, colors=TEXTO_SEC, length=0)
ax2.tick_params(axis='y', length=0)
ax2.set_xlabel('Votos', fontsize=10, color=TEXTO_SEC, labelpad=12)
ax2.grid(axis='x', linestyle='--', linewidth=0.6,
         alpha=0.6, color=GRID_COLOR, zorder=0)
ax2.axvline(0, color=GRID_COLOR, linewidth=1, zorder=2)
 
fig2.text(
    0.07, 0.97,
    'Resultados electorales por municipio — Valle de Aburrá (sin Medellín)',
    ha='left', va='top',
    fontsize=17, fontweight='bold', color=TEXTO_PRINC
)
fig2.text(
    0.07, 0.935,
    'Elecciones presidenciales 31/05/2026 · 9 municipios del Área Metropolitana',
    ha='left', va='top',
    fontsize=10, color=TEXTO_SEC
)
fig2.text(
    0.07, 0.905,
    'Fuente: Preconteo Registraduría Nacional del Estado Civil · Ciencia, Economía y Sociedad M.L.',
    ha='left', va='top',
    fontsize=9, color=TEXTO_SEC, style='italic'
)
 
ax2.legend(
    loc='lower right',
    fontsize=10,
    framealpha=1,
    edgecolor=GRID_COLOR,
    facecolor=FONDO,
    labelcolor=TEXTO_PRINC
)
 
plt.tight_layout(rect=[0, 0, 1, 0.90])
plt.savefig(
    r'C:\Users\david\Downloads\ces_analisis_electoral\outputs\grafica_valle_aburra_sin_medellin.png',
    dpi=160,
    bbox_inches='tight',
    facecolor=FONDO
)
print("Gráfica Valle de Aburrá guardada.")