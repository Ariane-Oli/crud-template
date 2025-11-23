import os
import json
from utils.dynamodb_client import get_dynamodb_client

dynamodb_client = get_dynamodb_client()
table_name = os.environ["TABLE_NAME"]
iuu_identifier = "template_id"

def delete_template(event, context):
    template_id = event["pathParameters"][iuu_identifier]

    try:
        response = dynamodb_client.delete_item(
            TableName=table_name,
            Key={iuu_identifier: {"S": template_id}}
            ReturnValues = "ALL_OLD"
        )

        if "Attributes" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Template not found"})
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Template deleted successfully"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error deleting template", "error": str(e)})
        },