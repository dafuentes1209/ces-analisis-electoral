# Análisis Electoral Medellín — CES M.L.

**Ciencia, Economía y Sociedad M.L.** — Análisis de datos electorales del Valle de Aburrá.

## Descripción

Análisis de resultados electorales por comuna en Medellín para las elecciones de Senado 2022,
con foco en los candidatos Iván Cepeda, Abelardo De La Espriella, Paloma Valencia y Sergio Fajardo.

## Estructura del proyecto

```
ces_analisis_electoral/
│
├── data/
│   ├── electoral_medellin.csv       # Datos crudos por comuna
│   └── comunas_procesadas.csv      # Datos con % y coordenadas
│
├── src/
│   ├── grafica_electoral.py        # Gráfica comparativa con matplotlib
│   └── mapa_folium.py              # Mapa interactivo con Folium
│
├── outputs/
│   ├── grafica_electoral_medellin.png
│   └── mapa_electoral_medellin.html  # Abrir en navegador
│
└── README.md
```

## Requisitos

```bash
pip install pandas matplotlib folium branca
```

## Uso

```bash
# Generar gráfica
python src/grafica_electoral.py

# Generar mapa interactivo
python src/mapa_folium.py
# Luego abrir outputs/mapa_electoral_medellin.html en el navegador
```

## Fuente de datos

- Registraduría Nacional del Estado Civil — resultados Senado 2022
- Coordenadas comunas: datos geográficos públicos de Medellín

## Próximos pasos

- [ ] Agregar datos municipio a municipio del Valle de Aburrá
- [ ] Cruzar con datos socioeconómicos (DANE — GEIH)
- [ ] Análisis de narrativa digital de la campaña
- [ ] Documento de posición final

---
*Proyecto independiente — CES M.L. · Medellín, 2026*
