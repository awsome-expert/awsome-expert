import tldextract

from constructs import Construct
from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_ses as ses,
)
from .contact_lambda import ContactLambda
from .contact_api import ContactAPI

class AWSomeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, domain_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create lambda function
        awsome_lambda = ContactLambda(
            self, 'ContactLambda',
            account=kwargs["env"].account,
            region=kwargs["env"].region,
        )

        # Retrieve the Route 53 hosted zone for the domain
        apex_domain = tldextract.extract(domain_name).registered_domain
        hosted_zone = route53.PublicHostedZone.from_lookup(self, "AWSomeExpertHostedZone",
            domain_name=apex_domain,
        )

        # Create certificate for the domain name
        certificate = acm.Certificate(self, "ContactAPICert",
            domain_name=domain_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

        # Create HTTP API Gateway enpoint with custom domain name
        ContactAPI(
            self, 'ContactAPI',
            domain_name=domain_name,
            certificate=certificate,
            awsome_lambda=awsome_lambda,
            hosted_zone=hosted_zone,
        )

        # SES domain verification
        ses.EmailIdentity(self, "AWSomeEmailIdentity",
            identity=ses.Identity.public_hosted_zone(hosted_zone),
        )
