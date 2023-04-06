import re

import aws_cdk as cdk
from aws_cdk.assertions import (
    Template,
    Match,
    Capture,
)

from awsome.awsome_stack.awsome_stack import AWSomeStack

def get_awsome_stack_template():
    app = cdk.App()
    stack = AWSomeStack(
        app, "AWSomeStack",
        env=cdk.Environment(
            account="123456789012",
            region="eu-west-1",
        ),
        domain_name="api.awsome.expert"
    )
    return Template.from_stack(stack)

def test_acm_certificate_created():
    template = get_awsome_stack_template()
    template.resource_count_is("AWS::CertificateManager::Certificate", 1)
    template.has_resource_properties(
        "AWS::CertificateManager::Certificate", {
            "DomainName": "api.awsome.expert",
        },
    )

def test_acm_validation():
    template = get_awsome_stack_template()
    template.has_resource_properties(
        "AWS::CertificateManager::Certificate", {
            "ValidationMethod": "DNS",
        },
    )
    template.has_resource_properties(
        "AWS::CertificateManager::Certificate", {
            "DomainValidationOptions": [
            {
                "DomainName": "api.awsome.expert",
                "HostedZoneId": Match.any_value()
            }]
        },
    )

def test_ses_domain_identity_created():
    template = get_awsome_stack_template()
    template.resource_count_is("AWS::SES::EmailIdentity", 1)
    template.has_resource_properties(
        "AWS::SES::EmailIdentity", {
            "EmailIdentity": "awsome.expert",
        },
    )

def test_ses_domain_identity_validation():
    template = get_awsome_stack_template()
    email_identity = Capture()
    template.has_resource_properties(
        "AWS::Route53::RecordSet", {
            "Type": "CNAME",
            "Name": {
                "Fn::GetAtt": Match.array_with([
                    email_identity,
                    "DkimDNSTokenName1"
                ])
            },
        },
    )
    assert re.match("^AWSomeEmailIdentity", email_identity.as_string())
    template.resource_properties_count_is(
        "AWS::Route53::RecordSet", {
            "Type": "CNAME",
            "Name": {
                "Fn::GetAtt": Match.array_with([
                    email_identity.as_string(),
                ])
            },
        }, 3
    )
