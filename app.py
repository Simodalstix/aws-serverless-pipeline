#!/usr/bin/env python3

from aws_cdk import App
from aws_serverless_pipeline.aws_serverless_pipeline_stack import AwsServerlessPipelineStack

app = App()
AwsServerlessPipelineStack(app, "AwsServerlessPipelineStack")
app.synth()
