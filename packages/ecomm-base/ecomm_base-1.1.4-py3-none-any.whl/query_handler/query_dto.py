from enum import Enum
from pydantic import BaseModel
from typing import Optional,List

# Model enum
class Model(Enum):
    blog=1
    appliance=2
    brand=3
    product=4
    faq=5
    contact=6
    advice_article=7
    advice_article_type=8

# Sort class
class Sort(BaseModel):
    field: str
    order: str

# Filter class
class Filter(BaseModel):
    operator: str
    field: str
    value: str

# Populate class
class Populate(BaseModel):
    field: str

# Pagination class
class Pagination(BaseModel):
    page: int=1
    pagesize: int=10

# Query DTO class
class QueryDTO(BaseModel):
    model:Optional[int]=None                   # Entity or module name
    id:Optional[int]=None                      # -1 for list, >0 for specific record ID
    slug:Optional[str]=None                    # Slug URLs
    sorts:Optional[List[Sort]]=None            # List of sorting parameters
    filters:Optional[List[Filter]]=None        # List of filters
    union_filter_operator:Optional[str]="and"  # Logical operator (e.g., 'and', 'or') for multiple fields
    populate:Optional[List[Populate]]=None     # Fields to include      
    pagination:Optional[Pagination]=None       # Pagination details
    is_list:Optional[bool]=True



