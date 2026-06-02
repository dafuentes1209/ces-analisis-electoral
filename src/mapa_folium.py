import folium
import pandas as pd
import json
import branca.colormap as cm

# ── Rutas ──────────────────────────────────────────────────────────────────
RUTA_CSV    = r'C:\Users\david\Downloads\ces_analisis_electoral\data\comunas_procesadas.csv'
RUTA_GEO    = r'C:\Users\david\Downloads\ces_analisis_electoral\data\medellin.geojson'
RUTA_OUT    = r'C:\Users\david\Downloads\ces_analisis_electoral\outputs'

# ── Datos ──────────────────────────────────────────────────────────────────
df = pd.read_csv(RUTA_CSV)
df['comuna_geo'] = df['comuna'].str.replace('Laureles-Estadio', 'Laureles Estadio')

total = df['ivan_cepeda'] + df['abelardo_de_la_espriella'] + df['paloma_valencia'] + df['sergio_fajardo']
df['pct_cepeda']  = (df['ivan_cepeda'] / total * 100).round(1)
df['pct_ade']     = (df['abelardo_de_la_espriella'] / total * 100).round(1)
df['pct_paloma']  = (df['paloma_valencia'] / total * 100).round(1)
df['pct_fajardo'] = (df['sergio_fajardo'] / total * 100).round(1)
df['pct_fajardo_paloma'] = (df['pct_fajardo'] + df['pct_paloma']).round(1)

with open(RUTA_GEO, encoding='utf-8') as f:
    geojson = json.load(f)

# ── Función principal ──────────────────────────────────────────────────────
def generar_mapa(columna_pct, colores, titulo, subtitulo, nombre_archivo):
    data = df.set_index('comuna_geo').to_dict('index')
    vals = [v[columna_pct] for v in data.values()]

    colormap = cm.LinearColormap(
        colors=colores,
        vmin=min(vals),
        vmax=max(vals),
        caption=subtitulo
    )

    m = folium.Map(location=[6.2530, -75.5736], zoom_start=12, tiles='CartoDB positron')
    colormap.add_to(m)

    def estilo(feature):
        nombre = feature['properties'].get('NOMBRE', '')
        if nombre not in data:
            return {'fillColor': '#e5e7eb', 'color': '#9ca3af', 'weight': 1, 'fillOpacity': 0.3}
        return {
            'fillColor': colormap(data[nombre][columna_pct]),
            'color': '#374151',
            'weight': 1.5,
            'fillOpacity': 0.8
        }

    def resaltar(feature):
        return {'fillOpacity': 0.95, 'weight': 3, 'color': '#111827'}

    # Tooltip al pasar el mouse
    tooltip = folium.GeoJsonTooltip(
        fields=['NOMBRE'],
        aliases=['Comuna:'],
        style='font-family:sans-serif;font-size:12px;'
    )

    # Popup al hacer clic
    for feature in geojson['features']:
        nombre = feature['properties'].get('NOMBRE', '')
        if nombre in data:
            r = data[nombre]
            html = f"""
            <div style='font-family:sans-serif;font-size:13px;min-width:220px;'>
              <b style='font-size:15px'>{nombre}</b><br><br>
              <table style='width:100%;border-collapse:collapse;'>
                <tr style='background:#eff6ff'>
                  <td><b>Iván Cepeda</b></td>
                  <td align='right'>{int(r['ivan_cepeda']):,}</td>
                  <td align='right'><b style='color:#2563EB'>{r['pct_cepeda']}%</b></td>
                </tr>
                <tr>
                  <td>De La Espriella</td>
                  <td align='right'>{int(r['abelardo_de_la_espriella']):,}</td>
                  <td align='right'>{r['pct_ade']}%</td>
                </tr>
                <tr style='background:#fdf4ff'>
                  <td>Paloma Valencia</td>
                  <td align='right'>{int(r['paloma_valencia']):,}</td>
                  <td align='right'><b style='color:#DB2777'>{r['pct_paloma']}%</b></td>
                </tr>
                <tr style='background:#f0fdf4'>
                  <td>Sergio Fajardo</td>
                  <td align='right'>{int(r['sergio_fajardo']):,}</td>
                  <td align='right'><b style='color:#059669'>{r['pct_fajardo']}%</b></td>
                </tr>
                <tr style='background:#fefce8'>
                  <td><b>Fajardo + Paloma</b></td>
                  <td align='right'></td>
                  <td align='right'><b style='color:#ca8a04'>{r['pct_fajardo_paloma']}%</b></td>
                </tr>
              </table>
            </div>
            """
            feature['properties']['popup_html'] = html

    folium.GeoJson(
        geojson,
        style_function=estilo,
        highlight_function=resaltar,
        tooltip=tooltip,
        popup=folium.GeoJsonPopup(fields=['popup_html'], aliases=[''], labels=False)
    ).add_to(m)

    # Título
    m.get_root().html.add_child(folium.Element(f"""
    <div style='position:fixed;top:15px;left:50%;transform:translateX(-50%);
         background:white;padding:10px 18px;border-radius:8px;
         box-shadow:0 2px 8px rgba(0,0,0,0.15);z-index:9999;
         font-family:sans-serif;text-align:center;'>
      <b style='font-size:14px;color:#111827'>{titulo}</b><br>
      <span style='font-size:11px;color:#6b7280'>{subtitulo}</span><br>
      <span style='font-size:10px;color:#9ca3af'>Ciencia, Economía y Sociedad M.L.</span>
    </div>
    """))

    ruta = RUTA_OUT + '\\' + nombre_archivo
    m.save(ruta)
    print(f"✓ Guardado: {nombre_archivo}")

# ── Generar los tres mapas ─────────────────────────────────────────────────
generar_mapa(
    columna_pct='pct_cepeda',
    colores=['#ede9fe', '#c4b5fd', '#7c3aed', '#5b21b6', '#3b0764'],
    titulo='Análisis Electoral Medellín — Iván Cepeda',
    subtitulo='% votos Cepeda por comuna · Senado 2022',
    nombre_archivo='mapa_cepeda.html'
)

generar_mapa(
    columna_pct='pct_ade',
    colores=['#fff7ed', '#fed7aa', '#fb923c', '#ea580c', '#9a3412'],
    titulo='Análisis Electoral Medellín — De La Espriella',
    subtitulo='% votos De La Espriella por comuna · Senado 2022',
    nombre_archivo='mapa_abelardo.html'
)

generar_mapa(
    columna_pct='pct_fajardo_paloma',
    colores=['#f0fdf4', '#bbf7d0', '#4ade80', '#16a34a', '#14532d'],
    titulo='Análisis Electoral Medellín — Fajardo + Paloma Valencia',
    subtitulo='% votos combinados Fajardo + Paloma por comuna · Senado 2022',
    nombre_archivo='mapa_fajardo_paloma.html'
)