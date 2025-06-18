import os

from cibus_api.cibus_api import CibusApi
CIBUS_API_TOKEN=os.getenv("CIBUS_USERNAME")
CIBUS_USERNAME=os.getenv("CIBUS_USERNAME")
CIBUS_PASSWORD=os.getenv("CIBUS_PASSWORD")



class AutoCouponGrabber:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__token=self._get_token_through_ui()
        self.__cibus_api = CibusApi(token=self.__token)


    def _get_token_through_ui(self):
        from token_extractor.token_extractor import extract_token_from_ui
        return extract_token_from_ui(
            username=self.__username,
            password=self.__password
        )

    def _check_day_validity(self):
        ...

    def _check_time_validity(self):
        ...

    def _check_if_purchased_today(self):
        from datetime import datetime
        today = datetime.now().strftime("%d/%m/%Y")
        order_history = self.__cibus_api.get_order_history_in_time_range(
            from_date=today,
            to_date=today
        )
        print(order_history)

    def purchase_coupon(self):
        ...



if __name__ == '__main__':
    auto_grabber = AutoCouponGrabber(
        username=CIBUS_USERNAME,
        password=CIBUS_PASSWORD
    )
    # auto_grabber._get_token_through_ui()

    yes=auto_grabber._check_if_purchased_today()
    print("banana")