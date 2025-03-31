import json
import boto3
import os
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['MESSAGES_TABLE'])

def lambda_handler(event, context):
    try:
        print("Received event:", event)

        body = json.loads(event['body'])
        sender = body['sender']
        content = body['content']

        item = {
            "message_id": str(uuid.uuid4()),
            "sender": sender,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Stored successfully", "item": item})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error", "error": str(e)})
        }
