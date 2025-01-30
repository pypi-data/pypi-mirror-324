import requests
import os
from . import log_handler

logger = log_handler.logger


endpoint = os.environ['USER_INFO_ENDPOINT']

def get_user_info_tenant(event):
    try:
        headers = {"Authorization": "Bearer " + event['headers']['Authorization']}
        tenant = requests.get(endpoint, headers=headers).json()["custom:tenant_id"]
        current_user_id = requests.get(endpoint, headers=headers).json()["sub"]
        current_user_name = requests.get(endpoint, headers=headers).json()["username"]
        
        return tenant, current_user_name, current_user_id
        
    except Exception as e:
        logger.error("error occured retrieving tenant data  %s....",str(e))
        
        return None, None, None
    

def get_user_info(event):
    try:
        headers = {"Authorization": "Bearer " + event['headers']['Authorization']}
        response = requests.get(endpoint, headers=headers).json()
        return response.get("username", None), response.get("sub", None), response.get("custom:role", None)
        
    except Exception as e:
        logger.error("error occured retrieving tenant data  %s....",str(e))
        
        return None, None, None
        