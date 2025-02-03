import json
import unittest
from unittest.mock import MagicMock, patch

from villa_python_sdk.calculator import CostCalculator
from villa_python_sdk.types import CalculatedOrderResponse, ErrorResponse, Order


class TestCostCalculator(unittest.TestCase):
    @patch("boto3.client")
    def test_calculate_success(self, mock_boto_client):
        """Test a successful cost calculation."""
        mock_lambda_client = MagicMock()
        mock_boto_client.return_value = mock_lambda_client

        mock_response = {
            "Payload": MagicMock(
                read=MagicMock(
                    return_value=json.dumps(
                        {"statusCode": 200, "body": json.dumps({"cost": 100.0})}
                    )
                )
            )
        }
        mock_lambda_client.invoke.return_value = mock_response

        calculator = CostCalculator(branch="dev")

        input_order: Order = {
            "branchId": "1023",
            "couponCodeList": ["9I7Y2KEY"],
            "productList": [],
            "shipping": {
                "scheduleList": [],
                "shippingLat": 13.73204799,
                "shippingLon": 100.56762289,
                "shippingAddress": "595 Sukhumvit Rd",
                "shippingFirstName": "tor",
                "shippingLastName": "intanon",
                "shippingPhone": "061-002-0199",
                "shippingProvince": "Bangkok",
                "shippingType": "DELIVERY",
            },
        }

        result: CalculatedOrderResponse = calculator.calculate(input_order)

        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"cost": 100.0})
        mock_lambda_client.invoke.assert_called_once()

    @patch("boto3.client")
    def test_calculate_client_error(self, mock_boto_client):
        """Test an AWS ClientError when invoking Lambda."""
        mock_lambda_client = MagicMock()
        mock_boto_client.return_value = mock_lambda_client

        from botocore.exceptions import ClientError

        mock_lambda_client.invoke.side_effect = ClientError(
            error_response={
                "Error": {
                    "Code": "ResourceNotFoundException",
                    "Message": "Function not found",
                }
            },
            operation_name="Invoke",
        )

        calculator = CostCalculator(branch="dev")

        input_order: Order = {
            "branchId": "1023",
            "couponCodeList": [],
            "productList": [],
            "shipping": {
                "scheduleList": [],
                "shippingLat": 0.0,
                "shippingLon": 0.0,
                "shippingAddress": "",
                "shippingFirstName": "",
                "shippingLastName": "",
                "shippingPhone": "",
                "shippingProvince": "",
                "shippingType": "DELIVERY",
            },
        }

        result = calculator.calculate(input_order)
        # Type narrowing using key presence
        assert "error" in result and "message" in result
        result_error: ErrorResponse = result  # type: ignore

        self.assertIsInstance(result_error, dict)
        self.assertEqual(result_error["error"], "AWS Client Error")
        self.assertIn("ResourceNotFoundException", result_error["message"])

        mock_lambda_client.invoke.assert_called_once()

    @patch("boto3.client")
    def test_calculate_json_decode_error(self, mock_boto_client):
        """Test a JSON decode error when Lambda returns invalid JSON."""
        mock_lambda_client = MagicMock()
        mock_boto_client.return_value = mock_lambda_client

        mock_response = {
            "Payload": MagicMock(read=MagicMock(return_value="Invalid JSON"))
        }
        mock_lambda_client.invoke.return_value = mock_response

        calculator = CostCalculator(branch="dev")

        input_order: Order = {
            "branchId": "1023",
            "couponCodeList": [],
            "productList": [],
            "shipping": {
                "scheduleList": [],
                "shippingLat": 0.0,
                "shippingLon": 0.0,
                "shippingAddress": "",
                "shippingFirstName": "",
                "shippingLastName": "",
                "shippingPhone": "",
                "shippingProvince": "",
                "shippingType": "DELIVERY",
            },
        }

        result = calculator.calculate(input_order)
        # Type narrowing using key presence
        assert "error" in result and "message" in result
        result_error: ErrorResponse = result  # type: ignore

        self.assertIsInstance(result_error, dict)
        self.assertEqual(result_error["error"], "JSON Decode Error")
        self.assertIn("Expecting value", result_error["message"])

        mock_lambda_client.invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()
