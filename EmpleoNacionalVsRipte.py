import os
import pandas as pd
import matplotlib.pyplot as plt
path_regs = '/content/empleo_nacional_estacional_trimestral.csv'
if os.path.exists(path_regs):
    df_reg = pd.read_csv(path_regs)               # local
else:
    df_reg = pd.read_csv(
        'https://apis.datos.gob.ar/series/api/series/?ids=OEDE_empleo_8TYgv5&format=csv',
        skiprows=2                               # omitir encabezados extra
    )                                             # API :contentReference[oaicite:6]{index=6}

# 2) Leer o descargar RIPTE
#    - Desde CSV local (subido a /content) o desde Infra.datos.gob.ar:
path_ripte = '/content/remuneracion-imponible-promedio-trabajadores-estables-ripte-total-pais-pesos-serie-mensual.csv'
if os.path.exists(path_ripte):
    df_ripte = pd.read_csv(path_ripte)           # local
else:
    df_ripte = pd.read_csv(
        'https://infra.datos.gob.ar/catalog/sspm/dataset/158/distribution/158.1/download/remuneracion-imponible-promedio-trabajadores-estables-ripte-total-pais-pesos-serie-mensual.csv'
    )                                             # Infra.datos.gob.ar :contentReference[oaicite:7]{index=7}

# 3) Estandarizar nombres de columna
#    Asumimos: columna 0 = fecha; columna 1 = valor
df_reg.rename(columns={df_reg.columns[0]: "fecha", df_reg.columns[1]: "empleados_registrados"}, inplace=True)
df_ripte.rename(columns={df_ripte.columns[0]: "fecha", df_ripte.columns[1]: "RIPTE_pesos"}, inplace=True)

# 4) Parsear fechas
df_reg  ["fecha"] = pd.to_datetime(df_reg  ["fecha"])   #
df_ripte["fecha"] = pd.to_datetime(df_ripte["fecha"])   #

# 5) Unir series por fecha (inner join)
df = pd.merge(
    df_reg   [["fecha","empleados_registrados"]],
    df_ripte [["fecha","RIPTE_pesos"]],
    on="fecha",
    how="inner"
)                                                         #

# 6) Calcular proporción (%) de “cobertura” RIPTE
df["pct_ripte"] = df["RIPTE_pesos"] / df["empleados_registrados"] * 100

# 7) Mostrar tabla completa de resultados
print(df.to_string(index=False))

# 8) Mostrar solo el último período
u = df.iloc[-1]
print(f"\nÚltimo período: {u['fecha'].strftime('%Y-%m')}")
print(f"  • Empleados registrados: {u['empleados_registrados']:,}")
print(f"  • RIPTE (promedio $):      {u['RIPTE_pesos']:,}")
print(f"  • % de cobertura RIPTE:    {u['pct_ripte']:.2f}%")

# 9) Graficar evolución de niveles absolutos
plt.figure()
plt.plot(df["fecha"], df["empleados_registrados"], label="Registrados")  #
plt.plot(df["fecha"], df["RIPTE_pesos"],           label="RIPTE ($)")    #
plt.xlabel("Fecha"); plt.ylabel("Cantidad / Pesos")
plt.title("Empleados registrados vs. RIPTE")
plt.legend(); plt.grid(True); plt.show()

# 10) Graficar % de cobertura RIPTE
plt.figure()
plt.plot(df["fecha"], df["pct_ripte"], label="% RIPTE")  #
plt.xlabel("Fecha"); plt.ylabel("% Cobertura")
plt.title("Proporción de RIPTE sobre empleo registrado")
plt.grid(True); plt.show()
