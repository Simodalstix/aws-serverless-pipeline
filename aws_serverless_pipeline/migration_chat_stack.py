import os
import aws_cdk as cdk
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as iam
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_cognito as cognito


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
        # Grant the Lambda read access to the DynamoDB table
        messages_table.grant_read_data(get_messages_function)
        
        # API Gateway to expose the Lambda as a POST endpoint
        api = apigateway.RestApi(
            self, "MigrationChatApi",
            rest_api_name="Migration Chat Service",
            description="API for posting chat messages during pharmacy migrations."
        )

                # Cognito User Pool for authentication
        user_pool = cognito.UserPool(
            self, "MigrationChatUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(username=True, email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY
        )

        # App client (for login via hosted UI or API calls)
        user_pool_client = user_pool.add_client(
            "MigrationChatClient",
            auth_flows=cognito.AuthFlow(user_password=True),
        )
                # Cognito Authorizer for API Gateway
        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self, "MigrationChatAuthorizer",
            cognito_user_pools=[user_pool]
        )

        messages = api.root.add_resource("messages")
        messages.add_method(
            "POST",
            apigateway.LambdaIntegration(post_message_function),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )
        messages.add_method(
            "GET",
            apigateway.LambdaIntegration(get_messages_function),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        