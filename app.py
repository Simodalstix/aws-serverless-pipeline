#!/usr/bin/env python3

from aws_cdk import App
from aws_serverless_pipeline.aws_serverless_pipeline_stack import AwsServerlessPipelineStack
from aws_serverless_pipeline.migration_chat_stack import MigrationChatStack

app = App()
AwsServerlessPipelineStack(app, "AwsServerlessPipelineStack")
MigrationChatStack(app, "MigrationChatStack")
app.synth()
