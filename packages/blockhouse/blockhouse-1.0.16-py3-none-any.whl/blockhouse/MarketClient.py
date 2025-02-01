import requests
from blockhouse.client.sor_connector import SORConnector


class MarketClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://go-api.blockhouse.app"
        self.sor_connector = None

    def fetch_sor_credentials(self) -> dict:
        """
        Fetch SOR credentials from the Go API.

        Returns:
            dict: SOR credentials including access key, secret key, region, and endpoint.
        """
        headers = {"x-api-key": self.api_key}
        response = requests.get(self.api_url + "/fix/sor-credentials", headers=headers)
        response.raise_for_status()

        credentials_data = response.json().get("data")
        if not credentials_data:
            raise ValueError("Failed to retrieve SOR credentials.")

        return credentials_data

    def initialize_sor_connector(self):
        """
        Initialize the SOR connector with fetched SOR credentials.
        """
        credentials = self.fetch_sor_credentials()
        self.sor_connector = SORConnector(
            aws_access_key_id=credentials["aws_access_key_id"],
            aws_secret_access_key=credentials["aws_secret_access_key"],
            region_name=credentials["sor_region"],
            endpoint=credentials["sagemaker_endpoint"],
        )

    def send_market_data(
        self,
        payload: dict,
    ) -> dict:
        """_summary_
        Send a market to the market API.
        Args:
            timestamp_ny (str): Timestamp in New York timezone
            side (str): Side of the trade
            price (float): Price of the trade
            size (int): Size of the trade
            symbol (str): Symbol of the trade

        Raises:
            ValueError: If side or order_type is invalid

        Returns:
            dict: Response from the Trade API
        """
        if not self.sor_connector:
            self.initialize_sor_connector()

        headers = {"x-api-key": self.api_key}
        try:
            response = requests.post(
                self.api_url + "/fix/market", headers=headers, json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            return {"error": str(err)}


if __name__ == "__main__":
    # Initialize the client
    client = MarketClient("72c6249e7745b7502d84e794f16f3e38")

    # Define the full market data schema
    market_data = {
        "timestamp_ny": "2024-07-31T20:07:25",
        "side": "Bid",
        "price": 102.578125,
        "size": 4,
        "symbol": "10_YEAR",
    }

    # Send the market data
    response = client.send_market_data(market_data)

    print(response)
