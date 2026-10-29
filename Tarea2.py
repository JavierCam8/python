import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy import stats

# ---------------------------------------------------------
# 0. CONFIGURACIÓN GENERAL Y ESTILOS
# ---------------------------------------------------------
# Cargar datos (cambiar la ruta si tu archivo está en formato .xlsx o .csv)
try:
    df = pd.read_csv(r"C:\Users\jcama\Documents\cucei\mineria de datos\Nueva carpeta\industry_dataset_structured.xlsx - industry_dataset_structured - industry_dataset_structured.xlsx - industry_dataset_structured.csv")
except Exception:
    df = pd.read_excel(r"C:\Users\jcama\Documents\cucei\mineria de datos\Nueva carpeta\industry_dataset_structured.xlsx - industry_dataset_structured - industry_dataset_structured.xlsx - industry_dataset_structured.xlsx")
# Asegurar cálculo del Batch si no existe explícitamente
if 'Batch' not in df.columns and 'Product_ID' in df.columns:
    df['Batch'] = (df['Product_ID'] - 1) // 20 + 1

# Mapeo de colores, marcadores y estilos
LINE_COLORS = {'Line_A': '#1f77b4', 'Line_B': '#ff7f0e', 'Line_C': '#2ca02c'}
LINE_MARKERS = {'Line_A': 'o', 'Line_B': 's', 'Line_C': '^'}

SHIFT_COLORS = {'Morning': '#9467bd', 'Evening': '#8c564b', 'Night': '#d62728'}
SHIFT_STYLES = {'Morning': '-', 'Evening': '--', 'Night': '-.'}


def setup_axes_style(ax):
    """Aplica la configuración general de cuadrícula y spines requerida."""
    ax.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('#222222')
        spine.set_linewidth(1.2)


# Set seaborn style general
sns.set_theme(style='white', font_scale=1.0)


# =========================================================
# FIGURA 1: Producción vs. defectos (dispersión)
# =========================================================
fig, ax = plt.subplots(figsize=(8, 6))
setup_axes_style(ax)

for line, color in LINE_COLORS.items():
    sub_df = df[df['Production_Line'] == line]
    ax.scatter(
        sub_df['Units_Produced'],
        sub_df['Defect_Rate'],
        color=color,
        marker=LINE_MARKERS[line],
        label=line,
        alpha=0.7,
        edgecolor='#1a1a1a',
        linewidth=0.6,
        s=45,
    )

ax.set_title('Fig. 1: Units_Produced vs Defect_Rate', fontweight='bold', pad=12)
ax.set_xlabel('Units_Produced')
ax.set_ylabel('Defect_Rate')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
ax.legend(title='Production_Line', loc='upper right', framealpha=0.9)
plt.tight_layout()
plt.savefig('Fig_1_Scatter_Defect_Rate.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 2: Energía vs. ingresos (dispersión + tendencia)
# =========================================================
fig, ax = plt.subplots(figsize=(8, 6))
setup_axes_style(ax)

# Datos y modelo OLS
x = df['Energy_Consumption_kWh']
y = df['Revenue_USD']
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# Puntos observaciones
ax.scatter(
    x,
    y,
    color='#90EE90',
    edgecolor='#2e8b57',
    linewidth=0.7,
    alpha=0.75,
    s=50,
    label='Observaciones',
)

# Línea OLS
x_vals = np.linspace(x.min(), x.max(), 100)
ax.plot(
    x_vals,
    intercept + slope * x_vals,
    color='#e41a1c',
    linestyle='--',
    linewidth=2,
    label='Tendencia (OLS)',
)

ax.set_title(
    f'Fig. 2: Energía vs Ingresos ($r={r_value:.2f}$)',
    fontweight='bold',
    pad=12,
)
ax.set_xlabel('Energy_Consumption_kWh')
ax.set_ylabel('Revenue_USD')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f'{val:,.0f}'))
ax.legend(loc='upper left', framealpha=0.9)
plt.tight_layout()
plt.savefig('Fig_2_Energy_vs_Revenue.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 3: Distribución de defectos (histograma)
# =========================================================
fig, ax = plt.subplots(figsize=(8, 6))
setup_axes_style(ax)

mean_val = df['Defect_Rate'].mean()
median_val = df['Defect_Rate'].median()

# Histograma
n, bins, patches = ax.hist(
    df['Defect_Rate'],
    bins=20,
    color='#87cefa',
    edgecolor='#1e90ff',
    linewidth=1.0,
    alpha=0.85,
)

# Líneas Media / Mediana
ax.axvline(
    mean_val,
    color='#2ca02c',
    linestyle='--',
    linewidth=1.8,
    label=f'Media ({mean_val:.2%})',
)
ax.axvline(
    median_val,
    color='#d62728',
    linestyle='-.',
    linewidth=1.8,
    label=f'Mediana ({median_val:.2%})',
)

# Etiquetas flotantes en las líneas
max_freq = max(n)
ax.text(
    mean_val,
    max_freq * 0.85,
    f' {mean_val:.2%}',
    color='#2ca02c',
    rotation=90,
    va='center',
    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#2ca02c'),
)
ax.text(
    median_val,
    max_freq * 0.65,
    f' {median_val:.2%}',
    color='#d62728',
    rotation=90,
    va='center',
    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#d62728'),
)

ax.set_title('Fig. 3: Distribución de Defect_Rate', fontweight='bold', pad=12)
ax.set_xlabel('Defect_Rate')
ax.set_ylabel('Frecuencia')
ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.legend(loc='upper left', framealpha=0.9)
plt.tight_layout()
plt.savefig('Fig_3_Defect_Rate_Hist.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 4: Tiempos muertos (histograma + KDE)
# =========================================================
fig, ax = plt.subplots(figsize=(8, 6))
setup_axes_style(ax)

downtime = df['Downtime_Minutes'].dropna()

# Histograma
counts, bin_edges, patches = ax.hist(
    downtime,
    bins=15,
    color='#f28e2b',
    edgecolor='#1a1a1a',
    linewidth=1.2,
    alpha=0.8,
    label='Frecuencia',
)

# Moda (centro del bin con mayor frecuencia)
max_idx = np.argmax(counts)
bin_center_mode = (bin_edges[max_idx] + bin_edges[max_idx + 1]) / 2.0
ax.axvline(
    bin_center_mode,
    color='#2ca02c',
    linestyle='--',
    linewidth=1.5,
    label='Moda (bin)',
)

# Percentiles P90 y P95
p90 = np.percentile(downtime, 90)
p95 = np.percentile(downtime, 95)

ax.axvline(
    p90, color='#1f77b4', linestyle=':', linewidth=1.5, label=f'P90 ({p90:.1f})'
)
ax.axvline(
    p95,
    color='#d62728',
    linestyle='-.',
    linewidth=1.5,
    label=f'P95 ({p95:.1f})',
)

# Sombreado cola derecha >= P95
ax.axvspan(
    p95,
    downtime.max(),
    color='#d62728',
    alpha=0.2,
    label='Cola derecha (≥P95)',
)

# KDE en eje secundario
ax2 = ax.twinx()
ax2.grid(False)  # No cuadrícula secundaria
sns.kdeplot(downtime, ax=ax2, color='#111111', linewidth=2.0, label='Densidad (KDE)')
ax2.set_ylabel('Densidad (KDE)')

# Combinar leyendas de ambos ejes
lines_1, labels_1 = ax.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', framealpha=0.9)

ax.set_title(
    'Fig. 4: Distribución de Downtime_Minutes', fontweight='bold', pad=12
)
ax.set_xlabel('Downtime_Minutes')
ax.set_ylabel('Frecuencia')
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.tight_layout()
plt.savefig('Fig_4_Downtime_Minutes_Hist.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 5: Productividad por línea (barras + error)
# =========================================================
fig, ax = plt.subplots(figsize=(8, 6))
setup_axes_style(ax)

# Cálculo de Promedio y Error Estándar (EE)
stats_line = (
    df.groupby('Production_Line')['Units_Produced']
    .agg(
        mean='mean',
        sem=lambda x: x.std() / np.sqrt(x.count()) if len(x) > 0 else 0,
    )
    .sort_values(by='mean', ascending=False)
)

bars = ax.bar(
    stats_line.index,
    stats_line['mean'],
    yerr=stats_line['sem'],
    capsize=6,
    color=[LINE_COLORS[l] for l in stats_line.index],
    edgecolor='#1a1a1a',
    linewidth=1.0,
    alpha=0.85,
)

# Etiquetas sobre barras
for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval + (yval * 0.02),
        f'{yval:.1f}',
        ha='center',
        va='bottom',
        fontweight='bold',
    )

ax.set_title(
    r'Fig. 5: Productividad promedio por línea ($\pm$EE)',
    fontweight='bold',
    pad=12,
)
ax.set_xlabel('Production_Line')
ax.set_ylabel('Units_Produced (promedio)')
plt.tight_layout()
plt.savefig('Fig_5_Productivity_by_Line.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 6: Ingresos por turno (barras + error)
# =========================================================
fig, ax = plt.subplots(figsize=(8, 6))
setup_axes_style(ax)

stats_shift = df.groupby('Shift')['Revenue_USD'].agg(
    mean='mean', sem=lambda x: x.std() / np.sqrt(x.count())
)
shift_order = ['Morning', 'Evening', 'Night']
stats_shift = stats_shift.reindex(
    [s for s in shift_order if s in stats_shift.index]
)

bars = ax.bar(
    stats_shift.index,
    stats_shift['mean'],
    yerr=stats_shift['sem'],
    capsize=6,
    color=[SHIFT_COLORS[s] for s in stats_shift.index],
    edgecolor='#1a1a1a',
    linewidth=1.0,
    alpha=0.85,
)

for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval + (yval * 0.02),
        f'{yval:,.0f}',
        ha='center',
        va='bottom',
        fontweight='bold',
    )

ax.set_title(
    r'Fig. 6: Ingresos promedio por turno ($\pm$EE)', fontweight='bold', pad=12
)
ax.set_xlabel('Shift')
ax.set_ylabel('Revenue_USD (promedio)')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f'{val:,.0f}'))
plt.tight_layout()
plt.savefig('Fig_6_Revenue_by_Shift.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 7: Costos por turno (boxplot)
# =========================================================
fig, ax = plt.subplots(figsize=(8, 6))
setup_axes_style(ax)

shifts_present = [s for s in ['Morning', 'Evening', 'Night'] if s in df['Shift'].unique()]
data_to_plot = [
    df[df['Shift'] == s]['Cost_per_Unit'].dropna() for s in shifts_present
]

bp = ax.boxplot(
    data_to_plot,
    patch_artist=True,
    notch=True,
    tick_labels=shifts_present,
    medianprops=dict(color='#d62728', linewidth=2.0),
    flierprops=dict(
        marker='o', markerfacecolor='#888888', alpha=0.6, markersize=5
    ),
)

for patch, shift in zip(bp['boxes'], shifts_present):
    patch.set_facecolor(SHIFT_COLORS[shift])
    patch.set_alpha(0.5)
    patch.set_edgecolor('#1a1a1a')
    patch.set_linewidth(1.2)

ax.set_title('Fig. 7: Cost_per_Unit por Shift (Boxplot)', fontweight='bold', pad=12)
ax.set_xlabel('Shift')
ax.set_ylabel('Cost_per_Unit')
plt.tight_layout()
plt.savefig('Fig_7_Cost_per_Unit_Boxplot.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 8: Calidad por línea y turno (boxplots 2 subgrupos)
# =========================================================
fig, ax = plt.subplots(figsize=(9, 6))
setup_axes_style(ax)

sns.boxplot(
    data=df,
    x='Production_Line',
    y='Defect_Rate',
    hue='Shift',
    hue_order=['Morning', 'Evening', 'Night'],
    palette=SHIFT_COLORS,
    ax=ax,
    fliersize=4,
    linewidth=1.2,
)

ax.set_title(
    'Fig. 8: Defect_Rate por línea y turno (Boxplots)', fontweight='bold', pad=12
)
ax.set_xlabel('Production_Line')
ax.set_ylabel('Defect_Rate')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
ax.legend(title='Shift', loc='upper left', framealpha=0.9)
plt.tight_layout()
plt.savefig('Fig_8_Defect_Rate_Line_Shift.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 9: Densidad de energía (KDE)
# =========================================================
fig, ax = plt.subplots(figsize=(8, 6))
setup_axes_style(ax)

energy = df['Energy_Consumption_kWh'].dropna()
mean_e = energy.mean()
median_e = energy.median()

sns.kdeplot(
    energy, ax=ax, color='#2ca02c', fill=True, alpha=0.25, linewidth=2, label='KDE'
)

ax.axvline(
    mean_e,
    color='#111111',
    linestyle='--',
    linewidth=1.5,
    label=f'Media ({mean_e:.1f})',
)
ax.axvline(
    median_e,
    color='#d62728',
    linestyle='-.',
    linewidth=1.5,
    label=f'Mediana ({median_e:.1f})',
)

ax.set_title(
    'Fig. 9: Densidad de Energy_Consumption_kWh', fontweight='bold', pad=12
)
ax.set_xlabel('Energy_Consumption_kWh')
ax.set_ylabel('Densidad')
ax.legend(loc='upper right', framealpha=0.9)
plt.tight_layout()
plt.savefig('Fig_9_Energy_KDE.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 10: Mapa de calor (heatmap)
# =========================================================
fig, ax = plt.subplots(figsize=(10, 8))

# Variables numéricas
num_cols = df.select_dtypes(include=[np.number]).columns
corr = df[num_cols].corr()

sns.heatmap(
    corr,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    center=0,
    vmin=-1,
    vmax=1,
    linewidths=0.5,
    cbar_kws={'label': 'Correlation (r)'},
    ax=ax,
)

ax.set_title('Fig. 10: Heatmap de correlación', fontweight='bold', pad=12)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('Fig_10_Correlation_Heatmap.png', dpi=300)
plt.show()


# =========================================================
# FIGURA 11: Tendencias con incertidumbre (líneas + bandas)
# =========================================================
fig, ax = plt.subplots(figsize=(9, 6))
setup_axes_style(ax)

# Agrupación por Batch y Línea
batch_stats = (
    df.groupby(['Batch', 'Production_Line'])['Units_Produced']
    .agg(
        mean='mean',
        sem=lambda x: x.std() / np.sqrt(x.count()) if len(x) > 1 else 0,
    )
    .reset_index()
)

for line in ['Line_A', 'Line_B', 'Line_C']:
    if line in batch_stats['Production_Line'].unique():
        sub = batch_stats[batch_stats['Production_Line'] == line]
        ax.plot(
            sub['Batch'],
            sub['mean'],
            marker=LINE_MARKERS[line],
            color=LINE_COLORS[line],
            linewidth=2,
            label=line,
        )
        ax.fill_between(
            sub['Batch'],
            sub['mean'] - sub['sem'],
            sub['mean'] + sub['sem'],
            color=LINE_COLORS[line],
            alpha=0.2,
        )

        # Etiquetar último punto
        last_row = sub.iloc[-1]
        ax.text(
            last_row['Batch'] + 0.1,
            last_row['mean'],
            line,
            color=LINE_COLORS[line],
            fontweight='bold',
            va='center',
        )

ax.set_title(
    r'Fig. 11: Tendencias Units_Produced por Línea ($\pm$EE)',
    fontweight='bold',
    pad=12,
)
ax.set_xlabel('Batch')
ax.set_ylabel('Units_Produced (media)')
ax.legend(title='Production_Line', loc='lower right', framealpha=0.9)
plt.tight_layout()
plt.savefig('Fig_11_Trends_Units_Produced.png', dpi=300)
plt.show()


# =========================================================
# FIGURAS 12-15: LIENZO COMBINADO (Subplots 2x2)[cite: 1]
# =========================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    'Figs. 12-15: Resumen de distribución, producción y relación',
    fontsize=14,
    fontweight='bold',
    y=0.98,
)

# --- FIG 12: Densidad de Temperature_C por Shift[cite: 1]
ax12 = axes[0, 0]
setup_axes_style(ax12)
for shift in ['Morning', 'Evening', 'Night']:
    sub_temp = df[df['Shift'] == shift]['Temperature_C'].dropna()
    if not sub_temp.empty:
        sns.kdeplot(
            sub_temp,
            ax=ax12,
            color=SHIFT_COLORS[shift],
            linestyle=SHIFT_STYLES[shift],
            linewidth=2,
            label=shift,
        )
ax12.set_title(
    'Fig. 12: Densidad de Temperature_C por Shift', fontweight='bold'
)
ax12.set_xlabel('Temperature_C')
ax12.set_ylabel('Densidad')
ax12.legend(title='Shift', framealpha=0.9)

# --- FIG 13: Area apilada Units_Produced por Shift (Batch)[cite: 1]
ax13 = axes[0, 1]
setup_axes_style(ax13)
pivot_batch = df.pivot_table(
    index='Batch', columns='Shift', values='Units_Produced', aggfunc='sum'
).fillna(0)
shift_cols = [s for s in ['Morning', 'Evening', 'Night'] if s in pivot_batch.columns]

ax13.stackplot(
    pivot_batch.index,
    [pivot_batch[s] for s in shift_cols],
    labels=shift_cols,
    colors=[SHIFT_COLORS[s] for s in shift_cols],
    alpha=0.85,
)
ax13.set_title(
    'Fig. 13: Área apilada Units_Produced por Shift (Batch)', fontweight='bold'
)
ax13.set_xlabel('Batch')
ax13.set_ylabel('Units_Produced (suma)')
ax13.legend(title='Shift', loc='upper left', framealpha=0.9)

# --- FIG 14: Composición de Turnos por Línea (%)[cite: 1]
ax14 = axes[1, 0]
setup_axes_style(ax14)
ct = pd.crosstab(df['Production_Line'], df['Shift'], normalize='index') * 100
shifts_order = [s for s in ['Morning', 'Evening', 'Night'] if s in ct.columns]
ct = ct[shifts_order]

bottoms = np.zeros(len(ct))
for shift in shifts_order:
    values = ct[shift].values
    bars = ax14.bar(
        ct.index,
        values,
        bottom=bottoms,
        label=shift,
        color=SHIFT_COLORS[shift],
        edgecolor='#1a1a1a',
        linewidth=0.8,
    )
    # Etiquetado interno >= 8%[cite: 1]
    for i, val in enumerate(values):
        if val >= 8.0:
            ax14.text(
                i,
                bottoms[i] + val / 2.0,
                f'{val:.0f}%',
                ha='center',
                va='center',
                color='white',
                fontweight='bold',
            )
    bottoms += values

ax14.set_title('Fig. 14: Composición de Turnos por Línea (%)', fontweight='bold')
ax14.set_xlabel('Production_Line')
ax14.set_ylabel('% de registros')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
ax14.legend(title='Shift', framealpha=0.9)

# --- FIG 15: Units_Produced vs Revenue_USD (por línea)[cite: 1]
ax15 = axes[1, 1]
setup_axes_style(ax15)
for line in ['Line_A', 'Line_B', 'Line_C']:
    sub = df[df['Production_Line'] == line]
    ax15.scatter(
        sub['Units_Produced'],
        sub['Revenue_USD'],
        color=LINE_COLORS[line],
        marker=LINE_MARKERS[line],
        label=line,
        alpha=0.7,
        edgecolor='#1a1a1a',
        linewidth=0.5,
    )

# Tendencia global opcional
x_tot = df['Units_Produced'].dropna()
y_tot = df['Revenue_USD'].dropna()
if len(x_tot) > 0:
    sl, ic, r_v, p_v, st_e = stats.linregress(x_tot, y_tot)
    x_range = np.linspace(x_tot.min(), x_tot.max(), 100)
    ax15.plot(
        x_range,
        ic + sl * x_range,
        color='#333333',
        linestyle='--',
        linewidth=1.8,
        label='Tendencia',
    )

ax15.set_title(
    'Fig. 15: Units_Produced vs Revenue_USD (por línea)', fontweight='bold'
)
ax15.set_xlabel('Units_Produced')
ax15.set_ylabel('Revenue_USD')
ax15.yaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f'{val:,.0f}'))
ax15.legend(title='Production_Line', framealpha=0.9)

plt.tight_layout()
plt.savefig('Figs_12_15_Subplots_Grid.png', dpi=300)
plt.show()