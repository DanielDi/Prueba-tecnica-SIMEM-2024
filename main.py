import funciones
import pandas as pd
import os

if __name__ == '__main__':
    # Rutas de entrada
    ruta_generacion_2022 = 'DatosPrueba\Generacion_(kWh)_2022.xlsx'
    ruta_generacion_2023 = 'DatosPrueba\Generacion_(kWh)_2023.xlsx'
    ruta_recursos = 'DatosPrueba\Listado_Recursos_Generacion.xlsx'
    ruta_precios_2022 = 'DatosPrueba\Precio_Bolsa_Nacional_($kwh)_2022.xlsx'
    ruta_precios_2023 = 'DatosPrueba\Precio_Bolsa_Nacional_($kwh)_2023.xlsx'

    #Rutas de salida
    ruta_generacion = 'output\Generacion_(kWh)_unificado.xlsx'
    ruta_generacion_agentes = 'output\pregunta2_tabla.csv'
    ruta_grafico_agentes = 'output\pregunta2_grafico.png'
    ruta_grafico_promedio_tipo = 'output\pregunta3_grafico1.jpg'
    ruta_grafico_promedio_total = 'output\pregunta3_grafico2.jpg'
    ruta_utilizacion_combustibles = 'output\pregunta4_tabla.csv'

    #Cargar los DataFrame
    df_recursos = pd.read_excel(ruta_recursos,skiprows=3)
    df_precios_2022 = pd.read_excel(ruta_precios_2022,skiprows=2)
    df_precios_2023 = pd.read_excel(ruta_precios_2023,skiprows=2)

    #Cargar xslx de las generaciones unificadas si existe, de lo contrario generarlo
    if os.path.exists(ruta_generacion):
        df_generacion = pd.read_excel(ruta_generacion)
    else:
        df_generacion_2022 = pd.read_excel(ruta_generacion_2022,skiprows=2)
        df_generacion_2023 = pd.read_excel(ruta_generacion_2023,skiprows=2)
        df_generacion = funciones.unificar_registros([df_generacion_2022, df_generacion_2023], ruta_generacion)

    #Generar csv de la generación por agente
    df_generacion_agente = funciones.csv_generacion_diaria(df_recursos, df_generacion, ruta_generacion_agentes)
    
    #Generar gráfico generación por día y agente
    funciones.graficar_agentes(df_generacion_agente, ruta_grafico_agentes)

    #Generar gráfico generación promedio mensual por tipo
    funciones.graficar_prom_tipo(df_generacion, ruta_grafico_promedio_tipo)

    #Generar gráfico generación promedio mensual total
    funciones.graficar_prom_total(df_generacion, ruta_grafico_promedio_total)

    #Generar tabla de porcentajes de participación de combustible
    funciones.generar_participación_combustibles(df_generacion, ruta_utilizacion_combustibles)

    #Enviar correo
    correos = ['despinalm@unal.edu.co', 'danieldi0102@gmail.com', 'animeigamer@hotmail.com']
    asunto = 'Envío de documentos'
    rutas = ['output\pregunta4_tabla.csv', 'output\pregunta3_grafico2.jpg']
    cuerpo = '''
    Adjunto archivos. 
    '''
    funciones.enviar_correo(correos, asunto, rutas, cuerpo)