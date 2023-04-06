import aws_cdk as cdk

from constructs import Construct
from aws_cdk import (
    Stage
)

from awsome.awsome_stack.awsome_stack import AWSomeStack

class DeployStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, domain_name: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        AWSomeStack(
            self, "AWSomeStack",
            env=cdk.Environment(
                account=kwargs["env"].account,
                region=kwargs["env"].region,
            ),
            domain_name=domain_name,
        )
