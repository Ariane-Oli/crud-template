import os
import json
from utils.dynamodb_client import get_dynamodb_client



dynamodb_client = get_dynamodb_client()
table_name = os.environ["TABLE_NAME"]
iuu_identifier = "template_id"


def create_template(event, context):
    # Extrai o body dentro da função
    body = json.loads(event["body"])

    template_id = body[iuu_identifier]

    item = {
        iuu_identifier: {"S": template_id},
        "name": {"S": body["name"]},
        "description": {"S": body["description"]},
    }

    dynamodb_client.put_item(TableName=table_name, Item=item)

    response = {

        "statusCode": 201,
        "body": json.dumps({"message": "Template created successfully", "template_id": template_id}),
    }
    return response
    