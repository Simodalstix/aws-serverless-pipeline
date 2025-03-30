import os
import aws_cdk as cdk
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as iam
from aws_cdk import aws_apigateway as apigateway

from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

class MigrationChatStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB table for storing chat messages
        messages_table = dynamodb.Table(
            self, "MessagesTable",
            partition_key=dynamodb.Attribute(
                name="message_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        # Lambda function to handle POST requests to store messages
        post_message_function = _lambda.Function(
            self, "PostMessageFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="post_message_lambda.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.getcwd(), "lambda")),
            environment={
                "MESSAGES_TABLE": messages_table.table_name
            },
        )
        # Grant the Lambda permission to write to the DynamoDB table
        messages_table.grant_write_data(post_message_function)
        
            
        # API Gateway to expose the Lambda as a POST endpoint
        api = apigateway.RestApi(
            self, "MigrationChatApi",
            rest_api_name="Migration Chat Service",
            description="API for posting chat messages during pharmacy migrations."
        )
        # Lambda function to handle GET requests and fetch messages
        get_messages_function = _lambda.Function(
            self, "GetMessagesFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="get_messages_lambda.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.getcwd(), "lambda")),
            environment={
                "MESSAGES_TABLE": messages_table.table_name
            },
        )
        messages = api.root.add_resource("messages")
        messages.add_method(
            "POST",
            apigateway.LambdaIntegration(post_message_function)
        )
        messages.add_method(
            "GET",
            apigateway.LambdaIntegration(get_messages_function)
        )

        