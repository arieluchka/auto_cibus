import requests
from requests.exceptions import RequestException, Timeout
from cibus_api.common.constants.api_config import ApiConfig

#todo: rewrite into simpler code

class CibusApi:
    def __init__(self, token):
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-App-Id': ApiConfig.APP_ID,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.cookies = {"token": token}  # Will be populated after login
        
    def __post_request(self, url, data=None, headers=None, cookies=None):
        try:
            # Use default values if not provided
            headers = headers if headers is not None else self.default_headers
            cookies = cookies if cookies is not None else self.cookies
            
            # Send the request
            response = requests.post(
                url=url,
                json=data,  # Automatically converts to JSON
                headers=headers,
                cookies=cookies,
                timeout=30  # Timeout after 30 seconds
            )
            
            # Raise an exception if the request failed
            response.raise_for_status()
            
            return response
            
        except Timeout:
            # Handle timeout specifically
            raise RequestException(f"Request to {url} timed out")
        except RequestException as e:
            # Re-raise the exception with more context
            raise RequestException(f"POST request to {url} failed: {str(e)}")
    
    def __get_request(self, url, headers=None, cookies=None):
        try:
            # Use default values if not provided
            headers = headers if headers is not None else self.default_headers
            cookies = cookies if cookies is not None else self.cookies
              # Send the request
            response = requests.get(
                url=url,
                headers=headers,
                cookies=cookies,
                timeout=30  # Timeout after 30 seconds
            )
            
            # Raise an exception if the request failed
            response.raise_for_status()
            
            return response
            
        except Timeout:
            # Handle timeout specifically
            raise RequestException(f"Request to {url} timed out")
        except RequestException as e:
            # Re-raise the exception with more context
            raise RequestException(f"GET request to {url} failed: {str(e)}")

    def get_order_history_in_time_range(self, from_date, to_date):
        from datetime import datetime
        from common.end_points import ApiEndpoints
        from .common.constants.api_call_type import ApiCallType
        from .common.cibus_objects.cibus_order_history import OrderHistoryResponse
        
        # Convert datetime objects to string format if needed
        if isinstance(from_date, datetime):
            from_date = from_date.strftime('%d/%m/%Y')
        if isinstance(to_date, datetime):
            to_date = to_date.strftime('%d/%m/%Y')
            
        # Validate date formats
        try:
            datetime.strptime(from_date, '%d/%m/%Y')
            datetime.strptime(to_date, '%d/%m/%Y')
        except ValueError:
            raise ValueError("Dates must be in 'DD/MM/YYYY' format")
        
        # Prepare the request data
        data = {
            "from_date": from_date,
            "to_date": to_date,
            "type": ApiCallType.ORDER_HISTORY.value
        }
        
        # Send the request
        response = self.__post_request(
            url=ApiEndpoints.DATA,
            data=data
        )
        
        # Parse the response
        response_json = response.json()
        
        # Create and return the typed response object
        return OrderHistoryResponse.from_dict(response_json)

    def get_cart_info(self):
        ...

    def add_product_to_cart(self):
        ...

    def get_restaurant_items(self):
        ...

    def apply_cart_order(self):
        ...