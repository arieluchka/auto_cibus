"""
Classes for representing Cibus order history data from the API.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, ClassVar, Union


@dataclass
class OrderHistoryColumn:
    """Represents a column in the order history response."""
    name: Optional[str]
    type: str
    key: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrderHistoryColumn':
        """Create an OrderHistoryColumn instance from a dictionary."""
        return cls(
            name=data.get('name'),
            type=data.get('type', ''),
            key=data.get('key', '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the OrderHistoryColumn instance to a dictionary."""
        return {
            'name': self.name,
            'type': self.type,
            'key': self.key
        }


@dataclass
class OrderHistoryHead:
    """Represents the header section of the order history response."""
    count: int
    columns: List[OrderHistoryColumn]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrderHistoryHead':
        """Create an OrderHistoryHead instance from a dictionary."""
        columns = []
        for column_data in data.get('columns', []):
            columns.append(OrderHistoryColumn.from_dict(column_data))

        return cls(
            count=data.get('count', 0),
            columns=columns
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the OrderHistoryHead instance to a dictionary."""
        columns_data = []
        for column in self.columns:
            columns_data.append(column.to_dict())

        return {
            'count': self.count,
            'columns': columns_data
        }


@dataclass
class OrderHistoryItem:
    """Represents a single order in the order history."""
    rest_name: str
    date: str
    time: str
    deal_id: int
    rule_name: str
    status: str
    voucher_code: str
    display_price: float
    coupon: float
    discount: float
    delivery_price: float
    price: float
    etc_company_price: float
    etc_employee_price: float
    otl_price: float
    order_type: int
    is_active: int
    restaurant_id: int
    logo: str
    refund_id: str = ""
    budget_activation_date: int = -1
    is_3rd_party: bool = False
    icon: str = ""
    barcode: Optional[str] = None

    # Calculated fields
    datetime_obj: Optional[datetime] = None

    def __post_init__(self):
        """Process fields after initialization."""
        # Parse date and time strings to datetime object
        if self.date and self.time:
            try:
                day, month, year = map(int, self.date.split('/'))
                hour, minute = map(int, self.time.split(':'))
                self.datetime_obj = datetime(year, month, day, hour, minute)
            except (ValueError, TypeError):
                self.datetime_obj = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrderHistoryItem':
        """Create an OrderHistoryItem instance from a dictionary."""
        return cls(
            rest_name=data.get('rest_name', ''),
            date=data.get('date', ''),
            time=data.get('time', ''),
            deal_id=data.get('deal_id', 0),
            rule_name=data.get('rule_name', ''),
            status=data.get('status', ''),
            voucher_code=data.get('voucher_code', ''),
            display_price=float(data.get('display_price', 0.0)),
            coupon=float(data.get('coupon', 0.0)),
            discount=float(data.get('discount', 0.0)),
            delivery_price=float(data.get('delivery_price', 0.0)),
            price=float(data.get('price', 0.0)),
            etc_company_price=float(data.get('etc_company_price', 0.0)),
            etc_employee_price=float(data.get('etc_employee_price', 0.0)),
            otl_price=float(data.get('otl_price', 0.0)),
            order_type=data.get('order_type', 0),
            is_active=data.get('is_active', 0),
            restaurant_id=data.get('restaurant_id', 0),
            logo=data.get('logo', ''),
            refund_id=data.get('refund_id', ''),
            budget_activation_date=data.get('budget_activation_date', -1),
            is_3rd_party=data.get('is_3rd_party', False),
            icon=data.get('icon', ''),
            barcode=data.get('barcode')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the OrderHistoryItem instance to a dictionary."""
        return {
            'rest_name': self.rest_name,
            'date': self.date,
            'time': self.time,
            'deal_id': self.deal_id,
            'rule_name': self.rule_name,
            'status': self.status,
            'voucher_code': self.voucher_code,
            'display_price': self.display_price,
            'coupon': self.coupon,
            'discount': self.discount,
            'delivery_price': self.delivery_price,
            'price': self.price,
            'etc_company_price': self.etc_company_price,
            'etc_employee_price': self.etc_employee_price,
            'otl_price': self.otl_price,
            'order_type': self.order_type,
            'is_active': self.is_active,
            'restaurant_id': self.restaurant_id,
            'logo': self.logo,
            'refund_id': self.refund_id,
            'budget_activation_date': self.budget_activation_date,
            'is_3rd_party': self.is_3rd_party,
            'icon': self.icon,
            'barcode': self.barcode
        }


@dataclass
class OrderHistoryResponse:
    """Represents the full response from the order history API call."""
    head: OrderHistoryHead
    list: List[OrderHistoryItem]
    code: int
    msg: str
    http_code: int

    # Class constants
    API_CALL_TYPE: ClassVar[str] = "prx_user_deals"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrderHistoryResponse':
        """Create an OrderHistoryResponse instance from a dictionary."""
        order_items = []
        for item_data in data.get('list', []):
            order_items.append(OrderHistoryItem.from_dict(item_data))

        return cls(
            head=OrderHistoryHead.from_dict(data.get('head', {'count': 0, 'columns': []})),
            list=order_items,
            code=data.get('code', 0),
            msg=data.get('msg', ''),
            http_code=data.get('http_code', 0)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the OrderHistoryResponse instance to a dictionary."""
        items_data = []
        for item in self.list:
            items_data.append(item.to_dict())

        return {
            'head': self.head.to_dict(),
            'list': items_data,
            'code': self.code,
            'msg': self.msg,
            'http_code': self.http_code
        }

    @property
    def is_success(self) -> bool:
        """Check if the response indicates success."""
        return self.code == 0 and self.http_code == 200
