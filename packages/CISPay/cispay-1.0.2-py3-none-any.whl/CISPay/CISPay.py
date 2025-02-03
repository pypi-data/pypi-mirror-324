import requests
from requests.exceptions import ConnectTimeout, ReadTimeout

class CISPay:
    def __init__(self, SHOP_UUID):
        """
        Arguments:
            SHOP_UUID: Merchant UUID (from '?' on merchant page)
            API_URL: CISPay API URL (do not edit)
        """

        self.SHOP_UUID = SHOP_UUID
        self.API_URL = 'https://api.cispay.pro'

    def order_create(self, amount, comment, expire):
        """
        Documentation: https://docs.cispay.pro/merchant/order/creating-order

        Arguments:
            amount: Order amount
            comment: Order comment
            expire: Order expire
        """

        api_url = self.API_URL + '/payment/create'
        data = {
            'shop_to': self.SHOP_UUID,
            'sum': round(amount, 2),
            'comment': comment,
            'expire': expire
        }

        try:
            response = requests.post(api_url, json=data)
        except ConnectTimeout:
            return 'ConnectTimeout'
        except ReadTimeout:
            return 'ReadTimeout'
        
        response_code = response.status_code
        if(response_code == 200):
            try:
                response_data = response.json()
            except:
                return 'Failed to read JSON'

            if response_data["status"] == "success":
                return response_data
            else:
                return f"Error: {response_data['message']}"
        else:
            return f"Failed to get response: {response_code}"

        
    def order_info(self, order_id):
        """
        Documentation: https://docs.cispay.pro/merchant/order/info

        Arguments:
            order_uuid: Order UUID on CISPay
        """

        api_url = self.API_URL + '/payment/info'
        data = {
            'shop_uuid': self.SHOP_UUID,
            'order_uuid': order_id
        }

        try:
            response = requests.post(api_url, json=data)
        except ConnectTimeout:
            return 'ConnectTimeout'
        except ReadTimeout:
            return 'ReadTimeout'

        response_code = response.status_code
        if(response_code == 200):
            try:
                response_data = response.json()
            except:
                return 'Failed to read JSON'

            if response_data["status"] in ['success', 'waiting', 'expired']:
                return response_data
            else:
                return f"Error: {response_data['message']}"
        else:
            return f"Failed to get response: {response_code}"  
