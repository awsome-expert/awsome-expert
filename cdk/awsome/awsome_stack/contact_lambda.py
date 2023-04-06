import os
import sys
import shutil

from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
)

class ContactLambda(Construct):

    @property
    def contact_lambda(self):
        return self._contact_lambda

    def __init__(self, scope: Construct, id: str, account: str, region: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # IAM role for the lambda function
        lambdaRole = iam.Role(
            self, "AWSomeContactRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        lambdaRole.add_to_policy(iam.PolicyStatement(
            actions=["logs:CreateLogGroup"],
            resources=[f"arn:aws:logs:{region}:{account}:*"],
        ))
        lambdaRole.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=[
                    f"arn:aws:logs:{region}:{account}:log-group:/aws/lambda/AWSomeStack*:*",
                    f"arn:aws:logs:{region}:{account}:log-group:/aws/lambda/Deploy-AWSomeStack*:*",
                ],
            ),
        )
        lambdaRole.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "ssm:GetParameter",
                    "ssm:GetParameters",
                    "ssm:ListTagsForResource",
                ],
                resources=[f"arn:aws:ssm:{region}:{account}:parameter/freelance/*"],
            ),
        )
        lambdaRole.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "ses:SendEmail",
                    "ses:SendRawEmail",
                ],
                resources=["*"],
            ),
        )

        if "pytest" in sys.modules:
            # Create dummy file for tests
            zip_file = '../contact/contact.zip'
            os.system('touch ' + zip_file)
        else:
            # Compile Go project
            os.system('cd ../contact && GOOS=linux GOARCH=amd64 go build .')
            # Compress binary
            zip_file = shutil.make_archive('../contact/contact', 'zip', '../contact', 'contact')

        # Lambda function
        cwd = os.getcwd()
        self._contact_lambda = _lambda.Function(
            self, "AWSomeContactLambda",
            runtime=_lambda.Runtime.GO_1_X,
            code=_lambda.Code.from_asset(os.path.join(cwd, zip_file)),
            handler='contact',
            role=lambdaRole,
        )
