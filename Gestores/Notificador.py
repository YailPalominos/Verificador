import plivo

# Inicializa el cliente de Plivo
client = plivo.RestClient(auth_id='SK64e175f6ab0ccb5312bb98b061c391ca', auth_token='3vLPUcSvumFZqhAkr3pjK2IPYKoMLByf')

# Enviar el SMS
response = client.messages.create(
    src='+4779174671',  # Número del remitente (tuyo o de Plivo)
    dst='+4772607424',  # Número del destinatario
    text='Hola bb pa que me estas llamando!'
)

# Mostrar el ID del mensaje
print(f"Mensaje enviado con ID: {response['message_uuid']}")
