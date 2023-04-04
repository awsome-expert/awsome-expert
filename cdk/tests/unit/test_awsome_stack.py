# import aws_cdk as core
# import aws_cdk.assertions as assertions
# from awsome.awsome_stack import AWSomeStack


# def test_sqs_queue_created():
#     app = core.App()
#     stack = AWSomeStack(app, "AWSomeStack")
#     template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
