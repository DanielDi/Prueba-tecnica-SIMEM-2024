# Prueba-tecnica-SIMEM-2024

Instructivo para ejecutar
---------------------

Crear ambiente virtual:

```
$ python -m venv prueba-env
```

Activar ambiente virtual:
```
$ source prueba-env/Scripts/activate
```

Instalar requerimientos:
```
$ pip install -r requirements.txt
```

Configurar correo
---------------------
Para poder hacer envío del correo crear el archivo .env en la raiz con los siguientes datos:

EMAIL = "tu correo"

PASSWORD = "tu contraseña"

Ejecutar prueba
---------------------
```
$ python main.py
```
# Informe de prueba
En el archivo funciones.py encontrará la solución a cada uno de los puntos seguida de un comentario que indica la pregunta a la que hace referencia.

La solución para el punto 5 la encontrará en el archivo "correo.py"

Modelo de predicción
---------------------
```
           * * *

Tit   = total number of iterations
Tnf   = total number of function evaluations
Tnint = total number of segments explored during Cauchy searches
Skip  = number of BFGS updates skipped
Nact  = number of active bounds at final generalized Cauchy point
Projg = norm of the final projected gradient
F     = final function value

           * * *

   N    Tit     Tnf  Tnint  Skip  Nact     Projg        F
    3     20     22      1     0     0   6.907D-06   5.389D+00
  F =   5.3894763044614695

CONVERGENCE: NORM_OF_PROJECTED_GRADIENT_<=_PGTOL
                               SARIMAX Results
==============================================================================
Dep. Variable:        Precio Promedio   No. Observations:                  730
Model:               SARIMAX(1, 1, 1)   Log Likelihood               -3934.318
Date:                Sun, 03 Mar 2024   AIC                           7874.635
Time:                        23:19:33   BIC                           7888.410
Sample:                    01-01-2022   HQIC                          7879.950
                         - 12-31-2023
Covariance Type:                  opg
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
ar.L1          0.6655      0.094      7.069      0.000       0.481       0.850
ma.L1         -0.5352      0.103     -5.176      0.000      -0.738      -0.333
sigma2      2852.2299     55.048     51.814      0.000    2744.338    2960.122
===================================================================================
Ljung-Box (L1) (Q):                   0.57   Jarque-Bera (JB):              7889.57
Prob(Q):                              0.45   Prob(JB):                         0.00
Heteroskedasticity (H):              11.33   Skew:                            -1.57
Prob(H) (two-sided):                  0.00   Kurtosis:                        18.81
===================================================================================
```