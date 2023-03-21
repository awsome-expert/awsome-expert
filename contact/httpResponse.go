package main

import (
	"github.com/aws/aws-lambda-go/events"
)

type HTTPResponse struct{}

// GetSuccess returns eather an 304 - not modified or an 200 - ok response
// Cache-Control is set to one week for old data, and 15 minutes for data that we are still waiting for
func (r *HTTPResponse) GetSuccess() events.APIGatewayV2HTTPResponse {
	response := events.APIGatewayV2HTTPResponse{
		StatusCode:      200,
		IsBase64Encoded: false,
		Headers: map[string]string{
			"content-type":                "application/json",
			"Access-Control-Allow-Origin": "*",
		},
	}

	return response
}

// GetError returns an HTTP error resonse
func (r *HTTPResponse) GetError() events.APIGatewayV2HTTPResponse {
	return events.APIGatewayV2HTTPResponse{
		StatusCode:      500,
		IsBase64Encoded: false,
		Headers: map[string]string{
			"Access-Control-Allow-Origin": "*",
		},
	}
}
