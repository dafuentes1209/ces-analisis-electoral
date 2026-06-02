import folium
import pandas as pd
import json
import branca.colormap as cm

# ── Rutas ──────────────────────────────────────────────────────────────────
RUTA_CSV_MED   = r'C:\Users\david\Downloads\ces_analisis_electoral\data\comunas_procesadas.csv'
RUTA_CSV_VALLE = r'C:\Users\david\Downloads\ces_analisis_electoral\data\valle_aburra_presidencial_2026.csv'
RUTA_GEO       = r'C:\Users\david\Downloads\ces_analisis_electoral\data\valle_aburra_completo.geojson'
RUTA_OUT       = r'C:\Users\david\Downloads\ces_analisis_electoral\outputs'

# ── Datos Medellín (comunas) ───────────────────────────────────────────────
df_med = pd.read_csv(RUTA_CSV_MED)
df_med['nombre_geo'] = df_med['comuna'].str.replace('Laureles-Estadio', 'Laureles Estadio')

total_med = (df_med['ivan_cepeda'] + df_med['abelardo_de_la_espriella'] +
             df_med['paloma_valencia'] + df_med['sergio_fajardo'])
df_med['pct_cepeda']         = (df_med['ivan_cepeda'] / total_med * 100).round(1)
df_med['pct_ade']             = (df_med['abelardo_de_la_espriella'] / total_med * 100).round(1)
df_med['pct_paloma']          = (df_med['paloma_valencia'] / total_med * 100).round(1)
df_med['pct_fajardo']         = (df_med['sergio_fajardo'] / total_med * 100).round(1)
df_med['pct_fajardo_paloma']  = (df_med['pct_fajardo'] + df_med['pct_paloma']).round(1)
df_med['tipo'] = 'comuna'

# ── Datos Valle de Aburrá (municipios) ────────────────────────────────────
df_val = pd.read_csv(RUTA_CSV_VALLE)
df_val['nombre_geo'] = df_val['municipio'].str.upper()

df_val['pct_cepeda']         = df_val['pct_cepeda'].round(1)
df_val['pct_ade']             = df_val['pct_abelardo'].round(1)
df_val['pct_paloma']          = df_val['pct_paloma'].round(1)
df_val['pct_fajardo']         = df_val['pct_fajardo'].round(1)
df_val['pct_fajardo_paloma']  = (df_val['pct_fajardo'] + df_val['pct_paloma']).round(1)
df_val.rename(columns={
    'abelardo_de_la_espriella': 'abelardo_de_la_espriella',
    'ivan_cepeda': 'ivan_cepeda',
    'paloma_valencia': 'paloma_valencia',
    'sergio_fajardo': 'sergio_fajardo'
}, inplace=True)
df_val['tipo'] = 'municipio'

# Renombrar columna de votos para que coincida con Medellín
df_val['abelardo_de_la_espriella'] = df_val['abelardo_de_la_espriella']

# ── Cargar GeoJSON combinado ───────────────────────────────────────────────
with open(RUTA_GEO, encoding='utf-8') as f:
    geojson = json.load(f)

# ── Función principal ──────────────────────────────────────────────────────
def generar_mapa(columna_pct, colores, titulo, subtitulo, nombre_archivo):

    # Combinar datos Medellín + municipios en un diccionario unificado
    data = {}
    for _, row in df_med.iterrows():
        data[row['nombre_geo']] = row.to_dict()
    for _, row in df_val.iterrows():
        data[row['nombre_geo']] = row.to_dict()

    vals = [v[columna_pct] for v in data.values() if columna_pct in v]
    colormap = cm.LinearColormap(
        colors=colores,
        vmin=min(vals),
        vmax=max(vals),
        caption=subtitulo
    )

    m = folium.Map(location=[6.2100, -75.5736], zoom_start=11, tiles='CartoDB positron')
    colormap.add_to(m)

    def estilo(feature):
        nombre = feature['properties'].get('NOMBRE', '')
        if nombre not in data or columna_pct not in data[nombre]:
            return {'fillColor': '#e5e7eb', 'color': '#9ca3af', 'weight': 1, 'fillOpacity': 0.3}
        peso = 2 if data[nombre].get('tipo') == 'municipio' else 1
        return {
            'fillColor': colormap(data[nombre][columna_pct]),
            'color': '#374151',
            'weight': peso,
            'fillOpacity': 0.8
        }

    def resaltar(feature):
        return {'fillOpacity': 0.95, 'weight': 3, 'color': '#111827'}

    tooltip = folium.GeoJsonTooltip(
        fields=['NOMBRE'],
        aliases=['Zona:'],
        style='font-family:sans-serif;font-size:12px;'
    )

    # Agregar popup_html a cada feature
    for feature in geojson['features']:
        nombre = feature['properties'].get('NOMBRE', '')
        if nombre in data:
            r = data[nombre]
            tipo_label = 'Municipio' if r.get('tipo') == 'municipio' else 'Comuna'
            fuente = 'Preconteo Registraduría 31/05/2026' if r.get('tipo') == 'municipio' else 'Datos campaña 08/03/2026'

            ic  = int(r.get('ivan_cepeda', 0))
            ade = int(r.get('abelardo_de_la_espriella', 0))
            pv  = int(r.get('paloma_valencia', 0))
            sf  = int(r.get('sergio_fajardo', 0))

            html = f"""
            <div style='font-family:sans-serif;font-size:13px;min-width:230px;'>
              <b style='font-size:15px'>{nombre}</b>
              <span style='font-size:10px;color:#6b7280;margin-left:6px;'>{tipo_label}</span><br><br>
              <table style='width:100%;border-collapse:collapse;'>
                <tr style='background:#ede9fe'>
                  <td><b>Iván Cepeda</b></td>
                  <td align='right'>{ic:,}</td>
                  <td align='right'><b style='color:#7c3aed'>{r['pct_cepeda']}%</b></td>
                </tr>
                <tr style='background:#fff7ed'>
                  <td>De La Espriella</td>
                  <td align='right'>{ade:,}</td>
                  <td align='right'><b style='color:#ea580c'>{r['pct_ade']}%</b></td>
                </tr>
                <tr style='background:#f0f9ff'>
                  <td>Paloma Valencia</td>
                  <td align='right'>{pv:,}</td>
                  <td align='right'><b style='color:#0284c7'>{r['pct_paloma']}%</b></td>
                </tr>
                <tr style='background:#fefce8'>
                  <td>Sergio Fajardo</td>
                  <td align='right'>{sf:,}</td>
                  <td align='right'><b style='color:#ca8a04'>{r['pct_fajardo']}%</b></td>
                </tr>
                <tr style='border-top:1px solid #e5e7eb'>
                  <td><b>Fajardo + Paloma</b></td>
                  <td align='right'></td>
                  <td align='right'><b style='color:#16a34a'>{r['pct_fajardo_paloma']}%</b></td>
                </tr>
              </table>
              <div style='margin-top:6px;font-size:9px;color:#9ca3af;font-style:italic;'>
                Fuente: {fuente} · CES M.L.
              </div>
            </div>
            """
            feature['properties']['popup_html'] = html
        else:
            feature['properties']['popup_html'] = feature['properties'].get('NOMBRE', '')

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
         font-family:sans-serif;text-align:center;max-width:500px;'>
      <b style='font-size:14px;color:#111827'>{titulo}</b><br>
      <span style='font-size:11px;color:#6b7280'>{subtitulo}</span><br>
      <span style='font-size:10px;color:#9ca3af'>Ciencia, Economía y Sociedad M.L. · Datos: Registraduría Nacional</span>
    </div>
    """))

    # Leyenda
    m.get_root().html.add_child(folium.Element("""
    <div style='position:fixed;bottom:40px;left:20px;z-index:9999;
         background:white;padding:10px 14px;border-radius:8px;
         box-shadow:0 2px 8px rgba(0,0,0,0.12);font-family:sans-serif;font-size:11px;'>
      <b style='color:#374151;'>Zonas</b><br><br>
      <div style='display:flex;align-items:center;gap:6px;margin-bottom:5px;'>
        <div style='width:18px;height:3px;background:#374151;'></div>
        Borde grueso = municipio
      </div>
      <div style='display:flex;align-items:center;gap:6px;'>
        <div style='width:18px;height:1px;background:#374151;'></div>
        Borde fino = comuna Medellín
      </div>
    </div>
    """))

    ruta = RUTA_OUT + '\\' + nombre_archivo
    m.save(ruta)
    print(f"✓ Guardado: {nombre_archivo}")


# ── Generar los tres mapas ─────────────────────────────────────────────────
generar_mapa(
    columna_pct='pct_cepeda',
    colores=['#ede9fe', '#c4b5fd', '#7c3aed', '#5b21b6', '#3b0764'],
    titulo='Análisis Electoral Valle de Aburrá — Iván Cepeda',
    subtitulo='% votos Cepeda · Comunas Medellín (03/2026) + Municipios Valle de Aburrá (05/2026)',
    nombre_archivo='mapa_cepeda.html'
)

generar_mapa(
    columna_pct='pct_ade',
    colores=['#fff7ed', '#fed7aa', '#fb923c', '#ea580c', '#9a3412'],
    titulo='Análisis Electoral Valle de Aburrá — De La Espriella',
    subtitulo='% votos De La Espriella · Comunas Medellín (03/2026) + Municipios Valle de Aburrá (05/2026)',
    nombre_archivo='mapa_abelardo.html'
)

generar_mapa(
    columna_pct='pct_fajardo_paloma',
    colores=['#f0fdf4', '#bbf7d0', '#4ade80', '#16a34a', '#14532d'],
    titulo='Análisis Electoral Valle de Aburrá — Fajardo + Paloma Valencia',
    subtitulo='% votos combinados · Comunas Medellín (03/2026) + Municipios Valle de Aburrá (05/2026)',
    nombre_archivo='mapa_fajardo_paloma.html'
)
