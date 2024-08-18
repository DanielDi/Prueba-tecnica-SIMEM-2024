import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

ruta_precios_2022 = 'DatosPrueba\Precio_Bolsa_Nacional_($kwh)_2022.xlsx'
ruta_precios_2023 = 'DatosPrueba\Precio_Bolsa_Nacional_($kwh)_2023.xlsx'
df_precios_2022 = pd.read_excel(ruta_precios_2022,skiprows=2)
df_precios_2023 = pd.read_excel(ruta_precios_2023,skiprows=2)

df_precios = pd.concat([df_precios_2022, df_precios_2023], ignore_index=True)

df_precios['Fecha'] = df_precios['Fecha'].dt.date

horas = list(map(str, range(24)))
df_precios['Precio Promedio'] = df_precios[horas].mean(axis=1)

df_precios = df_precios[['Fecha', 'Precio Promedio']]

# Establecer la columna 'Fecha' como el índice del DataFrame
df_precios.set_index('Fecha', inplace=True)

# Convertir el índice a un objeto de tiempo
df_precios.index = pd.to_datetime(df_precios.index)

from statsmodels.tsa.statespace.sarimax import SARIMAX

# Seleccionar el Precio Promedio
serie_precios = df_precios['Precio Promedio']

# Identificar el orden del modelo ARIMA
p = 1
d = 1
q = 1

# Crear el modelo SARIMAX
modelo_arima = SARIMAX(serie_precios, order=(p, d, q))

# Entrenar el modelo con los datos históricos
resultado = modelo_arima.fit()

# Predecir el precio para un periodo futuro
df_precios['forecast']=resultado.predict(start=700)
df_precios[['Precio Promedio','forecast']].plot(figsize=(12,8))

# Visualizar la serie original y la predicción
#plt.plot(serie_precios, label="Serie original")
#plt.plot(prediccion, label="Predicción")
plt.legend()
plt.show()

# Imprimir el resumen del modelo
print(resultado.summary())