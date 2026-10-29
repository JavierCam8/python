import numpy as np
import pandas as pd
import os


# 1. IMPORTACIÓN Y EXPLORACIÓN

print("=== 1. IMPORTACIÓN Y EXPLORACIÓN ===")
file_path = r"C:\Users\jcama\Documents\cucei\mineria de datos\Nueva carpeta\student-mat.csv"

# A. Cargar el archivo
try:
    df = pd.read_csv(file_path, sep=';')
    if len(df.columns) <= 1:
        df = pd.read_csv(file_path, sep=',')
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    df = pd.read_csv(file_path, sep=None, engine='python')

# Limpiar espacios ocultos en los nombres de las columnas
df.columns = df.columns.str.strip()

print("\n[INFO] Columnas detectadas en tu archivo:")
print(df.columns.tolist())

# B. Crear columna student_id utilizando el índice original
df["student_id"] = df.index
cols = ["student_id"] + [c for c in df.columns if c != "student_id"]
df = df[cols]

# C. Revisar dimensiones
filas, columnas = df.shape
print(f"\nC. Dimensiones: {filas} filas y {columnas} columnas.")

# D. Identificar tipos de datos
print("\nD. Tipos de datos por columna:")
print(df.dtypes)

# E. Primeras 10 filas
print("\nE. Primeras 10 filas:")
print(df.head(10))

# F. Estadísticas descriptivas de columnas numéricas
print("\nF. Estadísticas descriptivas:")
print(df.describe())

# 2. LIMPIEZA DE DATOS

print("\n=== 2. LIMPIEZA DE DATOS ===")

# A. Seleccionar el 5% de las posiciones numéricas y poner NaN
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if "student_id" in num_cols:
    num_cols.remove("student_id")

df_corrupted = df.copy()
total_celdas = len(df_corrupted) * len(num_cols)
n_nan = int(total_celdas * 0.05)

np.random.seed(42)
row_indices = np.random.choice(df_corrupted.index, size=n_nan, replace=True)
col_indices = np.random.choice(num_cols, size=n_nan, replace=True)

for r, c in zip(row_indices, col_indices):
    df_corrupted.loc[r, c] = np.nan

# B. Contar nulos
print("\nB.a. Nulos por columna:")
print(df_corrupted.isnull().sum())

print("\nB.b. Nulos por fila (primeras 10 filas):")
print(df_corrupted.isnull().sum(axis=1).head(10))

# C. Aplicar reglas de limpieza
df_cleaned = df_corrupted.copy()

# C.a Eliminar filas si hay nulos en categóricas clave (sex, school, address)
cat_keys = ["sex", "school", "address"]
cat_keys_present = [c for c in cat_keys if c in df_cleaned.columns]
if cat_keys_present:
    df_cleaned = df_cleaned.dropna(subset=cat_keys_present)

# C.b Reemplazar nulos en numéricas por la mediana
num_target_cols = ["age", "G1", "G2", "G3", "Dalc", "Walc"]
num_target_cols_present = [c for c in num_target_cols if c in df_cleaned.columns]

for col in num_target_cols_present:
    mediana = df_cleaned[col].median()
    df_cleaned[col] = df_cleaned[col].fillna(mediana)

# D. Verificar ausencia de nulos
print(f"\nD. Total de nulos al final: {df_cleaned.isnull().sum().sum()}")



# 3. FILTRADO Y SELECCIÓN

print("\n=== 3. FILTRADO Y SELECCIÓN ===")

# Validar que las columnas G1, G2 y G3 existen para evitar KeyError
calificaciones = ["G1", "G2", "G3"]
if all(col in df_cleaned.columns for col in calificaciones):
    # A. Crear columna avg_grade
    df_cleaned["avg_grade"] = (df_cleaned["G1"] + df_cleaned["G2"] + df_cleaned["G3"]) / 3
else:
    print("⚠️ ERROR: Faltan columnas G1, G2 o G3 en tu CSV. Revisa el archivo original.")
    # Fallback temporal para que el código no falle si el CSV está mal
    df_cleaned["avg_grade"] = 0 

# B. Estudiantes con avg_grade > 12
estudiantes_promedio_alto = df_cleaned[df_cleaned["avg_grade"] > 12]
print(f"B. Estudiantes con avg_grade > 12: {len(estudiantes_promedio_alto)}")

# C. Estudiantes con Walc >= 4
if "Walc" in df_cleaned.columns:
    estudiantes_alto_alcohol_finsem = df_cleaned[df_cleaned["Walc"] >= 4]
    print(f"C. Estudiantes con Walc >= 4: {len(estudiantes_alto_alcohol_finsem)}")

# D. Estudiantes con studytime > mediana
if "studytime" in df_cleaned.columns:
    mediana_studytime = df_cleaned["studytime"].median()
    estudiantes_alto_estudio = df_cleaned[df_cleaned["studytime"] > mediana_studytime]
    print(f"D. Estudiantes con studytime > mediana ({mediana_studytime}): {len(estudiantes_alto_estudio)}")


# 4. CREACIÓN DE COLUMNAS NUEVAS

print("\n=== 4. CREACIÓN DE COLUMNAS NUEVAS ===")

if "Dalc" in df_cleaned.columns and "Walc" in df_cleaned.columns:
    # A. Columna high_alcohol: True si (Dalc + Walc) >= 6
    df_cleaned["high_alcohol"] = (df_cleaned["Dalc"] + df_cleaned["Walc"]) >= 6

    # B. Columna alcohol_category
    def categorizar_alcohol(row):
        total = row["Dalc"] + row["Walc"]
        if total <= 3:
            return "Low"
        elif 4 <= total <= 5:
            return "Moderate"
        else:
            return "High"

    df_cleaned["alcohol_category"] = df_cleaned.apply(categorizar_alcohol, axis=1)
    print("Columnas 'high_alcohol' y 'alcohol_category' creadas correctamente.")
else:
    print("⚠️ Faltan columnas Dalc y Walc.")


# 5. AGRUPACIONES

print("\n=== 5. AGRUPACIONES ===")

if "sex" in df_cleaned.columns:
    # A. Promedio de avg_grade por sexo
    print("A. Promedio de avg_grade por sexo:")
    print(df_cleaned.groupby("sex")["avg_grade"].mean())

    # B. Mediana de Walc por sexo
    if "Walc" in df_cleaned.columns:
        print("\nB. Mediana de Walc por sexo:")
        print(df_cleaned.groupby("sex")["Walc"].median())

if "alcohol_category" in df_cleaned.columns:
    # C. Conteo de estudiantes por categoría de alcohol
    print("\nC. Conteo por alcohol_category:")
    print(df_cleaned["alcohol_category"].value_counts())

    # D. Promedio del tiempo de estudio por categoría de alcohol
    if "studytime" in df_cleaned.columns:
        print("\nD. Promedio de studytime por alcohol_category:")
        print(df_cleaned.groupby("alcohol_category")["studytime"].mean())

# 6. ORDENAMIENTO Y TOP-N

print("\n=== 6. ORDENAMIENTO Y TOP-N ===")

# A. Ordenar por avg_grade de mayor a menor
df_sorted = df_cleaned.sort_values(by="avg_grade", ascending=False)

# B. Top 10 estudiantes
top10 = df_sorted.head(10).copy()

# C. Bottom 10 estudiantes
bottom10 = df_sorted.tail(10).copy()
print("DataFrames 'top10' y 'bottom10' generados.")

# 7. INTEGRACIÓN DE RESULTADOS (CONCAT Y MERGE)

print("\n=== 7. INTEGRACIÓN DE RESULTADOS ===")

# A. Concatenación
top10["grupo"] = "top"
bottom10["grupo"] = "bottom"
ranking20 = pd.concat([top10, bottom10], ignore_index=True)

# B. Tabla resumen_sex
if all(col in df_cleaned.columns for col in ["sex", "Walc", "Dalc"]):
    resumen_sex = (
        df_cleaned.groupby("sex")
        .agg(
            promedio_avg_grade=("avg_grade", "mean"),
            promedio_Walc=("Walc", "mean"),
            promedio_Dalc=("Dalc", "mean"),
        )
        .reset_index()
    )

    # C. Merge tipo left entre ranking20 y resumen_sex
    ranking20_enriquecido = pd.merge(ranking20, resumen_sex, on="sex", how="left")

    # D. Dimensiones
    print(f"D.a Dimensiones ranking20: {ranking20.shape[0]} filas por {ranking20.shape[1]} columnas")
    print(f"D.b Dimensiones ranking20_enriquecido: {ranking20_enriquecido.shape[0]} filas por {ranking20_enriquecido.shape[1]} columnas")


# 8. CRUCE DE VARIABLES

print("\n=== 8. CRUCE DE VARIABLES ===")

if "sex" in df_cleaned.columns and "alcohol_category" in df_cleaned.columns:
    # A. Tabla cruzada sex vs alcohol_category
    print("A. Tabla cruzada (sex vs alcohol_category):")
    print(pd.crosstab(df_cleaned["sex"], df_cleaned["alcohol_category"]))

if "alcohol_category" in df_cleaned.columns and "studytime" in df_cleaned.columns:
    # B. Tabla cruzada alcohol_category vs studytime
    print("\nB. Tabla cruzada (alcohol_category vs studytime):")
    print(pd.crosstab(df_cleaned["alcohol_category"], df_cleaned["studytime"]))

# 9. EXPORTACIÓN

print("\n=== 9. EXPORTACIÓN ===")

# Obtener directorio del archivo original para guardar los CSV ahí
output_dir = os.path.dirname(file_path)

top10.to_csv(os.path.join(output_dir, "top10.csv"), index=False)
bottom10.to_csv(os.path.join(output_dir, "bottom10.csv"), index=False)
ranking20.to_csv(os.path.join(output_dir, "ranking20.csv"), index=False)

if 'ranking20_enriquecido' in locals():
    ranking20_enriquecido.to_csv(os.path.join(output_dir, "ranking20_enriquecido.csv"), index=False)

print(" Proceso completado exitosamente. Se generaron los archivos CSV en tu carpeta de trabajo.")