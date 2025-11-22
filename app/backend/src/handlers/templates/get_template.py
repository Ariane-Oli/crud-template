import os
import json
from utils.dynamodb_client import get_dynamodb_client

dynamodb_client = get_dynamodb_client()
table_name = os.environ["TABLE_NAME"]
iuu_identifier = "template_id"

def get_template(event, context):
    template_id = event["pathParameters"][iuu_identifier]

    response -= dynamodb_client.get_item(
        TableName=table_name,  
        Key={iuu_identifier: {"S": template_id}}
    )

    # Verifica se o item foi encontrado
    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Template not found"}),
        }

    item = {
        "template_id": response["Item"][iuu_identifier]["S"],
        "name": response["Item"]["name"]["S"],
        "description": response["Item"]["description"]["S"],
    }

    return {
        "statusCode": 200,
        "body": json.dumps(item),
    }