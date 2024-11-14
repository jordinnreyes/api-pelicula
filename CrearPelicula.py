import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        # Entrada (json)
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Evento recibido",
                "evento": event
            }
        }))

        # Extraer los datos de la solicitud
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Generar UUID para la nueva película
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }

        # Conectar con DynamoDB y agregar la nueva película
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log de ejecución exitosa
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada exitosamente",
                "pelicula": pelicula,
                "response": response
            }
        }))

        # Salida (json)
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Log de error
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error al crear la película",
                "error": str(e)
            }
        }))
        return {
            'statusCode': 500,
            'error': "Ocurrió un error al crear la película",
            'detalle_error': str(e)
        }

