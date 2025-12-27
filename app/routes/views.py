from typing import Optional
import strawberry

from app.schemas import BranchConnection, BankConnection, BranchType, BankType, BranchFilterInput
from app.services import get_branch_service, get_bank_service
from app.core.logger import logger, log_graphql_query


@strawberry.type
class Query:
    
    @strawberry.field
    def branches(
        self,
        first: int = 20,
        after: Optional[str] = None,
        filter: Optional[BranchFilterInput] = None
    ) -> BranchConnection:
        log_graphql_query(
            "branches",
            {"first": first, "after": after, "filter": filter}
        )
        logger.info(f"GraphQL Query: branches(first={first}, after={after}, filter={filter})")
        
        service = get_branch_service()
        return service.get_all_branches(first=first, after=after, filter_input=filter)
    
    @strawberry.field
    def branch(self, ifsc: str) -> Optional[BranchType]:
        log_graphql_query("branch", {"ifsc": ifsc})
        logger.info(f"GraphQL Query: branch(ifsc={ifsc})")
        
        service = get_branch_service()
        return service.get_branch_by_ifsc(ifsc)
    
    @strawberry.field
    def banks(
        self,
        first: int = 20,
        after: Optional[str] = None
    ) -> BankConnection:
        log_graphql_query("banks", {"first": first, "after": after})
        logger.info(f"GraphQL Query: banks(first={first}, after={after})")
        
        service = get_bank_service()
        return service.get_all_banks(first=first, after=after)
    
    @strawberry.field
    def bank(self, id: int) -> Optional[BankType]:
        log_graphql_query("bank", {"id": id})
        logger.info(f"GraphQL Query: bank(id={id})")
        
        service = get_bank_service()
        return service.get_bank_by_id(id)


schema = strawberry.Schema(query=Query)
