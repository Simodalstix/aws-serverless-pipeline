# Visitor Tracker – AWS Serverless Pipeline (CDK + Python)

This project is a simple, serverless visitor tracking system built with the AWS CDK (Python). When someone visits my website or makes a GET request to the API Gateway endpoint, a Lambda function logs their IP address, timestamp, and User-Agent string to a DynamoDB table. At the same time, a visitor count is incremented and returned in the response.

It's designed as a learning project to explore how serverless systems work in practice — from API Gateway and Lambda to DynamoDB and IAM roles — using Infrastructure as Code.

## Architecture Overview

This CDK stack sets up:

- API Gateway: Exposes a public GET endpoint
- AWS Lambda: Handles logic for counting and logging visitors
- DynamoDB: Stores both the total visitor count and individual log entries
- IAM Roles: Grants least-privilege access to Lambda

Planned improvements:
- TTL settings for automatic log expiration
- Optional API key protection
- A separate /status endpoint for metrics

## Getting Started

### 1. Set up my Python environment (I need more muscle memory!)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Bootstrap my AWS environment (if needed)

```bash
cdk bootstrap
```

### 3. Deploy the stack

```bash
cdk deploy
```

After deployment, the API endpoint will be output to the terminal.

## How It Works

Each request to the API:

1. Triggers the Lambda function.
2. Increments a counter in DynamoDB.
3. Logs the visitor's IP, timestamp, and User-Agent.
4. Returns the current visitor count as JSON.

Example response:

```json
{
  "visitor_count": 42
}
```

## Tech Stack

- AWS CDK (Python)
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Python + boto3

## Goals and Reflections

This project helped reinforce key concepts around:

- API Gateway event structure and header parsing
- Basic IAM permissions for Lambda-DynamoDB access
- Using Python and boto3 to interact with AWS services
- Writing repeatable infrastructure using CDK

Next I'm going to expand on this with a simple CLI tool.

## Author

Simon Parker  
https://simostack.com | https://github.com/Simodalstix
