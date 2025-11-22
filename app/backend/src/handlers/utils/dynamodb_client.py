import boto3

def get_dynamodb_client():
  
    endpoint_url = "http://localhost:8000"
    serviço = "dynamodb"
    region_name = "sa-east-1"
   
    return boto3.client("dynamodb", endpoint_url=endpoint_url, region_name=region_name)