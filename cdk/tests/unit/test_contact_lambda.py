import re

from aws_cdk import Stack
from aws_cdk.assertions import (
    Template,
    Match,
    Capture,
)

from awsome.awsome_stack.contact_lambda import ContactLambda

def get_contact_lambda_template():
    stack = Stack()
    ContactLambda(
        stack, 'ContactLambda',
        account="123456789012",
        region="eu-west-1",
    )
    return Template.from_stack(stack)

def test_lambdafunction_created():
    template = get_contact_lambda_template()
    template.resource_count_is("AWS::Lambda::Function", 1)

def test_iam_role_created():
    template = get_contact_lambda_template()
    template.resource_count_is("AWS::IAM::Role", 1)

def test_iam_role_used():
    template = get_contact_lambda_template()
    role_name_capture = Capture()
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Role": {
                "Fn::GetAtt": Match.array_with([
                    role_name_capture
                ])
            },
        },
    )
    assert re.match("^ContactLambdaAWSomeContactRole", role_name_capture.as_string())

def test_iam_policy_log_group():
    template = get_contact_lambda_template()
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": Match.array_with([{
                "Action": "logs:CreateLogGroup",
                "Effect": "Allow",
                "Resource": "arn:aws:logs:eu-west-1:123456789012:*"
            },{
                "Action": [
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Effect": "Allow",
                "Resource": [
                    "arn:aws:logs:eu-west-1:123456789012:log-group:/aws/lambda/AWSomeStack*:*",
                    "arn:aws:logs:eu-west-1:123456789012:log-group:/aws/lambda/Deploy-AWSomeStack*:*"
                ]
            }])
        }
    })

def test_iam_policy_ssm_parameters():
    template = get_contact_lambda_template()
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": Match.array_with([{
                "Action": [
                    "ssm:GetParameter",
                    "ssm:GetParameters",
                    "ssm:ListTagsForResource"
                ],
                "Effect": "Allow",
                "Resource": "arn:aws:ssm:eu-west-1:123456789012:parameter/freelance/*"
            }])
        }
    })

def test_iam_policy_send_email():
    template = get_contact_lambda_template()
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": Match.array_with([{
                "Action": [
                    "ses:SendEmail",
                    "ses:SendRawEmail"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }])
        }
    })
