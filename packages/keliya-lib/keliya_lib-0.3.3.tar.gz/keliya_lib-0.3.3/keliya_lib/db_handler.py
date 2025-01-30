import json
import os
from . import log_handler
from decimal import Decimal
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
import uuid

logger = log_handler.logger
now = datetime.now().isoformat()
table_suffix = os.environ['DB_TABLE']
env = os.environ['ENV']
tenant = os.environ['TENANT']
global_pk_label = os.environ['PK']
global_sk_label = os.environ['SK']
table_name = f"{tenant}-{env}-{table_suffix}"
dynamodb = boto3.resource('dynamodb')
global_table = dynamodb.Table(table_name)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def get_by_pk(pk,table=None,pk_label=None):
    global global_table, global_pk_label
    if table is not None:
        global_table = table
    if pk_label is not None:
        global_pk_label = pk_label
    logger.info("executing db_handler.get_by_pk")
    data = global_table.get_item(Key={global_pk_label: pk})
    if "Item" in data:
        return {
            'statusCode': 200,
            'body': json.dumps(data['Item'],default=decimal_default)
        }
                
    else:
        return {
            'statusCode': 204,
            'body': json.dumps({"error":"no content"})
        }

def get_by_pk_and_sk(pk, sk, table=None,pk_label=None,sk_label=None):
    logger.info("executing db_handler.get_by_pk_and_sk")
    global global_table, global_pk_label, global_sk_label
    if table is not None:
        global_table = table
    if pk_label is not None:
        global_pk_label = pk_label
    if sk_label is not None:
        global_sk_label = sk_label

    data = global_table.get_item(
            Key={
                global_pk_label: pk,
                global_sk_label: sk
            }
        )
    if "Item" in data:
        return {
            'statusCode': 200,
            'body': json.dumps(data['Item'],default=decimal_default)
        }
                
    else:
        return {
            'statusCode': 204,
            'body': json.dumps({"error":"no content"})
        }

def get_all_by_pagination(query_string_parameters,table=None,pk_label=None):
    global global_table, global_pk_label
    if table is not None:
        global_table = table
    if pk_label is not None:
        global_pk_label = pk_label
    page_size = int(query_string_parameters.get('pageSize', 10))
    page_number = int(query_string_parameters.get('pageNumber', 1))
    last_evaluated_key = query_string_parameters.get('lastEvaluatedKey') if 'lastEvaluatedKey' in query_string_parameters else None 
    offset = (page_number - 1) * page_size
    exclusive_start_key = None
    response = None

    try:
        if offset != 0:
            exclusive_start_key = {global_pk_label: last_evaluated_key} if last_evaluated_key else None
            response = global_table.scan(Limit=page_size, ExclusiveStartKey=exclusive_start_key)
        else:
            response = global_table.scan(Limit=page_size)
                    
        logger.info("retrieved data for page: %s", page_number) 
    
    except Exception as e:
        logger.error("error occured retrieving data  %s....",str(e))
        return {
            'statusCode': 400,
            'body': json.dumps({"error":"something went wrong"})
        }    

    items = response['Items']
    
    return {
        'statusCode': 200,
        'body': json.dumps({ "data": items, "lastEvaluatedKey" : items[-1][global_pk_label] if items else 'null'}, default=decimal_default)
    }
    
def insert(data,table=None, pk=str(uuid.uuid4()), sk=None, pk_label=None, sk_label=None):
    body = json.loads(data)
    global global_table, global_pk_label, global_sk_label
    if table is not None:
        global_table = table
    if pk_label is not None:
        global_pk_label = pk_label
    if sk_label is not None:
        global_sk_label = sk_label
    
    body[global_pk_label] = pk
    if sk is not None:
        body[global_sk_label] = sk

    body['createdDate'] = now
    body['updatedDate'] = now
    try:
        global_table.put_item(Item=body)
    except Exception as e:
        logger.error("error occured saving data  %s....",str(e))
        return {
            'statusCode': 400,
            'body': json.dumps({"error":"something went wrong."})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({"message":"request success."})
    }

def delete(pk, sk, table=None,pk_label=None,sk_label=None):
    global global_table, global_pk_label, global_sk_label
    express = {}
    if table is not None:
        global_table = table
    if pk_label is not None:
        global_pk_label = pk_label
        express = {global_pk_label: pk}
    if sk_label is not None:
        global_sk_label = sk_label
        express = {global_pk_label: pk, global_sk_label: sk}

    try:
        response = global_table.delete_item(Key=express)
        return {
            'statusCode': 202,
            'body': json.dumps({"message":"Item deleted successfully."})
        } 
    except Exception as e:
        logger.error("error deleting data  %s....", str(e))
        return {
            'statusCode': 400,
            'body': json.dumps({"error":"something went wrong"})
        }