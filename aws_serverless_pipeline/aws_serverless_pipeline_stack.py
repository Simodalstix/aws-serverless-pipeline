from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct

class AwsServerlessPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        _lambda.Function(
            self, "MyFirstLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda_app")
        )
