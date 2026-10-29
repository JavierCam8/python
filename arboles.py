import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# 1. Cargar la base de datos
file_path = "C:/Users/jcama/Documents/cucei/mineria de datos/Nueva carpeta/NASA Near-Earth Objects-selected-columns.csv"
df = pd.read_csv(file_path)

# 2. Limpieza de filas completamente vacías
df = df.dropna(how='all')

# Verificación por si el CSV no tiene filas con datos
if df.empty or df['is_potentially_hazardous_asteroid'].dropna().empty:
    print("⚠️ ADVERTENCIA: El archivo CSV está vacío de datos. Generando muestra de prueba...")
    np.random.seed(42)
    n_samples = 500
    df = pd.DataFrame({
        'kilometers_estimated_diameter_min': np.random.exponential(scale=0.2, size=n_samples),
        'absolute_magnitude_h': np.random.uniform(14, 28, size=n_samples),
        'is_potentially_hazardous_asteroid': np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15])
    })

# 3. Selección de variables
feature_cols = ['kilometers_estimated_diameter_min', 'absolute_magnitude_h']
target_col = 'is_potentially_hazardous_asteroid'

X = df[feature_cols].copy()
y = df[target_col].copy()

# Rellenar valores nulos con la mediana
X = X.fillna(X.median())
y = y.dropna().astype(int)

# 4. División en conjuntos de entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Escalado de datos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Entrenamiento del modelo
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)

# 7. Evaluación del modelo
y_pred = model.predict(X_test_scaled)

print("--- RESULTADOS DEL MODELO ---")
print(f"Precisión General (Accuracy): {accuracy_score(y_test, y_pred):.4f}\n")
print("Reporte de Clasificación:")
print(classification_report(y_test, y_pred))

# ==========================================
# 8. MATRIZ DE CONFUSIÓN
# ==========================================
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print("\n--- MATRIZ DE CONFUSIÓN (Texto) ---")
print(f"Verdaderos Negativos (TN - Correcto NO Peligroso) : {tn}")
print(f"Falsos Positivos     (FP - Falsa Alarma)          : {fp}")
print(f"Falsos Negativos     (FN - Peligro No Detectado)  : {fn}")
print(f"Verdaderos Positivos (TP - Correcto Peligroso)    : {tp}\n")

# Gráfica de la Matriz de Confusión
plt.figure(figsize=(6, 5))
sns.heatmap(
    cm, 
    annot=True, 
    fmt='d', 
    cmap='Blues',
    xticklabels=['No Peligroso (0)', 'Peligroso (1)'],
    yticklabels=['No Peligroso (0)', 'Peligroso (1)']
)
plt.title('Matriz de Confusión - Detección de Asteroides')
plt.xlabel('Predicción del Modelo')
plt.ylabel('Valor Real (Dataset)')
plt.tight_layout()
plt.show()

# 9. Función para realizar predicciones individuales
def predecir_asteroide(diametro_km, magnitud):
    datos_nuevo = np.array([[diametro_km, magnitud]])
    datos_escalados = scaler.transform(datos_nuevo)
    
    prediccion = model.predict(datos_escalados)[0]
    probabilidad = model.predict_proba(datos_escalados)[0][1]
    
    if prediccion == 1:
        return f"⚠️ ATENCIÓN: Asteroide POTENCIALMENTE PELIGROSO (Probabilidad: {probabilidad:.2%})"
    else:
        return f"✅ SEGURO: Asteroide NO peligroso (Probabilidad de peligro: {probabilidad:.2%})"

# Ejemplo de prueba
print(predecir_asteroide(diametro_km=0.5, magnitud=18.0))