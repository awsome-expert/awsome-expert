from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    pipelines,
)

from .deploy_stage import DeployStage

class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, domain_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = pipelines.CodePipeline(
            self, "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection("awsome-expert/awsome-expert", "shellsteps",
                    connection_arn="arn:aws:codestar-connections:eu-west-1:846764252037:connection/8a64d1b3-354d-4007-9e30-e00183d794a7"
                ),
                commands=[
                    "cd cdk",
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth",
                ],
                primary_output_directory="cdk/cdk.out",
            ),
        )

        # # Create a tests stage
        # unit_tests_stage = pipeline.add_wave("Tests")
        # unit_tests_stage.add_pre(pipelines.ShellStep(
        #     "CDKUnitTests",
        #     commands=[
        #         "cd cdk",
        #         "pip install -r requirements.txt",
        #         "pip install -r requirements-dev.txt",
        #         "pytest",
        #     ],
        # ))

        pipelines.ShellStep(
            "CDKUnitTests",
            commands=[
                "cd cdk",
                "pip install -r requirements.txt",
                "pip install -r requirements-dev.txt",
                "pytest",
            ],
        )

        # Create the deploy stage
        pipeline.add_stage(DeployStage(
            self, "Deploy",
            env=cdk.Environment(
                account=kwargs["env"].account,
                region=kwargs["env"].region,
            ),
            domain_name=domain_name,
        ))
