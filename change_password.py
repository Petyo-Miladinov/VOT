import json
import boto3

def change_password(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    body = json.loads(event['body'])

    username = body['username']
    old_password = body['oldPassword']
    new_password = body['newPassword']

    response = table.get_item(Key={'username': username})

    if 'Item' in response:
        if response['Item']['password'] == old_password:
            table.update_item(
                Key={'username': username},
                UpdateExpression='SET password = :val1',
                ExpressionAttributeValues={
                    ':val1': new_password
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps('Password changed successfully')
            }
        else:
            return {
                'statusCode': 403,
                'body': json.dumps('Old password is incorrect')
            }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('User not found')
        }
