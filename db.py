import boto3
from constants import REGION
TABLE_NAME = "PokemonTable"

dynamodb = boto3.resource('dynamodb', region_name=REGION)

def create_table_if_not_exists():
    existing_tables = boto3.client('dynamodb', region_name=REGION).list_tables()['TableNames']
    if TABLE_NAME not in existing_tables:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'name', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'name', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Creating table {TABLE_NAME}... Waiting for it to become active...")
        table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
        print("Table created!")
    else:
        print(f"Table {TABLE_NAME} already exists.")

table = dynamodb.Table(TABLE_NAME)

def save_pokemon_to_db(pokemon):
    item = pokemon.copy()
    item['name'] = item['name'].lower()
    table.put_item(Item=item)

def get_pokemon_from_db(name):
    response = table.get_item(Key={'name': name.lower()})
    return response.get('Item')
