import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

# ==========================================
# 1. CONSTRUCCIÓN DEL GRAFO
# ==========================================
print("1. Cargando datos y construyendo grafo...")
path_edges = r"C:\Users\jcama\Documents\cucei\mineria de datos\Nueva carpeta (2)\twitch\twitch\PTBR\musae_PTBR_edges.csv"
path_target = r"C:\Users\jcama\Documents\cucei\mineria de datos\Nueva carpeta (2)\twitch\twitch\PTBR\musae_PTBR_target.csv"

df_edges = pd.read_csv(path_edges)
df_target = pd.read_csv(path_target)

col_source, col_target = df_edges.columns[0], df_edges.columns[1]

G = nx.from_pandas_edgelist(df_edges, source=col_source, target=col_target)
target_dict = dict(zip(df_target['new_id'], df_target['mature']))
nx.set_node_attributes(G, target_dict, name='mature')

print(f"   Grafo construido: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas.")

# ==========================================
# 2. DIBUJAR RED (GRIS Y TARGET)
# ==========================================
print("2. Generando visualización inicial de la red...")
seed_pos = 42
pos = nx.spring_layout(G, k=0.15, iterations=30, seed=seed_pos)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Grafo 1: Todos los nodos en gris
axes[0].set_title("Red Twitch PT - Nodos Unificados (Gris)")
nx.draw_networkx_nodes(G, pos, node_size=15, node_color='lightgray', ax=axes[0])
nx.draw_networkx_edges(G, pos, alpha=0.05, edge_color='gray', ax=axes[0])
axes[0].axis('off')

# Grafo 2: Nodos coloreados según el Target ('mature')
node_colors_target = [G.nodes[n].get('mature', 0) for n in G.nodes()]
axes[1].set_title("Red Twitch PT - Coloreado por Target (0: No Maduro, 1: Maduro)")
nx.draw_networkx_nodes(G, pos, node_size=15, node_color=node_colors_target, cmap=plt.cm.coolwarm, ax=axes[1])
nx.draw_networkx_edges(G, pos, alpha=0.05, edge_color='gray', ax=axes[1])
axes[1].axis('off')

plt.tight_layout()
plt.savefig('red_twitch_target.png', dpi=300)
plt.close()
print("   Imagen guardada como 'red_twitch_target.png'.")

# ==========================================
# 3. CÁLCULO DE MÉTRICAS DE RED
# ==========================================
print("3. Calculando métricas de red...")
metrics = {
    'degree_centrality': nx.degree_centrality(G),
    'betweenness_centrality': nx.betweenness_centrality(G, k=300, seed=42),
    'closeness_centrality': nx.closeness_centrality(G),
    'eigenvector_centrality': nx.eigenvector_centrality(G, max_iter=1000),
    'clustering_coefficient': nx.clustering(G)
}

df_metrics = pd.DataFrame(metrics)
df_metrics['mature'] = [G.nodes[n].get('mature', 0) for n in df_metrics.index]
print("   Métricas calculadas con éxito.")

# ==========================================
# 4. GRAFOS ADICIONALES POR MÉTRICA
# ==========================================
print("4. Generando gráficos por métrica...")
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

metric_names = list(metrics.keys())
for idx, m_name in enumerate(metric_names):
    ax = axes[idx]
    ax.set_title(f"Métrica: {m_name.replace('_', ' ').title()}")
    values = [metrics[m_name][n] for n in G.nodes()]
    
    nodes_plot = nx.draw_networkx_nodes(G, pos, node_size=20, node_color=values, cmap=plt.cm.viridis, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.05, edge_color='gray', ax=ax)
    plt.colorbar(nodes_plot, ax=ax, fraction=0.046, pad=0.04)
    ax.axis('off')

axes[5].axis('off')
plt.tight_layout()
plt.savefig('metricas_red.png', dpi=300)
plt.close()
print("   Imagen guardada como 'metricas_red.png'.")

# ==========================================
# 5. IDENTIFICACIÓN TOP 5 NODOS
# ==========================================
print("\n5. === TOP 5 NODOS POR CADA MÉTRICA ===")
for m_name in metric_names:
    top5 = df_metrics[m_name].nlargest(5)
    print(f"\nTop 5 - {m_name.upper()}:")
    for node_id, val in top5.items():
        is_mature = G.nodes[node_id].get('mature', 'N/A')
        print(f"  Nodo ID: {node_id:<5} | Valor: {val:.5f} | Target (mature): {is_mature}")

# ==========================================
# 6. DIVISIÓN ESTRATIFICADA (TRAIN 80% / TEST 20%)
# ==========================================
print("\n6. Dividiendo nodos en entrenamiento (80%) y prueba (20%)...")
all_nodes = np.array(list(G.nodes()))
y = np.array([G.nodes[n].get('mature', 0) for n in all_nodes])

train_nodes, test_nodes, y_train, y_test = train_test_split(
    all_nodes, y, test_size=0.20, stratify=y, random_state=42
)

print(f"   Nodos de Entrenamiento: {len(train_nodes)}")
print(f"   Nodos de Prueba: {len(test_nodes)}")

# ==========================================
# 7. CONSTRUCCIÓN DE REPRESENTACIONES Y MODELADO
# ==========================================
print("7. Construyendo matrices de representación (Modelo A y Modelo B)...")

node_to_idx = {node: idx for idx, node in enumerate(all_nodes)}
train_indices = [node_to_idx[n] for n in train_nodes]

# Modelo A: Matriz de adyacencia relativa
adj_matrix_full = nx.to_numpy_array(G, nodelist=all_nodes)
X_A_full = adj_matrix_full[:, train_indices]

# Modelo B: Distancias más cortas hacia nodos de training
spl_dict = dict(nx.all_pairs_shortest_path_length(G))
INF_REPLACEMENT = G.number_of_nodes()

X_B_full = np.zeros((len(all_nodes), len(train_nodes)), dtype=float)
for i, u in enumerate(all_nodes):
    for j, v in enumerate(train_nodes):
        X_B_full[i, j] = spl_dict[u][v] if v in spl_dict[u] else INF_REPLACEMENT

train_mask = np.isin(all_nodes, train_nodes)
test_mask = np.isin(all_nodes, test_nodes)

X_A_train, X_A_test = X_A_full[train_mask], X_A_full[test_mask]
X_B_train, X_B_test = X_B_full[train_mask], X_B_full[test_mask]

# Entrenamiento Random Forest
print("   Entrenando clasificadores Random Forest...")
rf_A = RandomForestClassifier(n_estimators=200, random_state=42)
rf_A.fit(X_A_train, y_train)
y_pred_A = rf_A.predict(X_A_test)

rf_B = RandomForestClassifier(n_estimators=200, random_state=42)
rf_B.fit(X_B_train, y_train)
y_pred_B = rf_B.predict(X_B_test)

# ==========================================
# 8. EVALUACIÓN Y GUARDADO DE MATRICES DE CONFUSIÓN
# ==========================================
print("\n8. === EVALUACIÓN DE MODELOS ===")

acc_A = accuracy_score(y_test, y_pred_A)
f1_A = f1_score(y_test, y_pred_A, average='macro')

acc_B = accuracy_score(y_test, y_pred_B)
f1_B = f1_score(y_test, y_pred_B, average='macro')

print("\n--- MODELO A (ADYACENCIA) ---")
print(f"Accuracy: {acc_A:.4f} | F1-Score (Macro): {f1_A:.4f}")
print(classification_report(y_test, y_pred_A))

print("\n--- MODELO B (DISTANCIAS) ---")
print(f"Accuracy: {acc_B:.4f} | F1-Score (Macro): {f1_B:.4f}")
print(classification_report(y_test, y_pred_B))

# Visualizar matrices de confusión
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

cm_A = confusion_matrix(y_test, y_pred_A)
sns.heatmap(cm_A, annot=True, fmt='d', cmap='Blues', ax=axes[0])
axes[0].set_title('Modelo A: Matriz de Adyacencia')
axes[0].set_xlabel('Predicción')
axes[0].set_ylabel('Real')

cm_B = confusion_matrix(y_test, y_pred_B)
sns.heatmap(cm_B, annot=True, fmt='d', cmap='Oranges', ax=axes[1])
axes[1].set_title('Modelo B: Matriz de Distancias')
axes[1].set_xlabel('Predicción')
axes[1].set_ylabel('Real')

plt.tight_layout()
plt.savefig('matrices_confusion.png', dpi=300)
plt.close()

print("\n Proceso completado exitosamente. Las imágenes fueron guardadas en la carpeta de trabajo.")