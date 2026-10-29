import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# 1. Cargar datos
ruta = r"C:\Users\jcama\Documents\cucei\mineria de datos\Nueva carpeta\zombies.csv"
df = pd.read_csv(ruta)

# 2. Definir variables reales del dataset
# Usaremos 'age' (edad) para predecir 'zombie' (0 o 1)
X = df[['age']]
y = df['zombie']

# Eliminar filas que tengan datos faltantes (NaN) en estas columnas
df_limpio = pd.concat([X, y], axis=1).dropna()
X = df_limpio[['age']]
y = df_limpio['zombie']

# 3. Dividir datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entrenar el modelo de Regresión Logística
modelo = LogisticRegression()
modelo.fit(X_train, y_train)

# 5. Graficar la curva logística
plt.figure(figsize=(9, 5))

# Puntos de datos reales del conjunto de prueba
sns.scatterplot(x=X_test['age'], y=y_test, color='red', label='Datos reales (Test)', s=60, zorder=3)

# Rango de edades para dibujar la curva suave
x_rango = np.linspace(X['age'].min(), X['age'].max(), 300).reshape(-1, 1)
y_prob = modelo.predict_proba(x_rango)[:, 1]

plt.plot(x_rango, y_prob, color='blue', linewidth=2.5, label='Probabilidad (Curva Logística)')
plt.axhline(0.5, color='gray', linestyle='--', alpha=0.7, label='Umbral (0.5)')

plt.title('Regresión Logística: Predicción de Estado Zombi según Edad')
plt.xlabel('Edad (age)')
plt.ylabel('Probabilidad de ser Zombi')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()

# 6. Evaluación del modelo
y_pred = modelo.predict(X_test)
print("\n--- Matriz de Confusión ---")
print(confusion_matrix(y_test, y_pred))
print("\n--- Reporte de Clasificación ---")
print(classification_report(y_test, y_pred))