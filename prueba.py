import pandas as pd

ruta_recursos = 'DatosPrueba\Listado_Recursos_Generacion.xlsx'
ruta_generacion = 'output\Generacion_(kWh)_unificado.xlsx'
ruta_generacion_agentes = 'output\pregunta2_tabla.csv'
df_recursos = pd.read_excel(ruta_recursos,skiprows=3)
df_generacion = pd.read_excel(ruta_generacion)

horas = list(map(str, range(24)))
df_generacion['Total Generado'] = df_generacion[horas].sum(axis=1)

# Hacer match para agregar 'Agente Representante' al df_generacion
df_generacion = pd.merge(df_generacion, df_recursos[['Código SIC', 'Agente Representante']], left_on='Código Recurso', right_on='Código SIC', how='left')


grupo_generacion = df_generacion.groupby(['Fecha', 'Agente Representante'])['Total Generado'].sum()

df_generacion_dia = pd.DataFrame(grupo_generacion)
df_generacion_dia = df_generacion_dia.reset_index()
df_generacion_dia.rename(columns={'Código Agente': 'Codigo Agente'}, inplace=True)
df_generacion_dia.to_csv(ruta_generacion_agentes, index=False)