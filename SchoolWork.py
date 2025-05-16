!pip install pandas
!pip install matplotlib
import pandas as pd
import matplotlib.pyplot as plt
archivo = "https://raw.githubusercontent.com/IgnacioPardo/Tecnologias_Exponenciales_2024/main/Qatar_2022/Fifa_world_cup_matches.csv"

# Leer datos del archivo
# Completar
mundial: pd.DataFrame = pd.read_csv(archivo)

mundial
# Checkear tipo de mundial
# Completar

type(mundial)
# Que datos tiene el dataset?
# Checkear columnas
# Completar

mundial.columns
equipo = "ARGENTINA"
# Seleccionar todos los partidos que jugo un equipo de "local"
# Completar

filtroLocal = mundial.team1 == equipo

partidosLocal: int = mundial[filtroLocal]

partidosLocal = mundial[filtroLocal].team1

partidosLocal
# Seleccionar todos los partidos que jugo un equipo de "visitante"
# Completar

filtroVisitante = mundial.team2 == equipo

mundial[filtroVisitante].team2

partidosVisitante: int = mundial[filtroVisitante]
# Seleccionar todos los partidos que jugo un equipo (de "local" o "visitante")
# Completar

partidos: pd.DataFrame = mundial[filtroLocal | filtroVisitante]
partidos

# Cuantos goles hizo el equipo en total
# Completar



golesLocal = mundial.groupby("team1")["number of goals team1"].sum()
golesVisitante = mundial.groupby("team2")["number of goals team2"].sum()
goles = golesLocal + golesVisitante

goles
# Cuantos goles hizo el equipo en promedio
# Completar

golesPromedio = goles / len(partidos)
golesPromedio
# Cuantos partidos gano el equipo
# Completar

filtroGanadosLocal = filtroLocal["number of goals team1"] > filtroLocal["number of goals team 2"]
filtroGanadosLocal
# Graficar los goles hechos por el equipo en cada partido

fig, ax = plt.subplots()
# Completar
# Contar cuantos goles hizo cada equipo en total en el mundial
# Completar

equipos =
goles =
