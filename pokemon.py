import pandas as pd
import scipy.stats as stats
# Load the dataset
df = pd.read_csv("C:\\Users\\jcama\\Documents\\cucei\\mineria de datos\\Nueva carpeta\\All_Pokemon-selected-columns.csv")

t_stat, p_val = stats.ttest_1samp(df['Att'], 70)

print(f"Estadístico t: {t_stat:.4f}")
print(f"p-value: {p_val:.4e}")