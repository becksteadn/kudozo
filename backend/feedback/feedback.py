import json
import logging
import os
import time
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')

def handle_error(message):
    return {
        "statusCode": 500,
        "body": message,
        "headers": {
            "Access-Control-ALlow-Origin": "*"
        }
    }

def main(event, context):
    try:
        data = json.loads(event['body'])
    except:
        print(event['body'])
        return handle_error("Could not convert body to JSON.")
    if 'value' not in data or 'path' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create feedback item.")

    timestamp = str(time.time())
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'createdAt': timestamp,
        'path': data["path"],
        'value': data["value"]
    }

    table.put_item(Item=item)

    body = {
        "message": "Thank you for your feedback!",
        "item": item,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin": "*"
        }
    }

    return response