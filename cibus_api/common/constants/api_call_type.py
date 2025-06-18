from enum import Enum

class ApiCallType(Enum):
    """Types of API calls supported by the system"""
    ORDER_HISTORY = "prx_user_deals"
    CART_INFORMATION = "prx_get_cart"
    ADD_TO_CART = "prx_add_prod_to_cart"
    NEW_SITE_FLAG = "prx_newsite_flag"
    APPLY_ORDER = "prx_apply_order"
    PREVIOUS_ORDERS = "prx_get_prev_orders"