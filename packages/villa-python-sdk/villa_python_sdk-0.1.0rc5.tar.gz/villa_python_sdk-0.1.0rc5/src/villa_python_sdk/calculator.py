import json

import boto3
from botocore.exceptions import ClientError

from .types import CalculatedOrderResponse, Order


class CostCalculator:
    """
    CostCalculator is used to calculate the cost of an order by invoking the
    'calculate-cost' Lambda function with provided order details.

    Additional details can be provided here.
    """

    def __init__(self, branch: str = "dev", region_name: str = "ap-southeast-1"):
        """Initialize the Lambda client."""
        self.lambda_client = boto3.client("lambda", region_name=region_name)
        if branch == "dev":
            self.function_arn = "calculate-cost-2-pack-master"
        else:
            self.function_arn = "calculate-cost-2-pack-master"

    def calculate(
        self,
        input_order_object: Order,
    ) -> CalculatedOrderResponse:
        """
        Invoke the calculate-cost Lambda function with API Gateway proxy
        format.

        :param input_order_object: Dictionary with order details
        :return: Dictionary with response or error
        """
        # Create API Gateway proxy integration payload
        payload = {
            "resource": "/calculate-cost",
            "path": "/cost-calculation",
            "httpMethod": "POST",
            "headers": {"Content-Type": "application/json"},
            "queryStringParameters": None,
            "pathParameters": None,
            "body": json.dumps(input_order_object),
        }

        try:
            response = self.lambda_client.invoke(
                FunctionName=self.function_arn,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload),
            )

            # Parse the response
            response_payload = json.loads(response["Payload"].read())

            # Handle Lambda function response
            if response_payload.get("statusCode") == 200:
                return json.loads(response_payload["body"])
            else:
                # raise Exception(response_payload.get("body", "Unknown error"))
                raise Exception(response_payload)

        except ClientError as e:
            return {"error": "AWS Client Error", "message": str(e)}
        except json.JSONDecodeError as e:
            return {"error": "JSON Decode Error", "message": str(e)}
        except Exception as e:
            return {"error": "General Error", "message": str(e)}


# Example usage
if __name__ == "__main__":
    client = CostCalculator(branch="dev")
    data = json.load(open("../../tests/test_data/order1_input.json"))
    print("input is ", data)

    try:
        result = client.calculate(input_order_object=data)
        print("Cost calculation result:", result)

    except Exception as e:
        print("Error:", str(e))
        raise e
