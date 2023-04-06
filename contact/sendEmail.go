package main

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/sesv2"
	"github.com/aws/aws-sdk-go-v2/service/sesv2/types"
)

type SendEmail struct {
	Svc *sesv2.Client
}

func (s *SendEmail) Send(fromName *string, fromEmail *string, toEmail *string, sendEmail *string, details *string) (*sesv2.SendEmailOutput, error) {
	return s.Svc.SendEmail(context.TODO(), &sesv2.SendEmailInput{
		Content: &types.EmailContent{
			Simple: &types.Message{
				Subject: &types.Content{
					Data:    aws.String(fmt.Sprintf("New AWSome message from %s", *fromName)),
					Charset: aws.String("UTF-8"),
				},
				Body: &types.Body{
					Text: &types.Content{
						Data:    aws.String(fmt.Sprintf("From: %s\nEmail: %s\n\n%s", *fromName, *fromEmail, *details)),
						Charset: aws.String("UTF-8"),
					},
				},
			},
		},
		Destination: &types.Destination{
			ToAddresses: []string{*toEmail},
		},
		FromEmailAddress: sendEmail,
	})
}
