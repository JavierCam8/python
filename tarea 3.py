import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 10})

df = pd.read_csv(r"C:\Users\jcama\Documents\cucei\mineria de datos\Nueva carpeta\RPG.csv")

# ----------------------------------------------------
# 1. SALIDA CONTINUA - ENTRADA CONTINUA: Level vs Magic
# ----------------------------------------------------
var_A = 'Level'
var_B = 'Magic'

# Normality tests
stat_A, p_A = stats.shapiro(df[var_A])
stat_B, p_B = stats.shapiro(df[var_B])

# Correlation tests
r_pearson, p_pearson = stats.pearsonr(df[var_A], df[var_B])
rho_spearman, p_spearman = stats.spearmanr(df[var_A], df[var_B])

print("--- SECCIÓN 1 ---")
print(f"Shapiro {var_A}: W={stat_A:.4f}, p={p_A:.4e}")
print(f"Shapiro {var_B}: W={stat_B:.4f}, p={p_B:.4e}")
print(f"Pearson: r={r_pearson:.4f}, p={p_pearson:.4e}")
print(f"Spearman: rho={rho_spearman:.4f}, p={p_spearman:.4e}")

# Plot 1: Normality (Histograms & QQ-Plots) and Scatter
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Histograms
sns.histplot(df[var_A], kde=True, ax=axes[0,0], color='skyblue')
axes[0,0].set_title(f'Histograma de {var_A}')

sns.histplot(df[var_B], kde=True, ax=axes[0,1], color='salmon')
axes[0,1].set_title(f'Histograma de {var_B}')

# QQ Plots
stats.probplot(df[var_A], dist="norm", plot=axes[1,0])
axes[1,0].set_title(f'Q-Q Plot de {var_A}')

stats.probplot(df[var_B], dist="norm", plot=axes[1,1])
axes[1,1].set_title(f'Q-Q Plot de {var_B}')

plt.tight_layout()
plt.savefig('sec1_normality.png')
plt.close()

# Scatter Plot with Regression line and 95% CI
plt.figure(figsize=(8, 6))
sns.regplot(x=var_A, y=var_B, data=df, scatter_kws={'alpha':0.5, 'color':'teal'}, line_kws={'color':'red', 'linewidth':2}, ci=95)
plt.title(f'Diagrama de Dispersión: {var_A} vs {var_B} (con IC 95%)')
plt.xlabel('Nivel (Level)')
plt.ylabel('Magia (Magic)')
plt.savefig('sec1_scatter.png')
plt.close()

# ----------------------------------------------------
# 2. SALIDA CONTINUA - ENTRADA CATEGÓRICA: Level vs FBoss
# ----------------------------------------------------
cont_var = 'Level'
cat_var = 'FBoss'

g_false = df[df[cat_var] == False][cont_var]
g_true = df[df[cat_var] == True][cont_var]

# Normality per group
w_f, p_norm_f = stats.shapiro(g_false)
w_t, p_norm_t = stats.shapiro(g_true)

# Homogeneity of variance (Levene)
stat_lev, p_lev = stats.levene(g_false, g_true)

# Tests
ttest_stat, ttest_p = stats.ttest_ind(g_false, g_true)
mwu_stat, mwu_p = stats.mannwhitneyu(g_false, g_true)

mean_f, mean_t = g_false.mean(), g_true.mean()
diff_mean = mean_t - mean_f

print("\n--- SECCIÓN 2 ---")
print(f"Normality FBoss=False: W={w_f:.4f}, p={p_norm_f:.4e}")
print(f"Normality FBoss=True: W={w_t:.4f}, p={p_norm_t:.4e}")
print(f"Levene Test: Stat={stat_lev:.4f}, p={p_lev:.4e}")
print(f"Mean FBoss=False: {mean_f:.2f}, Mean FBoss=True: {mean_t:.2f}, Diff: {diff_mean:.2f}")
print(f"t-test: t={ttest_stat:.4f}, p={ttest_p:.4e}")
print(f"Mann-Whitney U: U={mwu_stat:.4f}, p={mwu_p:.4e}")

# Boxplot
plt.figure(figsize=(7, 5))
sns.boxplot(x=cat_var, y=cont_var, data=df, palette='Set2')
sns.stripplot(x=cat_var, y=cont_var, data=df, color='black', alpha=0.2, jitter=0.2)
plt.title('Distribución de Level según FBoss')
plt.xlabel('FBoss (Derrotó al Jefe Final)')
plt.ylabel('Nivel (Level)')
plt.savefig('sec2_boxplot.png')
plt.close()

# ----------------------------------------------------
# 3. SALIDA CATEGÓRICA - ENTRADA CATEGÓRICA: Class vs FBoss
# ----------------------------------------------------
contingency_tab = pd.crosstab(df['Class'], df['FBoss'])
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency_tab)

# Cramer's V
n = contingency_tab.sum().sum()
min_dim = min(contingency_tab.shape) - 1
cramers_v = np.sqrt(chi2 / (n * min_dim))

print("\n--- SECCIÓN 3 ---")
print("Contingency Table:")
print(contingency_tab)
print("\nExpected Counts:")
print(pd.DataFrame(expected, index=contingency_tab.index, columns=contingency_tab.columns))
print(f"Chi2={chi2:.4f}, dof={dof}, p={p_chi2:.4e}, Cramer's V={cramers_v:.4f}")

# Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(contingency_tab, annot=True, fmt='d', cmap='Blues', cbar=True)
plt.title('Tabla de Contingencia (Frecuencias Observadas): Class vs FBoss')
plt.xlabel('FBoss')
plt.ylabel('Clase (Class)')
plt.savefig('sec3_heatmap.png')
plt.close()

# Standardized residuals heatmap
obs = contingency_tab.values
std_residuals = (obs - expected) / np.sqrt(expected * (1 - contingency_tab.sum(axis=0).values / n) * (1 - contingency_tab.sum(axis=1).values[:, None] / n))
std_res_df = pd.DataFrame(std_residuals, index=contingency_tab.index, columns=contingency_tab.columns)

plt.figure(figsize=(8, 6))
sns.heatmap(std_res_df, annot=True, fmt='.2f', cmap='vlag', center=0, cbar=True)
plt.title('Residuos Estandarizados Ajustados: Class vs FBoss')
plt.xlabel('FBoss')
plt.ylabel('Clase (Class)')
plt.savefig('sec3_std_residuals.png')
plt.close()

# ----------------------------------------------------
# 4. SALIDA CATEGÓRICA - ENTRADA CONTINUA: FBoss vs Level
# ----------------------------------------------------
df['FBoss_num'] = df['FBoss'].astype(int)
model = smf.logit('FBoss_num ~ Level', data=df).fit(disp=False)

beta0 = model.params['Intercept']
beta1 = model.params['Level']
p_beta1 = model.pvalues['Level']
odds_ratio = np.exp(beta1)
conf_int = model.conf_int().loc['Level']
or_ci_lower = np.exp(conf_int[0])
or_ci_upper = np.exp(conf_int[1])

print("\n--- SECCIÓN 4 ---")
print(model.summary())
print(f"Beta0 (Intercept): {beta0:.4f}")
print(f"Beta1 (Level): {beta1:.4f}, p-value: {p_beta1:.4e}")
print(f"Odds Ratio: {odds_ratio:.4f} (95% CI: [{or_ci_lower:.4f}, {or_ci_upper:.4f}])")

# Logistic regression plot
plt.figure(figsize=(8, 6))
sns.regplot(x='Level', y='FBoss_num', data=df, logistic=True, ci=95,
            scatter_kws={'alpha': 0.3, 'color': 'indigo'}, line_kws={'color': 'darkorange', 'linewidth': 2.5})
plt.title('Curva Logística Ajustada: Probabilidad de FBoss según Level')
plt.xlabel('Nivel (Level)')
plt.ylabel('Probabilidad Estimada de FBoss (1 = True, 0 = False)')
plt.savefig('sec4_logistic.png')
plt.close()