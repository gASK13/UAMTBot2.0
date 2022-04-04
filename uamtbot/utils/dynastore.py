import boto3
from botocore.exceptions import ClientError


class DynaStore:
    def __init__(self, table_name):
        self.dynamodb = boto3.Session().resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table(table_name)

    def store(self, key, value):
        self.table.put_item(Item={'id': key, 'data': value})

    def delete(self, key):
        self.table.delete_item(Key={'id': key})

    def get(self, key):
        try:
            response = self.table.get_item(Key={'id': key})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            if 'Item' in response:
                return response['Item']['data']
        return None
