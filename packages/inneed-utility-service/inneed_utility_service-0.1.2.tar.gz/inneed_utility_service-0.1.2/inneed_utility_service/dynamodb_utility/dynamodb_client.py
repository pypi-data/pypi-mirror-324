import boto3
from inneed_utility_service.error_utility.error_handler import ErrorHandler
from inneed_utility_service.error_utility.error_handler import DynamoDBConnectionError, DynamoDBOperationError

class DynamoDBClient:
    @ErrorHandler.handle_error(DynamoDBConnectionError, "Failed to initialize DynamoDB client")
    def __init__(self, region: str):
        """
        Initialize a DynamoDB client.
        Only the AWS region is required.
        """
        self.region = region
        try:
            self.ddb = boto3.client('dynamodb', region_name=self.region)
        except Exception as e:
            raise DynamoDBConnectionError(
                message=f"Error initializing DynamoDB client for region {self.region}",
                original_exception=e
            )

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error listing DynamoDB tables")
    def list_tables(self):
        """List all DynamoDB tables."""
        response = self.ddb.list_tables()
        return response.get('TableNames', [])

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error creating DynamoDB table")
    def create_table(self, table_name: str, key_schema: list, attribute_definitions: list, provisioned_throughput: dict):
        """
        Create a new DynamoDB table.

        Args:
            table_name: Name of the table.
            key_schema: List of key schema definitions.
            attribute_definitions: List of attribute definitions.
            provisioned_throughput: Dict with ReadCapacityUnits and WriteCapacityUnits.
        """
        return self.ddb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput=provisioned_throughput
        )

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error describing DynamoDB table")
    def describe_table(self, table_name: str):
        """Describe a DynamoDB table."""
        response = self.ddb.describe_table(TableName=table_name)
        return response.get('Table', {})

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error updating DynamoDB table")
    def update_table(self, table_name: str, provisioned_throughput: dict):
        """
        Update a DynamoDB table's provisioned throughput.

        Args:
            table_name: Name of the table.
            provisioned_throughput: Dict with updated ReadCapacityUnits and WriteCapacityUnits.
        """
        return self.ddb.update_table(
            TableName=table_name,
            ProvisionedThroughput=provisioned_throughput
        )

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error deleting DynamoDB table")
    def delete_table(self, table_name: str):
        """Delete a DynamoDB table."""
        return self.ddb.delete_table(TableName=table_name)

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error putting item into DynamoDB table")
    def put_item(self, table_name: str, item: dict):
        """Insert or replace an item in a DynamoDB table."""
        return self.ddb.put_item(TableName=table_name, Item=item)

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error retrieving item from DynamoDB table")
    def get_item(self, table_name: str, key: dict):
        """Retrieve an item from a DynamoDB table."""
        response = self.ddb.get_item(TableName=table_name, Key=key)
        return response.get('Item', {})

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error updating item in DynamoDB table")
    def update_item(self, table_name: str, key: dict, update_expression: str, expression_attribute_values: dict, return_values: str = "UPDATED_NEW"):
        """
        Update an existing item in a DynamoDB table.

        Args:
            table_name: Name of the table.
            key: Primary key dict to identify the item.
            update_expression: An update expression defining attributes to modify.
            expression_attribute_values: Values for the expression attributes.
            return_values: Specifies what values to return (default is "UPDATED_NEW").
        """
        return self.ddb.update_item(
            TableName=table_name,
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues=return_values
        )

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error deleting item from DynamoDB table")
    def delete_item(self, table_name: str, key: dict):
        """Delete an item from a DynamoDB table."""
        return self.ddb.delete_item(TableName=table_name, Key=key)

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error querying DynamoDB table")
    def query(self, table_name: str, key_condition_expression: str, expression_attribute_values: dict):
        """
        Query items in a DynamoDB table.

        Args:
            table_name: Name of the table.
            key_condition_expression: A condition expression for the key.
            expression_attribute_values: Values for the expression attributes.
        """
        response = self.ddb.query(
            TableName=table_name,
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response.get('Items', [])

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error scanning DynamoDB table")
    def scan(self, table_name: str, filter_expression: str = None, expression_attribute_values: dict = None):
        """
        Scan a DynamoDB table.

        Args:
            table_name: Name of the table.
            filter_expression: Optional filter expression to narrow results.
            expression_attribute_values: Optional dict of values for the filter expression.
        """
        if filter_expression and expression_attribute_values:
            response = self.ddb.scan(
                TableName=table_name,
                FilterExpression=filter_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
        else:
            response = self.ddb.scan(TableName=table_name)
        return response.get('Items', [])

    @ErrorHandler.handle_error(DynamoDBOperationError, "Error batch writing to DynamoDB table")
    def batch_write_item(self, request_items: dict):
        """
        Batch write items to one or more tables.

        Args:
            request_items: A dict mapping table names to a list of write requests.
        """
        return self.ddb.batch_write_item(RequestItems=request_items)
