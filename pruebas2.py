import funciones
correos = ['despinalm@unal.edu.co', 'danieldi0102@gmail.com', 'animeigamer@hotmail.com']
asunto = 'este es el asunto'
rutas = ['output\pregunta4_tabla.csv', 'output\pregunta3_grafico2.jpg']
cuerpo = 'Esto es el cuerpo del texto'
funciones.enviar_correo(correos, asunto, rutas, cuerpo)