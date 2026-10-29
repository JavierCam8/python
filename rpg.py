import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# 1. Cargar el dataset
df = pd.read_csv(r"C:\Users\jcama\Documents\cucei\mineria de datos\Nueva carpeta\RPG.csv")

# 2. Seleccionar SOLO las columnas numéricas para el PCA
X = df.select_dtypes(include=['number'])

# 3. Estandarizar las características numéricas
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Aplicar PCA (reducir a 2 componentes)
pca = PCA(n_components=2)
componentes = pca.fit_transform(X_scaled)

# 5. Crear el DataFrame con los resultados
df_pca = pd.DataFrame(data=componentes, columns=['PC1', 'PC2'])
df_pca['Class'] = df['Class']

# --- NUEVO: 6. Integración de K-Means ---
# Definimos K igual al número de clases únicas reales (o puedes poner un entero manual como k = 3)
k = len(df['Class'].unique())

# Instanciar y entrenar K-Means usando las 2 componentes del PCA
kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
df_pca['Cluster'] = kmeans.fit_predict(componentes)

# Extraer las coordenadas de los centroides calculados
centroides = kmeans.cluster_centers_

# 7. Imprimir varianza explicada
varianza = pca.explained_variance_ratio_
print(f"Varianza PC1: {varianza[0]:.2%}")
print(f"Varianza PC2: {varianza[1]:.2%}")
print(f"Varianza Total: {sum(varianza):.2%}")

# --- NUEVO: 8. Visualización comparativa (Clases Reales vs K-Means) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Gráfico 1: Clases reales del dataset
for clase in df_pca['Class'].unique():
    subset = df_pca[df_pca['Class'] == clase]
    ax1.scatter(subset['PC1'], subset['PC2'], label=str(clase), alpha=0.6)

ax1.set_title("Clases Reales (RPG)")
ax1.set_xlabel(f"PC1 ({varianza[0]:.1%})")
ax1.set_ylabel(f"PC2 ({varianza[1]:.1%})")
ax1.legend()
ax1.grid(True)

# Gráfico 2: Agrupamiento encontrado por K-Means y sus Centroides
for cluster_id in range(k):
    subset = df_pca[df_pca['Cluster'] == cluster_id]
    ax2.scatter(subset['PC1'], subset['PC2'], label=f"Cluster {cluster_id}", alpha=0.8)

# Graficar los centroides marcados con una 'X' roja
ax2.scatter(centroides[:, 0], centroides[:, 1], c='red', s=200, marker='X', label='Centroides')

ax2.set_title(f"Agrupamiento K-Means (K={k})")
ax2.set_xlabel(f"PC1 ({varianza[0]:.1%})")
ax2.set_ylabel(f"PC2 ({varianza[1]:.1%})")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()