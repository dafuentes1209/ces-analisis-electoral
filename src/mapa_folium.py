import folium
import pandas as pd
from folium.plugins import MarkerCluster
import branca.colormap as cm

df = pd.read_csv('/home/claude/comunas_procesadas.csv')

# Mapa centrado en Medellín
m = folium.Map(
    location=[6.2530, -75.5736],
    zoom_start=13,
    tiles='CartoDB positron'
)

# Escala de color para % Cepeda (azul)
colormap = cm.LinearColormap(
    colors=['#dbeafe', '#93c5fd', '#3b82f6', '#1d4ed8', '#1e3a8a'],
    vmin=df['pct_cepeda'].min(),
    vmax=df['pct_cepeda'].max(),
    caption='% votos Iván Cepeda'
)
colormap.add_to(m)

# Colores por ganador
color_ganador = {
    'Cepeda':           '#2563EB',
    'De La Espriella':  '#6B7280',
    'Paloma Valencia':  '#DB2777',
    'Fajardo':          '#059669',
}

for _, row in df.iterrows():
    popup_html = f"""
    <div style='font-family:sans-serif; font-size:13px; min-width:200px;'>
      <b style='font-size:15px'>{row['comuna']}</b><br><br>
      <table style='width:100%;border-collapse:collapse;'>
        <tr style='background:#eff6ff'><td><b>Iván Cepeda</b></td>
            <td align='right'>{int(row['ivan_cepeda']):,}</td>
            <td align='right'><b style='color:#2563EB'>{row['pct_cepeda']}%</b></td></tr>
        <tr><td>De La Espriella</td>
            <td align='right'>{int(row['abelardo_de_la_espriella']):,}</td>
            <td align='right'>{row['pct_ade']}%</td></tr>
        <tr><td>Paloma Valencia</td>
            <td align='right'>{int(row['paloma_valencia']):,}</td>
            <td align='right'>{row['pct_paloma']}%</td></tr>
        <tr><td>Sergio Fajardo</td>
            <td align='right'>{int(row['sergio_fajardo']):,}</td>
            <td align='right'>{row['pct_fajardo']}%</td></tr>
      </table><br>
      <span style='color:#6b7280;font-size:11px'>Ganador: <b>{row['ganador']}</b></span>
    </div>
    """

    radio = 300 + int(row['ivan_cepeda'] / 150)  # tamaño proporcional a votos

    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=radio / 80,
        color=colormap(row['pct_cepeda']),
        fill=True,
        fill_color=colormap(row['pct_cepeda']),
        fill_opacity=0.75,
        weight=1.5,
        popup=folium.Popup(popup_html, max_width=260),
        tooltip=f"{row['comuna']} — Cepeda: {row['pct_cepeda']}%"
    ).add_to(m)

    # Etiqueta con nombre
    folium.Marker(
        location=[row['lat'] + 0.003, row['lon']],
        icon=folium.DivIcon(
            html=f"<div style='font-size:9px;font-family:sans-serif;color:#374151;font-weight:600;white-space:nowrap;'>{row['comuna']}</div>",
            icon_size=(120, 20),
            icon_anchor=(60, 0)
        )
    ).add_to(m)

# Título
title_html = """
<div style='position:fixed;top:15px;left:50%;transform:translateX(-50%);
     background:white;padding:10px 18px;border-radius:8px;
     box-shadow:0 2px 8px rgba(0,0,0,0.15);z-index:9999;
     font-family:sans-serif;text-align:center;'>
  <b style='font-size:14px;color:#111827'>Análisis Electoral Medellín — Senado 2022</b><br>
  <span style='font-size:11px;color:#6b7280'>Círculos = votos Cepeda · Color = % sobre total 4 candidatos</span><br>
  <span style='font-size:10px;color:#9ca3af'>Ciencia, Economía y Sociedad M.L.</span>
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

m.save('/mnt/user-data/outputs/mapa_electoral_medellin.html')
print("Mapa guardado.")
