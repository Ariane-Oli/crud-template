import os
import json
from utils.dynamodb_client import get_dynamodb_client

dynamodb_client = get_dynamodb_client()
table_name = os.environ["TABLE_NAME"]
iuu_identifier = "template_id"

def update_template(template_id, update_data):

    template_id = event["pathParameters"]["id_key"]
    update_data = json.loads(event["body"])
    
    body = json.loads(event.get("body", "{}"))
    name = body.get("name")
    description = body.get("description")

    if not name and not description:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No fields to update"})
        }   
    else:
        update_expression = "SET"
        expression_attribute_values = {}
        expression_attribute_names = {}

        if name:
            update_expression += "#N = :name, "
            expression_attribute_values[":name"] = name
            expression_attribute_names["#N"] = "name"

        if description:
            update_expression += "#D = :description, "
            expression_attribute_values[":description"] = description
            expression_attribute_names["#D"] = "description"

        update_expression = update_expression.rstrip(", ")

        try:
            dynamodb_client.update_item(
                TableName=table_name,
                Key={iuu_identifier: {"S": template_id}},
                UpdateExpression=update_expression,
                ExpressionAttributeValues={k: {"S": v} for k, v in expression_attribute_values.items()},
                ExpressionAttributeNames=expression_attribute_names
            )
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Template updated successfully"})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"message": f"Error updating template: {str(e)}"})
            }