import json
import requests

class OrangeSMSAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def _encode_credentials(self):
        """Encode client_id and client_secret in Base64."""
        import base64
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def get_token(self):
        """Obtain an access token from the Orange API."""
        url = 'https://api.orange.com/oauth/v3/token'
        headers = {
            'Authorization': f"Basic {self._encode_credentials()}",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }
        data = {
            'grant_type': 'client_credentials',
        }
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            response_data = response.json()
            self.token = response_data.get('access_token')
            return self.token
        else:
            raise Exception(f"Failed to get token: {response.status_code}, {response.text}")

    def send_sms(self, sender_address, receiver_address, message):
        """Send an SMS message using the Orange API."""
        if not self.token:
            raise Exception("Access token is missing. Please call get_token() first.")

        url = f'https://api.orange.com/smsmessaging/v1/outbound/tel:{sender_address}/requests'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        data = {
            "outboundSMSMessageRequest": {
                "address": f"tel:{receiver_address}",
                "senderAddress": f"tel:{sender_address}",
                "outboundSMSTextMessage": {
                    "message": message
                }
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to send SMS: {response.status_code}, {response.text}")

    def get_usage_stats(self):
        """Retrieve SMS usage statistics."""
        if not self.token:
            raise Exception("Access token is missing. Please call get_token() first.")

        url = 'https://api.orange.com/sms/admin/v1/statistics'
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get usage stats: {response.status_code}, {response.text}")

    def show_balance_sms(self):
        """Retrieve SMS balance information."""
        if not self.token:
            raise Exception("Access token is missing. Please call get_token() first.")

        url = 'https://api.orange.com/sms/admin/v1/contracts'
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get SMS balance: {response.status_code}, {response.text}")
