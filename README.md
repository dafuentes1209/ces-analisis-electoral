# Análisis Electoral Valle de Aburrá — CES M.L.

**Ciencia, Economía y Sociedad M.L.** — Análisis de datos electorales del Valle de Aburrá, Colombia.

Proyecto independiente de análisis político-electoral que combina datos de la Registraduría Nacional
con herramientas de visualización geoespacial para entender el comportamiento electoral del
Área Metropolitana del Valle de Aburrá.

---

## Estructura del proyecto

```
ces_analisis_electoral/
│
├── data/
│   ├── electoral_medellin.csv              # Votos por comuna — Medellín (legislativas 08/03/2026)
│   ├── comunas_procesadas.csv             # Datos con % y coordenadas por comuna
│   ├── valle_aburra_presidencial_2026.csv # Votos por municipio — Valle de Aburrá (presidenciales 31/05/2026)
│   ├── medellin.geojson                   # Polígonos comunas y corregimientos de Medellín
│   └── valle_aburra_completo.geojson      # Polígonos comunas Medellín + 9 municipios Valle de Aburrá
│
├── src/
│   ├── grafica_electoral.py               # 2 gráficas de barras con matplotlib
│   └── mapa_folium.py                     # 3 mapas choropleth interactivos con Folium
│
├── outputs/
│   ├── grafica_electoral_medellin.png         # Gráfica por comunas
│   ├── grafica_valle_aburra_sin_medellin.png  # Gráfica por municipios
│   ├── mapa_cepeda.html                       # Mapa % votos Cepeda
│   ├── mapa_abelardo.html                     # Mapa % votos De La Espriella
│   └── mapa_fajardo_paloma.html               # Mapa % votos Fajardo + Paloma combinados
│
└── README.md
```

---

## Requisitos

```bash
pip install pandas matplotlib folium branca
```

## Uso

```bash
# Generar las 2 gráficas de barras
python src/grafica_electoral.py

# Generar los 3 mapas interactivos (abrir los .html en el navegador)
python src/mapa_folium.py
```

---

## Fuentes de datos

| Datos | Fuente | Elección |
|---|---|---|
| Votos por comuna — Medellín | Datos internos campaña | Legislativas 08/03/2026 |
| Votos por municipio — Valle de Aburrá | Preconteo Registraduría Nacional | Presidenciales 31/05/2026 |
| GeoJSON comunas Medellín | Portal Geográfico Medellín | — |
| GeoJSON municipios Antioquia | Metabolism of Cities / datos.gov.co | — |

---

## Hallazgos principales

**1. El voto duro de Cepeda está en el nororiente popular de Medellín**
Popular (38.2%), Santa Cruz (35%) y Manrique (33.7%) son las comunas con mejor resultado relativo.
En El Poblado apenas alcanza el 6.3%. El voto existente hay que movilizarlo, no conquistarlo.

**2. El electorado de Fajardo y Paloma es la principal oportunidad de crecimiento**
Suman entre el 18% y el 25% en comunas como Laureles, La América y Belén. Son el blanco
estratégico para segunda vuelta — no el votante duro de Abelardo.

**3. Bello es el municipio más estratégico del Valle de Aburrá**
63.055 votos para Cepeda (27.94%) y 36.896 votos combinados de Fajardo+Paloma.
Mejor relación esfuerzo/voto potencial fuera de Medellín.

**4. Envigado y Sabaneta son territorio hostil pero no abandonable**
Abelardo obtiene el 65.4% y el 61.98% respectivamente. La estrategia no es ganar
sino activar el voto abstencionista progresista y reducir la brecha.

**5. Abelardo domina en todos los municipios del Valle de Aburrá sin excepción**
Entre el 48% (Barbosa, Caldas) y el 65% (Envigado). El territorio es adverso —
la eficiencia en movilización del voto propio es clave.

**6. El perfil territorial del voto refleja una brecha socioeconómica clara**
El voto de Cepeda es consistentemente más alto en zonas de menor ingreso.
Una base electoral ideológicamente coherente que responde a propuestas redistributivas.

---

## Recomendaciones estratégicas

1. Concentrar recursos en **Popular, Santa Cruz, Manrique y Aranjuez** — voto propio que hay que movilizar.
2. Trabajar el voto **Fajardo+Paloma en Laureles, La América y Belén** — con argumentos de propuesta.
3. Priorizar **Bello** sobre los municipios del sur — mejor relación esfuerzo/voto potencial.
4. Estrategia diferenciada para **Envigado y Sabaneta** — enfocada en abstencionistas y voto joven.

---

## Próximos pasos

- [ ] Dashboard narrativo unificado estilo La Silla Vacía
- [ ] Cruzar con datos socioeconómicos DANE — GEIH
- [ ] Expandir análisis a nivel de mesa de votación
- [ ] Documento de posición formal del grupo

---

*Ciencia, Economía y Sociedad M.L. · Medellín, junio 2026*