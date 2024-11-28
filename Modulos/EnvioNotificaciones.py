import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EnvioNotificaciones:
 
    direccion_correo = "yail.2014.yppo@gmail.com"
    usuarioSMTP = "smtp.gmail.com"
    contrasena = "ukne lhmg ilfx xdmu"
    puerto = 587

    def generar_tabla_verificaciones(verificaciones):
        """Genera una tabla HTML con las verificaciones"""
        filas = ""
        for verificacion in verificaciones:
            filas += f"""
            <tr>
                <td>{verificacion.id_verificador}</td>
                <td>{verificacion.fecha.split(" ")[1]}</td>
                <td>{verificacion.tipo}</td>
                <td>{verificacion.categoria}</td>
            </tr>
            """
        tabla = f"""
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr>
                    <th>Id Verificador</th>
                    <th>Hora</th>
                    <th>Tipo</th>
                    <th>Categoria</th>
                </tr>
            </thead>
            <tbody>
                {filas}
            </tbody>
        </table>
        """
        return tabla

    @staticmethod
    def enviar_correo(destinatario, asunto, nombre_completo, verificaciones):
 
        try:
            # Generar el cuerpo del mensaje HTML
            tabla_html = EnvioNotificaciones.generar_tabla_verificaciones(verificaciones)
            mensaje_html = f"""
            <html>
                <body>
                    <p>Estimado(a) {nombre_completo},</p>
                    <p>A continuacion, las verificaciones realizadas el dia de hoy:</p>
                    {tabla_html}
                    <p>Saludos cordiales,</p>
                    <p>El equipo de Verificaciones</p>
                </body>
            </html>
            """

            # Crear el mensaje
            msg = MIMEMultipart()
            msg["From"] = EnvioNotificaciones.direccion_correo
            msg["To"] = destinatario
            msg["Subject"] = asunto

            # Agregar el cuerpo del mensaje como HTML
            msg.attach(MIMEText(mensaje_html, "html"))

            # Conectar con el servidor SMTP
            with smtplib.SMTP(EnvioNotificaciones.usuarioSMTP, EnvioNotificaciones.puerto) as servidor:
                servidor.starttls()
                servidor.login(EnvioNotificaciones.direccion_correo, EnvioNotificaciones.contrasena)
                servidor.send_message(msg)

            print("Correo enviado exitosamente a", destinatario)
        except Exception as e:
            print("Error al enviar el correo:", str(e))
