import os
import pandas as pd
import numpy as np

code = "B-2362-" #Código del cual se desea extraer la información de la SBS.
years = list(range(2011, 2020)) #Rango de años a extraer.

#Código por meses debido a que la SBS separa sus archivos Excel de esta manera.
code_month = {"Enero": 'en', "Febrero": 'fe', "Marzo": 'ma',
			  "Abril": 'ab', "Mayo": 'my', "Junio": 'jn',
			  "Julio": 'jl', "Agosto": 'ag', "Setiembre": 'se',
			  "Octubre": 'oc', "Noviembre": 'no', "Diciembre": 'di'}

#Éstas son las columnas que se han deseado en este caso, los valores variarán
#según el código.
cols = ["Créditos corporativos", "Créditos a grandes empresas",
		"Créditos a medianas empresas", "Créditos pequeñas empresas",
		"Créditos a microempresas", "Créditos de consumo",
		"Créditos hipotecarios para vivienda"]

#Principales argumentos para obtener la data de internet
main_col = "TOTAL BANCA MÚLTIPLE"
link = "http://intranet2.sbs.gob.pe/estadistica/financiera"

dates = []
data = {}

for col in cols:
	data[col] = []

for year in years:
	for i, code_m in enumerate(code_month.values()):

		month = list(code_month.keys())[i]
		full_link = f"{link}/{year}/{month}/{code}{code_m}{year}.XLS"

		#Los if-statements se han realizado debido a irregularidades que muestran
		#los archivos Excel de la SBS.
		if year == 2013 and code_m == "di":
			df = pd.read_excel(full_link, index_col=0, header=5)
		elif year in list(range(2011, 2014)):
			df = pd.read_excel(full_link, index_col=1, header=4)
		elif year == 2015 and (code_m in ["ag", "se", "oc"]):
			df = pd.read_excel(full_link, index_col=0, header=4)
		else:
			df = pd.read_excel(full_link, index_col=0, header=5)

		index = list(df.index.values)
		for ind in index:
			if ind in cols:

				try:
					value = df.loc[ind, main_col]
				except KeyError:
					value = np.nan
				finally:
					data[ind].append(value)
		
		dates.append(str(year) + "-" + str(i+1))
		
		if year == 2019 and code_m == "ag":
			break

	print(f"Se extrajo la data del año {year} satisfactoriamente!")

dates = pd.to_datetime(dates, format="%Y-%m")
data = pd.DataFrame(data, index=dates)
data.to_excel("data_extraida.xlsx")
