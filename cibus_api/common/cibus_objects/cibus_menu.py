"""
Classes for representing Cibus restaurant menu data from the API.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, ClassVar, Union


@dataclass
class MenuElement:
    """Base class for menu elements (categories and items)."""
    name: str
    price: int
    order: int
    is_mandatory: int
    img: str
    max_items: int
    free_items: int
    caloric_value: Optional[str]
    gluten_free: int
    vegan: Optional[int]
    vegetarian: Optional[int]
    spice_level_name: Optional[str]
    elm_hash: int
    elm_desc_hash: Optional[int]
    element_id: int
    element_type: int
    min_items: int
    description: str
    child_count: int
    has_freebies: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MenuElement':
        """Create a MenuElement instance from a dictionary."""
        return cls(
            name=data.get('name', ''),
            price=data.get('price', 0),
            order=data.get('order', 0),
            is_mandatory=data.get('is_mandatory', 0),
            img=data.get('img', ''),
            max_items=data.get('max_items', 0),
            free_items=data.get('free_items', 0),
            caloric_value=data.get('caloric_value'),
            gluten_free=data.get('gluten_free', 0),
            vegan=data.get('vegan'),
            vegetarian=data.get('vegetarian'),
            spice_level_name=data.get('spice_level_name'),
            elm_hash=data.get('elm_hash', 0),
            elm_desc_hash=data.get('elm_desc_hash'),
            element_id=data.get('element_id', 0),
            element_type=data.get('element_type', 0),
            min_items=data.get('min_items', 0),
            description=data.get('description', ''),
            child_count=data.get('child_count', 0),
            has_freebies=data.get('has_freebies', False),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the MenuElement instance to a dictionary."""
        return {
            'name': self.name,
            'price': self.price,
            'order': self.order,
            'is_mandatory': self.is_mandatory,
            'img': self.img,
            'max_items': self.max_items,
            'free_items': self.free_items,
            'caloric_value': self.caloric_value,
            'gluten_free': self.gluten_free,
            'vegan': self.vegan,
            'vegetarian': self.vegetarian,
            'spice_level_name': self.spice_level_name,
            'elm_hash': self.elm_hash,
            'elm_desc_hash': self.elm_desc_hash,
            'element_id': self.element_id,
            'element_type': self.element_type,
            'min_items': self.min_items,
            'description': self.description,
            'child_count': self.child_count,
            'has_freebies': self.has_freebies,
        }

    @property
    def is_category(self) -> bool:
        """Check if this element is a category."""
        return self.element_type == 12

    @property
    def is_item(self) -> bool:
        """Check if this element is a menu item."""
        return self.element_type == 13


@dataclass
class MenuItem(MenuElement):
    """Represents a menu item (element_type=13)."""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MenuItem':
        """Create a MenuItem instance from a dictionary."""
        return super().from_dict(data)


@dataclass
class MenuCategory(MenuElement):
    """Represents a menu category (element_type=12) containing items."""
    items: Dict[int, List[MenuItem]] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MenuCategory':
        """Create a MenuCategory instance from a dictionary."""
        category = cls(**{
            'name': data.get('name', ''),
            'price': data.get('price', 0),
            'order': data.get('order', 0),
            'is_mandatory': data.get('is_mandatory', 0),
            'img': data.get('img', ''),
            'max_items': data.get('max_items', 0),
            'free_items': data.get('free_items', 0),
            'caloric_value': data.get('caloric_value'),
            'gluten_free': data.get('gluten_free', 0),
            'vegan': data.get('vegan'),
            'vegetarian': data.get('vegetarian'),
            'spice_level_name': data.get('spice_level_name'),
            'elm_hash': data.get('elm_hash', 0),
            'elm_desc_hash': data.get('elm_desc_hash'),
            'element_id': data.get('element_id', 0),
            'element_type': data.get('element_type', 0),
            'min_items': data.get('min_items', 0),
            'description': data.get('description', ''),
            'child_count': data.get('child_count', 0),
            'has_freebies': data.get('has_freebies', False),
        })
        
        # Process child items
        for element_type, items_data in data.items():
            if isinstance(element_type, str) and element_type.isdigit():
                type_id = int(element_type)
                if type_id != category.element_type:  # Skip the self-reference
                    category.items[type_id] = []
                    for item_data in items_data:
                        category.items[type_id].append(MenuItem.from_dict(item_data))
        
        return category
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the MenuCategory instance to a dictionary."""
        result = super().to_dict()
        
        # Add child items
        for element_type, items in self.items.items():
            items_data = []
            for item in items:
                items_data.append(item.to_dict())
            result[str(element_type)] = items_data
        
        return result
    
    def get_all_items(self) -> List[MenuItem]:
        """Get all items in this category regardless of element_type."""
        all_items = []
        for items in self.items.values():
            all_items.extend(items)
        return all_items


@dataclass
class RestaurantMenuResponse:
    """Represents the full response from the restaurant menu API call."""
    categories: Dict[int, List[MenuCategory]]
    code: int
    msg: str
    http_code: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RestaurantMenuResponse':
        """Create a RestaurantMenuResponse instance from a dictionary."""
        categories = {}
        
        # Process each element type at the top level
        for key, value in data.items():
            if key.isdigit():
                element_type = int(key)
                categories[element_type] = []
                
                for category_data in value:
                    categories[element_type].append(MenuCategory.from_dict(category_data))
        
        return cls(
            categories=categories,
            code=data.get('code', 0),
            msg=data.get('msg', ''),
            http_code=data.get('http_code', 0)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the RestaurantMenuResponse instance to a dictionary."""
        result = {
            'code': self.code,
            'msg': self.msg,
            'http_code': self.http_code
        }
        
        # Add categories
        for element_type, categories in self.categories.items():
            categories_data = []
            for category in categories:
                categories_data.append(category.to_dict())
            result[str(element_type)] = categories_data
        
        return result
    
    @property
    def is_success(self) -> bool:
        """Check if the response indicates success."""
        return self.code == 0 and self.http_code == 200
    
    def get_all_categories(self) -> List[MenuCategory]:
        """Get all categories regardless of element_type."""
        all_categories = []
        for categories in self.categories.values():
            all_categories.extend(categories)
        return all_categories
    
    def get_all_items(self) -> List[MenuItem]:
        """Get all menu items regardless of category."""
        all_items = []
        for categories in self.categories.values():
            for category in categories:
                all_items.extend(category.get_all_items())
        return all_items
    
    def find_item_by_id(self, element_id: int) -> Optional[MenuItem]:
        """Find a menu item by its element_id."""
        for item in self.get_all_items():
            if item.element_id == element_id:
                return item
        return None
    
    def find_category_by_id(self, element_id: int) -> Optional[MenuCategory]:
        """Find a category by its element_id."""
        for category in self.get_all_categories():
            if category.element_id == element_id:
                return category
        return None
