import os
import httpx
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.session import Session
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from aisuite.provider import Provider, LLMError
from aisuite.framework import ChatCompletionResponse
import json


class AwsHttpProvider(Provider):
    def __init__(self, **config):
        """
        Initialize the AWS Bedrock provider with the given configuration.

        Args:
            **config: Configuration options for the provider.
        """
        self.region_name = config.get(
            "region_name", os.getenv("AWS_REGION_NAME", "us-west-2")
        )
        self.api_endpoint = f"https://bedrock-runtime.{self.region_name}.amazonaws.com"

        # Create a botocore session and signer for AWS request signing
        self.session = Session()

        try:
            self.credentials = self.session.get_credentials()
            if self.credentials is None:
                raise NoCredentialsError
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise LLMError(f"Unable to load AWS credentials: {str(e)}")

        self.service_name = "bedrock"
        self.inference_parameters = [
            "maxTokens",
            "temperature",
            "topP",
            "stopSequences",
        ]

    def sign_request(self, method, url, headers, body):
        """
        Sign an HTTP request using SigV4.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: The complete URL
            headers: Dictionary of headers
            body: The body of the request (string or JSON)

        Returns:
            Signed request headers
        """
        request = AWSRequest(
            method=method, url=url, data=json.dump(body), headers=headers
        )
        SigV4Auth(self.credentials, self.service_name, self.region_name).add_auth(
            request
        )
        return dict(request.headers)

    def make_request(self, model, payload):
        """
        Make a synchronous HTTP POST request to the Bedrock Converse API.

        Args:
            model: Model ID or ARN
            payload: JSON payload for the request

        Returns:
            The response from the API in JSON format.
        """
        url = f"{self.api_endpoint}/model/{model}/converse"
        headers = {
            "Content-Type": "application/json",
        }

        # Sign the request with SigV4
        signed_headers = self.sign_request("POST", url, headers, body=payload)

        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=signed_headers)

            if response.status_code != 200:
                raise LLMError(
                    f"Request to AWS Bedrock failed with status code {response.status_code}: {response.text}"
                )

        return response.json()

    def normalize_response(self, response):
        """Normalize the response from the Bedrock API to match OpenAI's response format."""
        norm_response = ChatCompletionResponse()
        norm_response.choices[0].message.content = response["output"]["message"][
            "content"
        ][0]["text"]
        return norm_response

    def chat_completions_create(self, model, messages, **kwargs):
        system_message = []
        if messages[0]["role"] == "system":
            system_message = [{"text": messages[0]["content"]}]
            messages = messages[1:]

        formatted_messages = []
        for message in messages:
            if message["role"] != "system":
                formatted_messages.append(
                    {"role": message["role"], "content": [{"text": message["content"]}]}
                )

        inference_config = {}
        additional_model_request_fields = {}

        for key, value in kwargs.items():
            if key in self.inference_parameters:
                inference_config[key] = value
            else:
                additional_model_request_fields[key] = value

        payload = {
            "messages": formatted_messages,
            "system": system_message,
            "inferenceConfig": inference_config,
            "additionalModelRequestFields": additional_model_request_fields,
        }

        response = self.make_request(model, payload)
        return self.normalize_response(response)
