#!/usr/bin/env python3
import os

import aws_cdk as cdk

from awsome.pipeline.pipeline_stack import PipelineStack

app = cdk.App()

PipelineStack(
    app, "AWSomePipelineStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION'),
    ),
    domain_name="api.awsome.expert",
)

app.synth()
