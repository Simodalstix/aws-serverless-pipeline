import json
import uuid
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['MESSAGES_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))

    message = {
        "message_id": str(uuid.uuid4()),
        "sender": body.get("sender", "anonymous"),
        "content": body.get("content", ""),
        "timestamp": datetime.utcnow().isoformat()
    }

    table.put_item(Item=message)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Stored successfully", "item": message})
    }
