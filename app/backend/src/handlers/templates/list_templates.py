import os
import json
from utils.dynamodb_client import get_dynamodb_client

dynamodb_client = get_dynamodb_client()
table_name = os.environ["TABLE_NAME"]
iuu_identifier = "template_id"

def get_template(event, context):

    response = dynamodb_client.scan(TableName=table_name)

    items = []

    for item in response.get("Items", []):
        items.append({
            "template_id": item[iuu_identifier]["S"],
            "name": item["name"]["S"],
            "description": item["description"]["S"],
        })

    return {
        "statusCode": 200,
        "body": json.dumps(items),
    }