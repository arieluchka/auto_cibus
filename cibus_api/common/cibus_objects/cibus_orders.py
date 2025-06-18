"""
Classes for representing Cibus order data from the API.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, ClassVar


@dataclass
class Logo:
    """Represents logo information for a restaurant."""
    logo: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Logo':
        """Create a Logo instance from a dictionary."""
        return cls(logo=data.get('logo', ''))

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Logo instance to a dictionary."""
        return {'logo': self.logo}


@dataclass
class RequestedObject:
    """Represents an ordered item with its details."""
    object_id: int
    variation_id: int
    quantity: int
    options: List[Any] = field(default_factory=list)

    @classmethod
    def from_list(cls, data: List[Any]) -> 'RequestedObject':
        """Create a RequestedObject instance from a list."""
        if len(data) >= 4:
            return cls(
                object_id=data[0],
                variation_id=data[1],
                quantity=data[2],
                options=data[3]
            )
        return cls(
            object_id=0,
            variation_id=0,
            quantity=0,
            options=[]
        )

    def to_list(self) -> List[Any]:
        """Convert the RequestedObject instance to a list."""
        return [self.object_id, self.variation_id, self.quantity, self.options]


@dataclass
class Order:
    """Represents a single order with all its details."""
    restaurant_id: int
    favorit_id: int
    requested_objects: List[RequestedObject]
    description: str
    order_type: int
    deal_id: int
    kitchen_type: int
    name: str
    address: str
    rate: float
    rates: int
    price: int
    date_str: str
    is_open: bool
    is_kosher: bool
    images: List[str]
    logos: Logo
    is_web_order: bool
    is_approved: bool
    
    # Calculated fields
    date: Optional[datetime] = None
    
    def __post_init__(self):
        """Process fields after initialization."""
        # Parse date string to datetime object
        if self.date_str:
            try:
                day, month, year = map(int, self.date_str.split('/'))
                self.date = datetime(year, month, day)
            except (ValueError, TypeError):
                self.date = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Order':
        """Create an Order instance from a dictionary."""
        requested_objects = []
        for obj_data in data.get('requested_objects', []):
            requested_objects.append(RequestedObject.from_list(obj_data))
        
        return cls(
            restaurant_id=data.get('restaurant_id', 0),
            favorit_id=data.get('favorit_id', 0),
            requested_objects=requested_objects,
            description=data.get('description', ''),
            order_type=data.get('order_type', 0),
            deal_id=data.get('deal_id', 0),
            kitchen_type=data.get('kitchen_type', 0),
            name=data.get('name', ''),
            address=data.get('address', ''),
            rate=data.get('rate', 0.0),
            rates=data.get('rates', 0),
            price=data.get('price', 0),
            date_str=data.get('date', ''),
            is_open=bool(data.get('is_open', 0)),
            is_kosher=bool(data.get('is_kosher', 0)),
            images=data.get('images', []),
            logos=Logo.from_dict(data.get('logos', {'logo': ''})),
            is_web_order=bool(data.get('is_web_order', False)),
            is_approved=bool(data.get('is_approved', False))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Order instance to a dictionary."""
        requested_objects_data = []
        for obj in self.requested_objects:
            requested_objects_data.append(obj.to_list())
        
        return {
            'restaurant_id': self.restaurant_id,
            'favorit_id': self.favorit_id,
            'requested_objects': requested_objects_data,
            'description': self.description,
            'order_type': self.order_type,
            'deal_id': self.deal_id,
            'kitchen_type': self.kitchen_type,
            'name': self.name,
            'address': self.address,
            'rate': self.rate,
            'rates': self.rates,
            'price': self.price,
            'date': self.date_str,
            'is_open': 1 if self.is_open else 0,
            'is_kosher': 1 if self.is_kosher else 0,
            'images': self.images,
            'logos': self.logos.to_dict(),
            'is_web_order': self.is_web_order,
            'is_approved': self.is_approved
        }
    
    def get_total_quantity(self) -> int:
        """Calculate the total quantity of items in this order."""
        return sum(obj.quantity for obj in self.requested_objects)


@dataclass
class PreviousOrdersResponse:
    """Represents the full response from the previous orders API call."""
    queue_orders: List[Order]
    prev_orders: List[Order]
    code: int
    msg: str
    http_code: int
    
    # Class constants
    API_CALL_TYPE: ClassVar[str] = "prx_get_prev_orders"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PreviousOrdersResponse':
        """Create a PreviousOrdersResponse instance from a dictionary."""
        queue_orders = []
        for order_data in data.get('queue_orders', []):
            queue_orders.append(Order.from_dict(order_data))
        
        prev_orders = []
        for order_data in data.get('prev_orders', []):
            prev_orders.append(Order.from_dict(order_data))
        
        return cls(
            queue_orders=queue_orders,
            prev_orders=prev_orders,
            code=data.get('code', 0),
            msg=data.get('msg', ''),
            http_code=data.get('http_code', 0)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the PreviousOrdersResponse instance to a dictionary."""
        queue_orders_data = []
        for order in self.queue_orders:
            queue_orders_data.append(order.to_dict())
        
        prev_orders_data = []
        for order in self.prev_orders:
            prev_orders_data.append(order.to_dict())
        
        return {
            'queue_orders': queue_orders_data,
            'prev_orders': prev_orders_data,
            'code': self.code,
            'msg': self.msg,
            'http_code': self.http_code
        }
    
    @property
    def is_success(self) -> bool:
        """Check if the response indicates success."""
        return self.code == 0 and self.http_code == 200
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders (both queue and previous)."""
        return self.queue_orders + self.prev_orders
