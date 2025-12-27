"""
GraphQL Types (Strawberry) - The "Shape"
Defines the structure for GraphQL queries
"""
from typing import Optional, List
import strawberry

from app.core.logger import logger


@strawberry.type
class BankType:
    """Bank GraphQL Type"""
    id: int
    name: str
    
    def __post_init__(self):
        logger.debug(f"BankType created: {self.name}")


@strawberry.type
class BranchType:
    """Branch GraphQL Type"""
    ifsc: str
    branch: str
    address: str
    city: str
    district: str
    state: str
    bank: BankType
    
    def __post_init__(self):
        logger.debug(f"BranchType created: {self.ifsc}")


@strawberry.type
class BranchEdge:
    """Branch Edge for pagination"""
    node: BranchType
    cursor: str


@strawberry.type
class PageInfo:
    """Page information for pagination"""
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str] = None
    end_cursor: Optional[str] = None


@strawberry.type
class BranchConnection:
    """Branch connection for pagination"""
    edges: List[BranchEdge]
    page_info: PageInfo
    total_count: int


@strawberry.type
class BankEdge:
    """Bank Edge for pagination"""
    node: BankType
    cursor: str


@strawberry.type
class BankConnection:
    """Bank connection for pagination"""
    edges: List[BankEdge]
    page_info: PageInfo
    total_count: int


@strawberry.input
class BranchFilterInput:
    """Input type for filtering branches"""
    ifsc: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    bank_name: Optional[str] = None
    branch_name: Optional[str] = None


@strawberry.input
class BankFilterInput:
    """Input type for filtering banks"""
    name: Optional[str] = None
