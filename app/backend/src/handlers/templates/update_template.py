import os
import json
from utils.dynamodb_client import get_dynamodb_client

dynamodb_client = get_dynamodb_client()
table_name = os.environ["TABLE_NAME"]


def update_template(event, context):

    template_id = event["pathParameters"]["template_id"]  

    body = json.loads(event.get("body", "{}"))
    name = body.get("name")
    description = body.get("description")

    if not name and not description:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No fields to update"})
        } 
      
    update_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    if name:
        update_parts.append("name = :name")
        expression_attribute_values[":name"] = name 
        expression_attribute_names["#N"] = "name"

    if description:
        update_parts.append("description = :description")
        expression_attribute_values[":description"] = description
        expression_attribute_names["#D"] = "description"

    update_expression = "SET " + ", ".join(update_parts)
    
    try:
        dynamodb_client.update_item(
            TableName=table_name,
            Key={"id": {"S": template_id}},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Template updated successfully"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error updating template", "error": str(e)})
        }