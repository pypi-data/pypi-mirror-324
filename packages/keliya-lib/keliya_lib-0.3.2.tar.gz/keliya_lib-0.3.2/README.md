# keliya_lib

`keliya_lib` is a Python package designed to streamline AWS Lambda development with DynamoDB. It facilitates database queries, logging, and permissions management for Lambda functions.

## Features

- Simplified DynamoDB queries
- Enhanced logging capabilities
- Fine-grained permissions management

## Installation

You can install `keliya_lib` via pip:

```bash
pip install keliya_lib
```

## Usage

Here's a brief overview of how to use `keliya_lib` in your AWS Lambda functions:

### DynamoDB Queries

```python
from keliya_lib import db_handler



# Perform a insert query
result = db_handler.insert(services_table, event['body'])
```

### Logging

```python
from keliya_lib import log_handler

# Initialize logger
logger = log_handler.logger

# Log an info message
logger.info('This is an info message')

# Log an error message
logger.error('An error occurred')
```

### Permissions Management

Permissions management feature helps manage user permissions for accessing Lambda functions. 

```python
from keliya_lib import permission_handler

# check Permission
permission_handler.check_permission(tenant, current_user_id, table_name, http_method)
```

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
