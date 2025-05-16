import os
import pandas as pd                            # pandas.read_csv, rename, merge, to_datetime
import matplotlib.pyplot as plt               # plt.figure & plt.plot

# 1) Verifica que tus CSV estén en /content
print("Archivos en /content:", os.listdir('/content'))

# 2) Carga los CSV locales
df_ripte   = pd.read_csv('/content/remuneracion-imponible-promedio-trabajadores-estables-ripte-total-pais-pesos-serie-mensual.csv')
df_canasta = pd.read_csv('/content/valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv')

# 3) Renombra dinámicamente: col 0=fecha; col 1=RIPTE; col 1 y 2 de canasta = CBA, CBT
fecha_r, val_r         = df_ripte.columns[0], df_ripte.columns[1]
fecha_c, cba_c, cbt_c  = df_canasta.columns[0], df_canasta.columns[1], df_canasta.columns[2]
df_ripte.rename(columns={fecha_r:"fecha", val_r:"RIPTE_pesos"}, inplace=True)
df_canasta.rename(columns={fecha_c:"fecha", cba_c:"CBA_pesos", cbt_c:"CBT_pesos"}, inplace=True)

# 4) Pasa 'fecha' a datetime
df_ripte["fecha"]   = pd.to_datetime(df_ripte["fecha"])
df_canasta["fecha"] = pd.to_datetime(df_canasta["fecha"])

# 5) Une por fecha
df = pd.merge(
    df_ripte[["fecha","RIPTE_pesos"]],
    df_canasta[["fecha","CBA_pesos","CBT_pesos"]],
    on="fecha", how="inner"
)

# 6) Define factor de equivalencia para una familia de 4 (2 adultos + 2 niños)
#    Adulto = 1.0; Niño = 0.6 (puedes ajustar según tu modelo)
eq_factor = 2*1.0 + 2*0.6   # = 3.2

# 7) Calcula costo de la Canasta Básica Familiar (CBF)
df["CBF_pesos"] = df["CBA_pesos"] * eq_factor

# 8) Calcula cuántas canastas:
df["ripte_x_cbas"] = df["RIPTE_pesos"] / df["CBA_pesos"]      # adult-eq
df["ripte_x_cbfs"] = df["RIPTE_pesos"] / df["CBF_pesos"]      # familia de 4

# 9) Muestra los resultados
print(df[["fecha","ripte_x_cbas","ripte_x_cbfs"]].to_string(index=False))

# 10) Último período
u = df.iloc[-1]
print(f"\nÚltimo mes: {u['fecha'].strftime('%Y-%m')}")
print(f"  • Adult-eq CBA con 1 RIPTE: {u['ripte_x_cbas']:.2f}")
print(f"  • Familia de 4 CBF con 1 RIPTE: {u['ripte_x_cbfs']:.2f}")

# 11) Grafica comparación
plt.figure()
plt.plot(df["fecha"], df["ripte_x_cbas"],  label="RIPTE / CBA (adult-eq)")
plt.plot(df["fecha"], df["ripte_x_cbfs"], label="RIPTE / CBF (fam.4)")
plt.xlabel("Fecha")
plt.ylabel("Número de canastas")
plt.title("Canastas comprables con un RIPTE mensual")
plt.legend()
plt.grid(True)
plt.show()
