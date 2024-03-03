import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

class Correo:
    load_dotenv()
    correo_origen = os.getenv("EMAIL")
    contraseña = os.getenv("PASSWORD")

    def __init__(self, destinatario, copia, asunto, rutas_archivos, cuerpo):
        self.destinatario = destinatario
        self.copia = copia
        self.asunto = asunto
        self.rutas_archivos = rutas_archivos
        self.cuerpo = cuerpo

    def enviar_correo(self):
        """
        Envía un correo a los destinarios con los archivos adjuntos
        Args:
            correo: Correo elemento del tipo correo
        """    
        # Verificar cantidad de archivos
        if len(self.rutas_archivos) > 5:
            raise ValueError("Excepción lanzada cuando la lista es mayor a 5.")

        email = EmailMessage()
        email['From'] = self.correo_origen
        email['To'] = self.destinatario
        email['Cc'] = ', '.join(self.copia)
        email['Subject'] = self.asunto
        email.set_content(self.cuerpo)

        # Adjuntar archivos de la lista de rutas
        for ruta in self.rutas_archivos:
            nombre = ruta.split('\\')[-1]
            tipo = nombre.split('.')[-1]
            with open(ruta, 'rb') as content_file:
                content = content_file.read()
                email.add_attachment(content, maintype='application', subtype=tipo, filename=nombre)

        context = ssl.create_default_context( )

        # Enviar correo
        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
            smtp.login(self.correo_origen, self.contraseña)
            smtp.send_message(email)
            smtp.quit()
            print("correo enviado")