import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['MESSAGES_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    response = table.scan(
        Limit=10,
    )

    items = sorted(response.get('Items', []), key=lambda x: x['timestamp'], reverse=True)

    return {
        "statusCode": 200,
        "body": json.dumps(items)
    }
