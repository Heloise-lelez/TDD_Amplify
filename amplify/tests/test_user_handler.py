
import boto3
from moto import mock_dynamodb
from boto3.dynamodb.conditions import Key



@mock_dynamodb
def test_add_and_get_user_by_email():

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.create_table(
        TableName='UserTable',
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'email', 'AttributeType': 'S'},
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'email-index',
                'KeySchema': [
                    {'AttributeName': 'email', 'KeyType': 'HASH'}
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='UserTable')

   # Insertion d’un utilisateur
    table.put_item(Item={
        'user_id': 'abc123',
        'email': 'test@example.com',
        'name': 'Héloïse'
    })

    # Requête via GSI pour chercher par email
    response = table.query(
        IndexName='email-index',
        KeyConditionExpression=Key('email').eq('test@example.com')
    )

    assert len(response['Items']) == 1
    assert response['Items'][0]['name'] == 'Héloïse'
    print("✅ Test réussi :", response['Items'][0])