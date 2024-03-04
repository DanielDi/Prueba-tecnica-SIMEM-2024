import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from correo import *
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Primer punto
def unificar_registros(lista_df_generaciones, ruta_generacion):
    """
    Unifica los dataframes Generacion_(kWh)_AAAA
    Args:
        lista_df_generaciones (list[DataFrame]): lista de DF a juntar.
        ruta_generacion (str): ruta para guardar el df generado

    Returns:
        DataFrame con los DFs unificados
    """    
    df_generaciones = pd.concat(lista_df_generaciones, ignore_index=True)

    df_generaciones['Fecha'] = df_generaciones['Fecha'].dt.date
    df_generaciones.to_excel(ruta_generacion, index=False)

    print('Archivo generado exitosamente en: ', ruta_generacion)
    
    return df_generaciones

#Segundo punto
def csv_generacion_diaria(df_recursos, df_generacion, ruta_generacion_agentes):
    horas = list(map(str, range(24)))
    df_generacion['Total Generado'] = df_generacion[horas].sum(axis=1)

    # Hacer merge para agregar 'Agente Representante' al df_generacion
    df_generacion = pd.merge(df_generacion, df_recursos[['Código SIC', 'Agente Representante']], left_on='Código Recurso', right_on='Código SIC', how='left')

    #Agrupar la sumatoria de lo generado por día y por agente 
    grupo_generacion = df_generacion.groupby(['Fecha', 'Agente Representante'])['Total Generado'].sum()

    df_generacion_dia = pd.DataFrame(grupo_generacion)
    df_generacion_dia = df_generacion_dia.reset_index()
    df_generacion_dia.to_csv(ruta_generacion_agentes, index=False)

    return df_generacion_dia

def graficar_agentes(df_agentes, ruta_grafico_agentes):
    df_aagg = df_agentes[df_agentes['Agente Representante'] == 'EMPRESAS PUBLICAS DE MEDELLIN E.S.P.']
    df_sprg = df_agentes[df_agentes['Agente Representante'] == 'ENEL COLOMBIA SA ESP']
    df_hlag = df_agentes[df_agentes['Agente Representante'] == 'ISAGEN S.A. E.S.P.']
    
    df_aagg['Fecha'] = pd.to_datetime(df_aagg['Fecha'])
    df_sprg['Fecha'] = pd.to_datetime(df_sprg['Fecha'])
    df_hlag['Fecha'] = pd.to_datetime(df_hlag['Fecha'])
    
    plt.figure(figsize=(40, 10))
    sns.lineplot(x='Fecha', y='Total Generado', data=df_aagg, label='EMPRESAS PUBLICAS DE MEDELLIN')
    sns.lineplot(x='Fecha', y='Total Generado', data=df_sprg, label='ENEL COLOMBIA')
    sns.lineplot(x='Fecha', y='Total Generado', data=df_hlag, label='ISAGEN')
    plt.tick_params(axis="x",labelsize=10,rotation=45)
    
    plt.xlabel('Fecha')
    plt.ylabel('Total Generado')
    plt.legend()
    plt.savefig(ruta_grafico_agentes)
    plt.show()

#Tercer punto
def graficar_prom_tipo(df_generacion, ruta_grafico_promedio_tipo):
    # Dar formato a la columna Fecha
    df_generacion['Fecha'] = pd.to_datetime(df_generacion['Fecha'])
    # Agregar columna mes
    df_generacion['Mes'] = df_generacion['Fecha'].dt.strftime('%Y-%m')

    # Calcular el promedio de generación por tipo y mes
    df_promedio = df_generacion.groupby(['Mes', 'Tipo Generación'])['Total Generado'].mean().reset_index()

    # Crear un gráfico de líneas
    plt.figure(figsize=(10, 6))

    # Iterar sobre cada tipo de generación
    for tipo_generacion in df_promedio['Tipo Generación'].unique():
        df_tipo = df_promedio[df_promedio['Tipo Generación'] == tipo_generacion]
        plt.plot(df_tipo['Mes'], df_tipo['Total Generado'], marker='o', label=tipo_generacion)

    plt.xlabel('Mes')
    plt.ylabel('Generación Promedio')
    plt.title('Generación Promedio Mensual por Tipo de Generación')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(ruta_grafico_promedio_tipo)
    plt.show()

def graficar_prom_total(df_generacion, ruta_grafico_promedio_total):
    # Agregar una columna de año-mes
    df_generacion['Mes'] = df_generacion['Fecha'].dt.strftime('%Y-%m')

    # Calcular el promedio total de generación por mes
    df_promedio_mensual = df_generacion.groupby('Mes')['Total Generado'].mean().reset_index()

    # Crear un gráfico de líneas
    plt.figure(figsize=(10, 6))

    plt.plot(df_promedio_mensual['Mes'], df_promedio_mensual['Total Generado'], marker='o')

    plt.xlabel('Mes')
    plt.ylabel('Generación Promedio Total')
    plt.title('Generación Promedio Mensual Total')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(ruta_grafico_promedio_total)
    plt.show()

# Cuarto punto
def generar_participación_combustibles(df_generacion, ruta_utilizacion_combustibles):
    # Agregar una columna de año-mes
    df_generacion['Mes'] = df_generacion['Fecha'].dt.strftime('%Y-%m')
    
    # Calcular el total generado por cada tipo de combustible en cada mes
    df_combustible_mes = df_generacion.groupby(['Mes', 'Combustible'])['Total Generado'].sum().unstack(fill_value=0)
    
    # Calcular el porcentaje que representa cada tipo de combustible respecto al total generado en ese mes
    df_porcentaje_combustible_mes = df_combustible_mes.div(df_combustible_mes.sum(axis=1), axis=0) * 100

    # Redondear los valores a dos decimales
    df_porcentaje_combustible_mes = df_porcentaje_combustible_mes.round(2)
    
    df_porcentaje_combustible_mes.to_csv(ruta_utilizacion_combustibles)

# Quinto punto
def enviar_correo(correos: list[str], asunto: str, rutas: list[str], texto: str) -> None:
    """
    Enviar correo a los destinatarios con los archivos en las rutas adjuntas
    Args:
        correos: list[str] lista de destinatarios.
        asunto: str Asunto del correo
        rutas: list[str] Rutas de los archivos a enviar
        texto: str Cuerpo del correo
    """    
    correo = Correo(correos[0], correos[1:], asunto, rutas, texto)
    try:
        correo.enviar_correo()
    except ValueError as error:
        print(error)

#Bonus
def generar_modelo_prediccion(lista_precios, ruta_prediccion):
    # Unir DataFrames de precios
    df_precios = pd.concat(lista_precios, ignore_index=True)
    df_precios['Fecha'] = df_precios['Fecha'].dt.date

    horas = list(map(str, range(24)))
    df_precios['Precio Promedio'] = df_precios[horas].mean(axis=1)

    # Tomar fecha y precio promedio únicamente
    df_precios = df_precios[['Fecha', 'Precio Promedio']]

    # Establecer la columna 'Fecha' como el índice del DataFrame
    df_precios.set_index('Fecha', inplace=True)

    # Convertir el índice a la fecha
    df_precios.index = pd.to_datetime(df_precios.index)

    # Crear el modelo SARIMAX
    modelo_arima = SARIMAX(df_precios['Precio Promedio'], order=(1, 1, 1))

    # Entrenar el modelo con los datos históricos
    resultado = modelo_arima.fit()

    # Predecir el precio para un periodo futuro
    df_precios['forecast']=resultado.predict(start=700)

    #Graficar resultados
    df_precios[['Precio Promedio','forecast']].plot(figsize=(12,8))
    plt.legend()
    plt.savefig(ruta_prediccion)
    plt.show()

    # Imprimir el resumen del modelo
    print(resultado.summary())