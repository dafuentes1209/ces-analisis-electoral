import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Cargar datos
df = pd.read_csv('/mnt/user-data/outputs/electoral_medellin.csv')

# Excluir filas no-comunas para la gráfica principal
df_comunas = df[~df['codigo'].isin([90, 98, 99])].copy()
df_comunas = df_comunas.sort_values('ivan_cepeda', ascending=True)

# Colores por candidato
colores = {
    'ivan_cepeda':               '#2563EB',
    'abelardo_de_la_espriella':  '#6B7280',
    'paloma_valencia':           '#DB2777',
    'sergio_fajardo':            '#059669',
}
nombres = {
    'ivan_cepeda':               'Iván Cepeda',
    'abelardo_de_la_espriella':  'De La Espriella',
    'paloma_valencia':           'Paloma Valencia',
    'sergio_fajardo':            'Sergio Fajardo',
}

candidatos = list(colores.keys())
n = len(df_comunas)
bar_height = 0.18
y = range(n)

fig, ax = plt.subplots(figsize=(13, 9))
fig.patch.set_facecolor('#F8FAFC')
ax.set_facecolor('#F8FAFC')

for i, cand in enumerate(candidatos):
    offset = (i - 1.5) * bar_height
    bars = ax.barh(
        [yi + offset for yi in y],
        df_comunas[cand],
        height=bar_height,
        color=colores[cand],
        label=nombres[cand],
        alpha=0.92
    )

ax.set_yticks(list(y))
ax.set_yticklabels(df_comunas['comuna'], fontsize=10)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.')))
ax.set_xlabel('Votos', fontsize=11, color='#374151')
ax.set_title('Resultados electorales por comuna — Medellín\nCepeda · De La Espriella · Paloma Valencia · Fajardo',
             fontsize=13, fontweight='bold', color='#111827', pad=15)

ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
ax.grid(axis='x', linestyle='--', alpha=0.4, color='#9CA3AF')
ax.spines[['top','right','left']].set_visible(False)
ax.tick_params(axis='y', length=0)

# Resaltar comunas donde Cepeda gana
for i, (_, row) in enumerate(df_comunas.iterrows()):
    if row['ivan_cepeda'] > row['abelardo_de_la_espriella']:
        ax.axhspan(i - 0.45, i + 0.45, color='#2563EB', alpha=0.06)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/grafica_electoral_medellin.png', dpi=150, bbox_inches='tight')
print("Gráfica guardada.")
