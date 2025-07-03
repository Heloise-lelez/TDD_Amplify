import json
import boto3
import os
import uuid



def handler(event, context):
  print('received event:')
  print(event)
  
  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps('Hello from your new Amplify Python lambda!')
  }

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["STORAGE_USERTABLE_NAME"])

def add_user(event, context):
    try:
        body = json.loads(event["body"])

        if "email" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'email'"})
            }


        user_id = str(uuid.uuid4())


        user_item = {
            "user_id": user_id,
            "name": body["name"],
            "email": body["email"]
        }

        # Insertion dans DynamoDB
        table.put_item(Item=user_item)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "User created successfully",
                "user": user_item
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def get_user_by_email(event, context):
    try:
        email = event["pathParameters"]["email"]

        # Récupération de l'utilisateur par email
        response = table.get_item(
            Key={"email": email}
        )

        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"})
            }

        user = response["Item"]

        return {
            "statusCode": 200,
            "body": json.dumps(user)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }