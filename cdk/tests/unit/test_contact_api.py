import tldextract
import re

from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_route53 as route53,
)

from aws_cdk.assertions import (
    Template,
    Capture,
)

from awsome.contact_lambda import ContactLambda
from awsome.contact_api import ContactAPI

def get_contact_api_template():
    domain_name = "api.awsome.expert"
    stack = Stack()
    awsome_lambda = ContactLambda(
        stack, 'ContactLambda',
        account="123456789012",
        region="eu-west-1",
    )
    apex_domain = tldextract.extract(domain_name).registered_domain
    hosted_zone = route53.HostedZone(
        stack, "AWSomeExpertHostedZone",
        zone_name=apex_domain,
    )
    certificate = acm.Certificate(
        stack, "ContactAPICert",
        domain_name=domain_name
    )
    ContactAPI(
        stack, 'ContactAPI',
        domain_name=domain_name,
        certificate=certificate,
        contact_lambda=awsome_lambda._contact_lambda,
        hosted_zone=hosted_zone,
    )
    return Template.from_stack(stack)

def test_api_gateway_created():
    template = get_contact_api_template()
    template.resource_count_is("AWS::ApiGatewayV2::Api", 1)
    template.has_resource_properties(
        "AWS::ApiGatewayV2::Api", {
            "Name": "AWSome Contact",
            "ProtocolType": "HTTP",
        },
    )

def test_domain_name_created():
    template = get_contact_api_template()
    template.resource_count_is("AWS::ApiGatewayV2::DomainName", 1)
    template.has_resource_properties(
        "AWS::ApiGatewayV2::DomainName", {
            "DomainName": "api.awsome.expert",
        },
    )

def test_domain_name_mapping():
    template = get_contact_api_template()
    template.resource_count_is("AWS::ApiGatewayV2::ApiMapping", 1)
    template.has_resource_properties(
        "AWS::ApiGatewayV2::ApiMapping", {
            "Stage": "$default",
        },
    )

def test_dns_alias_record_created():
    template = get_contact_api_template()
    template.resource_count_is("AWS::Route53::RecordSet", 1)
    custom_domain_name_resource = Capture()
    template.has_resource_properties(
        "AWS::Route53::RecordSet", {
            "Name": "api.awsome.expert.",
            "Type": "A",
            "AliasTarget": {
                "DNSName": {
                    "Fn::GetAtt": [
                        custom_domain_name_resource,
                        "RegionalDomainName",
                    ]
                },
            },
        },
    )
    assert re.match("^ContactAPIAWSomeAPIDomainName", custom_domain_name_resource.as_string())

def test_lambda_invoke_permissions():
    template = get_contact_api_template()
    template.resource_count_is("AWS::Lambda::Permission", 1)
    lambda_resource = Capture()
    template.has_resource_properties(
        "AWS::Lambda::Permission", {
            "Action": "lambda:InvokeFunction",
            "FunctionName": {
                "Fn::GetAtt": [
                    lambda_resource,
                    "Arn",
                ]
            }
        },
    )
    assert re.match("^ContactLambdaAWSomeContactLambda", lambda_resource.as_string())

def test_api_route():
    template = get_contact_api_template()
    template.resource_count_is("AWS::ApiGatewayV2::Route", 1)
    template.has_resource_properties(
        "AWS::ApiGatewayV2::Route", {
            "RouteKey": "ANY /contact",
        },
    )
