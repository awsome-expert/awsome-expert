from constructs import Construct
from aws_cdk import (
    aws_apigatewayv2_alpha as apigw,
    aws_apigatewayv2_integrations_alpha as apigw_integrations,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_certificatemanager as acm,
    aws_lambda as _lambda,
)

class ContactAPI(Construct):

    @property
    def contact_api(self):
        return self._contact_api

    def __init__(self, scope: Construct, id: str, domain_name: str, certificate: acm.ICertificate, contact_lambda: _lambda.IFunction, hosted_zone: route53.IHostedZone, **kwargs):
        super().__init__(scope, id, **kwargs)

        # API Gateway HTTP API
        self._contact_api = apigw.HttpApi(self, "AWSome Contact")
        contactIntegration = apigw_integrations.HttpLambdaIntegration('ContactAWSomeAPI', contact_lambda)
        self._contact_api.add_routes(
            path='/contact',
            methods=[apigw.HttpMethod.ANY],
            integration=contactIntegration,
        )

        # Create custom API domain name
        api_domain = apigw.DomainName(self, "AWSomeAPIDomainName",
            domain_name=domain_name,
            certificate=acm.Certificate.from_certificate_arn(self, "APICert",
                certificate_arn=certificate.certificate_arn,
            ),
        )

        # Map the custom API domain name to the HTTP API
        apigw.ApiMapping(self, "AWSomeContactDomainMapping",
            api=self._contact_api,
            domain_name=api_domain,
        )

        # Create API domain name in Route53 to point to the custom domain name in APIGateway
        route53.ARecord(self, "AWSomeAPIRecord",
            zone=hosted_zone,
            record_name=domain_name,
            target=route53.RecordTarget.from_alias(
                targets.ApiGatewayv2DomainProperties(api_domain.regional_domain_name, api_domain.regional_hosted_zone_id)
            ),
        )
