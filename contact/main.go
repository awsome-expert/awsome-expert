package main

import (
	"context"
	"log"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/sesv2"
	"github.com/aws/aws-sdk-go-v2/service/ssm"
)

// HandleRequest lambda init functions
func HandleRequest(ctx context.Context, request events.APIGatewayV2HTTPRequest) (events.APIGatewayV2HTTPResponse, error) {
	response := &HTTPResponse{}

	// Get requester email address and details
	fromEmail, ok := request.Headers["email"]
	if !ok {
		log.Println("Email is required")
		resp := response.GetError()
		return resp, nil
	}
	details := request.Headers["details"]

	// AWS CLI configuration
	cfg, err := config.LoadDefaultConfig(context.TODO(), func(o *config.LoadOptions) error {
		o.Region = "eu-west-1"
		return nil
	})
	if err != nil {
		resp := response.GetError()
		return resp, err
	}

	// Get parameters from SSM Parameter Store
	parameter := SSMParameter{
		Svc: ssm.NewFromConfig(cfg),
	}
	toEmail := parameter.GetParameter("freelance_contact_email")
	sendEmail := parameter.GetParameter("freelance_send_email")

	// Send email
	email := SendEmail{
		Svc: sesv2.NewFromConfig(cfg),
	}
	_, err = email.Send(&fromEmail, toEmail, sendEmail, &details)
	if err != nil {
		log.Println(err.Error())
		resp := response.GetError()
		return resp, err
	}

	resp := response.GetSuccess()
	return resp, nil
}

func main() {
	lambda.Start(HandleRequest)
}
