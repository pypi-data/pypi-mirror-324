import os
import boto3
from . import log_handler

logger = log_handler.logger

users_table_suffix = os.environ['USERS_TABLE_SUFFIX']
role_permissions_table_suffix = os.environ['ROLE_PERMISSIONS_TABLE_SUFFIX']

dynamodb = boto3.resource('dynamodb')

def check_permission(tenant, current_user_id, table, http_method):
    try: 
        users_table_name = tenant + users_table_suffix
        role_permissions_table_name = tenant + role_permissions_table_suffix

        users_table = dynamodb.Table(users_table_name)
        role_permissions_table = dynamodb.Table(role_permissions_table_name)

        users_data = users_table.get_item(Key={'userId': current_user_id})
        
        role_permissions_data = role_permissions_table.get_item(
            Key={
                'roleId': users_data['Item']['roleId'],
                'tableName': table
            }
        )
    except Exception as e:
        logger.error('error occured when checking prmission %s', e)
        return False

    if "Item" in role_permissions_data:
        return role_permissions_data['Item'][http_method]
    else:
        return False